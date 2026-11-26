"""Intelligent Document Assistant for Scholarship Certificates, Marksheets, CVs, and Research Proposals."""
from datetime import date
import logging
import re
from typing import Any, Dict, List, Optional

from src.parser.ocr_worker import OCRWorker
from src.parser.pdf_parser import PDFLayoutParser
from src.schemas.foa import DocumentAnalysisResponse, DocumentFieldResult

logger = logging.getLogger("MadadgaarAI.AI.DocumentAssistant")


class IntelligentDocumentAssistant:
    """Analyzes student and researcher documents to extract key fields, identify missing requirements, and assist checklists."""

    def __init__(self):
        self.pdf_parser = PDFLayoutParser()
        self.ocr_worker = OCRWorker()

    def analyze_document(
        self,
        raw_text: Optional[str] = None,
        file_bytes: Optional[bytes] = None,
        filename: Optional[str] = None,
        document_type_hint: Optional[str] = None,
    ) -> DocumentAnalysisResponse:
        extraction_method = "Direct Text Analysis"
        text = (raw_text or "").strip()

        if file_bytes:
            fname_low = (filename or "").lower()
            if fname_low.endswith(".pdf") or file_bytes[:4] == b"%PDF":
                parsed = self.pdf_parser.parse_pdf(file_bytes)
                text = parsed.raw_text or text
                extraction_method = "PDF OCR Fallback" if parsed.is_ocr_fallback else f"PDF Layout Parser ({parsed.num_pages} pages)"
            elif any(fname_low.endswith(ext) for ext in (".png", ".jpg", ".jpeg", ".webp", ".bmp")):
                ocr_txt = self.ocr_worker.process_image_bytes(file_bytes)
                text = ocr_txt or text
                extraction_method = "Image OCR Worker"
            else:
                try:
                    text = file_bytes.decode("utf-8", errors="ignore")
                    extraction_method = "Text File Decoder"
                except Exception:
                    pass

        doc_type = self._detect_document_type(text, document_type_hint)
        has_devanagari = bool(re.search(r"[\u0900-\u097F]", text))
        detected_lang = "hi+en (Bilingual)" if has_devanagari else "en"

        if doc_type == "INCOME_CERTIFICATE":
            return self._analyze_income_certificate(text, detected_lang, extraction_method)
        elif doc_type == "ACADEMIC_MARKSHEET":
            return self._analyze_marksheet(text, detected_lang, extraction_method)
        elif doc_type == "CASTE_OR_DOMICILE_CERTIFICATE":
            return self._analyze_caste_or_domicile(text, detected_lang, extraction_method)
        elif doc_type == "ADMISSION_BONAFIDE_LETTER":
            return self._analyze_admission_letter(text, detected_lang, extraction_method)
        elif doc_type == "RESEARCH_CV":
            return self._analyze_research_cv(text, detected_lang, extraction_method)
        else:
            return self._analyze_research_proposal(text, detected_lang, extraction_method)

    def _detect_document_type(self, text: str, hint: Optional[str] = None) -> str:
        if hint and hint.upper() not in ("AUTO", ""):
            h = hint.upper()
            if "INCOME" in h:
                return "INCOME_CERTIFICATE"
            if "MARKSHEET" in h or "GRADE" in h:
                return "ACADEMIC_MARKSHEET"
            if "CASTE" in h or "DOMICILE" in h or "EWS" in h or "OBC" in h:
                return "CASTE_OR_DOMICILE_CERTIFICATE"
            if "ADMISSION" in h or "BONAFIDE" in h:
                return "ADMISSION_BONAFIDE_LETTER"
            if "CV" in h or "RESUME" in h or "BIOSKETCH" in h:
                return "RESEARCH_CV"
            if "PROPOSAL" in h:
                return "RESEARCH_PROPOSAL"

        low = text.lower()
        if any(k in low for k in ["income certificate", "आय प्रमाण पत्र", "annual income", "tehsildar", "varshik aay"]):
            return "INCOME_CERTIFICATE"
        if any(k in low for k in ["marksheet", "statement of marks", "cgpa", "cbse", "icse", "board examination", "grade card"]):
            return "ACADEMIC_MARKSHEET"
        if any(k in low for k in ["caste certificate", "scheduled caste", "scheduled tribe", "non-creamy layer", "domicile", "निवास प्रमाण", "जाति प्रमाण"]):
            return "CASTE_OR_DOMICILE_CERTIFICATE"
        if any(k in low for k in ["bonafide certificate", "admission letter", "fee receipt", "enrolled in", "roll no"]):
            return "ADMISSION_BONAFIDE_LETTER"
        if any(k in low for k in ["curriculum vitae", "publications", "h-index", "google scholar", "assistant professor", "associate professor"]):
            return "RESEARCH_CV"
        return "RESEARCH_PROPOSAL"

    def _analyze_income_certificate(
        self, text: str, lang: str, method: str
    ) -> DocumentAnalysisResponse:
        fields: List[DocumentFieldResult] = []
        missing: List[str] = []
        warnings: List[str] = []
        profile_updates: Dict[str, Any] = {}

        # 1. Issuing Authority
        auth_match = re.search(
            r"(Tehsildar|Naib Tehsildar|Sub-Divisional Magistrate|SDM|Revenue Officer|District Magistrate|तहसीलदार|उपजिलाधिकारी)",
            text,
            re.I,
        )
        if auth_match:
            fields.append(
                DocumentFieldResult(
                    field_name="Issuing Authority",
                    extracted_value=auth_match.group(1),
                    status="DETECTED",
                    note="Recognized revenue authority designation found in text.",
                )
            )
        else:
            fields.append(
                DocumentFieldResult(
                    field_name="Issuing Authority",
                    extracted_value=None,
                    status="MISSING",
                    note="Must explicitly state Tehsildar / SDM / Revenue Officer.",
                )
            )
            missing.append("Competent Revenue Issuing Authority (Tehsildar / SDM)")

        # 2. Annual Income Amount
        inc_val: Optional[float] = None
        lakh_m = re.search(r"(?:Rs\.?|INR|₹)\s*([\d]+(?:\.\d+)?)\s*(?:lakhs?|lac|lacs)", text, re.I)
        num_m = re.search(r"(?:Rs\.?|INR|₹)\s*([\d]{1,2}(?:,\d{2,3})+|\d{5,7})", text, re.I)
        if lakh_m:
            inc_val = float(lakh_m.group(1)) * 100000.0
        elif num_m:
            inc_val = float(num_m.group(1).replace(",", ""))

        if inc_val is not None:
            fields.append(
                DocumentFieldResult(
                    field_name="Annual Family Income (INR)",
                    extracted_value=f"₹ {inc_val:,.0f} / year",
                    status="DETECTED",
                    note="Extracted gross annual family income figure.",
                )
            )
            profile_updates["family_annual_income_inr"] = inc_val
            profile_updates["verified_document_tag"] = "income_certificate"
        else:
            fields.append(
                DocumentFieldResult(
                    field_name="Annual Family Income (INR)",
                    extracted_value=None,
                    status="MISSING",
                    note="Could not locate numeric annual income in INR.",
                )
            )
            missing.append("Annual Family Income figure in INR (e.g. ₹ 1,80,000)")

        # 3. Certificate Number / Digital Verification Token
        cert_m = re.search(r"(?:Certificate\s*(?:No|Number|ID)|Application\s*No|क्रमांक|प्रमापन)\s*[:\-]?\s*([A-Z0-9/\-]{6,25})", text, re.I)
        if cert_m:
            fields.append(
                DocumentFieldResult(
                    field_name="Certificate / e-District Application ID",
                    extracted_value=cert_m.group(1),
                    status="DETECTED",
                    note="Digital verification serial/token detected.",
                )
            )
        else:
            fields.append(
                DocumentFieldResult(
                    field_name="Certificate / e-District Application ID",
                    extracted_value=None,
                    status="WARNING",
                    note="Ensure digital e-District barcode/application number is clearly legible.",
                )
            )
            warnings.append("Digital e-District Certificate/Application Number was not clearly detected.")

        # 4. Issue Date / Dynamic Indian Financial Year Check (April 1 cutoff)
        today = date.today()
        active_fy_start = today.year if today.month >= 4 else today.year - 1
        year_matches = re.findall(r"\b(20\d{2})\b", text)
        if year_matches:
            latest_yr = max(int(y) for y in year_matches)
            if latest_yr < active_fy_start:
                fields.append(
                    DocumentFieldResult(
                        field_name="Issue Year / Financial Year",
                        extracted_value=str(latest_yr),
                        status="WARNING",
                        note=f"Detected year {latest_yr} is older than active FY {active_fy_start}-{str(active_fy_start + 1)[-2:]}.",
                    )
                )
                warnings.append(
                    f"Certificate date ({latest_yr}) may be expired. Most portals require an Income Certificate issued on or after 1st April {active_fy_start}."
                )
            else:
                fields.append(
                    DocumentFieldResult(
                        field_name="Issue Year / Financial Year",
                        extracted_value=str(latest_yr),
                        status="DETECTED",
                        note=f"Matches active FY {active_fy_start}-{str(active_fy_start + 1)[-2:]} window.",
                    )
                )
        else:
            missing.append(f"Issue Date (must be on or after 1st April {active_fy_start})")

        recommendations = [
            "Verify that the Income Certificate is issued in the name of the earning parent/head of family where required (e.g. UP Dashmottar).",
            "Ensure the e-District QR code / Digital Signature is intact and not cropped when scanning.",
        ]

        return DocumentAnalysisResponse(
            document_type="INCOME_CERTIFICATE",
            detected_language=lang,
            extraction_method=method,
            extracted_fields=fields,
            missing_fields=missing,
            checklist_recommendations=recommendations,
            warnings=warnings,
            suggested_profile_updates=profile_updates,
        )

    def _analyze_marksheet(
        self, text: str, lang: str, method: str
    ) -> DocumentAnalysisResponse:
        fields: List[DocumentFieldResult] = []
        missing: List[str] = []
        warnings: List[str] = []
        profile_updates: Dict[str, Any] = {}

        # Percentage or CGPA
        pct_m = re.search(r"(\d{2}(?:\.\d{1,2})?)\s*%", text)
        cgpa_m = re.search(r"(?:CGPA|SGPA|GPA)\s*[:\-]?\s*(\d(?:\.\d{1,2})?)", text, re.I)
        if pct_m:
            pct_val = float(pct_m.group(1))
            fields.append(
                DocumentFieldResult(
                    field_name="Aggregate Percentage",
                    extracted_value=f"{pct_val:.2f}%",
                    status="DETECTED",
                    note="Aggregate marks percentage detected.",
                )
            )
            profile_updates["academic_percentage"] = pct_val
            profile_updates["verified_document_tag"] = "marksheet"
        elif cgpa_m:
            cgpa_val = float(cgpa_m.group(1))
            approx_pct = min(100.0, round(cgpa_val * 9.5, 2))
            fields.append(
                DocumentFieldResult(
                    field_name="CGPA / Grade Point",
                    extracted_value=f"{cgpa_val} CGPA (~{approx_pct}%)",
                    status="DETECTED",
                    note="CGPA detected and converted using standard 9.5 multiplier.",
                )
            )
            profile_updates["academic_percentage"] = approx_pct
            profile_updates["verified_document_tag"] = "marksheet"
        else:
            fields.append(
                DocumentFieldResult(
                    field_name="Aggregate Percentage / CGPA",
                    extracted_value=None,
                    status="MISSING",
                    note="Could not detect final percentage or CGPA.",
                )
            )
            missing.append("Aggregate Percentage (%) or Cumulative GPA (CGPA)")

        # Board / University
        board_m = re.search(r"(CBSE|Central Board|ICSE|State Board|University|Institute of Technology|NIT|IIT|AKTU|SPPU)", text, re.I)
        if board_m:
            fields.append(
                DocumentFieldResult(
                    field_name="Examining Board / University",
                    extracted_value=board_m.group(0),
                    status="DETECTED",
                    note="Board or University identifier located.",
                )
            )
        else:
            missing.append("Board / University Name & Roll Number")

        # Backlog / Fail warning check
        if re.search(r"\b(fail|backlog|atkt|compartment|supplementary)\b", text, re.I):
            warnings.append(
                "Detected keywords related to compartment/backlog/ATKT. Most scholarship renewals require passing all subjects in the first attempt."
            )

        return DocumentAnalysisResponse(
            document_type="ACADEMIC_MARKSHEET",
            detected_language=lang,
            extraction_method=method,
            extracted_fields=fields,
            missing_fields=missing,
            checklist_recommendations=[
                "Use DigiLocker-verified marksheet or self-attested scan of the original marksheet.",
                "Ensure Roll Number on the marksheet matches the Roll Number entered in NSP OTR.",
            ],
            warnings=warnings,
            suggested_profile_updates=profile_updates,
        )

    def _analyze_caste_or_domicile(
        self, text: str, lang: str, method: str
    ) -> DocumentAnalysisResponse:
        fields: List[DocumentFieldResult] = []
        missing: List[str] = []
        warnings: List[str] = []
        profile_updates: Dict[str, Any] = {}
        low = text.lower()

        if "non-creamy layer" in low or "obc" in low:
            cat = "OBC (Non-Creamy Layer)"
            profile_updates["social_category"] = cat
            fields.append(DocumentFieldResult(field_name="Social Category", extracted_value=cat, status="DETECTED", note="OBC category detected."))
            if "non-creamy layer" not in low and "ncl" not in low:
                warnings.append("OBC certificate must explicitly mention 'Non-Creamy Layer (NCL)' status for central scholarships.")
        elif "scheduled caste" in low or re.search(r"\bsc\b", low):
            cat = "SC (Scheduled Caste)"
            profile_updates["social_category"] = cat
            fields.append(DocumentFieldResult(field_name="Social Category", extracted_value=cat, status="DETECTED", note="Scheduled Caste detected."))
        elif "scheduled tribe" in low or re.search(r"\bst\b", low):
            cat = "ST (Scheduled Tribe)"
            profile_updates["social_category"] = cat
            fields.append(DocumentFieldResult(field_name="Social Category", extracted_value=cat, status="DETECTED", note="Scheduled Tribe detected."))
        elif "economically weaker" in low or "ews" in low:
            cat = "EWS (Economically Weaker Section)"
            profile_updates["social_category"] = cat
            fields.append(DocumentFieldResult(field_name="Social Category", extracted_value=cat, status="DETECTED", note="EWS category detected."))

        for st in ["Uttar Pradesh", "Maharashtra", "Rajasthan", "Bihar", "Assam", "West Bengal", "Karnataka", "Madhya Pradesh"]:
            if st.lower() in low:
                profile_updates["state_domicile"] = st
                fields.append(DocumentFieldResult(field_name="State Domicile", extracted_value=st, status="DETECTED", note=f"State '{st}' identified."))
                break

        if not fields:
            missing.append("Category Designation (SC/ST/OBC-NCL/EWS) or State Domicile Name")

        return DocumentAnalysisResponse(
            document_type="CASTE_OR_DOMICILE_CERTIFICATE",
            detected_language=lang,
            extraction_method=method,
            extracted_fields=fields,
            missing_fields=missing,
            checklist_recommendations=[
                "Ensure student name spelling on Caste/Domicile certificate matches Aadhaar card.",
                "For OBC-NCL and EWS, verify that the certificate is valid for the current financial year.",
            ],
            warnings=warnings,
            suggested_profile_updates=profile_updates,
        )

    def _analyze_admission_letter(
        self, text: str, lang: str, method: str
    ) -> DocumentAnalysisResponse:
        fields: List[DocumentFieldResult] = []
        missing: List[str] = []
        profile_updates: Dict[str, Any] = {"verified_document_tag": "bonafide"}
        low = text.lower()

        if any(k in low for k in ["b.tech", "b.e.", "engineering"]):
            lvl = "UG - Engineering / Technology (B.Tech/B.E.)"
            profile_updates["education_level"] = lvl
            fields.append(DocumentFieldResult(field_name="Course / Program", extracted_value=lvl, status="DETECTED", note="Engineering degree detected."))
        elif any(k in low for k in ["mbbs", "bds", "nursing", "b.pharm"]):
            lvl = "UG - Medical / Paramedical (MBBS/BDS/B.Pharm/Nursing)"
            profile_updates["education_level"] = lvl
            fields.append(DocumentFieldResult(field_name="Course / Program", extracted_value=lvl, status="DETECTED", note="Medical/Paramedical program detected."))
        elif any(k in low for k in ["m.tech", "m.sc", "m.a.", "mba", "mca"]):
            lvl = "Postgraduate (M.Tech / M.Sc / M.Com / M.A. / MBA / MCA)"
            profile_updates["education_level"] = lvl
            fields.append(DocumentFieldResult(field_name="Course / Program", extracted_value=lvl, status="DETECTED", note="Postgraduate program detected."))
        else:
            missing.append("Degree / Course Program Name")

        return DocumentAnalysisResponse(
            document_type="ADMISSION_BONAFIDE_LETTER",
            detected_language=lang,
            extraction_method=method,
            extracted_fields=fields,
            missing_fields=missing,
            checklist_recommendations=[
                "Bonafide certificate must be on official college letterhead with Principal/Registrar signature and institutional seal.",
            ],
            warnings=[],
            suggested_profile_updates=profile_updates,
        )

    def _analyze_research_cv(
        self, text: str, lang: str, method: str
    ) -> DocumentAnalysisResponse:
        fields: List[DocumentFieldResult] = []
        missing: List[str] = []
        warnings: List[str] = []
        profile_updates: Dict[str, Any] = {}
        low = text.lower()

        # Degree
        if any(k in low for k in ["ph.d", "phd", "doctorate"]):
            profile_updates["highest_degree"] = "Ph.D."
            fields.append(DocumentFieldResult(field_name="Highest Qualification", extracted_value="Ph.D. / Doctorate", status="DETECTED", note="Doctoral qualification found."))
        elif any(k in low for k in ["m.tech", "m.e.", "m.sc"]):
            profile_updates["highest_degree"] = "M.Tech / Postgraduate"
            fields.append(DocumentFieldResult(field_name="Highest Qualification", extracted_value="Master's Degree", status="DETECTED", note="Postgraduate degree found."))
            warnings.append("Major extramural calls (DST-CRG, ANRF-POWER, CSIR-EMR) require a Ph.D. degree for Principal Investigators.")
        else:
            missing.append("Highest Academic Degree (e.g. Ph.D.)")

        # Publications count
        pub_m = re.search(r"(\d{1,3})\s*(?:peer-reviewed|sci|scopus|journal)?\s*publications?", low)
        doi_count = len(re.findall(r"\b10\.\d{4,9}/[-._;()/:A-Za-z0-9]+\b", text))
        pub_count = int(pub_m.group(1)) if pub_m else (doi_count if doi_count > 0 else None)
        if pub_count is not None:
            profile_updates["publications_count"] = pub_count
            profile_updates["sci_publications_count"] = pub_count
            fields.append(
                DocumentFieldResult(
                    field_name="Publications Count",
                    extracted_value=f"{pub_count} Publications",
                    status="DETECTED",
                    note="Extracted publication count from CV.",
                )
            )
        else:
            missing.append("SCI / Scopus Publication Count & Top 5 DOIs")

        # Age
        age_m = re.search(r"\bage\s*[:\-]?\s*(\d{2})\b", low)
        if age_m:
            age_val = int(age_m.group(1))
            profile_updates["applicant_age"] = age_val
            fields.append(DocumentFieldResult(field_name="Applicant Age", extracted_value=f"{age_val} years", status="DETECTED", note="Age extracted."))

        # Summary snippet
        profile_updates["research_summary"] = text[:500]

        return DocumentAnalysisResponse(
            document_type="RESEARCH_CV",
            detected_language=lang,
            extraction_method=method,
            extracted_fields=fields,
            missing_fields=missing,
            checklist_recommendations=[
                "List top 5 peer-reviewed SCI publications relevant to the proposed project with full DOIs.",
                "Include details of ongoing and completed sponsored research projects with sanction numbers.",
            ],
            warnings=warnings,
            suggested_profile_updates=profile_updates,
        )

    def _analyze_research_proposal(
        self, text: str, lang: str, method: str
    ) -> DocumentAnalysisResponse:
        fields: List[DocumentFieldResult] = []
        missing: List[str] = []
        warnings: List[str] = []
        profile_updates: Dict[str, Any] = {"research_summary": text[:600]}
        low = text.lower()

        # Check key statutory proposal sections
        section_checks = [
            ("Objectives / Aim", ["objective", "aim", "goal"]),
            ("Methodology / Work Plan", ["methodology", "work package", "experimental design", "architecture"]),
            ("Budget Breakdown", ["budget", "lakhs", "crore", "manpower", "equipment", "recurring"]),
            ("Timeline / Milestones", ["timeline", "milestone", "month", "year 1", "gantt"]),
        ]
        for label, kws in section_checks:
            if any(k in low for k in kws):
                fields.append(
                    DocumentFieldResult(
                        field_name=label,
                        extracted_value="Present in text",
                        status="DETECTED",
                        note=f"Detected {label} section content.",
                    )
                )
            else:
                fields.append(
                    DocumentFieldResult(
                        field_name=label,
                        extracted_value=None,
                        status="MISSING",
                        note=f"Proposal should include a dedicated {label} section.",
                    )
                )
                missing.append(label)

        lakh_m = re.search(r"(?:Rs\.?|INR|₹)\s*([\d]+(?:\.\d+)?)\s*(?:lakhs?|lac|lacs)", text, re.I)
        if lakh_m:
            amt = float(lakh_m.group(1)) * 100000.0
            profile_updates["requested_funding_inr"] = amt
            fields.append(
                DocumentFieldResult(
                    field_name="Proposed Budget Outlay",
                    extracted_value=f"₹ {amt:,.0f}",
                    status="DETECTED",
                    note="Proposed budget amount extracted.",
                )
            )
            if amt > 500000 and "quotation" not in low and "gem" not in low:
                warnings.append("Equipment budget > ₹5 Lakhs requires 3 vendor proforma quotations or GeM portal comparison.")

        return DocumentAnalysisResponse(
            document_type="RESEARCH_PROPOSAL",
            detected_language=lang,
            extraction_method=method,
            extracted_fields=fields,
            missing_fields=missing,
            checklist_recommendations=[
                "Ensure Institutional Overhead percentage matches the target agency cap (e.g. 10% for DST/CSIR).",
                "Attach Head of Institution Endorsement Certificate and PI/Co-PI Declaration.",
            ],
            warnings=warnings,
            suggested_profile_updates=profile_updates,
        )

