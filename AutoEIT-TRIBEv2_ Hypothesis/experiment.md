# AutoEIT + TRIBE v2 Experiment: Brain-State Similarity for EIT Scoring

**Experiment 1 (EXP-1)**  
**Date:** April 2026  
**Author:** Jb Anmol (GSoC 2026 - HumanAI Foundation)

---

## 1. Research Question

### Primary Question
Does TRIBE v2 brain-state similarity between native speaker prompts and learner responses correlate with human-evaluated EIT scores?

### Hypothesis
- **Core Hypothesis:** Same sentence → Same brain activation pattern
- If learner preserves meaning, brain patterns will be similar to prompt
- Brain-state similarity can predict 0-4 EIT scores

### Why This Matters
- EIT (Elicited Imitation Task) scores meaning preservation, not form
- Standard ASR/AI fails: phonetic errors → wrong scores
- Neural approach captures semantic meaning, not surface form

---

## 2. Background

### 2.1 The Problem
- Learners produce phonetic variations: "corkalme" instead of "cortarme"
- Standard metrics (WER, BLEU) penalize valid responses
- Need: meaning-based evaluation

### 2.2 TRIBE v2 as Solution
- Predicts fMRI-like brain responses from audio
- Uses Wav2Vec-BERT (audio features) → unified Transformer → brain space
- Captures high-level semantic meaning, not surface form
- Output: fsaverage5 cortical mesh (~20k vertices)

### 2.3 Neural Synchrony Evidence
From "Brain Synchrony in Language Communication.md":
> "When individuals process identical linguistic stimuli (like repeating the same sentence), their brains actively couple and produce highly similar electrophysiological and hemodynamic fluctuations."

This is **Intersubject Correlation (ISC)** - the neural basis for our hypothesis.

---

## 3. Methods

### 3.1 Dataset
| Parameter | Value |
|-----------|-------|
| **Participant** | 038010-2A |
| **Audio File** | data/raw_audio/038010_EIT-2A.mp3 |
| **Duration** | ~9 minutes |
| **Items** | 30 sentences |
| **Start Offset** | 150s (English instructions skipped) |

### 3.2 Stimuli
Source: `test2_scoring/outputs/scores/extracted_data.json`

| Item | Stimulus (Target) |
|------|-------------------|
| 1 | Quiero cortarme el pelo |
| 2 | El libro está en la mesa |
| 3 | El carro lo tiene Pedro |
| 4 | El se ducha cada mañana |
| 5 | ¿Qué dice usted que va a hacer hoy? |
| 6 | Dudo que sepa manejar muy bien |
| 7 | Las calles de esta ciudad son muy anchas |
| 8 | Puede que llueva mañana todo el día |
| 9 | Las casas son muy bonitas pero caras |
| 10 | Me gustan las películas que acaban bien |
| 11 | El chicko con el que yo salgo es español |
| 12 | Después de cenar me fui a dormir tranquilo |
| 13 | Quiero una casa en la que vivan mis animales |
| 14 | Hay muchas personas que no tienen trabajo |
| 15 | Ella tiene que trabajar mañana |
| 16 | Mi padre va a ir al médico |
| 17 | Juan tiene dos hermanos |
| 18 | El profesor va a explicar la lección |
| 19 | Me voy a poner una chaqueta |
| 20 | ¿Cuántos años tiene ella? |
| 21 | El agua está muy fría |
| 22 | Ese libro es muy interesante |
| 23 | Ellos van a comer en un restaurante |
| 24 | Tengo que comprar leche |
| 25 | La tienda está cerrada |
| 26 | Él no quiere ir a la fiesta |
| 27 | Hoy es un día muy bueno |
| 28 | Ella vive en una casa pequeña |
| 29 | El niño está jugando en el parque |
| 30 | Mi madre quiere un café |

### 3.3 Audio Segmentation

**Structure:**
```
[150s offset: English instructions]
Item 1: [Native prompt] → [pause] → [Learner response]
Item 2: [Native prompt] → [pause] → [Learner response]
...
Item 30: [Native prompt] → [pause] → [Learner response]
```

**Timestamp Source:** `EXP-1/timestamps/038010_EIT-2A_timestamps.csv`

**Process:**
1. Manual annotation using Audacity
2. Mark prompt_start, prompt_end, learner_start, learner_end
3. Segment audio into 30 prompt files + 30 response files
4. Convert to WAV format for TRIBE v2

### 3.4 TRIBE v2 Processing

| Parameter | Value |
|-----------|-------|
| **Model** | facebook/tribev2 |
| **Input** | Audio (WAV format) |
| **Output** | fMRI predictions |
| **Mesh** | fsaverage5 (~20k vertices) |
| **Resolution** | 1 TR = 1 second |
| **Hemodynamic Offset** | 5 seconds (applied by model) |

**Processing Steps:**
```python
# For each item:
1. Load prompt_audio.wav → get_events_dataframe() → predict() → prompt_preds
2. Load response_audio.wav → get_events_dataframe() → predict() → response_preds
3. Save both predictions to EXP-1/predictions/
```

### 3.5 Similarity Metrics

| Metric | Formula | Use Case |
|--------|---------|----------|
| **Cosine Similarity** | cos(A, B) = (A·B)/(\|\|A\|\|×\|\|B\|\|) | Whole-brain spatial pattern |
| **Pearson Correlation** | r = cov(A,B)/(σA × σB) | Linear relationship |
| **Euclidean Distance** | \|\|A - B\|\| | Absolute difference |
| **Region-weighted** | Weighted sum of ROI similarities | Semantic focus |

