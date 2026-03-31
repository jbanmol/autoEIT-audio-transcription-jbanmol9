# 🎯 AutoEIT — Test II: Automated Scoring System

**GSoC 2026 · HumanAI Foundation · Applicant: Jb Anmol**

---

## 📌 Objective

Implement a reproducible automated scoring system that applies the **EIT Scoring Rubric (Ortega, 2000)** to evaluate 120 transcribed learner productions from Test I. The system compares each learner's transcription to the target stimulus and assigns a score 0-4 based on meaning preservation.

---

## 📋 Task Description (per GSoC 2026 TEST Description)

> *"Implement a reproducible script that applies the meaning-based rubric to the sentence transcriptions (comparing learner utterances to prompt sentences provided) and outputs sentence-level scores for each utterance in the sample data files."*

### Input
- Test I output: Excel with transcriptions (Column C)
- Target stimuli (Column B)

### Output
- Scores (0-4) for each of 120 items
- Score + Rationale columns in Excel format

---

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Test I Output   │ →  │ LLM-as-Judge    │ →  │ Scored Excel    │
│ (120 items)     │    │ (Groq API)      │    │ (Score 0-4)     │
│ Stimulus +      │    │ llama-4-scout   │    │ + Rationale     │
│ Transcription   │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Pipeline Stages

| Stage | Script | Purpose |
|:------|:-------|:--------|
| 1. Extract | `01_extract_data.py` | Parse Excel → JSON (120 items) |
| 2. Score | `02_score_with_groq.py` | LLM judge with rubric prompt |
| 3. Validate | Consistency check | 20% sample scored twice |
| 4. Write-back | `04_populate_scores.py` | Excel with Score + Rationale |

---

## 🔬 Methodology & Design Choices

### Why LLM-as-Judge?

| Alternative Approach | Limitation | Why LLM-as-Judge Wins |
|---------------------|------------|----------------------|
| String matching | Cannot evaluate meaning | ✅ Understands semantic content |
| BLEU/similarity metrics | Cannot distinguish 2 vs 3 | ✅ Follows 0-4 rubric exactly |
| Rule-based systems | Requires extensive pattern coding | ✅ Learns rubric from examples |
| Fine-tuned classifier | Needs training data (insufficient) | ✅ Zero-shot capability |

### Model Selection: `llama-4-scout-17b-16e-instruct`

| Factor | Decision Rationale |
|--------|-------------------|
| **Free tier** | Groq free API (no credit card required) |
| **Speed** | 30K TPM, fast inference on LPU |
| **Quality** | Latest Llama 4 architecture |
| **Context** | Handles prompt + stimulus + transcription |

### Prompt Engineering

The judge prompt includes:
1. **Role framing**: "You are an expert SLA researcher"
2. **Full rubric**: 0-4 score definitions with criteria
3. **Few-shot examples**: Annotated examples from rubric document
4. **Special rules**: Best final response, no penalty for hesitations
5. **Structured output**: `<score>` and `<reasoning>` tags

### Validation Strategy (No Human Calibration)

Since no ground truth exists for these 4 participants, we validate by:

1. **Consistency Check**: Score 24 items (20%) twice, report agreement rate
   - Result: **100% agreement** (24/24)
   
2. **Known Examples Test**: Run on rubric examples to verify prompt works
   
3. **Edge Case Verification**:
   - Empty transcription → score 0
   - Exact match → score 4
   - Minimal words → score 0

---

## 📊 Results

### 🎓 How a Human Would Score (Approximation)

When a researcher scores EIT transcriptions, they look at each sentence and ask: *"How well did the learner reproduce what they heard?"* Here's how the scores break down in human terms:

| Score | What It Means | Real Example |
|:-----:|:--------------|:--------------|
| **0** | "I can barely understand what they tried to say" | Only 1-2 words, or garbled |
| **1** | "They got some words but lost the meaning" | About half there, but message is gone |
| **2** | "Close but not quite right" | Most words there, but meaning is off |
| **3** | "I understood what they meant" | Minor grammar slip, but meaning clear |
| **4** | "Perfect repetition" | Exactly what they heard |

### Score Distribution

| Score | Count | Percentage | Human Interpretation |
|:-----:|:------:|:----------:|:---------------|
| 0 | 36 | 30.0% | "Couldn't make out what they said" |
| 1 | 12 | 10.0% | "Got fragments, but meaning lost" |
| 2 | 25 | 20.8% | "Almost, but meaning shifted" |
| 3 | 19 | 15.8% | "Good enough - I understood them" |
| 4 | 28 | 23.3% | "Spot on - they nailed it" |

**Mean Score: 1.93** (SD: 1.43)

### Consistency Validation

| Metric | Result |
|--------|--------|
| Sample Size | 24 items (20%) |
| Agreement Rate | 100% |
| Disagreements | 0 |

---

## 📁 Directory Structure

```
test2_scoring/
├── config/
│   └── test2_config.yaml          # Model, paths, settings
├── data/
│   ├── input/                     # (Links to Test I output)
│   └── output/
│       └── scored_results.xlsx   # ✅ Final output (120 scored items)
├── src/
│   ├── 01_extract_data.py         # Excel → JSON
│   ├── 02_score_with_groq.py      # LLM-as-Judge scoring
│   ├── 04_populate_scores.py      # Write to Excel
│   └── utils/
│       ├── prompt_builder.py     # Judge prompt construction
│       └── score_parser.py        # Parse LLM output
├── outputs/
│   └── scores/
│       ├── extracted_data.json   # 120 items extracted
│       └── all_scores.json        # All scores + rationales
├── .env.example                   # Environment template
├── requirements.txt
└── README.md                      # This file
```

---

## 🚀 Quick Start

### Prerequisites

1. **Get Groq API Key** (free, no credit card):
   - Sign up at https://console.groq.com/
   - Create API key

2. **Set Environment Variable**:
   ```bash
   export GROQ_API_KEY="your_key_here"
   ```

### Run Pipeline

```bash
cd test2_scoring

# Step 1: Extract data from Test I output
python src/01_extract_data.py

# Step 2: Score all items (requires GROQ_API_KEY)
python src/02_score_with_groq.py

# Step 3: Write scores to Excel
python src/04_populate_scores.py
```

---

## ⚠️ Important Notes

- **Test I is NOT affected** — Original Excel file backed up before modifications
- **Transparent scoring** — Every score includes rationale for auditability
- **Reproducible** — Same API key + prompt = same results
- **Free API tier** — 30 RPM, 500K tokens/day (sufficient for 120 items)

---

## 📝 Scoring Rubric Reference (Ortega, 2000)

| Score | Description | Examples |
|:-----:|:------------|:---------|
| **0** | Nothing/Garbled/Minimal | "Manaña", "El examen que [gibberish]" |
| **1** | ~50% preserved, meaning lost | "Dudo que sepa ma-" |
| **2** | >50% preserved, meaning inexact | "Ella sola cerveza y no come nada" |
| **3** | Meaning fully preserved | "Quiero cortar mi pelo" |
| **4** | Exact repetition | "El libro está en la mesa" |

---

## ✅ Deliverables

1. **Scored Excel**: `test2_scoring/data/output/scored_results.xlsx`
   - Column D: LLM_Score (0-4)
   - Column E: LLM_Rationale (explanation)

2. **Raw Scores**: `test2_scoring/outputs/scores/all_scores.json`

3. **Reproducible Scripts**: All source code in `test2_scoring/src/`

4. **Documentation**: This README + Methodology document

---

> ✅ **Test II Complete.** All 120 items scored with rationales, ready for evaluation.