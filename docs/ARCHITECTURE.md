# MadadgaarAI System Architecture & Engineering Specification

This document outlines the end-to-end architectural design, mathematical foundations, data ingestion pipelines, and multi-criteria evaluation engines powering **MadadgaarAI**.

---

## 1. High-Level Architecture Overview

MadadgaarAI bridges Indian statutory scholarship portals, governmental research funding agencies, and academic applicants using an asynchronous multi-tier pipeline:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        Statutory Portals & APIs                        │
│   (NSP, AICTE, UGC, MahaDBT, UP Scholarship, DST, ANRF/SERB, CSIR, DBT) │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                         Asynchronous Web Crawlers
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   Ingestion & Deduplication Engine                     │
│    • SHA-256 Content Hashing & Checkpointing                           │
│    • Layout-Aware PDF Parser & Heuristic Tesseract OCR Fallback        │
│    • Pydantic Schema Validation & Semantic Normalization               │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                    Normalized Grants & Scholarships
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                      Hybrid Knowledge Storage                          │
│    • SQLite Structured Relational Store (madadgaar.db)                 │
│    • In-Memory BM25 Sparse Inverted Index                              │
│    • 384-Dimensional Dense Semantic Embeddings (all-MiniLM-L6-v2)      │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
               Unified Retrieval & Constraint Evaluation
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                      Intelligent Reasoning Engines                     │
│  🎓 Vidyarthi AI (Student Matcher)   🔬 Research Alignment Engine      │
│  • Zero-knowledge constraint solver  • Reciprocal Rank Fusion (k=60)   │
│  • Means-tested income thresholding  • MoF OM-compliant budget drafter │
│  • Aadhaar-DBT bank seeding checker  • RFC 5545 .ics deadline alerts   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Ingestion & Document Processing Pipeline

### 2.1 SHA-256 Deduplication & Checkpointing
Every ingested portal circular or scheme announcement is evaluated against a cryptographic content hash:
$$\text{Hash} = \text{SHA-256}(\text{Notice Content} \parallel \text{Agency} \parallel \text{Title})$$
If the hash matches an existing record in SQLite, the document is tagged as already indexed, avoiding expensive re-embedding operations and database bloat.

### 2.2 Text Density Routing & OCR Fallback
Incoming notices in PDF format vary between searchable digital PDFs and scanned circulars:
- **Character Density Threshold ($\tau = 120\text{ chars/page}$)**: If the average character density falls below $\tau$, the document is routed to the `OCRWorker` leveraging `pytesseract`.
- **Page Capping ($N \le 15$)**: Avoids compute bottlenecks by selectively parsing the executive summary, eligibility requirements, and budget breakdown sections.

---

## 3. Hybrid Semantic Search & Reciprocal Rank Fusion (RRF)

To achieve high retrieval accuracy without missing exact scheme names or statutory abbreviations (e.g., "AICTE Pragati", "DST-CRG", "TARE"), MadadgaarAI combines sparse lexical search with dense semantic embeddings via **Reciprocal Rank Fusion**.

### 3.1 Mathematical Formulation
Given a query $q$, the ranking score for document $d$ across both sparse ($R_{\text{BM25}}$) and dense ($R_{\text{Dense}}$) rankings is computed as:

$$\text{RRF}(d) = \sum_{m \in \{\text{BM25}, \text{Dense}\}} \frac{1}{k + R_m(d)}$$

Where:
- $k = 60$ is the standard smoothing constant preventing top-ranked outliers from skewing the fused score.
- $R_{\text{BM25}}(d)$ is the 1-based rank of document $d$ produced by the Okapi BM25 inverted index.
- $R_{\text{Dense}}(d)$ is the 1-based rank of document $d$ calculated via cosine similarity between the 384-dimensional dense embeddings:

$$\text{Sim}_{\text{dense}}(q, d) = \frac{\mathbf{e}_q \cdot \mathbf{e}_d}{\|\mathbf{e}_q\| \|\mathbf{e}_d\|}$$

---

## 4. Vidyarthi AI: Zero-Knowledge Student Scholarship Matcher

The student scholarship engine prioritizes privacy and accuracy:
1. **Zero-Knowledge Architecture**: Does not require personally identifiable credentials (no Aadhaar numbers or bank details stored).
2. **Multi-Constraint Verification Matrix**:
   - **Domicile Compliance**: central schemes permit All-India domiciles; state schemes (e.g., MahaDBT, UP Dashmottar) enforce strict domicile validation.
   - **Gender & Social Category Exclusivity**: Automated filtering for female-exclusive schemes (e.g., AICTE Pragati, Kotak Kanya) and category-specific reservations (SC, ST, OBC, EBC, DNT, Minority).
   - **Means-Tested Income Bounds**: Verifies annual family income against statutory ceilings (e.g., ₹2.5 Lakh, ₹6 Lakh, ₹8 Lakh).
   - **Academic Minimums**: Verifies 12th standard percentage thresholds and current enrollment level (Diploma, UG, PG, Ph.D.).

3. **Output Artifacts**:
   - Categorized by **Guaranteed** vs. **High Probability** opportunities.
   - Actionable document checklists mapped to exact issuing authorities (Tehsildar / Revenue Department, State E-District, College Registrar).
   - Direct active registration deep-links bypassing complex portal homepages.
   - Bilingual Hinglish (*"Saral Samjhauti"*) plain-language summaries for simplified student understanding.
