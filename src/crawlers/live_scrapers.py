"""Modular Asynchronous Real-Time Scrapers for Government Portals, Top Companies, Scholarships & Research Funding."""
from abc import ABC, abstractmethod
import asyncio
from datetime import date
import hashlib
import logging
import re
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urljoin
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import httpx

from src.schemas.opportunity import OpportunityCategory

logger = logging.getLogger("MadadgaarAI.Crawlers.Live")

MONTH_MAP = {
    "jan": 1, "january": 1, "feb": 2, "february": 2, "mar": 3, "march": 3,
    "apr": 4, "april": 4, "may": 5, "jun": 6, "june": 6, "jul": 7, "july": 7,
    "aug": 8, "august": 8, "sep": 9, "sept": 9, "september": 9, "oct": 10, "october": 10,
    "nov": 11, "november": 11, "dec": 12, "december": 12,
}


def parse_deadline_from_text(text: str) -> Optional[date]:
    """Parses ISO, US MM/DD/YYYY, DD-MM-YYYY, or textual dates."""
    if not text:
        return None
    candidates: List[date] = []

    for m in re.finditer(r"\b(202[5-9]|203[0-2])-(\d{1,2})-(\d{1,2})\b", text):
        try:
            candidates.append(date(int(m.group(1)), int(m.group(2)), int(m.group(3))))
        except ValueError:
            pass

    for m in re.finditer(
        r"\b(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(202[5-9]|203[0-2])\b",
        text,
        re.I,
    ):
        try:
            mon = MONTH_MAP[m.group(1).lower()[:3]]
            candidates.append(date(int(m.group(3)), mon, int(m.group(2))))
        except ValueError:
            pass

    for m in re.finditer(
        r"\b(\d{1,2})(?:st|nd|rd|th)?\s+(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?),?\s+(202[5-9]|203[0-2])\b",
        text,
        re.I,
    ):
        try:
            mon = MONTH_MAP[m.group(2).lower()[:3]]
            candidates.append(date(int(m.group(3)), mon, int(m.group(1))))
        except ValueError:
            pass

    for m in re.finditer(r"\b(\d{1,2})/(\d{1,2})/(202[5-9]|203[0-2])\b", text):
        a, b, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
        try:
            if a <= 12 and b <= 31:
                candidates.append(date(y, a, b))
            elif b <= 12 and a <= 31:
                candidates.append(date(y, b, a))
        except ValueError:
            pass

    if not candidates:
        return None
    future = [d for d in candidates if d >= date.today()]
    return max(future) if future else max(candidates)


def infer_domain(text: str) -> str:
    low = text.lower()
    if any(k in low for k in ["software", "ai ", "artificial intelligence", "machine learning", "genai", "data science", "computer", "cyber", "python", "react", "developer", "web dev", "cloud", "computing", "robotics", "nlp", "ml "]):
        return "Computer Science & AI"
    if any(k in low for k in ["mechanical", "electrical", "electronics", "civil", "engineering", "vlsi", "semiconductor", "hardware", "aerospace", "materials", "drone", "renewable energy", "water"]):
        return "Engineering"
    if any(k in low for k in ["health", "medical", "medtech", "biotech", "biomedical", "clinical", "pharma", "biology", "genom", "cancer", "life science", "nursing", "icmr"]):
        return "Healthcare & Biotech"
    if any(k in low for k in ["marketing", "finance", "business", "management", "economics", "sales", "hr ", "human resource", "content", "social media", "accounting", "mba", "commerce", "operations"]):
        return "Business & Marketing"
    if any(k in low for k in ["physics", "chemistry", "mathematics", "matrics", "climate", "energy", "environment", "astronomy", "geoscience", "quantum", "research"]):
        return "Science & Research"
    if any(k in low for k in ["design", "ui/ux", "graphic", "video", "arts", "humanities", "law", "policy", "journalism", "communications"]):
        return "Design, Policy & Arts"
    return "General"