### 3.6 Region-of-Interest (ROI) Analysis

Target regions for language processing:
| Region | Role | Expected Pattern |
|--------|------|-----------------|
| **TPJ** | Semantic integration | Meaning preserved? |
| **Wernicke** | Language comprehension | Understanding intact? |
| **Broca (IFG)** | Morphosyntax, production | Grammatical encoding |
| **Auditory Cortex** | Sound processing | Acoustic similarity |

### 3.7 Validation

**Comparison Data:** LLM-as-judge scores from `test2_scoring/outputs/scores/all_scores.json`

**Analysis:**
1. Compute brain similarity for all 30 items
2. Get LLM-as-judge scores (0-4)
3. Calculate correlation (Pearson r, Spearman ρ)
4. Calibrate thresholds for 0-4 mapping
5. Report accuracy vs LLM scores

---

## 4. Expected Results

### Scenario Mapping
| Scenario | Brain Similarity | Expected Score |
|----------|-----------------|----------------|
| Exact match | High (>0.8) | 4 |
| Meaning preserved, grammar altered | Moderate-High (0.6-0.8) | 3 |
| Partial meaning | Moderate (0.4-0.6) | 2 |
| Wrong meaning / garbled | Low (<0.4) | 1 or 0 |

### Success Criteria
- **Primary:** Correlation (r) > 0.5 between brain similarity and LLM scores
- **Secondary:** Threshold-based scoring achieves >70% accuracy

---

## 5. Limitations & Vulnerabilities

### 5.1 Methodological Limitations
| Limitation | Impact | Mitigation |
|------------|--------|------------|
| **No real fMRI** | TRIBE v2 predicts, not measures | Acknowledge as limitation |
| **Audio-only input** | Video cues not captured | Note in conclusions |
| **Single participant** | Results may not generalize | Propose multi-participant study |
| **Average brain model** | Individual differences ignored | Discuss generalizability |

### 5.2 Technical Limitations
| Limitation | Impact | Mitigation |
|------------|--------|------------|
| **Hemodynamic lag** | 5s offset in predictions | Account for timing |
| **Audio chunking** | 30-60s segments | Verify segment boundaries |
| **Manual timestamps** | Potential human error | Cross-validate with Whisper |
| **gTTS proxy (if needed)** | Not authentic prompt audio | Use only if necessary |

### 5.3 Validation Limitations
| Limitation | Impact | Mitigation |
|------------|--------|------------|
| **No ground truth** | Human scores unavailable | Use LLM-as-judge as proxy |
| **Small sample** | 30 items insufficient | Report confidence intervals |
| **LLM biases** | Systematic errors possible | Show error analysis |

### 5.4 Reporting Standards
- Always report: mean ± 95% CI
- Include: sample size, effect size, p-values
- Document: all preprocessing steps
- Publish: raw similarity scores alongside final results

---

## 6. File Structure

```
EXP-1/
├── timestamps/
│   └── 038010_EIT-2A_timestamps.csv    # Manual annotations
├── audio/
│   ├── prompt/                          # 30 prompt audio files
│   │   ├── prompt_01.wav
│   │   └── ...
│   └── response/                        # 30 response audio files
│       ├── response_01.wav
│       └── ...
├── predictions/
│   ├── prompt_preds/
│   │   └── item_01.npy
│   └── response_preds/
│       └── item_01.npy
├── similarity/
│   └── similarities.csv                 # All similarity scores
├── validation/
│   └── correlation_analysis.json        # Statistical results
├── logs/
│   └── processing_log.txt               # Full processing log
├── config.yaml                          # All parameters
└── README.md                           # This file
```

---

## 7. Timeline

| Phase | Task | Status |
|-------|------|--------|
| 1 | Create timestamp template | ✅ Complete |
| 2 | Manual timestamp annotation | 🔄 In Progress |
| 3 | Segment audio into prompt/response | ⏳ Pending |
| 4 | Generate TRIBE v2 predictions | ⏳ Pending |
| 5 | Compute similarity metrics | ⏳ Pending |
| 6 | Validate with LLM-as-judge scores | ⏳ Pending |
| 7 | Statistical analysis | ⏳ Pending |
| 8 | Document results | ⏳ Pending |

---

## 8. References

1. **TRIBE v2 Paper:** d'Ascoli et al. (2026). "A foundation model of vision, audition, and language for in-silico neuroscience." Meta AI.

2. **ISC Methodology:** "Measuring shared responses across subjects using intersubject correlation." bioRxiv.

3. **EIT Rubric:** Ortega, L. (2000). "Understanding SLA through Ionguever pronunciation research." In R. G. (Ed.), new perspectives on the study of SLA.

4. **Neural Synchrony:** Brain Synchrony in Language Communication.md (in this folder)

5. **TRIBE v2 Demo:** https://aidemos.atmeta.com/tribev2/

---

## 9. Code & Data Availability

| Item | Location |
|------|----------|
| **Audio** | `data/raw_audio/038010_EIT-2A.mp3` |
| **Stimuli** | `test2_scoring/outputs/scores/extracted_data.json` |
| **LLM Scores** | `test2_scoring/outputs/scores/all_scores.json` |
| **TRIBE v2** | `facebook/tribev2` (HuggingFace) |
| **Source Code** | `tribeV2_source/` |
| **Experiment Doc** | This file |

---

## 10. Changelog

| Date | Change | Author |
|------|--------|--------|
| 2026-04-03 | Initial experiment.md created | Jb Anmol |
| 2026-04-03 | Timestamp template created | Jb Anmol |

---

*This document will be updated throughout EXP-1.*
