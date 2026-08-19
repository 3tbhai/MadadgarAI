"""Automated Grant Proposal Skeleton Drafter for Indian Statutory Bodies."""
from datetime import datetime, timezone
from typing import Dict, List, Optional
from src.schemas.foa import AgencyType, FundingOpportunity, ProposalSection, ProposalSkeleton


class ProposalDrafter:
    def __init__(self):
        pass

    def draft_proposal_skeleton(
        self,
        foa: FundingOpportunity,
        project_title: Optional[str] = None,
        pi_name: str = "Dr. Principal Investigator",
        institution_name: str = "JK Lakshmipat University, Jaipur",
        custom_abstract: Optional[str] = None,
    ) -> ProposalSkeleton:
        """Generates an agency-tailored proposal outline matching FOA guidelines."""
        scheme_title = foa.title
        target_title = project_title or f"Advanced Investigation in {foa.ontology_tags[0].thematic_thrust if foa.ontology_tags else 'Target Domain'}"
        max_budget = foa.financials.max_amount_inr or 4000000.0

        # Itemized Budget Suggestions
        budget_map: Dict[str, str] = {
            "Non-Recurring (Capital Equipment)": f"₹ {max_budget * 0.40:,.2f} (40%) - Hardware, Workstations, Measurement Instruments",
            "Manpower (JRF / SRF / Postdoc)": f"₹ {max_budget * 0.30:,.2f} (30%) - Project Fellow stipends + HRA as per OM norms",
            "Consumables & Cloud Compute": f"₹ {max_budget * 0.15:,.2f} (15%) - Reagents, APIs, GPU Compute hours",
            "Domestic Travel & Field Trials": f"₹ {max_budget * 0.05:,.2f} (5%) - Conferences, project monitoring meetings",
            "Institutional Overhead": f"₹ {max_budget * (foa.financials.institutional_overhead_pct or 10.0)/100.0:,.2f} ({foa.financials.institutional_overhead_pct or 10}%) - Host institute admin and infra costs",
        }

        # Agency-Specific Section Templates
        sections: List[ProposalSection] = [
            ProposalSection(
                section_title="1. Project Executive Summary & National Relevance",
                section_description="High-level overview aligning proposed work with national technological missions.",
                drafted_content=(
                    f"Title: {target_title}\n"
                    f"Principal Investigator: {pi_name}\n"
                    f"Host Institution: {institution_name}\n"
                    f"Target Scheme: {foa.scheme_name or foa.title} ({foa.agency.value})\n\n"
                    f"Abstract:\n{custom_abstract or foa.brief_summary}\n\n"
                    f"National Importance: Directly addresses the objectives of {foa.agency.value} by advancing indigenous capabilities, IP generation, and skilled manpower development in India."
                ),
                tips=[
                    "Keep within 300 words as per statutory guidelines.",
                    "Highlight measurable socio-economic or technological impacts.",
                ],
            ),
            ProposalSection(
                section_title="2. State-of-the-Art Review & Gap Analysis",
                section_description="Critical synthesis of current global and Indian literature identifying research gaps.",
                drafted_content=(
                    f"Recent advancements in {', '.join(foa.thematic_areas[:3])} demonstrate significant potential; however, existing literature reveals clear limitations in scalability, localized benchmarking, and open-source availability. "
                    f"This proposal addresses these identified barriers through an innovative methodological framework."
                ),
                tips=[
                    "Cite at least 15-20 peer-reviewed publications from the last 3-5 years.",
                    "Explicitly differentiate your proposed approach from existing published models.",
                ],
            ),
            ProposalSection(
                section_title="3. Specific Research Objectives (Time-Targeted)",
                section_description="Clear, measurable, and bulleted scientific aims.",
                drafted_content=(
                    "• Objective 1 (Months 1-8): Design and validation of core architecture, synthetic baseline data generation, and benchmark harness setup.\n"
                    "• Objective 2 (Months 9-24): Implementation of advanced algorithmic models, hybrid integration pipeline, and iterative empirical validation.\n"
                    "• Objective 3 (Months 25-36): Prototype deployment, field validation, intellectual property filing (Patent), and submission of final technical report."
                ),
                tips=[
                    "Avoid overly broad objectives; keep them discrete and testable.",
                    "Map each objective to a corresponding deliverable in Section 5.",
                ],
            ),
            ProposalSection(
                section_title="4. Detailed Methodology, Work Packages & Architecture",
                section_description="Technical blueprint, mathematical formulation, and work package breakdown.",
                drafted_content=(
                    "• Work Package 1 (WP1): System Specification & Data Pipeline Ingestion.\n"
                    "• Work Package 2 (WP2): Modular Algorithmic Core, Optimization, and Evaluation.\n"
                    "• Work Package 3 (WP3): Integration, Reliability Testing, and Pilot Demonstration."
                ),
                tips=[
                    "Include a detailed system flowchart and architectural block diagram.",
                    "Specify quantitative performance criteria (e.g. F1-score > 90%, Latency < 100ms).",
                ],
            ),
            ProposalSection(
                section_title="5. Deliverables, Milestones & Year-Wise Gantt Chart",
                section_description="Tangible outcomes across the project lifecycle.",
                drafted_content=(
                    "• Year 1: Baseline system prototype, Comprehensive literature survey, 1 Scopus/SCI conference paper.\n"
                    "• Year 2: Fully functional pipeline, 2 Q1/Q2 Journal publications, 1 Provisional patent application.\n"
                    "• Year 3: Production-ready software artifact, final technical documentation, trained project scholar."
                ),
                tips=[
                    "Ensure milestone progress can be reviewed every 6 months by the Project Advisory Committee (PAC).",
                ],
            ),
            ProposalSection(
                section_title="6. Justification of Budget Estimates",
                section_description="Itemized costing and justification as per Ministry of Finance OM guidelines.",
                drafted_content="\n".join([f"• {k}: {v}" for k, v in budget_map.items()]),
                tips=[
                    "Clearly justify every capital equipment with respect to project deliverables.",
                    "Ensure manpower stipends conform strictly to DST/CSIR OM guidelines.",
                ],
            ),
        ]

        compliance_checklist = [
            f"Endorsement from the Head of Institution ({institution_name}) on official letterhead.",
            "Certificate from the Principal Investigator & Co-Investigators.",
            "Complete bio-data of PI and Co-PI including list of 5 most relevant publications.",
            "Quotations for capital equipment items exceeding ₹ 5.0 Lakhs.",
            "Institutional Ethics / IBSC / IAEC clearance certificate (if applicable).",
        ]

        return ProposalSkeleton(
            foa_id=foa.foa_id,
            scheme_title=scheme_title,
            agency=foa.agency,
            generated_at=datetime.now(timezone.utc),
            target_deadline=foa.deadlines.effective_deadline,
            sections=sections,
            suggested_budget_breakdown=budget_map,
            compliance_checklist=compliance_checklist,
        )
