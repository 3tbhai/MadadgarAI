"""On-Demand Deep-Page HTML, API & PDF Circular Analyzer (Feature 1.4)."""
from datetime import datetime, timezone
import json
import logging
import re
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import httpx
from pydantic import BaseModel, Field

from src.crawlers.link_verifier import DEFAULT_HEADERS
from src.crawlers.live_scrapers import parse_deadline_from_text, strip_html
from src.extractor.entity_extractor import FOAEntityExtractor
from src.parser.pdf_parser import PDFLayoutParser
from src.schemas.opportunity import LiveOpportunity

logger = logging.getLogger("MadadgaarAI.Crawlers.DeepAnalyzer")


class DeepPageAnalysis(BaseModel):
    opp_id: str
    source_url: str
    http_status: int = 200
    content_type: str = "text/html"
    page_title: str
    extracted_financials: str
    extracted_deadline: str
    eligibility_highlights: List[str] = Field(default_factory=list)
    required_documents: List[str] = Field(default_factory=list)
    application_steps: List[str] = Field(default_factory=list)
    direct_attachments: List[str] = Field(default_factory=list)
    key_excerpt: str = ""
    word_count: int = 0
    is_pdf_parsed: bool = False
    analyzed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class DeepPageAnalyzer:
    """Fetches and deeply parses an opportunity's live destination webpage, API, or PDF circular on demand."""

    def __init__(self):
        self.pdf_parser = PDFLayoutParser()
        self.entity_extractor = FOAEntityExtractor()

    async def _try_structured_api(self, client: httpx.AsyncClient, url: str) -> Optional[Dict[str, Any]]:
        """Enriches SPA portals (Grants.gov, Ashby, Lever) via their official public JSON APIs."""
        parsed = urlparse(url)
        host = parsed.netloc.lower()
        parts = [p for p in parsed.path.split("/") if p]

        try:
            # 1. Grants.gov Detail API
            if "grants.gov" in host and len(parts) >= 2 and parts[-1].isdigit():
                resp = await client.post(
                    "https://api.grants.gov/v1/api/fetchOpportunity",
                    json={"opportunityId": int(parts[-1])},
                )
                if resp.status_code == 200:
                    syn = (resp.json().get("data") or {}).get("synopsis") or {}
                    desc = strip_html(syn.get("synopsisDesc") or "")
                    floor = syn.get("awardFloor")
                    ceiling = syn.get("awardCeiling")
                    fin = ""
                    if ceiling and str(ceiling).isdigit():
                        fin = f"Up to ${int(ceiling):,}" + (f" (Floor: ${int(floor):,})" if floor and str(floor).isdigit() else "")
                    return {"text": desc, "financials": fin, "deadline": syn.get("responseDate") or ""}

            # 2. Ashby Job Posting API
            if "jobs.ashbyhq.com" in host and len(parts) >= 2:
                slug, job_id = parts[0], parts[1]
                resp = await client.get(f"https://api.ashbyhq.com/posting-api/job-board/{slug}")
                if resp.status_code == 200:
                    for j in resp.json().get("jobs", []):
                        j_url = j.get("jobUrl") or ""
                        if job_id in j_url or j.get("id") == job_id:
                            desc = strip_html(j.get("descriptionHtml") or "") or (j.get("descriptionPlain") or "")
                            comp = (j.get("compensation") or {}).get("compensationTierSummary") or ""
                            return {"text": desc, "financials": comp, "deadline": ""}

            # 3. Lever Postings API
            if "jobs.lever.co" in host and len(parts) >= 2:
                slug, job_id = parts[0], parts[1]
                resp = await client.get(f"https://api.lever.co/v0/postings/{slug}/{job_id}")
                if resp.status_code == 200:
                    j = resp.json()
                    lists_txt = " ".join(
                        f"{l.get('text', '')}: {strip_html(l.get('content', ''))}"
                        for l in (j.get("lists") or [])
                    )
                    desc = f"{j.get('descriptionPlain') or ''} {lists_txt} {j.get('additionalPlain') or ''}".strip()
                    return {"text": desc, "financials": "", "deadline": ""}
        except Exception as exc:
            logger.debug(f"Structured API enrichment skipped for {url}: {exc}")

        return None

    async def analyze_opportunity(self, opp: LiveOpportunity) -> DeepPageAnalysis:
        url = str(opp.source_url)
        raw_text = ""
        page_title = opp.title
        content_type = "text/html"
        http_status = opp.http_status
        is_pdf = False
        attachments: List[str] = []
        api_financials = ""
        api_deadline_raw = ""

        try:
            async with httpx.AsyncClient(verify=False, headers=DEFAULT_HEADERS, timeout=12.0, follow_redirects=True) as client:
                api_data = await self._try_structured_api(client, url)
                if api_data:
                    raw_text = api_data.get("text") or ""
                    api_financials = api_data.get("financials") or ""
                    api_deadline_raw = api_data.get("deadline") or ""
                    content_type = "application/json+html"

                if len(raw_text) < 120:
                    resp = await client.get(url)
                    http_status = resp.status_code
                    content_type = (resp.headers.get("content-type") or "text/html").split(";")[0].strip().lower()

                    if "pdf" in content_type or url.lower().endswith(".pdf") or resp.content[:4] == b"%PDF":
                        is_pdf = True
                        parsed_pdf = self.pdf_parser.parse_pdf(resp.content)
                        raw_text = parsed_pdf.raw_text or ""
                    else:
                        soup = BeautifulSoup(resp.text, "html.parser")
                        if soup.title and soup.title.string:
                            page_title = " ".join(soup.title.string.split())[:160]

                        # Collect JSON-LD JobPosting descriptions before stripping script tags
                        ld_snippets: List[str] = []
                        for s_tag in soup.select('script[type="application/ld+json"]'):
                            try:
                                ld_obj = json.loads(s_tag.string or "{}")
                                items_ld = ld_obj if isinstance(ld_obj, list) else [ld_obj]
                                for item_ld in items_ld:
                                    if isinstance(item_ld, dict) and item_ld.get("description"):
                                        ld_snippets.append(strip_html(str(item_ld["description"])))
                            except Exception:
                                pass

                        # Collect direct PDF guideline/circular links on the page
                        for a in soup.select("a[href]"):
                            href = (a.get("href") or "").strip()
                            if href.lower().endswith(".pdf") or "download" in href.lower() or "guideline" in href.lower():
                                full_a = urljoin(url, href)
                                if full_a.startswith("http") and full_a not in attachments:
                                    attachments.append(full_a)

                        for tag in soup(["script", "style", "noscript", "svg", "nav", "footer", "header"]):
                            tag.decompose()

                        main_node = (
                            soup.select_one("main, article, [role='main'], .job-description, .content, #content, .post-content")
                            or soup.body
                            or soup
                        )
                        dom_text = main_node.get_text(separator="\n", strip=True)
                        raw_text = "\n".join([dom_text] + ld_snippets).strip()
        except Exception as exc:
            logger.warning(f"Deep page fetch fallback for {url}: {exc}")

        if not raw_text.strip():
            raw_text = f"{opp.title}\n{opp.organization}\n{opp.eligibility}\n{opp.summary}"

        clean_lines = [
            " ".join(line.split())
            for line in raw_text.splitlines()
            if len(line.strip()) >= 18
        ]
        # Split dense API blobs into sentence-like segments so eligibility extraction works cleanly
        if len(clean_lines) <= 2 and len(raw_text) > 150:
            clean_lines = [
                s.strip()
                for s in re.split(r"(?<=[.!?])\s+|\s*•\s*", raw_text)
                if len(s.strip()) >= 20
            ]

        combined_text = "\n".join(clean_lines)
        words = combined_text.split()

        # 1. Financials extraction
        fin = self.entity_extractor.extract_financials(combined_text)
        fin_str = api_financials or opp.stipend_or_amount
        if not api_financials:
            if fin.max_amount_inr:
                fin_str = f"Up to ₹{fin.max_amount_inr:,.0f}" + (
                    f" (Monthly Stipend: ₹{fin.stipend_monthly_inr:,.0f})" if fin.stipend_monthly_inr else ""
                )
            elif fin.stipend_monthly_inr:
                fin_str = f"₹{fin.stipend_monthly_inr:,.0f} / month"
            else:
                curr_m = re.search(
                    r"((?:\$|USD|EUR|£|₹|Rs\.?|INR)\s?[\d,]+(?:\.\d+)?(?:\s*(?:-\s*(?:\$|USD|EUR|£|₹|Rs\.?)?\s?[\d,]+))?(?:\s*(?:million|lakhs?|crores?|k|per\s*(?:year|month|annum|hour)|/yr|/mo))?)",
                    combined_text,
                    re.I,
                )
                if curr_m:
                    fin_str = curr_m.group(1).strip()

        # 2. Deadline extraction
        dl = parse_deadline_from_text(api_deadline_raw) or parse_deadline_from_text(combined_text) or opp.deadline
        dl_str = dl.isoformat() if dl else ("Rolling / Ongoing" if opp.is_rolling else "Check Official Page")

        # 3. Eligibility highlights
        elig_keywords = [
            "eligible", "eligibility", "qualification", "degree", "bachelor", "master",
            "phd", "ph.d", "student", "faculty", "experience", "enrolled", "graduating",
            "requirement", "who can apply", "background in", "proficiency", "currently pursuing",
        ]
        elig_bullets: List[str] = []
        for line in clean_lines:
            low = line.lower()
            if 25 <= len(line) <= 240 and any(k in low for k in elig_keywords):
                if line not in elig_bullets:
                    elig_bullets.append(line)
            if len(elig_bullets) >= 5:
                break
        if not elig_bullets:
            elig_bullets = [opp.eligibility, f"Target Level: {opp.degree_level}", f"Field: {opp.domain}"]

        # 4. Required Documents detection
        doc_catalog = [
            ("Updated CV / Resume", ["resume", "curriculum vitae", "cv", "bio-data", "biosketch"]),
            ("Academic Transcripts / Marksheets", ["transcript", "marksheet", "grade card", "academic record", "cgpa"]),
            ("Statement of Purpose / Cover Letter", ["cover letter", "statement of purpose", "sop", "motivation letter", "personal statement"]),
            ("Research / Project Proposal", ["proposal", "project description", "research plan", "abstract", "technical plan"]),
            ("Letters of Recommendation / Endorsement", ["recommendation", "reference letter", "endorsement", "noc", "referee"]),
            ("Portfolio / GitHub / Code Samples", ["portfolio", "github", "code sample", "publications", "writing sample"]),
            ("Identity & Statutory Certificates (Aadhaar / Income / Category)", ["aadhaar", "income certificate", "caste", "domicile", "passport"]),
        ]
        c_low = combined_text.lower()
        req_docs: List[str] = []
        for doc_label, kws in doc_catalog:
            if any(k in c_low for k in kws):
                req_docs.append(doc_label)
        if not req_docs:
            if opp.category.value == "Internship":
                req_docs = ["Updated Resume / CV", "Academic Transcript / Enrollment Proof", "GitHub / Project Portfolio"]
            elif opp.category.value == "Funding":
                req_docs = ["Technical Research Proposal", "PI & Co-PI Bio-Sketch / CV", "Institutional Endorsement / Budget Sheet"]
            else:
                req_docs = ["Academic Marksheets / Transcripts", "Identity & Income/Eligibility Proof", "Statement of Purpose / Essay"]

        # 5. Clean un-prefixed Step-by-Step Application Flow (rendered inside <ol> in UI)
        submit_phrase = (
            f"Complete online submission before {dl.isoformat()}."
            if dl
            else "Complete online submission via the active rolling portal."
        )
        steps = [
            f"Open the verified official page at {opp.source_domain} ({url}).",
        ]
        if attachments:
            steps.append(f"Download and review the attached official PDF circular ({attachments[0]}).")
        steps.extend([
            f"Verify eligibility requirements ({opp.degree_level} • {opp.domain}).",
            f"Prepare required documents: {', '.join(req_docs[:3])}.",
            submit_phrase,
        ])

        excerpt = " ".join(clean_lines[:5])[:520] if clean_lines else opp.summary

        return DeepPageAnalysis(
            opp_id=opp.id,
            source_url=url,
            http_status=http_status,
            content_type=content_type,
            page_title=page_title,
            extracted_financials=fin_str,
            extracted_deadline=dl_str,
            eligibility_highlights=elig_bullets,
            required_documents=req_docs,
            application_steps=steps,
            direct_attachments=attachments[:4],
            key_excerpt=excerpt,
            word_count=len(words),
            is_pdf_parsed=is_pdf,
        )
