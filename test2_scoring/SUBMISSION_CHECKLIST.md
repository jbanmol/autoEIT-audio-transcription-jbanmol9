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