def infer_degree_level(text: str, category: OpportunityCategory) -> str:
    low = text.lower()
    if any(k in low for k in ["phd", "ph.d", "doctoral", "postdoc", "post-doctoral", "principal investigator", "faculty", "investigator", "professor", "j. c. bose", "kothari", "radhakrishnan"]):
        return "PhD / Faculty"
    if any(k in low for k in ["master", "postgraduate", "m.tech", "m.sc", "mba", "graduate student"]):
        return "Postgraduate"
    if any(k in low for k in ["undergraduate", "bachelor", "b.tech", "b.e.", "college student", "freshers", "intern", "single girl child"]):
        return "Undergraduate"
    if category == OpportunityCategory.FUNDING:
        return "PhD / Faculty"
    if category == OpportunityCategory.INTERNSHIP:
        return "Undergraduate"
    return "All Levels"


def strip_html(raw_html: str) -> str:
    if not raw_html:
        return ""
    soup = BeautifulSoup(raw_html, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    return " ".join(text.split())


def make_opportunity_id(canonical_url: str, title: str) -> str:
    payload = f"{canonical_url.lower()}|{re.sub(r'[^a-z0-9]+', '', title.lower())[:60]}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


class BaseLiveScraper(ABC):
    source_name: str = "Unknown"
    default_category: OpportunityCategory = OpportunityCategory.SCHOLARSHIP
    source_type: str = "Government"

    @abstractmethod
    async def fetch_raw(self, client: httpx.AsyncClient) -> List[Dict[str, Any]]:
        """Fetches live raw opportunity dicts from the external source. Never returns mock data."""
        pass


# =========================================================================
# 1. INDIAN & INTERNATIONAL GOVERNMENT PORTALS
# =========================================================================

class ANRFIndiaScraper(BaseLiveScraper):
    """Scrapes live Indian Govt research grants & fellowships from ANRF / SERB (anrfonline.in)."""
    source_name = "ANRF / SERB (Govt. of India)"
    default_category = OpportunityCategory.FUNDING
    source_type = "Government"
    URL = "https://anrfonline.in/ANRF/HomePage"

    async def fetch_raw(self, client: httpx.AsyncClient) -> List[Dict[str, Any]]:
        resp = await client.get(self.URL, timeout=14.0, follow_redirects=True)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        items: List[Dict[str, Any]] = []
        seen_urls = set()

        keywords = [
            "grant", "fellowship", "mission", "program", "scheme", "power",
            "tare", "matrics", "bose", "npdf", "pmecrg", "maha", "arg", "inclusivity", "pair",
        ]

        for a in soup.select("a[href]"):
            title = " ".join(a.get_text(" ", strip=True).split())
            href = (a.get("href") or "").strip()
            if len(title) < 10 or len(title) > 140 or not href or href.startswith("#") or href.lower().startswith("javascript"):
                continue
            low = (title + " " + href).lower()
            if not any(k in low for k in keywords):
                continue
            if any(skip in low for skip in ["login", "register", "contact", "faq", "sitemap", "homepage", "privacy", "rti", "tender"]):
                continue

            full_url = urljoin("https://anrfonline.in/", href)
            if full_url in seen_urls or full_url.rstrip("/") == "https://anrfonline.in/ANRF/HomePage":
                continue
            seen_urls.add(full_url)

            is_fellowship = "fellowship" in title.lower() or "npdf" in low or "bose" in low
            cat = OpportunityCategory.SCHOLARSHIP if is_fellowship else OpportunityCategory.FUNDING
            domain = infer_domain(title)

            items.append({
                "title": title,
                "organization": "Anusandhan National Research Foundation (ANRF), Govt. of India",
                "category": cat,
                "source_type": "Government",
                "domain": domain,
                "eligibility": "Indian Faculty, Principal Investigators, PhD Scholars & Recognized Academic Institutions",
                "degree_level": "PhD / Faculty",
                "deadline": parse_deadline_from_text(title),
                "is_rolling": True,
                "stipend_or_amount": "ANRF Govt. of India Statutory Grant / Fellowship",
                "funding_type": "Grant-in-Aid",
                "source_url": full_url,
                "summary": f"Official Government of India scheme hosted on the ANRF Online Portal: {title}. Check active call timeline and guidelines directly on anrfonline.in.",
                "tags": ["ANRF India", "Govt. of India", domain],
                "location": "India",
            })
            if len(items) >= 14:
                break
        return items


class UGCIndiaScraper(BaseLiveScraper):
    """Scrapes live Indian Govt fellowships & research grants from UGC India (ugc.gov.in/frg)."""
    source_name = "UGC India (Govt. of India)"
    default_category = OpportunityCategory.SCHOLARSHIP
    source_type = "Government"
    URL = "https://www.ugc.gov.in/frg"

    async def fetch_raw(self, client: httpx.AsyncClient) -> List[Dict[str, Any]]:
        resp = await client.get(self.URL, timeout=12.0, follow_redirects=True)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        items: List[Dict[str, Any]] = []
        seen_urls = set()

        for a in soup.select("a[href]"):
            title = " ".join(a.get_text(" ", strip=True).split())
            href = (a.get("href") or "").strip()
            if len(title) < 15 or len(title) > 150 or not href or href.startswith("#"):
                continue
            low = title.lower()
            if not any(k in low for k in ["fellowship", "scholarship", "grant", "kothari", "radhakrishnan", "savitribai"]):
                continue
            if "copyright" in low or "total no of hits" in low:
                continue

            full_url = urljoin("https://frg.ugc.ac.in/", href) if href.startswith("/download/") else urljoin("https://www.ugc.gov.in/", href)
            if full_url in seen_urls:
                continue
            seen_urls.add(full_url)

            cat = OpportunityCategory.SCHOLARSHIP if ("fellowship" in low or "scholarship" in low or "girl child" in low) else OpportunityCategory.FUNDING
            items.append({
                "title": title,
                "organization": "University Grants Commission (UGC), Ministry of Education, Govt. of India",
                "category": cat,
                "source_type": "Government",
                "domain": "Science & Research" if "research" in low else "General",
                "eligibility": "Students, Doctoral Fellows & Faculty at UGC-Recognized Indian Universities",
                "degree_level": infer_degree_level(title, cat),
                "deadline": None,
                "is_rolling": True,
                "stipend_or_amount": "UGC Statutory Fellowship / Research Grant",
                "funding_type": "Fully Funded" if cat == OpportunityCategory.SCHOLARSHIP else "Grant-in-Aid",
                "source_url": full_url,
                "summary": f"Official University Grants Commission (UGC India) program: {title}. Official scheme manual and eligibility details verified directly from UGC.",
                "tags": ["UGC India", "Ministry of Education", "Govt. of India"],
                "location": "India",
            })
        return items


class ICMRIndiaScraper(BaseLiveScraper):
    """Scrapes live medical & health research calls from ICMR India (icmr.gov.in/call-for-proposals)."""
    source_name = "ICMR (Govt. of India)"
    default_category = OpportunityCategory.FUNDING
    source_type = "Government"
    URL = "https://www.icmr.gov.in/call-for-proposals"

    async def fetch_raw(self, client: httpx.AsyncClient) -> List[Dict[str, Any]]:
        resp = await client.get(self.URL, timeout=12.0, follow_redirects=True)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        items: List[Dict[str, Any]] = []
        seen_urls = set()

        for a in soup.select("a[href]"):
            title = " ".join(a.get_text(" ", strip=True).split())
            href = (a.get("href") or "").strip()
            if len(title) < 22 or not href or href.startswith("#") or href.lower().startswith("javascript"):
                continue
            low = title.lower()
            if not any(k in low for k in ["call for", "proposal", "grant", "fellowship", "centre of excellence", "research", "clinical"]):
                continue
            if any(skip in low for skip in ["webinar", "flyer", "tender"]):
                continue

            full_url = urljoin("https://www.icmr.gov.in/", href)
            if full_url in seen_urls:
                continue
            seen_urls.add(full_url)

            items.append({
                "title": title[:160],
                "organization": "Indian Council of Medical Research (ICMR), Ministry of Health, Govt. of India",
                "category": OpportunityCategory.FUNDING,
                "source_type": "Government",
                "domain": "Healthcare & Biotech",
                "eligibility": "Indian Medical Colleges, Universities, Biomedical Scientists & ICMR Institutes",
                "degree_level": "PhD / Faculty",
                "deadline": parse_deadline_from_text(title),
                "is_rolling": True,
                "stipend_or_amount": "ICMR Extramural Research Grant",
                "funding_type": "Grant-in-Aid",
                "source_url": full_url,
                "summary": f"Official Indian Council of Medical Research (ICMR) call/notice: {title[:260]}",
                "tags": ["ICMR India", "Healthcare", "Govt. of India"],
                "location": "India",
            })
            if len(items) >= 8:
                break
        return items


class BIRACIndiaScraper(BaseLiveScraper):
    """Scrapes live Calls for Proposals from India's DBT-BIRAC portal (birac.nic.in/cfp.php)."""
    source_name = "DBT-BIRAC (Govt. of India)"
    default_category = OpportunityCategory.FUNDING
    source_type = "Government"
    URL = "https://birac.nic.in/cfp.php"

    async def fetch_raw(self, client: httpx.AsyncClient) -> List[Dict[str, Any]]:
        resp = await client.get(self.URL, timeout=12.0, follow_redirects=True)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        items: List[Dict[str, Any]] = []
        seen_urls = set()

        for a in soup.select("a[href]"):
            text = " ".join(a.get_text(" ", strip=True).split())
            href = (a.get("href") or "").strip()
            if len(text) < 18 or not href or href.startswith("#") or href.lower().startswith("javascript"):
                continue
            low = text.lower()
            if not any(k in low for k in ["call", "proposal", "grant", "fellowship", "ignition", "scheme", "biotech", "funding", "rfp"]):
                continue
            full_url = urljoin("https://birac.nic.in/", href)
            if full_url in seen_urls or full_url.rstrip("/") == "https://birac.nic.in" or full_url.lower().endswith("/index.php"):
                continue
            seen_urls.add(full_url)

            parent_txt = a.parent.get_text(" ", strip=True) if a.parent else text
            deadline = parse_deadline_from_text(parent_txt)
            domain = infer_domain(f"{text} biotechnology healthcare")

            items.append({
                "title": text[:160],
                "organization": "DBT-BIRAC (Dept. of Biotechnology, Govt. of India)",
                "category": OpportunityCategory.FUNDING,
                "source_type": "Government",
                "domain": domain,
                "eligibility": "Indian Academic Institutions, Biotech Startups, Researchers & Incubatees",
                "degree_level": "PhD / Faculty",
                "deadline": deadline,
                "is_rolling": deadline is None,
                "stipend_or_amount": "DBT-BIRAC Grant-in-Aid (See Official Call)",
                "funding_type": "Grant-in-Aid",
                "source_url": full_url,
                "summary": f"Live Indian Government Biotechnology Call for Proposals: {text[:260]}",
                "tags": ["DBT-BIRAC", "Govt. of India", domain],
                "location": "India",
            })
            if len(items) >= 10:
                break
        return items


class GrantsGovScraper(BaseLiveScraper):
    """Fetches live open research funding calls from the official Grants.gov JSON Search API."""
    source_name = "Grants.gov Official API"
    default_category = OpportunityCategory.FUNDING
    source_type = "Government"
    API_URL = "https://api.grants.gov/v1/api/search2"

    async def fetch_raw(self, client: httpx.AsyncClient) -> List[Dict[str, Any]]:
        payload = {"rows": 12, "oppStatuses": "posted", "keyword": "research science engineering"}
        resp = await client.post(self.API_URL, json=payload, timeout=12.0)
        resp.raise_for_status()
        data = resp.json()
        hits = data.get("data", {}).get("oppHits", [])
        items: List[Dict[str, Any]] = []

        for h in hits:
            opp_id = str(h.get("id") or "").strip()
            title = (h.get("title") or "").strip()
            if not opp_id or not title:
                continue
            agency = (h.get("agencyName") or h.get("agency") or "Federal Research Agency").strip()
            opp_num = (h.get("number") or opp_id).strip()
            close_raw = (h.get("closeDate") or "").strip()
            open_raw = (h.get("openDate") or "").strip()
            deadline = parse_deadline_from_text(close_raw)
            detail_url = f"https://www.grants.gov/search-results-detail/{opp_id}"
            domain = infer_domain(f"{title} {agency}")

            items.append({
                "title": title,
                "organization": agency,
                "category": OpportunityCategory.FUNDING,
                "source_type": "Government",
                "domain": domain,
                "eligibility": "Universities, Research Institutions, Principal Investigators & Eligible Labs",
                "degree_level": "PhD / Faculty",
                "deadline": deadline,
                "is_rolling": deadline is None,
                "stipend_or_amount": "Federal Research Grant (See FOA Ceiling)",
                "funding_type": "Grant-in-Aid",
                "source_url": detail_url,
                "summary": f"Official Funding Opportunity ({opp_num}) issued by {agency}. Posted: {open_raw or 'Active'}. Closing Date: {close_raw or 'See Notice'}.",
                "tags": [domain, "Grants.gov", opp_num],
                "location": "International / US Federal",
            })
        return items


# =========================================================================
# 2. TOP TECH COMPANIES (DIRECT OFFICIAL GREENHOUSE CAREER APIs)
# =========================================================================

class TopCompaniesGreenhouseScraper(BaseLiveScraper):
    """Fetches live official internships & research fellowships directly from top tech company career boards."""
    source_name = "Top Tech Companies (Official Careers)"
    default_category = OpportunityCategory.INTERNSHIP
    source_type = "Company / Corporate"

    COMPANIES: List[Tuple[str, str]] = [
        ("stripe", "Stripe"),
        ("databricks", "Databricks"),
        ("anthropic", "Anthropic"),
        ("figma", "Figma"),
        ("mongodb", "MongoDB"),
        ("pinterest", "Pinterest"),
        ("coinbase", "Coinbase"),
        ("duolingo", "Duolingo"),
        ("datadog", "Datadog"),
        ("brex", "Brex"),
        ("airbnb", "Airbnb"),
        ("robinhood", "Robinhood"),
    ]

    INTERN_WORD_RE = re.compile(r"\b(intern|internship|fellows?|co-op|apprentice|university\s+grad)\b", re.I)

    async def fetch_raw(self, client: httpx.AsyncClient) -> List[Dict[str, Any]]:
        items: List[Dict[str, Any]] = []

        async def _fetch_company(board_slug: str, company_name: str):
            url = f"https://boards-api.greenhouse.io/v1/boards/{board_slug}/jobs"
            try:
                resp = await client.get(url, timeout=9.0)
                if resp.status_code != 200:
                    return []
                jobs = resp.json().get("jobs", [])
                matched = []
                for j in jobs:
                    title = (j.get("title") or "").strip()
                    abs_url = (j.get("absolute_url") or "").strip()
                    if not title or not abs_url:
                        continue
                    if not self.INTERN_WORD_RE.search(title):
                        continue
                    loc = ((j.get("location") or {}).get("name") or "Global / Hybrid").strip()
                    low = title.lower()
                    is_fellow = "fellow" in low
                    cat = OpportunityCategory.SCHOLARSHIP if is_fellow else OpportunityCategory.INTERNSHIP
                    domain = infer_domain(f"{title} {company_name}")
                    degree = "PhD / Faculty" if ("phd" in low or is_fellow) else "Undergraduate"

                    matched.append({
                        "title": f"{company_name} — {title}",
                        "organization": company_name,
                        "category": cat,
                        "source_type": "Company / Corporate",
                        "domain": domain,
                        "eligibility": f"{degree} students & early-career talent ({loc})",
                        "degree_level": degree,
                        "deadline": None,
                        "is_rolling": True,
                        "stipend_or_amount": "Paid Corporate Internship / Fellowship",
                        "funding_type": "Paid / Stipend",
                        "source_url": abs_url,
                        "summary": f"Official {company_name} listing: {title} ({loc}). Direct application hosted on {company_name}'s verified career board.",
                        "tags": [company_name, domain, "Direct Company Portal"],
                        "location": loc,
                    })
                    if len(matched) >= 3:
                        break
                return matched
            except Exception as exc:
                logger.debug(f"Company board {board_slug} failed: {exc}")
                return []

        batches = await asyncio.gather(*(_fetch_company(slug, name) for slug, name in self.COMPANIES))
        for b in batches:
            items.extend(b)
        return items


class InternshalaScraper(BaseLiveScraper):
    """Scrapes live Indian company internships from Internshala."""
    source_name = "Internshala (India Companies)"
    default_category = OpportunityCategory.INTERNSHIP
    source_type = "Company / Corporate"

    URLS = [
        "https://internshala.com/internships/computer-science-internship/",
        "https://internshala.com/internships/",
    ]

    async def fetch_raw(self, client: httpx.AsyncClient) -> List[Dict[str, Any]]:
        items: List[Dict[str, Any]] = []
        seen_hrefs = set()

        for page_url in self.URLS:
            resp = await client.get(page_url, timeout=12.0, follow_redirects=True)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            cards = soup.select("div.individual_internship")

            for card in cards[:12]:
                title_el = card.select_one("a.job-title-href, h3.job-internship-name a, .profile a")
                if not title_el:
                    continue
                title = title_el.get_text(strip=True)
                href = title_el.get("href") or ""
                if not title or not href:
                    continue
                full_url = urljoin("https://internshala.com", href)
                if full_url in seen_hrefs:
                    continue
                seen_hrefs.add(full_url)

                comp_el = card.select_one("p.company-name, .company_name a, .company_name")
                company = comp_el.get_text(strip=True) if comp_el else "Indian Employer (Internshala)"

                stipend_el = card.select_one("span.stipend, .stipend")
                stipend = stipend_el.get_text(strip=True) if stipend_el else "Stipend on Listing"

                loc_el = card.select_one("div.locations a, .location_link, p.locations")
                location = loc_el.get_text(strip=True) if loc_el else "India / Remote"

                card_text = card.get_text(" ", strip=True)
                domain = infer_domain(f"{title} {company} {card_text}")
                funding_type = "Unpaid" if "unpaid" in stipend.lower() else "Paid / Stipend"

                items.append({
                    "title": title,
                    "organization": company,
                    "category": OpportunityCategory.INTERNSHIP,
                    "source_type": "Company / Corporate",
                    "domain": domain,
                    "eligibility": f"Students & Freshers eligible for {domain} ({location})",
                    "degree_level": infer_degree_level(f"{title} {card_text}", OpportunityCategory.INTERNSHIP),
                    "deadline": parse_deadline_from_text(card_text),
                    "is_rolling": True,
                    "stipend_or_amount": stipend,
                    "funding_type": funding_type,
                    "source_url": full_url,
                    "summary": f"{title} internship at {company} ({location}). Stipend: {stipend}.",
                    "tags": [domain, location, "India Internship"],
                    "location": location,
                })
        return items


class RSSOpportunityScraper(BaseLiveScraper):
    """Generic live RSS/XML feed scraper for Scholarships, Fellowships, and Research Funding."""

    def __init__(
        self,
        source_name: str,
        feed_url: str,
        default_category: OpportunityCategory,
        source_type: str = "Foundation / University",
        max_items: int = 12,
    ):
        self.source_name = source_name
        self.feed_url = feed_url
        self.default_category = default_category
        self.source_type = source_type
        self.max_items = max_items

    async def fetch_raw(self, client: httpx.AsyncClient) -> List[Dict[str, Any]]:
        resp = await client.get(self.feed_url, timeout=12.0, follow_redirects=True)
        resp.raise_for_status()
        root = ET.fromstring(resp.text)
        rss_items = root.findall(".//item")
        results: List[Dict[str, Any]] = []

        for elem in rss_items[: self.max_items]:
            title = (elem.findtext("title") or "").strip()
            link = (elem.findtext("link") or "").strip()
            if not title or not link:
                continue

            desc_raw = elem.findtext("description") or ""
            desc_clean = strip_html(desc_raw)
            cats = [c.text.strip() for c in elem.findall("category") if c.text and c.text.strip()]
            combined = f"{title} {' '.join(cats)} {desc_clean}"
            low = combined.lower()

            if self.default_category == OpportunityCategory.FUNDING:
                category = OpportunityCategory.FUNDING
            elif any(k in low for k in ["internship", "intern "]):
                category = OpportunityCategory.INTERNSHIP
            elif any(k in low for k in ["grant", "research funding", "seed fund", "call for proposals", "nsf"]):
                category = OpportunityCategory.FUNDING
            else:
                category = OpportunityCategory.SCHOLARSHIP

            deadline = parse_deadline_from_text(combined)
            domain = infer_domain(combined)

            amt_match = re.search(
                r"((?:\$|USD|EUR|£|₹|Rs\.?)\s?[\d,]+(?:\.\d+)?(?:\s*(?:million|lakhs?|crores?|k|per\s*(?:year|month)))?)",
                combined,
                re.I,
            )
            if amt_match:
                stipend = amt_match.group(1).strip()
            elif "fully funded" in low:
                stipend = "Fully Funded"
            elif "paid" in low:
                stipend = "Paid Opportunity"
            else:
                stipend = "See Official Notice"

            funding_type = (
                "Fully Funded" if "fully funded" in low
                else ("Grant-in-Aid" if category == OpportunityCategory.FUNDING else ("Paid / Stipend" if "paid" in low else "Merit / Competitive"))
            )

            org = self.source_name
            stype = self.source_type
            if "nsf.gov" in link:
                org = "National Science Foundation (NSF)"
                stype = "Government"
            elif any(c in low for c in ["google", "microsoft", "amazon", "nivea", "meta", "ibm", "intel", "nvidia"]):
                stype = "Company / Corporate"
            else:
                org_parts = re.split(r"\s*[\|\-–]\s*", title)
                if len(org_parts) >= 2 and 3 <= len(org_parts[0]) <= 55:
                    org = org_parts[0].strip()

            summary = desc_clean[:360] + ("..." if len(desc_clean) > 360 else "")
            if len(summary) < 15:
                summary = f"Live curated {category.value.lower()} opportunity: {title}."

            results.append({
                "title": title,
                "organization": org,
                "category": category,
                "source_type": stype,
                "domain": domain,
                "eligibility": f"{infer_degree_level(combined, category)} applicants — verify full criteria on official notice",
                "degree_level": infer_degree_level(combined, category),
                "deadline": deadline,
                "is_rolling": deadline is None,
                "stipend_or_amount": stipend,
                "funding_type": funding_type,
                "source_url": link,
                "summary": summary,
                "tags": (cats[:3] or [domain]) + [self.source_name],
                "location": "Global / India",
            })
        return results


def build_live_scrapers() -> List[BaseLiveScraper]:
    """Returns all verified live async scrapers across Government Portals, Top Companies, and Foundations."""
    return [
        # Indian Government Portals
        ANRFIndiaScraper(),
        UGCIndiaScraper(),
        ICMRIndiaScraper(),
        BIRACIndiaScraper(),
        # Global Government Research Funding Portals
        GrantsGovScraper(),
        RSSOpportunityScraper(
            source_name="NSF Funding",
            feed_url="https://www.nsf.gov/rss/rss_www_funding.xml",
            default_category=OpportunityCategory.FUNDING,
            source_type="Government",
            max_items=10,
        ),
        # Companies Offering Internships & Fellowships
        TopCompaniesGreenhouseScraper(),
        InternshalaScraper(),
        # Live Scholarships & Corporate/University Fellowships
        RSSOpportunityScraper(
            source_name="OpportunitiesCircle",
            feed_url="https://www.opportunitiescircle.com/feed/",
            default_category=OpportunityCategory.SCHOLARSHIP,
            source_type="Foundation / University",
            max_items=10,
        ),
        RSSOpportunityScraper(
            source_name="OpportunityDesk",
            feed_url="https://opportunitydesk.org/feed/",
            default_category=OpportunityCategory.SCHOLARSHIP,
            source_type="Foundation / University",
            max_items=10,
        ),
    ]
