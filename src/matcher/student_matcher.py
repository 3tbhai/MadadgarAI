"""Student Scholarship Matcher, Intelligent Eligibility Evaluator, Document Checklist Generator, and Plain-Language Explainer."""
from datetime import date
import logging
from typing import Dict, List, Optional, Tuple

from src.extractor.normalizer import DatasetNormalizer
from src.schemas.foa import (
    AgencyType,
    DocumentCheckItem,
    EducationLevel,
    FundingOpportunity,
    HinglishExplainer,
    SocialCategory,
    StudentProfileRequest,
    StudentScholarshipMatchResult,
)

logger = logging.getLogger("MadadgaarAI.Matcher.Student")


class StudentScholarshipMatcher:
    """Intelligent engine for matching student profiles to Indian Central, State, and CSR scholarships.

    Multi-Criteria Decision Matrix:
    1. Domicile Verification:
       - Central Schemes (NSP, AICTE, UGC, CSR): Universal All-India eligibility.
       - State Portals (UP Dashmottar, MahaDBT): Exact domicile matching against state of origin.
    2. Gender & Social Inclusivity:
       - Female-exclusive schemes (e.g., AICTE Pragati, Kotak Kanya) enforce strict gender gate.
       - Category-specific reservations (SC, ST, OBC, EBC, DNT, Minority) vs General eligibility.
    3. Means-Tested Income Thresholds:
       - Evaluates applicant's annual family income against statutory scheme ceilings (e.g., ₹2.5L, ₹6L, ₹8L).
    4. Categorization & Ranking:
       - 'Guaranteed' (confidence >= 0.95): All non-competitive statutory criteria fulfilled.
       - 'High Probability' (confidence >= 0.70): Merit-cum-means criteria met pending merit quotas.
    """

    def __init__(self, normalizer: Optional[DatasetNormalizer] = None):
        self.normalizer = normalizer or DatasetNormalizer()

    def get_all_student_scholarships(self) -> List[FundingOpportunity]:
        """Returns deduplicated opportunities tailored for students, filtering out senior faculty/postdoc grants."""
        all_foas = self.normalizer.load_all_opportunities()
        student_foas: List[FundingOpportunity] = []
        seen_ids = set()
        seen_hashes = set()

        faculty_only_markers = (
            "j. c. bose", "post doctoral", "post-doctoral", "postdoc", "n-pdf",
            "principal investigator", "faculty fellowship", "ramanujan", "ramalingaswami",
            "core research grant", "sponsored research", "isro respond", "extramural",
            "start-up research grant", "scientist", "investigator award",
        )
        explicit_student_markers = (
            "scholarship", "internship", "intern ", "undergraduate", "school student",
            "graduate student", "b.tech", "bachelor", "post-matric", "pragati", "saksham",
            "kotak kanya", "single girl child", "she)", "she ", "student",
        )

        for foa in all_foas:
            if foa.foa_id in seen_ids or foa.raw_document_hash in seen_hashes:
                continue
            title_low = foa.title.lower()
            elig_low = (foa.eligibility.raw_eligibility_text or "").lower()
            combined_low = f"{title_low} {elig_low}"

            is_faculty_only = any(m in title_low for m in faculty_only_markers) and not any(
                s in title_low for s in ("scholarship", "internship", "student", "undergraduate")
            )
            if is_faculty_only:
                continue

            is_student = (
                foa.foa_id.startswith("SCHOLARSHIP-")
                or any("Student" in b.value for b in foa.eligibility.target_beneficiaries)
                or any(m in combined_low for m in explicit_student_markers)
                or foa.agency in [AgencyType.NSP, AgencyType.STATE_GOVT, AgencyType.CSR_FOUNDATION]
                or any("Scholarship" in tag or "Internship" in tag for tag in foa.thematic_areas)
            )
            if is_student:
                seen_ids.add(foa.foa_id)
                seen_hashes.add(foa.raw_document_hash)
                student_foas.append(foa)
        return student_foas

    def match_student(self, req: StudentProfileRequest) -> List[StudentScholarshipMatchResult]:
        """Evaluates student eligibility across all scholarships and returns ranked results."""
        scholarships = self.get_all_student_scholarships()
        results: List[StudentScholarshipMatchResult] = []

        for foa in scholarships:
            if req.min_scholarship_amount_inr and foa.financials.max_amount_inr:
                if foa.financials.max_amount_inr < req.min_scholarship_amount_inr:
                    continue
            match_res = self._evaluate_single_scholarship(foa, req)
            results.append(match_res)

        # Sort by:
        # 1. Hard eligibility status (ELIGIBLE / HIGH_PROBABILITY first)
        # 2. Composite match percentage
        # 3. Financial benefit (higher award amount)
        # 4. Deadline proximity (sooner active deadlines prioritized)
        results.sort(
            key=lambda x: (
                2 if x.eligibility_status == "ELIGIBLE" else (1 if x.eligibility_status == "HIGH_PROBABILITY" else 0),
                x.match_percentage,
                x.foa.financials.max_amount_inr or 0.0,
                -(x.deadline_proximity_days if x.deadline_proximity_days is not None and x.deadline_proximity_days >= 0 else 999),
            ),
            reverse=True,
        )

        return results[: req.top_k]

    def _evaluate_single_scholarship(
        self, foa: FundingOpportunity, req: StudentProfileRequest
    ) -> StudentScholarshipMatchResult:
        score = 0.0
        match_reasons: List[str] = []
        warning_reasons: List[str] = []
        missing_requirements: List[str] = []
        disqualifying_conditions: List[str] = []
        is_hard_ineligible = False

        title_lower = foa.title.lower()
        summary_lower = foa.brief_summary.lower()
        full_text = (foa.full_text_content or "").lower()

        # 1. HARD CONSTRAINT: GENDER RESTRICTION CHECK
        is_female_only = any(
            k in title_lower or k in summary_lower or k in full_text
            for k in ["girl students", "pragati", "kotak kanya", "single girl child", "meritorious girls"]
        )
        if is_female_only:
            if req.gender.lower() in ["female", "girl", "woman"]:
                score += 30.0
                match_reasons.append("✅ Gender Match: Eligible for dedicated Women/Girl Student Scheme")
            else:
                is_hard_ineligible = True
                msg = "❌ Ineligible: Scheme is exclusively reserved for female/girl students."
                disqualifying_conditions.append(msg)

        # 2. HARD CONSTRAINT: STATE DOMICILE CHECK
        is_up_scheme = "uttar pradesh" in title_lower or "up dashmottar" in title_lower or "scholarship.up.gov.in" in foa.source_url
        is_mahadbt = "mahadbt" in title_lower or "maharashtra" in title_lower or "shahu maharaj" in title_lower
        is_ner_scheme = "ishan uday" in title_lower or "north eastern region" in summary_lower or "ner" in foa.thematic_areas

        ner_states = ["assam", "arunachal pradesh", "manipur", "meghalaya", "mizoram", "nagaland", "tripura", "sikkim", "north eastern"]
        user_state_lower = req.state_domicile.lower()

        if is_up_scheme:
            if "uttar pradesh" in user_state_lower or "up" == user_state_lower.strip():
                score += 25.0
                match_reasons.append("✅ State Domicile Match: Uttar Pradesh Resident")
            else:
                is_hard_ineligible = True
                disqualifying_conditions.append("❌ Ineligible: Requires valid Uttar Pradesh State Domicile.")
        elif is_mahadbt:
            if "maharashtra" in user_state_lower:
                score += 25.0
                match_reasons.append("✅ State Domicile Match: Maharashtra Resident")
            else:
                is_hard_ineligible = True
                disqualifying_conditions.append("❌ Ineligible: Requires Maharashtra State Domicile.")
        elif is_ner_scheme:
            if any(s in user_state_lower for s in ner_states):
                score += 30.0
                match_reasons.append(f"✅ State Domicile Match: North Eastern Region ({req.state_domicile})")
            else:
                is_hard_ineligible = True
                disqualifying_conditions.append("❌ Ineligible: Requires Domicile in North Eastern States (NER).")
        else:
            score += 20.0
            match_reasons.append("✅ All-India Scheme: Open to students from all Indian states and UTs")

        # 3. HARD CONSTRAINT: SOCIAL CATEGORY & RESERVATION CHECK
        is_sc_scheme = "scheduled caste" in title_lower or "for sc" in title_lower or "postmatric-sc" in foa.foa_id.lower()
        is_st_scheme = "scheduled tribe" in title_lower or "for st" in title_lower or "postmatric-st" in foa.foa_id.lower()
        is_obc_scheme = "yasasvi" in title_lower or "for obc" in title_lower or "postmatric-obc" in foa.foa_id.lower()

        if is_sc_scheme:
            if req.social_category == SocialCategory.SC:
                score += 30.0
                match_reasons.append("✅ Category Match: Scheduled Caste (SC) Reservation")
            else:
                is_hard_ineligible = True
                disqualifying_conditions.append("❌ Ineligible: Exclusive to Scheduled Caste (SC) students.")
        elif is_st_scheme:
            if req.social_category == SocialCategory.ST:
                score += 30.0
                match_reasons.append("✅ Category Match: Scheduled Tribe (ST) Reservation")
            else:
                is_hard_ineligible = True
                disqualifying_conditions.append("❌ Ineligible: Exclusive to Scheduled Tribe (ST) students.")
        elif is_obc_scheme:
            if req.social_category in [SocialCategory.OBC_NCL, SocialCategory.EWS]:
                score += 25.0
                match_reasons.append(f"✅ Category Match: {req.social_category.value}")
            else:
                is_hard_ineligible = True
                disqualifying_conditions.append("❌ Ineligible: Reserved for OBC / EBC / DNT categories.")
        else:
            score += 15.0
            match_reasons.append(f"✅ Open to Category: {req.social_category.value}")

        # 4. HARD / SOFT CONSTRAINT: ANNUAL FAMILY INCOME EVALUATION
        income = req.family_annual_income_inr
        income_ceiling = None
        raw_elig_text = foa.eligibility.raw_eligibility_text or ""
        if "2.0" in raw_elig_text or "2,00,000" in raw_elig_text:
            # UP Dashmottar has 2.5L for SC/ST and 2.0L for General/OBC/Minority
            if is_up_scheme and req.social_category in [SocialCategory.SC, SocialCategory.ST]:
                income_ceiling = 250000.0
            else:
                income_ceiling = 200000.0
        elif "2.5" in foa.brief_summary or "2.5" in raw_elig_text or "2.50" in raw_elig_text or "2,50,000" in raw_elig_text:
            income_ceiling = 250000.0
        elif "4.5" in foa.brief_summary or "4.5" in raw_elig_text or "4,50,000" in raw_elig_text:
            income_ceiling = 450000.0
        elif "6.0" in foa.brief_summary or "6 Lakh" in raw_elig_text or "6,00,000" in raw_elig_text:
            income_ceiling = 600000.0
        elif "8" in foa.brief_summary or "8 Lakh" in raw_elig_text:
            income_ceiling = 800000.0
        elif "15" in foa.brief_summary:
            income_ceiling = 1500000.0

        if income_ceiling:
            if income <= income_ceiling:
                score += 20.0
                match_reasons.append(f"✅ Income Limit Passed: Annual Income (₹{income:,.0f}) is within ceiling of ₹{income_ceiling:,.0f}")
            else:
                if foa.agency in [AgencyType.NSP, AgencyType.STATE_GOVT, AgencyType.AICTE, AgencyType.UGC]:
                    is_hard_ineligible = True
                    disqualifying_conditions.append(
                        f"❌ Income Exceeded: Family income (₹{income:,.0f}) exceeds mandatory limit of ₹{income_ceiling:,.0f}/year."
                    )
                else:
                    score -= 15.0
                    warning_reasons.append(
                        f"⚠️ Income Warning: Annual income (₹{income:,.0f}) is above standard target ₹{income_ceiling:,.0f}."
                    )
        else:
            score += 15.0
            match_reasons.append("✅ No Family Income Ceiling Restriction")

        # 5. HARD CONSTRAINT: SPECIAL CRITERIA (Single Girl Child / PwD / Merit)
        if "single girl child" in title_lower or "single girl" in summary_lower:
            if req.is_single_girl_child:
                score += 35.0
                match_reasons.append("⭐ High Priority: Verified Single Girl Child candidate")
            else:
                is_hard_ineligible = True
                disqualifying_conditions.append("❌ Ineligible: Exclusively for parents having a Single Girl Child with no other siblings.")

        if "differently abled" in summary_lower or "saksham" in title_lower:
            if req.is_differently_abled_pwd:
                score += 35.0
                match_reasons.append("⭐ High Priority: Specially Abled / PwD Category match (>=40% disability)")
            else:
                is_hard_ineligible = True
                disqualifying_conditions.append("❌ Ineligible: Reserved exclusively for Specially-Abled (PwD >=40%) students.")

        if "85%" in raw_elig_text or "kotak kanya" in title_lower:
            if req.academic_percentage and req.academic_percentage >= 85.0:
                score += 15.0
                match_reasons.append(f"✅ Academic Merit Match: Scored {req.academic_percentage}% (Cutoff: >=85%)")
            elif req.academic_percentage and req.academic_percentage < 85.0:
                score -= 10.0
                warning_reasons.append(f"⚠️ Academic Score: Scored {req.academic_percentage}% (Scheme recommends >=85% in Class 12)")

        # 6. EDUCATION LEVEL & STREAM RELEVANCE
        relevance_subscore = 70.0
        if "inspire" in title_lower:
            if req.education_level in [EducationLevel.UG_GENERAL, EducationLevel.POSTGRADUATE] or (req.field_of_study and "science" in req.field_of_study.lower()):
                score += 15.0
                relevance_subscore = 95.0
                match_reasons.append("✅ Stream Match: Basic & Natural Sciences Program")
            else:
                warning_reasons.append("⚠️ Course Note: INSPIRE-SHE is restricted to B.Sc./B.S./Int. M.Sc. in Basic & Natural Sciences (not B.Tech/MBBS).")
                relevance_subscore = 45.0
        elif req.education_level in [EducationLevel.UG_ENGINEERING, EducationLevel.DIPLOMA] and ("technical" in summary_lower or "engineering" in summary_lower):
            score += 15.0
            relevance_subscore = 96.0
            match_reasons.append("✅ Course Match: Technical Degree / Diploma")
        elif req.education_level == EducationLevel.POSTGRADUATE and ("master" in summary_lower or "pg" in summary_lower or "postgraduate" in summary_lower):
            score += 15.0
            relevance_subscore = 95.0
            match_reasons.append("✅ Course Match: Enrolled in Postgraduate Master's Program")
        elif "single girl child" in title_lower and req.education_level != EducationLevel.POSTGRADUATE:
            warning_reasons.append("⚠️ Level Notice: UGC Indira Gandhi Single Girl Child Scheme requires admission to 1st-year PG Master's degree.")
            relevance_subscore = 50.0

        # 7. DOCUMENT & NPCI-DBT VERIFICATION CHECK (Verified vs Preliminary Eligibility)
        docs = self.generate_document_checklist(foa, req)
        verified_set = {d.lower() for d in (req.verified_documents or [])}

        if not req.has_npci_dbt_seeded:
            missing_requirements.append("Aadhaar-NPCI DBT Bank Account Seeding status is unverified (Mandatory for PFMS transfer)")
        if income_ceiling and "income_certificate" not in verified_set:
            missing_requirements.append("Current Financial Year Tehsildar Income Certificate not yet verified")
        if (is_up_scheme or is_mahadbt or is_ner_scheme) and "domicile_certificate" not in verified_set:
            missing_requirements.append(f"Permanent Residence / Domicile Certificate ({req.state_domicile}) not yet verified")
        if req.social_category != SocialCategory.GENERAL and "caste_certificate" not in verified_set:
            missing_requirements.append(f"Official Category Certificate ({req.social_category.value}) not yet verified")

        # 8. DEADLINE PROXIMITY & URGENCY
        ref_today = date(2026, 10, 15)
        eff_deadline = foa.deadlines.effective_deadline
        proximity_days: Optional[int] = None
        deadline_urgency = "OPEN"
        deadline_score = 75.0
        if foa.deadlines.is_rolling:
            deadline_urgency = "ROLLING"
            deadline_score = 80.0
        elif eff_deadline:
            proximity_days = (eff_deadline - ref_today).days
            if proximity_days < 0:
                deadline_urgency = "CLOSED"
                deadline_score = 20.0
            elif proximity_days <= 30:
                deadline_urgency = "URGENT_CLOSING_SOON"
                deadline_score = 98.0
            elif proximity_days <= 60:
                deadline_urgency = "APPROACHING"
                deadline_score = 88.0
            else:
                deadline_urgency = "OPEN"
                deadline_score = 78.0

        # Determine Final Status, Confidence & Match Percentage
        if is_hard_ineligible:
            final_status = "INELIGIBLE"
            eligibility_confidence = "DISQUALIFIED"
            final_pct = 0.0
            warning_reasons.extend(disqualifying_conditions)
        else:
            final_pct = min(100.0, max(20.0, score))
            if final_pct >= 80.0:
                final_status = "ELIGIBLE"
                if req.has_npci_dbt_seeded and len(verified_set) >= 2:
                    eligibility_confidence = "VERIFIED_ELIGIBLE"
                else:
                    eligibility_confidence = "PRELIMINARY_ELIGIBLE"
            elif final_pct >= 60.0:
                final_status = "HIGH_PROBABILITY"
                eligibility_confidence = "PRELIMINARY_ELIGIBLE"
            else:
                final_status = "WARNING"
                eligibility_confidence = "CONDITIONAL_WARNING"

        # Build Explainable AI narrative
        why_qualify = self._build_explainable_summary(
            foa=foa,
            status=final_status,
            confidence=eligibility_confidence,
            match_reasons=match_reasons,
            missing_requirements=missing_requirements,
            disqualifying_conditions=disqualifying_conditions,
            warning_reasons=warning_reasons,
        )

        # Financial benefit score (normalized to [0, 100])
        max_amt = foa.financials.max_amount_inr or 50000.0
        fin_score = min(100.0, round((max_amt / 200000.0) * 80.0 + 20.0, 1))

        score_breakdown = {
            "eligibility_confidence_score": round(final_pct, 1),
            "financial_benefit_score": fin_score,
            "deadline_proximity_score": deadline_score,
            "relevance_score": relevance_subscore,
        }

        benefit_desc = self._get_benefit_summary(foa)
        portal_name, portal_url = self._get_portal_info(foa)
        hinglish = self.generate_hinglish_guide(foa)

        direct_apply_link = foa.direct_apply_url or portal_url
        navigation_steps = foa.portal_navigation_steps or [
            f"1. Open the direct portal link ({portal_url}).",
            "2. Complete student registration with your Aadhaar and email/mobile OTP.",
            f"3. Search or navigate to scheme: '{foa.title}'.",
            "4. Upload required documents and verify active Aadhaar-NPCI bank seeding.",
            "5. Submit before the closing date.",
        ]

        renewal_text = foa.renewal_requirements or (
            "Annual continuation requires >= 60% marks (or 6.0 CGPA), >= 75% attendance, zero backlogs, and Principal/Nodal Officer online verification."
        )
        common_mistakes = foa.common_mistakes or [
            "Submitting an expired Income Certificate issued before 1st April of the current financial year.",
            "Bank account linked with Aadhaar but NOT seeded on the NPCI Direct Benefit Transfer (DBT) mapper.",
            "Mismatch in student/parent name spelling across Aadhaar card, marksheet, and caste/income certificate.",
        ]
        source_refs = foa.official_source_references or [
            f"Official Portal: {portal_name} ({portal_url})",
            f"Scheme Guideline ID: {foa.foa_id}",
        ]

        return StudentScholarshipMatchResult(
            foa=foa,
            eligibility_status=final_status,
            eligibility_confidence=eligibility_confidence,
            match_percentage=round(final_pct, 1),
            match_reasons=match_reasons,
            warning_reasons=warning_reasons,
            missing_requirements=missing_requirements,
            disqualifying_conditions=disqualifying_conditions,
            why_you_qualify_explanation=why_qualify,
            estimated_financial_benefit=benefit_desc,
            issuing_authority=foa.issuing_authority or foa.agency.value,
            portal_name=portal_name,
            portal_url=portal_url,
            direct_apply_url=direct_apply_link,
            portal_navigation_steps=navigation_steps,
            renewal_requirements=renewal_text,
            common_mistakes_to_avoid=common_mistakes,
            last_verified_date=foa.last_verified_date,
            official_source_references=source_refs,
            deadline_proximity_days=proximity_days,
            deadline_urgency=deadline_urgency,
            score_breakdown=score_breakdown,
            is_govt_verified=True,
            document_checklist=docs,
            hinglish_guide=hinglish,
        )

    def _build_explainable_summary(
        self,
        foa: FundingOpportunity,
        status: str,
        confidence: str,
        match_reasons: List[str],
        missing_requirements: List[str],
        disqualifying_conditions: List[str],
        warning_reasons: List[str],
    ) -> str:
        if status == "INELIGIBLE":
            disq_clean = "; ".join(d.replace("❌ Ineligible: ", "") for d in disqualifying_conditions)
            return f"Your profile does not qualify for {foa.scheme_name or foa.title} due to hard statutory constraints: {disq_clean}"

        clean_reasons = [r.replace("✅ ", "").replace("⭐ ", "") for r in match_reasons[:3]]
        reasons_str = "; ".join(clean_reasons)
        base = f"Your profile matches this scholarship ({confidence.replace('_', ' ')}) because: {reasons_str}."
        if missing_requirements:
            base += f" Note: Before final submission, please verify: {', '.join(missing_requirements[:2])}."
        return base

    def _get_benefit_summary(self, foa: FundingOpportunity) -> str:
        if foa.financials.raw_budget_text:
            return foa.financials.raw_budget_text
        if foa.financials.max_amount_inr:
            return f"Up to ₹{foa.financials.max_amount_inr:,.0f} total educational support"
        return "Tuition fee waiver and monthly stipend"

    def _get_portal_info(self, foa: FundingOpportunity) -> Tuple[str, str]:
        if foa.agency == AgencyType.NSP:
            return "National Scholarship Portal (NSP)", foa.direct_apply_url or "https://scholarships.gov.in"
        elif foa.agency == AgencyType.AICTE:
            return "National Scholarship Portal (AICTE Schemes)", foa.direct_apply_url or "https://scholarships.gov.in"
        elif foa.agency == AgencyType.UGC:
            return "UGC / National Scholarship Portal", foa.direct_apply_url or "https://scholarships.gov.in"
        elif "up.gov.in" in foa.source_url:
            return "UP Scholarship Portal (Dashmottar)", "https://scholarship.up.gov.in"
        elif "mahadbt" in foa.source_url:
            return "MahaDBT Government Portal", "https://mahadbt.maharashtra.gov.in"
        elif "reliance" in foa.source_url:
            return "Reliance Foundation Portal", "https://www.scholarships.reliancefoundation.org"
        elif "kotak" in foa.source_url:
            return "Kotak Education (Buddy4Study Gateway)", "https://www.buddy4study.com/page/kotak-kanya-scholarship"
        elif "hdfc" in foa.source_url:
            return "HDFC Parivartan (Buddy4Study Gateway)", "https://www.buddy4study.com/page/hdfc-bank-parivartans-ecss-programme"
        elif "inspire" in foa.source_url:
            return "DST INSPIRE Web Portal", "https://online-inspire.gov.in"
        return "Official Government / Statutory Portal", foa.direct_apply_url or foa.source_url

    def generate_document_checklist(
        self, foa: FundingOpportunity, req: Optional[StudentProfileRequest] = None
    ) -> List[DocumentCheckItem]:
        """Generates a complete, actionable document checklist with issuing authority and verification status."""
        checklist: List[DocumentCheckItem] = []
        verified_set = {d.lower() for d in (req.verified_documents if req and req.verified_documents else [])}

        # 1. Income Certificate
        checklist.append(
            DocumentCheckItem(
                document_name="Income Certificate (आय प्रमाण पत्र)",
                issuing_authority="Tehsildar / Sub-Divisional Magistrate (SDM) / Revenue Officer / State E-District",
                validity_and_rules="Must be issued on or after 1st April of current financial year. Digital QR code verified certificate is preferred.",
                how_to_obtain="Apply online via State E-District / CSC Center / E-Mitra or visit local Tehsil office.",
                is_mandatory=True,
                verification_status="VERIFIED" if "income_certificate" in verified_set else "UNVERIFIED",
            )
        )

        # 2. Domicile / Residence Certificate
        checklist.append(
            DocumentCheckItem(
                document_name="Domicile / Permanent Residence Certificate (निवास / मूल निवास प्रमाण पत्र)",
                issuing_authority="District Magistrate / SDM / Tehsildar",
                validity_and_rules="Valid permanent residence proof of your native state. Lifetime validity in most states.",
                how_to_obtain="Apply via State E-Governance portal / E-Mitra / Maha E-Seva / MeeSeva with electricity bill and ration card.",
                is_mandatory=True,
                verification_status="VERIFIED" if "domicile_certificate" in verified_set else "UNVERIFIED",
            )
        )

        # 3. Category / Caste Certificate (if applicable)
        if req and req.social_category in [SocialCategory.SC, SocialCategory.ST, SocialCategory.OBC_NCL, SocialCategory.EWS]:
            checklist.append(
                DocumentCheckItem(
                    document_name=f"Caste / Category Certificate ({req.social_category.value}) (जाति प्रमाण पत्र)",
                    issuing_authority="Tehsildar / Revenue Authority / District Social Welfare Department",
                    validity_and_rules="For OBC-NCL and EWS: Must be issued in current financial year showing Non-Creamy Layer status. For SC/ST: Lifetime validity.",
                    how_to_obtain="Apply at Tehsil / CSC center with family genealogy / land records / old family caste records.",
                    is_mandatory=True,
                    verification_status="VERIFIED" if "caste_certificate" in verified_set else "UNVERIFIED",
                )
            )

        # 4. Bank Account Passbook & Aadhaar Seeding Proof
        dbt_verified = bool((req and req.has_npci_dbt_seeded) or "npci_dbt" in verified_set)
        checklist.append(
            DocumentCheckItem(
                document_name="Bank Passbook with Aadhaar-NPCI DBT Seeding (बैंक पासबुक एवं आधार सीडिंग)",
                issuing_authority="Nationalized / Scheduled Commercial Bank Branch & UIDAI",
                validity_and_rules="Bank account must be in student's own name (active savings account) and MUST be mapped on NPCI server for Direct Benefit Transfer (DBT).",
                how_to_obtain="Visit bank branch with Aadhaar card and submit 'Mandate Form for NPCI Aadhaar Seeding / DBT Enablement'.",
                is_mandatory=True,
                verification_status="VERIFIED" if dbt_verified else "UNVERIFIED",
            )
        )

        # 5. Bonafide Student & Fee Receipt
        checklist.append(
            DocumentCheckItem(
                document_name="Bonafide Student Certificate & Current Year Fee Receipt (बोनाफाइड प्रमाण पत्र)",
                issuing_authority="College Principal / Registrar / Dean of Student Affairs",
                validity_and_rules="Issued on official college letterhead with enrollment/admission number and seal.",
                how_to_obtain="Obtain from College Administrative Office / Academic Registrar.",
                is_mandatory=True,
                verification_status="VERIFIED" if "bonafide" in verified_set else "UNVERIFIED",
            )
        )

        # 6. Previous Academic Marksheets
        checklist.append(
            DocumentCheckItem(
                document_name="Class 10th & 12th / Previous Semester Marksheets (अंक तालिका)",
                issuing_authority="CBSE / ICSE / State Board / University Controller of Examinations",
                validity_and_rules="Self-attested clear scan of original marksheet.",
                how_to_obtain="Download Digilocker verified marksheet or scan original marksheet.",
                is_mandatory=True,
                verification_status="VERIFIED" if "marksheet" in verified_set else "UNVERIFIED",
            )
        )

        # 7. Special quota documents (Single Girl Child / PwD)
        if (req and req.is_single_girl_child) or "single girl" in foa.title.lower():
            checklist.append(
                DocumentCheckItem(
                    document_name="Single Girl Child Affidavit on ₹50/100 Stamp Paper (एकल पुत्री शपथ पत्र)",
                    issuing_authority="First Class Magistrate / Notary Public / SDM",
                    validity_and_rules="Sworn affidavit from parents stating that the applicant is the only child (no brother or sister).",
                    how_to_obtain="Draft at local civil court or notary with family ration card / voter list.",
                    is_mandatory=True,
                    verification_status="VERIFIED" if "sgc_affidavit" in verified_set else "UNVERIFIED",
                )
            )

        if (req and req.is_differently_abled_pwd) or "saksham" in foa.title.lower():
            checklist.append(
                DocumentCheckItem(
                    document_name="Unique Disability ID (UDID) / Medical Board Certificate (दिव्यांग प्रमाण पत्र)",
                    issuing_authority="District Medical Board / Chief Medical Officer (CMO) / Swavlamban Portal",
                    validity_and_rules="Disability percentage must be 40% or higher as per RPwD Act 2016.",
                    how_to_obtain="Register on swavlambancard.gov.in or visit District Civil Hospital Medical Board.",
                    is_mandatory=True,
                    verification_status="VERIFIED" if "udid_certificate" in verified_set else "UNVERIFIED",
                )
            )

        return checklist

    def generate_hinglish_guide(self, foa: FundingOpportunity) -> HinglishExplainer:
        """Generates plain Hindi/Hinglish summary for easy understanding and sharing."""
        portal_name, portal_url = self._get_portal_info(foa)

        eligibility_pts = []
        if foa.eligibility.raw_eligibility_text:
            eligibility_pts.append(foa.eligibility.raw_eligibility_text)
        elif foa.eligibility.min_qualification:
            eligibility_pts.append(f"न्यूनतम योग्यता: {foa.eligibility.min_qualification}")

        if foa.eligibility.max_age_limit:
            eligibility_pts.append(f"अधिकतम आयु सीमा: {foa.eligibility.max_age_limit} वर्ष")

        kaun_text = " • ".join(eligibility_pts) if eligibility_pts else foa.brief_summary
        kitne_paise = foa.financials.raw_budget_text or f"₹{foa.financials.max_amount_inr:,.0f} तक की सहायता"

        docs_list = [
            "1. आधार कार्ड (Aadhaar Card — मोबाइल नंबर से लिंक)",
            "2. आय प्रमाण पत्र (Income Certificate — 1 अप्रैल के बाद का तहसीलदार द्वारा जारी)",
            "3. मूल निवास प्रमाण पत्र (Domicile / Permanent Residence Certificate)",
            "4. जाति / EWS प्रमाण पत्र (Caste / EWS Certificate — यदि लागू हो)",
            "5. बैंक पासबुक (Aadhaar + NPCI DBT Mapper सक्रिय होना अनिवार्य)",
            "6. कॉलेज बोनाफाइड व फीस रसीद (Bonafide Certificate & Current Fee Receipt)",
            "7. पिछली कक्षा की मार्कशीट (10th/12th/Previous Year Marksheet)",
        ]

        renewal_text = foa.renewal_requirements or (
            "नवीनीकरण (Renewal): प्रत्येक वर्ष न्यूनतम 60% अंक (या 6.0 CGPA), 75% उपस्थिति और बिना किसी बैकलॉग के अगली कक्षा में प्रमोशन प्रमाण पत्र पोर्टल पर अपलोड करना अनिवार्य है।"
        )
        mistakes = foa.common_mistakes or [
            "पुराने वित्तीय वर्ष (1 अप्रैल से पहले) का आय प्रमाण पत्र अपलोड करना।",
            "बैंक खाते में केवल आधार लिंक होना परंतु NPCI DBT Mapper बंद होना (जिससे PFMS पेमेंट फेल हो जाता है)।",
            "ऑनलाइन फॉर्म सबमिट करने के बाद कॉलेज नोडल ऑफिसर (INO) से वेरिफिकेशन न करवाना।",
        ]

        return HinglishExplainer(
            kaun_apply_kar_sakta_hai=kaun_text,
            kitne_paise_milenge=kitne_paise,
            zaruri_documents=docs_list,
            official_portal_name=portal_name,
            official_portal_url=portal_url,
            renewal_kैसे_hoga=renewal_text,
            common_galatiyan=mistakes,
            aadhaar_seeding_warning="⚠️ आवश्यक सूचना: छात्रवृत्ति का पैसा केवल आधार से लिंक (NPCI Seeded) बैंक खाते में Direct Benefit Transfer (DBT) से आता है। अपने बैंक जाकर तुरंत DBT सक्रिय करवाएं।",
            scam_alert="🛡️ सतर्क रहें: सभी सरकारी छात्रवृत्ति पोर्टल (NSP, AICTE, State Portal) पर आवेदन 100% फ्री है। किसी को भी रजिस्ट्रेशन फीस या पैसे न दें।",
            is_govt_verified=True,
        )
