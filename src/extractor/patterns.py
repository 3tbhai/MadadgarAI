"""Specialized Regex Patterns and Entity Matchers for Indian Grant Circulars."""
import re

# Currency & Financial Ceilings (Lakhs, Crores, Direct Numeric)
BUDGET_LAKHS_PATTERN = re.compile(
    r"(?:Rs\.?|INR|₹)\s*([\d]+(?:\.\d+)?)\s*(?:lakhs?|lac|lacs)", re.I
)
BUDGET_CRORES_PATTERN = re.compile(
    r"(?:Rs\.?|INR|₹)\s*([\d]+(?:\.\d+)?)\s*(?:crores?|cr)", re.I
)
BUDGET_NUMERIC_PATTERN = re.compile(
    r"(?:Rs\.?|INR|₹)\s*([\d]{1,3}(?:,\d{2,3})+|\d{5,8})(?:\s*/-)?", re.I
)
STIPEND_MONTHLY_PATTERN = re.compile(
    r"(?:Rs\.?|INR|₹)\s*([\d,]+)\s*(?:per\s*month|p\.?m\.?|/-\s*p\.?m\.?|monthly)", re.I
)
OVERHEAD_PCT_PATTERN = re.compile(
    r"([\d]+(?:\.\d+)?)\s*%\s*(?:institutional\s*)?overheads?", re.I
)

# Deadlines & Dates
DATE_DD_MM_YYYY_PATTERN = re.compile(
    r"\b([0-3]?[0-9])[-/.]([0-1]?[0-9])[-/.](202[0-9])\b"
)
DATE_TEXTUAL_PATTERN = re.compile(
    r"\b([0-3]?[0-9](?:st|nd|rd|th)?)\s+(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)[,\s]+(202[0-9])\b",
    re.I,
)
ROLLING_CALL_PATTERN = re.compile(
    r"\b(rolling\s*(?:call|basis|proposal)|open\s*throughout\s*the\s*year|round\s*the\s*year)\b",
    re.I,
)

# Eligibility & Age Limits
AGE_LIMIT_PATTERN = re.compile(
    r"(?:age\s*(?:limit|ceiling)?\s*(?:is|should\s*be|up\s*to|<=|not\s*exceeding|below|maximum\s*of)?\s*)(\d{2})\s*years?",
    re.I,
)
QUALIFICATION_KEYWORDS = [
    ("Ph.D.", re.compile(r"\b(ph\.?d\.?|doctorate|doctoral)\b", re.I)),
    ("MD/MS/M.Ch", re.compile(r"\b(md|ms|m\.ch|dm)\b", re.I)),
    ("M.Tech / M.E.", re.compile(r"\b(m\.?tech|m\.?e\.?|master'?s\s+in\s+eng)", re.I)),
    ("B.Tech / B.E.", re.compile(r"\b(b\.?tech|b\.?e\.?|bachelor'?s\s+in\s+eng)", re.I)),
    ("Postgraduate", re.compile(r"\b(postgraduate|post-graduate|m\.sc|mca|mba)\b", re.I)),
    ("Undergraduate", re.compile(r"\b(undergraduate|10\+2|diploma|b\.sc)\b", re.I)),
]

# Institution Tiers
INSTITUTION_KEYWORDS = [
    ("CFTI", re.compile(r"\b(cfti|centrally\s+funded\s+technical\s+inst)", re.I)),
    ("IIT/IISc/NIT", re.compile(r"\b(iit|iisc|nit|iiser|iiit)\b", re.I)),
    ("UGC Recognized", re.compile(r"\b(ugc\s+recognized|central\s+universit|state\s+universit)", re.I)),
    ("AICTE Approved", re.compile(r"\b(aicte\s+approved|technical\s+institution)", re.I)),
    ("Private University (NAAC/NBA)", re.compile(r"\b(naac|nba|private\s+universit)", re.I)),
    ("National Lab / CSIR / ICMR", re.compile(r"\b(national\s+lab|csir\s+lab|icmr|drdo|icar)\b", re.I)),
    ("Startups / Incubatees", re.compile(r"\b(startup|incubatee|dpiit\s+registered|msme|entrepreneur)", re.I)),
]

# Target Beneficiary Types
BENEFICIARY_KEYWORDS = [
    ("Women Scientists", re.compile(r"\b(women\s+scientists?|female\s+researchers?|women\s+in\s+stem|gender)\b", re.I)),
    ("Early Career Researcher", re.compile(r"\b(early\s+career|young\s+scientists?|starting\s+grants?)\b", re.I)),
    ("Faculty / Principal Investigator", re.compile(r"\b(faculty|principal\s+investigators?|pi|regular\s+academic\s+positions?|professors?|assistant\s+profs?)\b", re.I)),
    ("PhD Scholars & Postdoctoral Fellows", re.compile(r"\b(phd\s+scholars?|postdocs?|postdoctorals?|jrf|srf|research\s+fellows?)\b", re.I)),
    ("UG / PG Students", re.compile(r"\b(undergraduates?|postgraduates?|students?\s+fellowships?|ug|pg|scholarships?)\b", re.I)),
    ("Startups & Industry Partners", re.compile(r"\b(startups?|industry\s+partners?|commercialization|spin-offs?|msme)\b", re.I)),
]
