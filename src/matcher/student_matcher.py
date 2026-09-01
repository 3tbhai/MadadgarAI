"""Student Scholarship Matcher, Eligibility Evaluator, Document Checklist Generator, and Plain-Language Explainer."""
import logging
from typing import Dict, List, Optional

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
    """Intelligent engine for matching student profiles to Indian Central, State, and CSR scholarships."""

    def __init__(self, normalizer: Optional[DatasetNormalizer] = None):
        self.normalizer = normalizer or DatasetNormalizer()

    def get_all_student_scholarships(self) -> List[FundingOpportunity]:
        """Returns all opportunities tailored for students."""
        all_foas = self.normalizer.load_all_opportunities()
        student_foas = []
        for foa in all_foas:
            # Check ID prefix or beneficiary tags or agency types
            is_student = (
                foa.foa_id.startswith("SCHOLARSHIP-")
                or any("Student" in b.value for b in foa.eligibility.target_beneficiaries)
                or foa.agency in [AgencyType.NSP, AgencyType.UGC, AgencyType.STATE_GOVT, AgencyType.CSR_FOUNDATION]
                or any("Scholarship" in tag for tag in foa.thematic_areas)
            )
            if is_student:
                student_foas.append(foa)
        return student_foas

    def match_student(self, req: StudentProfileRequest) -> List[StudentScholarshipMatchResult]:
        """Evaluates student eligibility across all scholarships and returns ranked results."""
        scholarships = self.get_all_student_scholarships()
        results: List[StudentScholarshipMatchResult] = []

        for foa in scholarships:
            match_res = self._evaluate_single_scholarship(foa, req)
            results.append(match_res)

        # Sort by match percentage descending, then by estimated max amount
        results.sort(
            key=lambda x: (
                1 if x.eligibility_status in ["ELIGIBLE", "HIGH_PROBABILITY"] else 0,
                x.match_percentage,
                x.foa.financials.max_amount_inr or 0.0,
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
        is_hard_ineligible = False
        ineligible_reasons: List[str] = []

        title_lower = foa.title.lower()
        summary_lower = foa.brief_summary.lower()
        full_text = (foa.full_text_content or "").lower()

        # 1. GENDER RESTRICTION CHECK
        is_female_only = any(
            k in title_lower or k in summary_lower or k in full_text
            for k in ["girl students", "pragati", "kotak kanya", "single girl child", "women"]
        )
        if is_female_only:
            if req.gender.lower() in ["female", "girl", "woman"]:
                score += 30.0
                match_reasons.append("✅ Gender Match: Eligible for dedicated Women/Girl Student Scheme")
            else:
                is_hard_ineligible = True
                ineligible_reasons.append("❌ Ineligible: Scheme is exclusively reserved for female/girl students.")

        # 2. STATE DOMICILE CHECK
        is_up_scheme = "uttar pradesh" in title_lower or "up dashmottar" in title_lower or "scholarship.up.gov.in" in foa.source_url
        is_mahadbt = "mahadbt" in title_lower or "maharashtra" in title_lower or "shahu maharaj" in title_lower
        is_ner_scheme = "ishan uday" in title_lower or "north eastern region" in summary_lower or "ner" in foa.thematic_areas

        ner_states = ["assam", "arunachal pradesh", "manipur", "meghalaya", "mizoram", "nagaland", "tripura", "sikkim"]
        user_state_lower = req.state_domicile.lower()

        if is_up_scheme:
            if "uttar pradesh" in user_state_lower or "up" == user_state_lower.strip():
                score += 25.0
                match_reasons.append("✅ State Domicile Match: Uttar Pradesh Resident")
            else:
                is_hard_ineligible = True
                ineligible_reasons.append("❌ Ineligible: Requires valid Uttar Pradesh State Domicile.")
        elif is_mahadbt:
            if "maharashtra" in user_state_lower:
                score += 25.0
                match_reasons.append("✅ State Domicile Match: Maharashtra Resident")
            else:
                is_hard_ineligible = True
                ineligible_reasons.append("❌ Ineligible: Requires Maharashtra State Domicile.")
        elif is_ner_scheme:
            if any(s in user_state_lower for s in ner_states):
                score += 30.0
                match_reasons.append(f"✅ State Domicile Match: North Eastern Region ({req.state_domicile})")
            else:
                is_hard_ineligible = True
                ineligible_reasons.append("❌ Ineligible: Requires Domicile in North Eastern States (NER).")
        else:
            score += 20.0
            match_reasons.append("✅ All-India Scheme: Open to students from all Indian states and UTs")

        # 3. SOCIAL CATEGORY & RESERVATION CHECK
        is_sc_scheme = "scheduled caste" in title_lower or "for sc" in title_lower or "postmatric-sc" in foa.foa_id.lower()
        is_st_scheme = "scheduled tribe" in title_lower or "for st" in title_lower or "postmatric-st" in foa.foa_id.lower()
        is_obc_scheme = "yasasvi" in title_lower or "for obc" in title_lower or "postmatric-obc" in foa.foa_id.lower()

        if is_sc_scheme:
            if req.social_category == SocialCategory.SC:
                score += 30.0
                match_reasons.append("✅ Category Match: Scheduled Caste (SC) Reservation")
            else:
                is_hard_ineligible = True
                ineligible_reasons.append("❌ Ineligible: Exclusive to Scheduled Caste (SC) students.")
        elif is_st_scheme:
            if req.social_category == SocialCategory.ST:
                score += 30.0
                match_reasons.append("✅ Category Match: Scheduled Tribe (ST) Reservation")
            else:
                is_hard_ineligible = True
                ineligible_reasons.append("❌ Ineligible: Exclusive to Scheduled Tribe (ST) students.")
        elif is_obc_scheme:
            if req.social_category in [SocialCategory.OBC_NCL, SocialCategory.EWS]:
                score += 25.0
                match_reasons.append(f"✅ Category Match: {req.social_category.value}")
            else:
                is_hard_ineligible = True
                ineligible_reasons.append("❌ Ineligible: Reserved for OBC / EBC / DNT categories.")
        else:
            score += 15.0
            match_reasons.append(f"✅ Open to Category: {req.social_category.value}")

        # 4. ANNUAL FAMILY INCOME EVALUATION
        income = req.family_annual_income_inr
        income_ceiling = None
        raw_elig_text = foa.eligibility.raw_eligibility_text or ""
        if "2.5" in foa.brief_summary or "2.5" in raw_elig_text or "2.50" in raw_elig_text:
            income_ceiling = 250000.0
        elif "2.0" in raw_elig_text or "2,00,000" in raw_elig_text:
            income_ceiling = 200000.0
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
                if foa.agency in [AgencyType.NSP, AgencyType.STATE_GOVT]:
                    is_hard_ineligible = True
                    ineligible_reasons.append(
                        f"❌ Income Exceeded: Family income (₹{income:,.0f}) exceeds mandatory government limit of ₹{income_ceiling:,.0f}/year."
                    )
                else:
                    score -= 15.0
                    warning_reasons.append(
                        f"⚠️ Income Warning: Annual income (₹{income:,.0f}) is above standard target ₹{income_ceiling:,.0f}."
                    )

        # 5. SPECIAL CRITERIA (Single Girl Child / PwD / Merit)
        if "single girl child" in title_lower or "single girl" in summary_lower:
            if req.is_single_girl_child:
                score += 35.0
                match_reasons.append("⭐ High Priority: Verified Single Girl Child candidate")
            else:
                is_hard_ineligible = True
                ineligible_reasons.append("❌ Ineligible: Exclusively for parents having a Single Girl Child with no other siblings.")

        if "differently abled" in summary_lower or "saksham" in title_lower:
            if req.is_differently_abled_pwd:
                score += 35.0
                match_reasons.append("⭐ High Priority: Specially Abled / PwD Category match (>=40% disability)")
            else:
                is_hard_ineligible = True
                ineligible_reasons.append("❌ Ineligible: Reserved exclusively for Specially-Abled (PwD >=40%) students.")

        if "85%" in raw_elig_text or "kotak kanya" in title_lower:
            if req.academic_percentage and req.academic_percentage >= 85.0:
                score += 15.0
                match_reasons.append(f"✅ Academic Merit Match: Scored {req.academic_percentage}% (Cutoff: >=85%)")
            elif req.academic_percentage and req.academic_percentage < 85.0:
                score -= 10.0
                warning_reasons.append(f"⚠️ Academic Score: Scored {req.academic_percentage}% (Scheme recommends >=85% in Class 12)")

        # 6. EDUCATION LEVEL RELEVANCE
        if req.education_level in [EducationLevel.UG_ENGINEERING, EducationLevel.DIPLOMA] and "technical" in summary_lower:
            score += 15.0
            match_reasons.append("✅ Course Match: Technical Degree / Diploma")
        elif req.education_level == EducationLevel.POSTGRADUATE and ("master" in summary_lower or "pg" in summary_lower):
            score += 15.0
            match_reasons.append("✅ Course Match: Enrolled in Postgraduate Master's Program")

        # Determine Final Status and Match Percentage
        if is_hard_ineligible:
            final_status = "INELIGIBLE"
            final_pct = 0.0
            warning_reasons.extend(ineligible_reasons)
        else:
            final_pct = min(100.0, max(20.0, score))
            if final_pct >= 80.0:
                final_status = "ELIGIBLE"
            elif final_pct >= 60.0:
                final_status = "HIGH_PROBABILITY"
            else:
                final_status = "WARNING"

        # Financial description
        benefit_desc = self._get_benefit_summary(foa)
        portal_name, portal_url = self._get_portal_info(foa)

        # Document Checklist
        docs = self.generate_document_checklist(foa, req)

        # Hinglish Explainer Guide
        hinglish = self.generate_hinglish_guide(foa)

        return StudentScholarshipMatchResult(
            foa=foa,
            eligibility_status=final_status,
            match_percentage=round(final_pct, 1),
            match_reasons=match_reasons,
            warning_reasons=warning_reasons,
            estimated_financial_benefit=benefit_desc,
            portal_name=portal_name,
            portal_url=portal_url,
            is_govt_verified=True,
            document_checklist=docs,
            hinglish_guide=hinglish,
        )

    def _get_benefit_summary(self, foa: FundingOpportunity) -> str:
        if foa.financials.raw_budget_text:
            return foa.financials.raw_budget_text
        if foa.financials.max_amount_inr:
            return f"Up to ₹{foa.financials.max_amount_inr:,.0f} total educational support"
        return "Tuition fee waiver and monthly stipend"

    def _get_portal_info(self, foa: FundingOpportunity) -> (str, str):
        if foa.agency == AgencyType.NSP:
            return "National Scholarship Portal (NSP)", "https://scholarships.gov.in"
        elif foa.agency == AgencyType.AICTE:
            return "AICTE Official Portal", "https://www.aicte-india.org"
        elif foa.agency == AgencyType.UGC:
            return "UGC Official Scholarship Portal", "https://www.ugc.gov.in"
        elif "up.gov.in" in foa.source_url:
            return "UP Scholarship Portal (Dashmottar)", "https://scholarship.up.gov.in"
        elif "mahadbt" in foa.source_url:
            return "MahaDBT Government Portal", "https://mahadbt.maharashtra.gov.in"
        elif "reliance" in foa.source_url:
            return "Reliance Foundation Portal", "https://www.scholarships.reliancefoundation.org"
        elif "kotak" in foa.source_url:
            return "Kotak Education Foundation", "https://kotakeducation.org/kotak-kanya-scholarship"
        elif "hdfc" in foa.source_url:
            return "HDFC Parivartan Portal", "https://www.hdfcbank.com"
        return "Official Government / Statutory Portal", foa.source_url

    def generate_document_checklist(
        self, foa: FundingOpportunity, req: Optional[StudentProfileRequest] = None
    ) -> List[DocumentCheckItem]:
        """Generates a complete, actionable document checklist with issuing authority."""
        checklist: List[DocumentCheckItem] = []

        # 1. Income Certificate
        checklist.append(
            DocumentCheckItem(
                document_name="Income Certificate (आय प्रमाण पत्र)",
                issuing_authority="Tehsildar / Sub-Divisional Magistrate (SDM) / Revenue Officer / State E-District",
                validity_and_rules="Must be issued on or after 1st April of current financial year. Digital QR code verified certificate is preferred.",
                how_to_obtain="Apply online via State E-District / CSC Center / E-Mitra or visit local Tehsil office.",
                is_mandatory=True,
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
                )
            )

        # 4. Bank Account Passbook & Aadhaar Seeding Proof
        checklist.append(
            DocumentCheckItem(
                document_name="Bank Passbook with Aadhaar-NPCI DBT Seeding (बैंक पासबुक एवं आधार सीडिंग)",
                issuing_authority="Nationalized / Scheduled Commercial Bank Branch & UIDAI",
                validity_and_rules="Bank account must be in student's own name (active savings account) and MUST be mapped on NPCI server for Direct Benefit Transfer (DBT).",
                how_to_obtain="Visit bank branch with Aadhaar card and submit 'Mandate Form for NPCI Aadhaar Seeding / DBT Enablement'.",
                is_mandatory=True,
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
            )
        )

        # 7. Special quota documents (Single Girl Child / PwD)
        if req and req.is_single_girl_child or "single girl" in foa.title.lower():
            checklist.append(
                DocumentCheckItem(
                    document_name="Single Girl Child Affidavit on ₹50/100 Stamp Paper (एकल पुत्री शपथ पत्र)",
                    issuing_authority="First Class Magistrate / Notary Public / SDM",
                    validity_and_rules="Sworn affidavit from parents stating that the applicant is the only child (no brother or sister).",
                    how_to_obtain="Draft at local civil court or notary with family ration card / voter list.",
                    is_mandatory=True,
                )
            )

        if req and req.is_differently_abled_pwd or "saksham" in foa.title.lower():
            checklist.append(
                DocumentCheckItem(
                    document_name="Unique Disability ID (UDID) / Medical Board Certificate (दिव्यांग प्रमाण पत्र)",
                    issuing_authority="District Medical Board / Chief Medical Officer (CMO) / Swavlamban Portal",
                    validity_and_rules="Disability percentage must be 40% or higher as per RPwD Act 2016.",
                    how_to_obtain="Register on swavlambancard.gov.in or visit District Civil Hospital Medical Board.",
                    is_mandatory=True,
                )
            )

        return checklist

    def generate_hinglish_guide(self, foa: FundingOpportunity) -> HinglishExplainer:
        """Generates plain Hindi/Hinglish summary for easy understanding and sharing."""
        portal_name, portal_url = self._get_portal_info(foa)

        # Kaun apply kar sakta hai
        eligibility_pts = []
        if foa.eligibility.raw_eligibility_text:
            eligibility_pts.append(foa.eligibility.raw_eligibility_text)
        elif foa.eligibility.min_qualification:
            eligibility_pts.append(f"न्यूनतम योग्यता: {foa.eligibility.min_qualification}")

        if foa.eligibility.max_age_limit:
            eligibility_pts.append(f"अधिकतम आयु सीमा: {foa.eligibility.max_age_limit} वर्ष")

        kaun_text = " • ".join(eligibility_pts) if eligibility_pts else foa.brief_summary

        # Kitne paise milenge
        kitne_paise = foa.financials.raw_budget_text or f"₹{foa.financials.max_amount_inr:,.0f} तक की सहायता"

        # Zaruri docs
        docs_list = [
            "1. आधार कार्ड (Aadhaar Card)",
            "2. आय प्रमाण पत्र (Income Certificate - 1 अप्रैल के बाद का)",
            "3. मूल निवास प्रमाण पत्र (Domicile Certificate)",
            "4. जाति प्रमाण पत्र (Caste Certificate - यदि लागू हो)",
            "5. बैंक पासबुक (Aadhaar + NPCI DBT लिंक होना आवश्यक)",
            "6. कॉलेज बोनाफाइड व फीस रसीद (Bonafide & Fee Receipt)",
            "7. पिछली कक्षा की मार्कशीट (10th/12th Marksheet)",
        ]

        return HinglishExplainer(
            kaun_apply_kar_sakta_hai=kaun_text,
            kitne_paise_milenge=kitne_paise,
            zaruri_documents=docs_list,
            official_portal_name=portal_name,
            official_portal_url=portal_url,
            aadhaar_seeding_warning="⚠️ आवश्यक सूचना: छात्रवृत्ति का पैसा केवल आधार से लिंक (NPCI Seeded) बैंक खाते में Direct Benefit Transfer (DBT) से आता है। अपने बैंक जाकर तुरंत DBT सक्रिय करवाएं।",
            scam_alert="🛡️ सतर्क रहें: सभी सरकारी छात्रवृत्ति पोर्टल (NSP, AICTE, State Portal) पर आवेदन 100% फ्री है। किसी को भी रजिस्ट्रेशन फीस या पैसे न दें।",
            is_govt_verified=True,
        )
