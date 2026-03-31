# AutoEIT: Test II Submission Checklist

**GSoC 2026 · HumanAI Foundation · Applicant: Jb Anmol**

---

## ✅ Submission Requirements (per GSoC 2026 TEST Description)

> *"Implement a reproducible script that applies the meaning-based rubric to the sentence transcriptions (comparing learner utterances to prompt sentences provided) and outputs sentence-level scores for each utterance in the sample data files."*

---

## 📋 What Was Required vs What Was Delivered

| Requirement | Delivered | File Location |
|:------------|:----------|:--------------|
| Reproducible script | ✅ Python scripts | `test2_scoring/src/*.py` |
| Apply meaning-based rubric | ✅ LLM-as-Judge with rubric | `src/utils/prompt_builder.py` |
| Compare utterances to prompts | ✅ Stimulus ↔ Transcription | Input: Test I output |
| Output sentence-level scores | ✅ 120 items scored | `test2_scoring/data/output/scored_results.xlsx` |

---

## 📦 Files to Submit

### Core Deliverables

| # | File | Description |
|:-:|:-----|:------------|
| 1 | `test2_scoring/data/output/scored_results.xlsx` | **Primary** — Excel with scores (0-4) + rationales |
| 2 | `test2_scoring/README.md` | Documentation with quick start |
| 3 | `test2_scoring/METHODOLOGY.md` | Design choices & validation justification |
| 4 | `test2_scoring/src/01_extract_data.py` | Script: Data extraction |
| 5 | `test2_scoring/src/02_score_with_groq.py` | Script: LLM-as-Judge scoring |
| 6 | `test2_scoring/src/04_populate_scores.py` | Script: Excel population |
| 7 | `test2_scoring/src/utils/prompt_builder.py` | Script: Rubric prompt |
| 8 | `test2_scoring/src/utils/score_parser.py` | Script: Output parser |
| 9 | `test2_scoring/config/test2_config.yaml` | Configuration |
| 10 | `test2_scoring/requirements.txt` | Dependencies |

### Supporting Files (for reference)

| # | File | Description |
|:-:|:-----|:------------|
| 11 | `test2_scoring/outputs/scores/extracted_data.json` | 120 items in JSON |
| 12 | `test2_scoring/outputs/scores/all_scores.json` | Raw scores + rationales |
| 13 | `test2_scoring/.env.example` | Environment template |
| 14 | `test2_scoring/README.md` | Quick start guide |

---

## 🎯 Verification Checklist

### Functionality
- [x] Script runs without errors
- [x] All 120 items scored
- [x] Scores are 0-4 (valid range)
- [x] Each score has rationale

### Output Format (Excel)
- [x] Column D: `LLM_Score` present
- [x] Column E: `LLM_Rationale` present
- [x] 30 rows per participant sheet
- [x] 4 participant sheets (38010-2A, 38011-1A, 38012-2A, 38015-1A)

### Documentation
- [x] README explains how to run
- [x] Methodology explains design choices
- [x] Configuration documented

### Validation
- [x] Consistency check performed (100%)
- [x] Edge cases verified
- [x] Known examples tested

### Research Standards
- [x] Reproducible (same API key + prompt = same results)
- [x] Transparent (rationale for every score)
- [x] Documented (design choices explained)
- [x] Backup preserved (Test I file intact)

---

## 📊 Score Summary

| Metric | Value |
|--------|-------|
| Total Items | 120 |
| Successfully Scored | 120 (100%) |
| Mean Score | 1.93 |
| Consistency Rate | 100% |

### Distribution
| Score | Count | % |
|:-----:|:-----:|:--:|
| 0 | 36 | 30.0% |
| 1 | 12 | 10.0% |
| 2 | 25 | 20.8% |
| 3 | 19 | 15.8% |
| 4 | 28 | 23.3% |

---

## 📧 Email Template for Mentors

**Subject**: AutoEIT Test II: Automated Scoring System - Jb Anmol

**Body**:

Dear HumanAI Foundation Team,

I have completed Test II (Automated Scoring System) for the AutoEIT project.

**Summary**:
- Applied the EIT Scoring Rubric (Ortega, 2000) to 120 transcribed learner productions
- Used LLM-as-Judge approach with Groq API (llama-4-scout model)
- Achieved 100% consistency in validation testing
- All scores include transparent rationales

**Deliverables**:
1. Scored Excel file (`scored_results.xlsx`) — 120 items with scores 0-4
2. Source code with reproducibility
3. Documentation (README + Methodology)

**Files**: Please find all required files in the attached/repository.

**Notes**:
- Test I data remains intact (backup created)
- Free API used (no cost to project)
- Ready for evaluation

Please let me know if you have any questions.

Best regards,  
Jb Anmol  
GSoC 2026 Applicant

---

## 🔗 Quick Test (Mentors)

To verify the system works:

```bash
# Clone/extract repository
cd test2_scoring

# Set API key (or use existing)
export GROQ_API_KEY="your_key"

# Run scoring
python src/01_extract_data.py
python src/02_score_with_groq.py
python src/04_populate_scores.py

# Check output
open data/output/scored_results.xlsx
```

---

**Checklist Completed**: ✅  
**Date**: March 31, 2026