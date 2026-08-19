"""Applicant Profile Compliance and Eligibility Constraint Verifier."""
import logging
from typing import List, Optional
from src.schemas.foa import BeneficiaryType, ComplianceCheckResult, EligibilityCriteria, ProfileMatchRequest

logger = logging.getLogger("MadadgaarAI.Matcher.Compliance")


class ComplianceChecker:
    def __init__(self):
        pass

    def evaluate_compliance(
        self, profile: ProfileMatchRequest, eligibility: EligibilityCriteria
    ) -> ComplianceCheckResult:
        """Evaluates an applicant profile against FOA eligibility constraints."""
        reasons: List[str] = []
        is_compliant = True
        status = "ELIGIBLE"

        # 1. Role / Beneficiary Check
        if eligibility.target_beneficiaries:
            matched_role = any(
                b == profile.user_role or b == BeneficiaryType.FACULTY
                for b in eligibility.target_beneficiaries
            )
            if not matched_role:
                reasons.append(
                    f"Notice target role is {[b.value for b in eligibility.target_beneficiaries]}, but applicant profile is '{profile.user_role.value}'."
                )
                is_compliant = False
                status = "INELIGIBLE"

        # 2. Age Limit Check
        age_check = None
        if eligibility.max_age_limit and profile.applicant_age:
            if profile.applicant_age > eligibility.max_age_limit:
                reasons.append(
                    f"Applicant age ({profile.applicant_age} yrs) exceeds max eligibility cap of {eligibility.max_age_limit} yrs."
                )
                is_compliant = False
                status = "INELIGIBLE"
                age_check = f"FAILED: {profile.applicant_age} > {eligibility.max_age_limit}"
            else:
                age_check = f"PASSED: {profile.applicant_age} <= {eligibility.max_age_limit}"
        elif eligibility.max_age_limit:
            age_check = f"NOTICE: Max age is {eligibility.max_age_limit} (applicant age not provided)."

        # 3. Qualification Check
        qual_check = None
        if eligibility.min_qualification:
            if "ph.d" in eligibility.min_qualification.lower():
                if profile.highest_degree and "ph.d" not in profile.highest_degree.lower() and "doctor" not in profile.highest_degree.lower():
                    reasons.append(
                        f"Requires Ph.D. degree, but applicant specified '{profile.highest_degree}'."
                    )
                    status = "WARNING" if is_compliant else "INELIGIBLE"
                    qual_check = f"WARNING: Ph.D. preferred/required."
                else:
                    qual_check = "PASSED: Degree criterion satisfied."
            else:
                qual_check = f"INFO: {eligibility.min_qualification}"

        # 4. Institution Check
        inst_check = None
        if profile.institution_type:
            inst_check = f"Applicant Institution: {profile.institution_type}."
        elif eligibility.eligible_institutions:
            inst_check = f"Eligible Tiers: {', '.join(eligibility.eligible_institutions[:2])}."

        if not reasons:
            reasons.append("All eligibility criteria fully satisfied.")

        return ComplianceCheckResult(
            is_compliant=is_compliant,
            status=status,
            reasons=reasons,
            age_check=age_check,
            qualification_check=qual_check,
            institution_check=inst_check,
        )
