# Contributing to MadadgaarAI

Thank you for contributing to **MadadgaarAI**, India's National Scholarship and Research Funding Intelligence System!

---

## 1. Code of Conduct

We are committed to providing a friendly, safe, and welcoming environment for all contributors, regardless of experience level, gender identity, or background.

---

## 2. Development Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/3tbhai/MadadgarAI.git
   cd MadadgarAI
   ```

2. **Create & Activate Virtual Environment**:
   ```bash
   python -m venv venv
   # On Windows PowerShell:
   .\venv\Scripts\Activate.ps1
   # On Linux / macOS:
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Pre-flight Diagnostics**:
   ```bash
   python scripts/check_system_health.py
   ```

---

## 3. Branching Strategy & Commit Guidelines

- **Branch Naming**:
  - `feat/<feature-name>` for new capabilities
  - `fix/<bug-description>` for bug fixes
  - `docs/<doc-update>` for documentation changes
  - `refactor/<module-name>` for code refactoring

- **Conventional Commits**:
  Please format commit messages according to the Conventional Commits specification:
  - `feat: ...`
  - `fix: ...`
  - `docs: ...`
  - `test: ...`
  - `ci: ...`
  - `chore: ...`

---

## 4. Coding Standards

- **Python Style**: Adhere to PEP 8 standards. Use `black` and `flake8` for formatting where applicable.
- **Type Annotations**: Provide explicit type hints for function signatures and public APIs.
- **Docstrings**: Document classes and public functions following Google or Sphinx docstring format.
- **Zero-Knowledge Privacy**: Never log or store personally identifiable student information (PVI/Aadhaar/bank credentials).

---

## 5. Testing & Verification

Before submitting any Pull Request:
```bash
# 1. Run full test suite
python -m pytest tests/ -v

# 2. Run retrieval benchmark
python -m evaluation.benchmark_runner
```
Ensure all tests pass and no regression occurs in retrieval metrics ($Hit@1 = 100\%$).

