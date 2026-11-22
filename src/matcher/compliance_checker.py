"""Applicant Profile Compliance and Eligibility Constraint Verifier for Research Grants."""
import logging
from typing import List, Optional
from src.schemas.foa import (
    BeneficiaryType,
    ComplianceCheckResult,
    EligibilityCriteria,
    FundingOpportunity,
    ProfileMatchRequest,
)

logger = logging.getLogger("MadadgaarAI.Matcher.Compliance")


class ComplianceChecker:
    def __init__(self):
        pass

    def evaluate_compliance(
        self,
        profile: ProfileMatchRequest,
        eligibility: EligibilityCriteria,
        foa: Optional[FundingOpportunity] = None,
    ) -> ComplianceCheckResult:
        """Evaluates a researcher/applicant profile against FOA eligibility constraints."""
        reasons: List[str] = []
        satisfied: List[str] = []
        unverified: List[str] = []
        disqualifiers: List[str] = []
        improvements: List[str] = []

        is_compliant = True
        status = "ELIGIBLE"

        # 1. Role / Beneficiary Check
        if eligibility.target_beneficiaries:
            matched_role = any(
                b == profile.user_role or b == BeneficiaryType.FACULTY
                for b in eligibility.target_beneficiaries
            )
            if not matched_role:
                msg = f"Notice target role is {[b.value for b in eligibility.target_beneficiaries]}, but applicant profile is '{profile.user_role.value}'."
                reasons.append(msg)
                disqualifiers.append(msg)
                improvements.append(
                    f"Apply with a Principal Investigator or Co-PI holding a '{eligibility.target_beneficiaries[0].value}' designation."
                )
                is_compliant = False
                status = "INELIGIBLE"
            else:
                satisfied.append(
                    f"Applicant role '{profile.user_role.value}' aligns with eligible target beneficiary criteria."
                )

        # 2. Age Limit Check
        age_check = None
        if eligibility.max_age_limit and profile.applicant_age:
            if profile.applicant_age > eligibility.max_age_limit:
                msg = f"Applicant age ({profile.applicant_age} yrs) exceeds max eligibility cap of {eligibility.max_age_limit} yrs."
                reasons.append(msg)
                disqualifiers.append(msg)
                improvements.append(
                    "Check if statutory 3-to-5 year age relaxation applies (SC/ST/OBC/Women/PwD) or designate an eligible younger faculty member as PI."
                )
                is_compliant = False
                status = "INELIGIBLE"
                age_check = f"FAILED: {profile.applicant_age} > {eligibility.max_age_limit}"
            else:
                age_check = f"PASSED: {profile.applicant_age} <= {eligibility.max_age_limit}"
                satisfied.append(
                    f"Applicant age ({profile.applicant_age} yrs) is within the statutory ceiling of {eligibility.max_age_limit} yrs."
                )
        elif eligibility.max_age_limit:
            age_check = f"NOTICE: Max age is {eligibility.max_age_limit} (applicant age not provided)."
            unverified.append(f"Applicant age must be <= {eligibility.max_age_limit} years at call closing date.")

        # 3. Qualification Check
        qual_check = None
        if eligibility.min_qualification:
            if "ph.d" in eligibility.min_qualification.lower():
                if (
                    profile.highest_degree
                    and "ph.d" not in profile.highest_degree.lower()
                    and "phd" not in profile.highest_degree.lower()
                    and "doctor" not in profile.highest_degree.lower()
                    and "md" not in profile.highest_degree.lower()
                ):
                    msg = f"Requires Ph.D. degree, but applicant specified '{profile.highest_degree}'."
                    reasons.append(msg)
                    disqualifiers.append(msg)
                    improvements.append(
                        "Include a Ph.D.-qualified regular faculty member as Principal Investigator (PI)."
                    )
                    status = "WARNING" if is_compliant else "INELIGIBLE"
                    qual_check = "WARNING: Ph.D. preferred/required."
                elif profile.highest_degree:
                    qual_check = "PASSED: Degree criterion satisfied."
                    satisfied.append(
                        f"Academic qualification ({profile.highest_degree}) satisfies '{eligibility.min_qualification}'."
                    )
                else:
                    qual_check = f"INFO: {eligibility.min_qualification}"
                    unverified.append(f"Minimum qualification required: {eligibility.min_qualification}.")
            else:
                qual_check = f"INFO: {eligibility.min_qualification}"
                satisfied.append(f"Qualification requirement noted: {eligibility.min_qualification}.")

        # 4. Institution Check
        inst_check = None
        if profile.institution_type:
            inst_check = f"Applicant Institution: {profile.institution_type}."
            satisfied.append(f"Institutional affiliation specified: {profile.institution_type}.")
            if "private" in profile.institution_type.lower() and not profile.has_dsir_siro_recognition:
                unverified.append(
                    "Private/Deemed universities must verify active DSIR SIRO recognition and NGO-DARPAN / PFMS registration."
                )
                improvements.append(
                    "Confirm your institution's valid DSIR SIRO certificate and PFMS Unique Agency Code before submission."
                )
        elif eligibility.eligible_institutions:
            inst_check = f"Eligible Tiers: {', '.join(eligibility.eligible_institutions[:2])}."
            unverified.append(
                f"Host institution must belong to eligible tiers: {', '.join(eligibility.eligible_institutions[:3])}."
            )

        # 5. Publication & Experience Check
        raw_elig = (eligibility.raw_eligibility_text or "").lower()
        if "publication" in raw_elig or "sci" in raw_elig:
            if profile.sci_publications_count is not None:
                if profile.sci_publications_count >= 3:
                    satisfied.append(f"Track record of {profile.sci_publications_count} SCI/Scopus publications meets call expectations.")
                else:
                    unverified.append(f"Call recommends >= 2-3 SCI publications (profile lists {profile.sci_publications_count}).")
                    improvements.append("Highlight high-impact peer-reviewed journal papers or include a Co-PI with complementary SCI publications.")
            elif profile.publications_count is not None and profile.publications_count >= 3:
                satisfied.append(f"Publication record ({profile.publications_count} papers) supports PI eligibility.")
            else:
                unverified.append("Minimum SCI/peer-reviewed publication count in the proposed thrust area remains unverified.")

        if "5 years" in raw_elig:
            if profile.research_experience_years is not None:
                if profile.research_experience_years >= 5:
                    satisfied.append(f"Research/teaching experience ({profile.research_experience_years} yrs) meets the >= 5 years requirement.")
                else:
                    unverified.append(f"Scheme recommends >= 5 years experience (profile specifies {profile.research_experience_years} yrs).")
                    improvements.append("Add a senior faculty Co-PI with >= 5 years regular service.")
            else:
                unverified.append("Minimum 5 years teaching/research experience requirement is unverified.")

        # 6. Budget & Duration Compatibility Check (if FOA provided)
        budget_check = None
        duration_check = None
        if foa:
            max_grant = foa.financials.max_amount_inr
            if max_grant and profile.requested_funding_inr:
                if profile.requested_funding_inr > max_grant:
                    budget_check = f"EXCEEDS CAP: Requested ₹{profile.requested_funding_inr:,.0f} > Call Ceiling ₹{max_grant:,.0f}"
                    disqualifiers.append(
                        f"Requested budget (₹{profile.requested_funding_inr:,.0f}) exceeds scheme ceiling of ₹{max_grant:,.0f}."
                    )
                    improvements.append(
                        f"Revise total project budget to stay within ₹{max_grant:,.0f} (including {foa.financials.institutional_overhead_pct or 10}% overhead)."
                    )
                    if status == "ELIGIBLE":
                        status = "WARNING"
                else:
                    budget_check = f"COMPATIBLE: Requested ₹{profile.requested_funding_inr:,.0f} <= Ceiling ₹{max_grant:,.0f}"
                    satisfied.append(
                        f"Proposed budget (₹{profile.requested_funding_inr:,.0f}) fits within the ₹{max_grant:,.0f} grant ceiling."
                    )
            elif max_grant:
                budget_check = f"CEILING: Up to ₹{max_grant:,.0f}"

            if foa.duration_months and profile.preferred_duration_months:
                if profile.preferred_duration_months > foa.duration_months:
                    duration_check = f"WARNING: Preferred {profile.preferred_duration_months}m > Standard {foa.duration_months}m"
                    improvements.append(f"Scope project milestones to fit the standard {foa.duration_months}-month tenure.")
                else:
                    duration_check = f"COMPATIBLE: {profile.preferred_duration_months}m <= {foa.duration_months}m"
                    satisfied.append(f"Target timeline ({profile.preferred_duration_months} months) aligns with call duration ({foa.duration_months} months).")

        # Standard statutory unverified items for all Indian extramural grants
        unverified.append("Head of Institution Endorsement Certificate & No-Objection Certificate (NOC) must be signed on official letterhead.")
        if eligibility.requires_industry_partner and not profile.has_industry_partner:
            disqualifiers.append("Mandatory Industry Partner / Co-Investigator requirement not yet satisfied.")
            improvements.append("Onboard an Indian MSME/DPIIT-recognized industry collaborator with an MoU.")

        if not improvements:
            improvements.append(
                "Include proforma vendor quotations for equipment > ₹5 Lakhs and align work packages with GFR 2017 norms."
            )

        if not reasons:
            reasons.append("All evaluated hard eligibility criteria are satisfied.")

        return ComplianceCheckResult(
            is_compliant=is_compliant,
            status=status,
            reasons=reasons,
            age_check=age_check,
            qualification_check=qual_check,
            institution_check=inst_check,
            budget_compatibility_check=budget_check,
            duration_compatibility_check=duration_check,
            satisfied_criteria=satisfied,
            unverified_criteria=unverified,
            disqualifying_factors=disqualifiers,
            improvement_suggestions=improvements,
        )
