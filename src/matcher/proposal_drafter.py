"""Automated Grant Proposal & SOP Drafter with Optional Official Gemini API Tailoring."""
from datetime import datetime, timezone
import json
import logging
import os
from typing import Dict, List, Optional
from src.schemas.foa import AgencyType, FundingOpportunity, ProposalSection, ProposalSkeleton

logger = logging.getLogger("MadadgaarAI.Matcher.ProposalDrafter")


class ProposalDrafter:
    def __init__(self):
        self._genai_client = None
        self._cached_key = ""

    def _get_gemini_client(self):
        key = (os.getenv("GEMINI_API_KEY") or "").strip()
        if not key:
            return None
        try:
            from google import genai
            if self._genai_client is None or self._cached_key != key:
                self._genai_client = genai.Client(api_key=key)
                self._cached_key = key
            return self._genai_client
        except Exception as exc:
            logger.debug(f"Gemini drafter client unavailable: {exc}")
            return None

    def _enrich_sections_with_gemini(
        self,
        foa: FundingOpportunity,
        sections: List[ProposalSection],
        is_student_sop: bool,
        pi_name: str,
        institution_name: str,
        custom_abstract: Optional[str],
    ) -> List[ProposalSection]:
        """Tailors the top narrative sections using Gemini when GEMINI_API_KEY is configured."""
        client = self._get_gemini_client()
        if client is None:
            return sections
        try:
            from google.genai import types
            model = (os.getenv("SARAL_GEMINI_MODEL") or os.getenv("MADADGAAR_GEMINI_MODEL") or "gemini-2.5-flash").strip()
            doc_kind = "Statement of Purpose (SOP) / Cover Application" if is_student_sop else "Research Grant Proposal"
            prompt = (
                f"Generate tailored, concrete, non-generic draft content for the first 3 sections of a {doc_kind}.\n"
                f"Opportunity Title: {foa.title}\n"
                f"Organization / Agency: {foa.issuing_authority or foa.agency.value}\n"
                f"Summary: {foa.brief_summary}\n"
                f"Thematic Areas: {', '.join(foa.thematic_areas[:5])}\n"
                f"Applicant / PI: {pi_name} ({institution_name})\n"
                f"Applicant Focus / Abstract: {custom_abstract or 'Not provided'}\n\n"
                "Return strict JSON with exact keys: "
                '{"section_1": "...", "section_2": "...", "section_3": "..."}. '
                "Each value should be 90-140 words of crisp, directly usable draft prose."
            )
            resp = client.models.generate_content(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3,
                    max_output_tokens=900,
                    response_mime_type="application/json",
                ),
            )
            raw = (getattr(resp, "text", None) or "").strip()
            if not raw:
                return sections
            parsed = json.loads(raw)
            updated = list(sections)
            for idx, key in enumerate(("section_1", "section_2", "section_3")):
                val = parsed.get(key)
                if isinstance(val, str) and len(val.strip()) > 40 and idx < len(updated):
                    updated[idx] = updated[idx].model_copy(update={"drafted_content": val.strip()})
            return updated
        except Exception as exc:
            logger.debug(f"Gemini proposal tailoring fallback triggered: {exc}")
            return sections

    def draft_proposal_skeleton(
        self,
        foa: FundingOpportunity,
        project_title: Optional[str] = None,
        pi_name: str = "Applicant / Principal Investigator",
        institution_name: str = "Your Academic / Research Institution",
        custom_abstract: Optional[str] = None,
        use_llm: bool = False,
    ) -> ProposalSkeleton:
        """Generates an agency-tailored 11-section proposal or SOP blueprint with optional live Gemini tailoring."""
        scheme_title = foa.title
        low_title = f"{foa.title} {' '.join(foa.thematic_areas)}".lower()
        is_student_sop = any(k in low_title for k in ("intern", "scholarship", "undergraduate", "student", "fellowship")) and not any(
            k in low_title for k in ("principal investigator", "core research grant", "faculty", "extramural")
        )
        primary_thrust = (
            foa.ontology_tags[0].thematic_thrust
            if foa.ontology_tags
            else (foa.thematic_areas[0] if foa.thematic_areas else "Emerging Scientific Systems")
        )
        thematic_str = ", ".join(foa.thematic_areas[:4]) if foa.thematic_areas else primary_thrust

        suggested_titles = [
            project_title or f"Indigenous Design, Algorithmic Optimization, and Field Validation in {primary_thrust}",
            f"Scalable Framework for {foa.thematic_areas[0] if foa.thematic_areas else 'Next-Generation Systems'}: Translational Deployment under {foa.agency.value}",
            f"Data-Driven Modeling and Hardware-Accelerated Architecture for {primary_thrust}",
        ]
        target_title = suggested_titles[0]

        max_budget = foa.financials.max_amount_inr or 4000000.0
        overhead_pct = foa.financials.institutional_overhead_pct if foa.financials.institutional_overhead_pct is not None else 10.0
        duration_m = foa.duration_months or 36
        stipend_mo = foa.financials.stipend_monthly_inr or 37000.0

        equip_pct = 0.40
        manpower_pct = 0.30
        consumables_pct = 0.15
        travel_contingency_pct = max(0.05, round(1.0 - (equip_pct + manpower_pct + consumables_pct + (overhead_pct / 100.0)), 3))

        # Itemized Budget Suggestions (preserving exact keys required by tests)
        budget_map: Dict[str, str] = {
            "Non-Recurring (Capital Equipment)": f"₹ {max_budget * equip_pct:,.2f} ({equip_pct*100:.0f}%) - Dedicated Compute/Testbed Hardware, Precision Sensors & Lab Instruments",
            "Manpower (JRF / SRF / Postdoc)": f"₹ {max_budget * manpower_pct:,.2f} ({manpower_pct*100:.0f}%) - Project Fellow stipends (₹{stipend_mo:,.0f}/mo + HRA as per DST/MoF OM norms)",
            "Consumables & Cloud Compute": f"₹ {max_budget * consumables_pct:,.2f} ({consumables_pct*100:.0f}%) - Lab Reagents, Prototyping PCB/Wafer Fabrication, Cloud GPU & Dataset Licenses",
            "Domestic Travel, Contingency & Field Trials": f"₹ {max_budget * travel_contingency_pct:,.2f} ({travel_contingency_pct*100:.1f}%) - PAC Review Travel, Field Validation, Patent Filing & Contingency",
            "Institutional Overhead": f"₹ {max_budget * (overhead_pct / 100.0):,.2f} ({overhead_pct:.1f}%) - Host Institute Administrative & Infrastructure Charges (as per {foa.agency.value} norms)",
        }

        sections: List[ProposalSection] = [
            ProposalSection(
                section_title="1. Project Title Options & Executive Abstract",
                section_description="Concise technical abstract and suggested titles aligned with the agency call.",
                drafted_content=(
                    f"Selected Title: {target_title}\n"
                    f"Alternative Title A: {suggested_titles[1]}\n"
                    f"Alternative Title B: {suggested_titles[2]}\n\n"
                    f"Principal Investigator: {pi_name}\n"
                    f"Host Institution: {institution_name}\n"
                    f"Target Scheme: {foa.scheme_name or foa.title} ({foa.agency.value})\n"
                    f"Project Duration: {duration_m} Months | Total Proposed Outlay: ₹ {max_budget:,.2f}\n\n"
                    f"Executive Abstract:\n"
                    f"{custom_abstract or foa.brief_summary} "
                    f"This project proposes a rigorous, reproducible architecture addressing critical bottlenecks in {thematic_str}, "
                    f"delivering validated prototypes, open benchmark datasets, and indigenous intellectual property tailored to Indian operating conditions."
                ),
                tips=[
                    "Keep the executive abstract within 250-300 words for e-PMS / ANRF portal text boxes.",
                    "State the quantitative improvement over existing baselines in the final sentence of the abstract.",
                ],
            ),
            ProposalSection(
                section_title="2. Problem Statement & National Relevance",
                section_description="Clear articulation of the scientific/technological bottleneck and alignment with national missions.",
                drafted_content=(
                    f"Core Problem: Existing solutions in {thematic_str} suffer from high imported capital costs, "
                    f"limited robustness under diverse Indian demographic/environmental conditions, and lack of standardized open benchmarks.\n\n"
                    f"National Relevance: This proposal directly supports the statutory mandate of {foa.issuing_authority or foa.agency.value} "
                    f"and national flagship missions (Atmanirbhar Bharat, National Quantum/AI/Bio Mission) by building self-reliant domestic R&D capacity, "
                    f"reducing import dependency, and training specialized scientific manpower (JRF/SRF/PhD)."
                ),
                tips=[
                    "Quantify the socio-economic or industrial problem in the Indian context using official ministry/NITI Aayog statistics.",
                ],
            ),
            ProposalSection(
                section_title="3. Specific Research Objectives (SMART & Time-Targeted)",
                section_description="Discrete, measurable, and verifiable scientific objectives.",
                drafted_content=(
                    f"• Objective 1 (Months 1–{max(6, duration_m // 4)}): Mathematical formulation, domain dataset curation, and baseline characterization for {foa.thematic_areas[0] if foa.thematic_areas else 'the target system'}.\n"
                    f"• Objective 2 (Months {max(7, duration_m // 4 + 1)}–{max(18, (duration_m * 2) // 3)}): Design, implementation, and iterative optimization of the core algorithmic/experimental framework.\n"
                    f"• Objective 3 (Months {max(19, (duration_m * 2) // 3 + 1)}–{duration_m - 3}): Hardware-in-the-loop / clinical / field validation, scalability stress-testing, and comparative benchmarking.\n"
                    f"• Objective 4 (Months {duration_m - 2}–{duration_m}): Technology readiness packaging (TRL 4–6), Indian Patent filing, open-source artifact release, and final project report submission."
                ),
                tips=[
                    "Limit to 3–4 crisp objectives; each objective must map directly to a Work Package and a measurable KPI.",
                ],
            ),
            ProposalSection(
                section_title="4. State-of-the-Art Literature Review Outline & Gap Analysis",
                section_description="Structured synthesis of international and national status identifying critical research gaps.",
                drafted_content=(
                    "4.1 International Status:\n"
                    f"Global research groups have explored foundational approaches in {thematic_str}, yet most rely on resource-intensive infrastructure or proprietary pipelines.\n\n"
                    "4.2 National Status (Indian R&D Landscape):\n"
                    "Leading Indian institutions (IITs, IISc, CSIR/ICMR labs, and state universities) have initiated foundational studies, creating an opportunity for translational synthesis.\n\n"
                    "4.3 Identified Research Gaps:\n"
                    "• Gap 1: Absence of localized, high-fidelity datasets and field-calibrated models.\n"
                    "• Gap 2: High computational/fabrication overhead preventing deployment in resource-constrained settings.\n"
                    "• Gap 3: Lack of end-to-end validation bridging laboratory proof-of-concept with field deployment."
                ),
                tips=[
                    "Cite 20–30 recent peer-reviewed papers (last 5 years), explicitly highlighting contributions by Indian research groups.",
                ],
            ),
            ProposalSection(
                section_title="5. Detailed Research Methodology & Experimental Design",
                section_description="Step-by-step scientific methodology, validation protocols, and fallback contingencies.",
                drafted_content=(
                    "Phase I — Data Acquisition & System Specification:\n"
                    "Establish standardized acquisition protocols, ethical/biosafety clearances (if applicable), and reproducible preprocessing pipelines.\n\n"
                    "Phase II — Core Modeling / Fabrication & Optimization:\n"
                    f"Develop modular components in {', '.join(foa.thematic_areas[:2]) if foa.thematic_areas else 'the target domain'} with ablation studies across key hyperparameters and physical constraints.\n\n"
                    "Phase III — Verification, Benchmarking & Risk Mitigation:\n"
                    "Evaluate against gold-standard benchmarks using statistical significance testing (95% confidence intervals). "
                    "Risk Mitigation: If primary hardware/reagent lead times exceed 12 weeks, parallel simulation and domestic vendor equivalents will maintain schedule continuity."
                ),
                tips=[
                    "Include a block diagram of the methodology and explicitly state the fallback plan if a high-risk experiment encounters delays.",
                ],
            ),
            ProposalSection(
                section_title="6. Work Packages (WP1–WP4) & Responsibilities",
                section_description="Modular breakdown of tasks across the Principal Investigator, Co-PI, and Project Fellows.",
                drafted_content=(
                    "• WP1 (System Architecture & Baseline Setup — Lead: PI & JRF): Requirements specification, equipment procurement via GeM portal, and baseline benchmarking.\n"
                    "• WP2 (Core R&D & Algorithmic/Lab Development — Lead: PI, Co-PI & JRF): Core model/device development, mid-term ablation studies, and internal validation.\n"
                    "• WP3 (Integration, Field Testing & Calibration — Lead: Co-PI & SRF): End-to-end integration, robustness testing, and external user/clinical evaluation.\n"
                    "• WP4 (Dissemination, IP Protection & Tech Transfer — Lead: PI): Q1 journal manuscripts, Indian patent drafting, workshop organization, and GFR 12-A closure."
                ),
                tips=[
                    "Clearly delineate PI vs. Co-PI responsibilities to justify multi-investigator collaboration.",
                ],
            ),
            ProposalSection(
                section_title="7. Project Timeline & Quarterly Milestone Schedule",
                section_description=f"Time-bound execution roadmap across the {duration_m}-month project lifecycle.",
                drafted_content=(
                    "• Q1–Q2 (Months 1–6): GeM equipment tendering, JRF recruitment, literature synthesis, and baseline dataset assembly.\n"
                    "• Q3–Q4 (Months 7–12): First prototype / v1 model implementation, initial experimental validation, and 1st Annual Progress Report + GFR 12-A UC/SE.\n"
                    "• Q5–Q8 (Months 13–24): Full-scale optimization, multi-scenario stress testing, 2 peer-reviewed journal submissions, and 2nd Year PAC review.\n"
                    f"• Q9–Final (Months 25–{duration_m}): Field pilot demonstration, Indian Patent filing, technology transfer documentation, and Final Technical Closure Report."
                ),
                tips=[
                    "Align milestones with the 6-monthly or annual Project Advisory Committee (PAC) review cycle.",
                ],
            ),
            ProposalSection(
                section_title="8. Expected Outcomes, Deliverables & Target KPIs",
                section_description="Quantifiable scientific, technological, and human-resource outputs.",
                drafted_content=(
                    "1. Tangible Prototype / Software Artifact: Validated TRL-4/5 system with documented API/hardware schematics.\n"
                    "2. Publications: 2–3 papers in Q1/Q2 SCI-indexed journals and 2 flagship international conference proceedings.\n"
                    "3. Intellectual Property: 1 Indian Patent application and copyrighted benchmark dataset/codebase.\n"
                    "4. Manpower Trained: 1–2 Junior/Senior Research Fellows trained in advanced R&D methodologies."
                ),
                tips=[
                    "Avoid vague promises; specify exact TRL progression (e.g., TRL 2 to TRL 5) and target journal tiers.",
                ],
            ),
            ProposalSection(
                section_title="9. Itemized Budget Breakdown (Ministry of Finance OM Norms)",
                section_description="Structured financial outlay across Recurring, Non-Recurring, and Institutional Overhead heads.",
                drafted_content="\n".join([f"• {k}: {v}" for k, v in budget_map.items()]),
                tips=[
                    "Verify that Non-Recurring capital equipment does not exceed the scheme-specific percentage cap (typically 30%–50%, or 85% for AICTE RPS).",
                ],
            ),
            ProposalSection(
                section_title="10. Detailed Justification of Expenditure",
                section_description="Mandatory line-by-line justification required by statutory financial committees.",
                drafted_content=(
                    f"• Capital Equipment (₹ {max_budget * equip_pct:,.2f}): Essential for dedicated high-throughput experimentation and compute; existing shared central facilities at {institution_name} will be leveraged to avoid duplication.\n"
                    f"• Manpower (₹ {max_budget * manpower_pct:,.2f}): 1 JRF/SRF (@ ₹{stipend_mo:,.0f}/month + applicable HRA per DST OM SR/S9/Z-05/2019 / 2023 revision) dedicated full-time to WP1–WP3 execution.\n"
                    f"• Consumables (₹ {max_budget * consumables_pct:,.2f}): Covers specialized reagents, sensor modules, minor electronic components, and cloud compute credits.\n"
                    f"• Travel & Contingency (₹ {max_budget * travel_contingency_pct:,.2f}): Covers mandatory PI attendance at PAC monitoring meetings, domestic field data collection, and stationery/patent charges.\n"
                    f"• Institutional Overhead (₹ {max_budget * (overhead_pct / 100.0):,.2f}): Calculated strictly at {overhead_pct:.1f}% as per {foa.agency.value} norms."
                ),
                tips=[
                    "Attach 3 competitive vendor quotations (or GeM portal product IDs) for any single equipment item costing above ₹5.0 Lakhs.",
                ],
            ),
            ProposalSection(
                section_title="11. Key Statutory & Foundational References",
                section_description="Reference template combining statutory guidelines and domain literature.",
                drafted_content=(
                    f"[1] {foa.issuing_authority or foa.agency.value}, '{foa.title} — Official Scheme Guidelines & Call Circular', {foa.source_url}, Verified {foa.last_verified_date.isoformat()}.\n"
                    "[2] Ministry of Finance, Department of Expenditure, 'General Financial Rules (GFR) 2017 — Rule 238: Utilization Certificates & Grants-in-Aid', Govt. of India.\n"
                    "[3] Department of Science & Technology (DST), 'Revised Emoluments and Service Conditions for Research Personnel (JRF/SRF/RA) Office Memorandum', Govt. of India.\n"
                    f"[4] Foundational Domain Benchmark in {foa.thematic_areas[0] if foa.thematic_areas else 'Target Area'} — [Insert PI's 5 most relevant peer-reviewed DOI citations here]."
                ),
                tips=[
                    "Include full DOIs for all technical references and list the PI's own prior publications in the domain.",
                ],
            ),
        ]

        compliance_checklist = [
            f"Endorsement Certificate signed by the Head of Institution ({institution_name}) with official seal.",
            "Certificate from the Principal Investigator & Co-Investigator(s) declaring no duplicate funding for the same proposal.",
            "Complete Bio-data of PI and Co-PI including list of top 5 peer-reviewed publications and ongoing/completed projects.",
            "GeM Portal IDs or 3 comparative vendor quotations for capital equipment items exceeding ₹ 5.0 Lakhs.",
            "Valid DSIR SIRO recognition certificate and PFMS Unique Agency Code of the host institution.",
            "Institutional Ethics Committee (IEC) / Biosafety (IBSC) / Animal Ethics (IAEC) clearance (if applicable).",
        ]

        key_refs = foa.official_source_references or [
            f"{foa.title} Official Portal ({foa.source_url})",
            "Ministry of Finance GFR 2017 Grants-in-Aid Guidelines",
        ]

        guideline_status = (
            f"Checked against indexed {foa.agency.value} ({foa.foa_id}) call structure (Max Ceiling: ₹{max_budget:,.0f}, "
            f"Overhead Cap: {overhead_pct:.1f}%, Tenure: {duration_m} months) and Ministry of Finance GFR 2017 / DST Fellowship OM norms. "
            "NOTE: Automated drafting does not certify final administrative compliance; PI must verify call-specific annexures and institutional sign-offs on the official portal before submission."
        )

        if use_llm:
            sections = self._enrich_sections_with_gemini(
                foa=foa,
                sections=sections,
                is_student_sop=is_student_sop,
                pi_name=pi_name,
                institution_name=institution_name,
                custom_abstract=custom_abstract,
            )

        return ProposalSkeleton(
            foa_id=foa.foa_id,
            scheme_title=scheme_title,
            agency=foa.agency,
            generated_at=datetime.now(timezone.utc),
            target_deadline=foa.deadlines.effective_deadline,
            suggested_titles=suggested_titles,
            sections=sections,
            suggested_budget_breakdown=budget_map,
            compliance_checklist=compliance_checklist,
            key_references=key_refs,
            guideline_verification_status=guideline_status,
        )
