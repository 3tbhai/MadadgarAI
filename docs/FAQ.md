# Frequently Asked Questions (FAQ) & Troubleshooting Guide

---

## 1. Installation & Environment

### Q1: Why does importing `torch` or `sentence_transformers` take 15–20 seconds on first launch on Windows?
**A:** On Windows systems, PyTorch initializes several internal DLLs (`torch_cpu.dll`, `c10.dll`). Subsequent calls will be cached. Additionally, setting the environment variable `HF_HUB_OFFLINE=1` once the `all-MiniLM-L6-v2` model is downloaded avoids online HTTP HEAD checks against the HuggingFace Hub.

### Q2: How do I resolve `Address already in use` (Port 8000)?
**A:** Another process is utilizing port 8000. You can change the port via environment variable:
```powershell
$env:MADADGAAR_PORT="8080"
python run.py
```
Or kill the process holding port 8000 in PowerShell:
```powershell
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process -Force
```

---

## 2. OCR & PDF Ingestion

### Q3: How do I configure Tesseract OCR on Windows?
**A:** If you want local OCR for scanned PDF circulars:
1. Download the installer from UB-Mannheim: `https://github.com/UB-Mannheim/tesseract/wiki`
2. Install to `C:\Program Files\Tesseract-OCR`
3. Add `C:\Program Files\Tesseract-OCR` to your System `PATH` or set `TESSERACT_CMD` in `.env`.

---

## 3. Student Scholarship Matching

### Q4: What is the difference between "Aadhaar Linked" and "NPCI DBT Seeded"?
**A:** 
- **Aadhaar Linked (KYC)**: Your bank has your Aadhaar number recorded for identification.
- **NPCI DBT Seeded (Active Mapper)**: Your account is mapped on the National Payments Corporation of India (NPCI) gateway to receive direct benefit transfers from the government.
- **Verification**: Students can verify active status by logging into `myaadhaar.uidai.gov.in` and navigating to **Bank Seeding Status**.

### Q5: How does the Zero-Knowledge principle protect student privacy?
**A:** The student matcher evaluates eligibility solely through in-memory rule matrices. It never requests, logs, or persists Aadhaar numbers, PAN cards, or bank account numbers to any database.

---

## 4. Academic Grants & Calendar Sync

### Q6: Can I import the generated `.ics` files into Google Calendar?
**A:** Yes! Download the `.ics` file from `/api/foas/{foa_id}/calendar` or the Web UI, open Google Calendar -> Settings -> Import & Export -> Select `.ics` file -> Import. The grant deadline and pre-configured 7-day and 24-hour reminder alarms will automatically appear.

