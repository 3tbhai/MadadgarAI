# MadadgaarAI: An AI-Powered Funding Intelligence System
**Automated FOA Ingestion, Semantic Tagging, and Grant Matching**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111%2B-green.svg)](https://fastapi.tiangolo.com)
[![Tests: Passing](https://img.shields.io/badge/Tests-20%2F20%20Passed-brightgreen.svg)]()

MadadgaarAI is an end-to-end funding intelligence platform engineered to ingest, parse, semantically tag, and match **Funding Opportunity Announcements (FOAs)** and scholarship circulars across Indian government and statutory portals (**DST, ANRF/SERB, CSIR, AICTE, NSP, DBT**).

---

## 🌟 Key Capabilities

1. **Multi-Source Asynchronous Crawlers**: Scheduled ingestion across Indian statutory bodies with SHA-256 deduplication and checkpointing.
2. **Multimodal Document Layout Parsing & OCR Fallback**: Automatic routing of scanned and raster PDFs to Tesseract OCR based on character density metrics.
3. **Structured Information Extraction & Validation**: Regex and NLP rules normalized into strict **Pydantic v2 schemas**, persisting to SQLite and exporting to JSON/CSV.
4. **Ontology-Aligned Semantic Tagging**: Categorizes opportunities into hierarchical Indian academic research taxonomies.
5. **Hybrid Semantic Retrieval (BM25 + Dense RRF)**: Reciprocal Rank Fusion ($k=60$) combining BM25 keyword matching with 384-dimensional dense semantic vectors.
6. **Profile-to-Grant Alignment & Compliance Verifier**: Upload/paste faculty or student research statements to get ranked grants and pass/warning/fail eligibility checks.
7. **RFC 5545 `.ics` Calendar Sync**: 1-click export of grant deadlines with 7-day and 24-hour reminder alarms.
8. **Automated Proposal Skeleton Drafter**: Generates Ministry of Finance OM-compliant budget breakdowns and structured technical proposal outlines.
9. **Interactive Glassmorphic Dashboard**: Modern, responsive dark-mode web application.

---

## 🏗️ Architecture

```
                               ┌─────────────────────────────┐
                               │    Public Indian Portals    │
                               │  (DST, ANRF, CSIR, AICTE)   │
                               └──────────────┬──────────────┘
                                              │ aiohttp / Playwright
                                              ▼
                               ┌─────────────────────────────┐
                               │     Ingestion & Caching     │
                               │   (SHA-256 Deduplication)   │
                               └──────────────┬──────────────┘
                                              │
                                              ▼
                               ┌─────────────────────────────┐
                               │   Layout Parser & OCR       │
                               │  (pdfplumber / Tesseract)   │
                               └──────────────┬──────────────┘
                                              │
                                              ▼
                               ┌─────────────────────────────┐
                               │  Entity Extractor (Pydantic)│
                               │  (Budgets, Dates, Tiers)    │
                               └───────┬─────────────┬───────┘
                                       │             │
                    Structured Metadata│             │Dense 384-d Vectors
                                       ▼             ▼
                        ┌──────────────────┐     ┌──────────────────┐
                        │ SQLite / CSV DB  │     │   Vector Index   │
                        └─────────┬────────┘     └────────┬─────────┘
                                  │                       │
                                  └───────────┬───────────┘
                                              │
                                              ▼
                               ┌─────────────────────────────┐
                               │  Hybrid Search Engine (RRF) │
                               │   BM25 + Dense Similarity   │
                               └──────────────┬──────────────┘
                                              │
                                              ▼
                               ┌─────────────────────────────┐
                               │  FastAPI Backend & Web UI   │
                               │  • Profile Matcher          │
                               │  • Proposal Skeleton Drafter│
                               │  • .ICS Calendar Exporter   │
                               └─────────────────────────────┘
```

---

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/3tbhai/MadadgarAI.git
cd MadadgarAI

# Install dependencies
pip install -r requirements.txt
```

### 2. Launch the Application & Web Dashboard

```bash
python3 -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```

Open your browser at: **[http://localhost:8000](http://localhost:8000)** (or Swagger Docs at **[http://localhost:8000/docs](http://localhost:8000/docs)**).

---

## 🧪 Running Tests and Evaluation Benchmark

### Run Automated Unit Tests (20/20 Passed)
```bash
python3 -m pytest tests/ -v
```

### Run Empirical Benchmark Evaluation
```bash
python3 -m evaluation.benchmark_runner
```

**Benchmark Results:**
- **Retrieval Mean Reciprocal Rank (MRR)**: `1.0000`
- **Retrieval Hit@1**: `100.00%`
- **Retrieval Hit@3**: `100.00%`
- **Extraction F1-Score**: `78.12%`

---

## 📡 API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Serves interactive web dashboard |
| `GET` | `/api/health` | Service health and total indexed schemes |
| `GET` | `/api/foas` | Filterable list of all funding opportunities |
| `GET` | `/api/foas/{foa_id}` | Detailed schema of a specific opportunity |
| `POST` | `/api/search` | Hybrid BM25 + Dense vector search via RRF |
| `POST` | `/api/match-profile` | Profile matching & compliance analysis |
| `GET` | `/api/foas/{foa_id}/calendar` | Download RFC 5545 `.ics` deadline file |
| `POST` | `/api/foas/{foa_id}/draft-proposal` | Draft tailored proposal skeleton |
| `POST` | `/api/ingest/trigger` | Trigger crawler ingestion pipeline |
| `GET` | `/api/stats` | Ingestion statistics & agency breakdown |

---

## 📁 Repository Structure

```
MadadgarAI/
├── data/
│   ├── raw/                 # Downloaded circulars and notices
│   ├── processed/           # SQLite database, JSON and CSV exports
│   └── benchmark/           # Annotated test datasets
├── src/
│   ├── api/                 # FastAPI REST API & endpoints
│   ├── config.py            # Global configuration and paths
│   ├── crawlers/            # DST, ANRF, CSIR, AICTE, NSP crawlers & seeds
│   ├── dashboard/           # Modern Glassmorphic Web UI
│   ├── embeddings/          # Ontology, dense embedder, vector store, hybrid RRF search
│   ├── extractor/           # Regex rules, entity extractor, normalizer
│   ├── matcher/             # Profile matcher, compliance checker, calendar sync, proposal drafter
│   ├── parser/              # PDF layout analyzer & OCR density evaluator
│   └── schemas/             # Strict Pydantic models
├── evaluation/              # Benchmark evaluation harness
├── tests/                   # 20 Unit and integration tests
├── requirements.txt         # Package dependencies
└── README.md
```

---

## 👥 Authors & Supervisor

* **Aman Singh** (2023BTECH006)
* **Anjisht Amritanshu** (2023BTECH009)
* **Ayush Choudhary** (2023BTECH020)
* **Supervisor**: Dr. Deepika Prakash

*Institute of Engineering and Technology (IET), JK Lakshmipat University, Jaipur.*
