# MadadgaarAI REST API Reference & Integration Guide

The MadadgaarAI backend provides high-performance RESTful APIs built on FastAPI. This guide provides example payloads, expected JSON structures, and `curl` testing commands.

---

## Base URL
```
http://localhost:8000
```

---

## 1. System Health Check
**Endpoint**: `GET /api/health`

Verifies that the API server is operational and reports the number of indexed funding and scholarship opportunities.

### Example Request
```bash
curl -X GET "http://localhost:8000/api/health"
```

### Example Response (200 OK)
```json
{
  "status": "healthy",
  "service": "MadadgaarAI Funding Intelligence",
  "total_opportunities": 21
}
```

---

## 2. Student Scholarship Eligibility Match
**Endpoint**: `POST /api/student/match`

Evaluates a student's profile across Central (NSP), State (UP, Maharashtra), AICTE/UGC, and CSR foundation schemes.

### Example Request
```bash
curl -X POST "http://localhost:8000/api/student/match" \
  -H "Content-Type: application/json" \
  -d '{
    "state_of_domicile": "Uttar Pradesh",
    "social_category": "OBC",
    "gender": "Female",
    "annual_family_income": 180000,
    "course_degree": "B.Tech",
    "education_level": "Undergraduate",
    "percentage_12th": 86.5,
    "is_specially_abled": false,
    "is_single_girl_child": false
  }'
```

### Example Response (200 OK)
```json
[
  {
    "scholarship": {
      "foa_id": "SCHOLARSHIP-UP-DASHMOTTAR-2026",
      "title": "Uttar Pradesh Post-Matric Scholarship & Fee Reimbursement Scheme (Dashmottar)",
      "agency": "State Govt",
      "award_amount": "100% Tuition Fee Refund + Monthly Maintenance Allowance",
      "direct_application_url": "https://scholarship.up.gov.in/RegistrationNew.aspx"
    },
    "match_category": "Guaranteed",
    "confidence_score": 0.98,
    "reasons": [
      "Domicile matches Uttar Pradesh",
      "Family income ₹1,80,000 is well within the ₹2,00,000 ceiling for OBC category"
    ],
    "application_instructions": [
      "Register at scholarship.up.gov.in using Aadhaar OTP authentication",
      "Select Post-Matric other than inter category"
    ]
  }
]
```

---

## 3. Hybrid Semantic Search
**Endpoint**: `POST /api/search`

Combines Okapi BM25 keyword matching with dense 384-dimensional semantic embeddings using Reciprocal Rank Fusion ($k=60$).

### Example Request
```bash
curl -X POST "http://localhost:8000/api/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "artificial intelligence semiconductor materials",
    "top_k": 3
  }'
```

### Response Attributes
- `foa`: Detailed Funding Opportunity Announcement object.
- `relevance_score`: Reciprocal Rank Fusion combined score.
- `bm25_score`: Okapi BM25 sparse lexical score.
- `dense_score`: Cosine similarity from dense embedding vector.

---

## 4. Academic Grant Profile Matching
**Endpoint**: `POST /api/match-profile`

Aligns faculty and researcher proposals with active statutory funding announcements (DST, ANRF, CSIR, DBT).

### Example Request
```bash
curl -X POST "http://localhost:8000/api/match-profile" \
  -H "Content-Type: application/json" \
  -d '{
    "research_summary": "Development of low-cost point-of-care microfluidic biosensors for rapid pathogen detection.",
    "user_role": "Faculty / Principal Investigator",
    "applicant_age": 38,
    "highest_degree": "Ph.D.",
    "top_k": 3
  }'
```

---

## 5. RFC 5545 Calendar Deadline Export
**Endpoint**: `GET /api/foas/{foa_id}/calendar`

Generates an `.ics` iCalendar file with 7-day and 24-hour reminder alarms that can be imported directly into Google Calendar, Microsoft Outlook, or Apple Calendar.

### Example Request
```bash
curl -X GET "http://localhost:8000/api/foas/DST-CRG-2026-01/calendar" -o grant_deadline.ics
```

---

## 6. Document Checklist & Hinglish Explainer
**Endpoints**:
- `GET /api/student/scholarships/{foa_id}/checklist`
- `GET /api/student/scholarships/{foa_id}/hinglish`

Returns issuance authorities (Tehsildar, College Registrar, E-District) and simplified *"Saral Samjhauti"* guides in Hindi/Hinglish.

