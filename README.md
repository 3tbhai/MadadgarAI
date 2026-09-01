# MadadgaarAI: National Scholarship & Research Funding Intelligence System
**Automated Scheme Ingestion, Zero-Knowledge Student Matching, and Grant Discovery**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111%2B-green.svg)](https://fastapi.tiangolo.com)
[![Tests: Passing](https://img.shields.io/badge/Tests-28%2F28%20Passed-brightgreen.svg)]()

MadadgaarAI is an end-to-end funding and scholarship intelligence platform engineered to ingest, parse, semantically tag, and match **Student Scholarships & Funding Opportunity Announcements (FOAs)** across Indian statutory portals (**NSP, AICTE, UGC, State Portals like MahaDBT & UP Scholarship, CSR Trusts, DST, ANRF/SERB, CSIR, DBT**).

---

## 🌟 Key Capabilities

### 🎓 1. "Vidyarthi AI" — Zero-Knowledge Student Scholarship Matcher
* **One-Click Eligibility Wizard**: Students input basic details (State of Domicile, Social Category, Gender, Annual Income, Course/Degree) and instantly discover **100% Guaranteed & High-Probability Scholarships**.
* **🚀 Direct Application Deep-Links**: Bypasses confusing portal homepages to send students directly to the active Online Registration / Application form (e.g. NSP OTR, UP Dashmottar Registration, MahaDBT Applicant Form, Kotak Kanya Apply).
* **🗺️ Step-by-Step Portal Navigation Guides**: Provides clear, numbered click-through instructions on which ministry, scheme category, and documents to select on complex government portals.
* **Comprehensive Indian Coverage**:
  * **Central (NSP)**: *PM-USP Central Sector Scheme*, *PM YASASVI (OBC/EBC/DNT)*, *Post-Matric for SC/ST*, *Ishan Uday (NER)*.
  * **AICTE & UGC**: *AICTE Pragati (₹50,000/yr for Girls in Tech)*, *AICTE Saksham (Specially-Abled)*, *UGC Single Girl Child PG Fellowship*.
  * **State Schemes**: *UP Dashmottar Fee Refund*, *MahaDBT Rajarshi Shahu Maharaj EBC Scheme*.
  * **CSR & Foundations**: *Reliance Foundation UG Scholarships*, *Kotak Kanya (₹1.5 Lakh/yr for Girls in STEM/MBBS/Law)*, *HDFC Parivartan*.
* **📄 Actionable Document Checklist**: Generates exact issuing authorities (*Tehsildar/Revenue Dept, State E-District, College Registrar*) and **Aadhaar-NPCI DBT Bank Seeding instructions**.
* **🇮🇳 "Saral Samjhauti" (Hinglish Plain-Language Guides)**: Converts 30-page complex legal circulars into simplified answers to *Kaun apply kare?*, *Kitne paise milenge?*, and *Kya document chahiye?*.
* **📲 1-Click WhatsApp Share**: Formats scholarship summaries with direct portal links for students to share with classmates and parents.
* **🛡️ Official Scam Shield**: Guarantees verified official portals with 100% free government application notices.

### 🔬 2. Academic & Faculty Grant Intelligence
* **Multi-Source Asynchronous Crawlers**: Scheduled ingestion across Indian statutory bodies with SHA-256 deduplication and checkpointing.
* **Multimodal Document Layout Parsing & OCR Fallback**: Automatic routing of scanned and raster PDFs to Tesseract OCR based on character density metrics.
* **Hybrid Semantic Retrieval (BM25 + Dense RRF)**: Reciprocal Rank Fusion ($k=60$) combining BM25 keyword matching with 384-dimensional dense semantic vectors.
* **Profile-to-Grant Alignment & Compliance Verifier**: Upload/paste faculty or student research statements to get ranked grants and pass/warning/fail eligibility checks.
* **RFC 5545 `.ics` Calendar Sync**: 1-click export of grant deadlines with 7-day and 24-hour reminder alarms.
* **Automated Proposal Skeleton Drafter**: Generates Ministry of Finance OM-compliant budget breakdowns and structured technical proposal outlines.
* **Interactive Glassmorphic Dashboard**: Modern, responsive dark-mode web application.

---

## 🏗️ Architecture

```
         ┌──────────────────────────────────────────────────────────┐
         │ Public Indian Portals (NSP, AICTE, UGC, State, DST, CSIR)│
         └────────────────────────────┬─────────────────────────────┘
                                      │ aiohttp / Scrapers
                                      ▼
         ┌──────────────────────────────────────────────────────────┐
         │ Ingestion, SHA-256 Deduplication & PDF/OCR Parser        │
         └────────────────────────────┬─────────────────────────────┘
                                      │
                                      ▼
         ┌──────────────────────────────────────────────────────────┐
         │ Entity Extractor & Pydantic Normalizer (Budgets, Dates)  │
         └─────────────────────┬──────────────────────────────┬─────┘
                               │                              │
                               ▼                              ▼
                 ┌──────────────────────────┐   ┌──────────────────────────┐
                 │  SQLite / CSV Database   │   │ Dense 384-d Vector Index │
                 └─────────────┬────────────┘   └─────────────┬────────────┘
                               └──────────────┬───────────────┘
                                              │
                                              ▼
                 ┌─────────────────────────────────────────────────────────┐
                 │     Hybrid Search (RRF) & Multi-Criteria Matcher        │
                 └────────────────────────────┬────────────────────────────┘
                                              │
               ┌──────────────────────────────┼──────────────────────────────┐
               ▼                              ▼                              ▼
    [🎓 Vidyarthi Hub]             [🔬 Faculty Grants]             [📄 Doc Checklists]
    • Am I Eligible? Wizard        • Dense Vector Match            • NPCI DBT Seeding
    • Hinglish Plain Explainer     • MoF Proposal Drafter          • Tehsildar Validity
    • WhatsApp 1-Click Share       • .ICS Deadline Alarms          • Scam Shield
```

---

## 🚀 Quick Start

### 1. Installation

```bash
# Clone repository
git clone https://github.com/3tbhai/MadadgarAI.git
cd MadadgarAI

# Create and activate virtual environment
python -m venv venv

# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# On Linux / macOS:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Launch Application & Web Dashboard

```bash
python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```

Open your browser at: **[http://localhost:8000](http://localhost:8000)** (or Swagger API Docs at **[http://localhost:8000/docs](http://localhost:8000/docs)**).

---

## 🧪 Running Tests and Evaluation Benchmark

### Run Automated Unit Tests (28/28 Passed)
```bash
python -m pytest tests/ -v
```

### Run Empirical Benchmark Evaluation
```bash
python -m evaluation.benchmark_runner
```

---

## 📡 API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Interactive Web Dashboard (Vidyarthi Hub & Grant Explorer) |
| `POST` | `/api/student/match` | Student profile eligibility evaluation & ranking |
| `GET` | `/api/student/scholarships` | Filterable list of student scholarship opportunities |
| `GET` | `/api/student/scholarships/{id}/checklist` | Issuing authority & document requirements |
| `GET` | `/api/student/scholarships/{id}/hinglish` | Plain Hindi/Hinglish summary for easy sharing |
| `GET` | `/api/student/meta` | Dropdown metadata for states, categories, and degrees |
| `POST` | `/api/search` | Hybrid BM25 + Dense vector search via RRF |
| `POST` | `/api/match-profile` | Faculty research profile alignment & compliance |
| `GET` | `/api/foas/{foa_id}/calendar` | Download RFC 5545 `.ics` deadline reminder |
| `POST` | `/api/foas/{foa_id}/draft-proposal` | Draft tailored MoF proposal skeleton |
| `POST` | `/api/ingest/trigger` | Trigger ingestion & index updates |

---

## 👥 Authors & Supervisor

* **Aman Singh** (2023BTECH006)
* **Anjisht Amritanshu** (2023BTECH009)
* **Ayush Choudhary** (2023BTECH020)
* **Supervisor**: Dr. Deepika Prakash

*Institute of Engineering and Technology (IET), JK Lakshmipat University, Jaipur.*
