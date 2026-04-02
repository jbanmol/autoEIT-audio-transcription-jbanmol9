
# Theoretical Framework: TRIBE v2 for Automated EIT Scoring
## Project: AutoEIT + Brain Encoding

---

## 1. Executive Summary

This document provides the theoretical foundation for using **TRIBE v2** (Meta AI's brain encoding model) to automate the scoring of **Elicited Imitation Tasks (EIT)** in second language acquisition research.

### Core Hypothesis

> **Same sentence → Same brain activation pattern**
>
> If the native speaker prompt and the student's response produce similar brain activation patterns, we can score EIT responses without human transcription.

### The Revolution

This isn't just another AI transcription tool. We're leveraging a fundamental neurobiological phenomenon—**neural synchrony**—to solve the hardest problem in language assessment: scoring meaning-preserving but grammatically imperfect responses.

---

## 2. Validating the Hypothesis: "Same Sentences = Same Waves"

### 2.1 The Document That Confirms Everything

The research document **"Brain Synchrony in Language Communication"** explicitly validates our hypothesis:

> *"When individuals process identical linguistic stimuli (like repeating the same sentence), their brains actively couple and produce highly similar electrophysiological and hemodynamic fluctuations."*

This is known as **neural synchrony** or **Intersubject Correlation (ISC)**.

### 2.2 Why This Happens: The Four Pillars

#### Pillar 1: The Shared Linguistic Space

Human brains do not process language merely as acoustic sounds. They map words to a **shared semantic space** where the neural code for a specific sentence's meaning is consistent across different individuals.

**Evidence**: ECoG studies (2024) showed:

- Word-level content appears in speaker's brain ~250ms **before** articulation
- Same content re-emerges in listener's brain ~250ms **after** hearing
- This is the "neural signature" of shared meaning

> [!TIP]
> **Key Insight**: This is exactly what happens in EIT—the instructor's sentence creates a neural template, and the student's brain either matches it or doesn't.

#### Pillar 2: Sensorimotor Integration in EIT

The EIT works precisely because the neural systems for speech perception and speech production **heavily overlap**.

> *"When the student listens to the instructor's prompt, their brain effectively 'primes' the exact same neural assemblies required to replicate that sentence."*

Research using MEG during speech imitation tasks shows:

- Strong functional connectivity between auditory cortex and ventral premotor cortex
- This "representational parity" means perception and production share neural substrates
- If the student correctly perceives the sentence, they're already prepared to produce it

#### Pillar 3: Speaker Independence

This is crucial for our hypothesis: **the neural sameness is independent of who is speaking**.

- **Low-level acoustic regions** (primary auditory cortex): May differ based on pitch/timbre
- **High-level cortical areas** (Default Mode Network, language network): Synchronize completely based on **meaning**

Studies show:

- When participants hear a sentence spoken by different individuals, spatial patterns in the DMN are similar
- Decoders trained on one person's brain can recognize content from another person's brain
- The brain maintains separate representations for "what" (meaning) and "who" (voice)

> [!NOTE]
> **Implication for EIT**: The student doesn't need to sound like the instructor—they just need to convey the same **meaning**.

#### Pillar 4: Frequency-Specific Synchrony

Different frequency bands in brain waves capture different aspects of linguistic processing:

| Band | Frequency | Role in Language |
| :--- | :--- | :--- |
| **Delta** | 0.5-4 Hz | Speech envelope, phrase-level parsing |
| **Theta** | 4-8 Hz | Syllable processing, phonological encoding |
| **Alpha** | 8-14 Hz | Attention, motor prediction |
| **Beta** | 12-25 Hz | Syntactic unification, predictive processing |
| **Gamma** | 30-90 Hz | Lexical-semantic retrieval |

> [!IMPORTANT]
> **Critical Finding**: In EIT-like verbal imitation tasks, enhanced synchrony appears specifically in **theta and alpha bands**—precisely the bands associated with phonological processing and motor planning.

---

## 3. Understanding TRIBE v2

### 3.1 What is TRIBE v2?

TRIBE v2 is a **tri-modal (audio, video, text) artificial intelligence foundation model** designed to predict high-resolution human brain activity (fMRI).

Instead of traditional models that rely on isolated tasks, TRIBE v2 was trained on over **1,000 hours of fMRI data** to map state-of-the-art AI embeddings directly to cortical space.

### 3.2 Architecture Deep Dive

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                            INPUTS                                       │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                 │
│  │    Audio    │    │    Video    │    │    Text     │                 │
│  │  (Wav2Vec)  │    │  (V-JEPA2)  │    │ (LLaMA 3.2) │                 │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘                 │
│         │                  │                  │                         │
│         └──────────────────┼──────────────────┘                         │
│                            │                                            │
│                            ▼                                            │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │              UNIFIED TRANSFORMER ENCODER (~1B params)          │    │
│  │  • Fuses multimodal representations                             │    │
│  │  • Maps to brain space (20,484 cortical vertices)               │    │
│  │  • Trained on 700+ subjects                                     │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                            │                                            │
│                            ▼                                            │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    OUTPUT                                        │    │
│  │  Predicted fMRI response on fsaverage5 cortical mesh           │    │
│  │  Shape: (n_timesteps, 20,484 vertices)                          │    │
│  └─────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3.3 Why TRIBE v2 is Perfect for EIT

| Feature | EIT Application |
| :--- | :--- |
| **Wav2Vec-BERT** | Processes raw audio—no transcriptions needed |
| **fMRI Output** | Same data type showing ISC in research |
| **700+ Subjects** | "Average brain" generalizes across individuals |
| **Foundation Model** | Can predict brain states for any audio/text |
| **No fMRI needed** | We use predictions as proxy for real brain responses |

---

## 4. The GSoC AutoEIT Problem: Test II

### 4.1 The Challenge

Test II requires grading a student's spoken sentence on a **0-4 scale** based on meaning preservation, even when grammar is wrong.

### 4.2 Why Standard AI Fails

| Approach | Problem |
| :--- | :--- |
| **String matching** | `"coltarme"` ≠ `"cortarme"` → fails even though meaning same |
| **WER (Word Error Rate)** | Penalizes phonetic errors → not fair to learners |
| **BLEU/ROUGE** | Requires exact words → fails on paraphrases |
| **ASR transcription** | Whisper "corrects" errors → loses learner data |

### 4.3 The Solution: Semantic Brain-State Comparison

**Instead of comparing text strings, compare brain waves.**

---

## 5. The Top-Tier Proposal: TRIBE v2 + ISC Scoring

### 5.1 The Algorithm

```text
┌──────────────────────────────────────────────────────────────────────────┐
│                     SEMANTIC BRAIN-STATE COMPARISON                      │
└──────────────────────────────────────────────────────────────────────────┘


STEP 1: Generate "Ground Truth" Brain State
──────────────────────────────────────────
Target Prompt (Audio) → TRIBE v2 → Brain Pattern A (20k vertices)
                                    ↓
                    "Standard brain" response to that meaning


STEP 2: Generate Learner's Brain State
────────────────────────────────────────
Student Response (Audio) → TRIBE v2 → Brain Pattern B (20k vertices)
                                    ↓
                    "Standard brain" response to student's meaning


STEP 3: Measure ISC (Intersubject Correlation)
──────────────────────────────────────────────
                              ┌────────────────────┐
                              │ Spatial Correlation │
                              │ (Cosine Similarity)│
                              │ + Temporal Align    │
                              │ + Region Focus      │
                              └────────────────────┘
                                         ↓
                              ISC Score (0.0 to 1.0)


STEP 4: Map to 0-4 Rubric
─────────────────────────
ISC = 0.95-1.0 → Score 4 (Exact match - both form and meaning perfect)
ISC = 0.80-0.94 → Score 3 (Meaning preserved, grammar altered)
ISC = 0.60-0.79 → Score 2 (Meaning ambiguous/incomplete)
ISC = 0.40-0.59 → Score 1 (Partial meaning, significant errors)
ISC < 0.40     → Score 0 (Garbled/Unrelated)
```

### 5.2 Why This Works for Meaning-Based Scoring

#### Score 4: Exact Match

- Both form and meaning identical
- Brain states nearly identical (maximum ISC)
- Example: Prompt "Quiero cortarme el pelo" → Response "Quiero cortarme el pelo"

#### Score 3: Meaning Preserved, Grammar Altered

- **Key insight**: TRIBE v2 captures contextual meaning using LLM embeddings
- Student uses synonymous substitution → triggers **same semantic brain regions**
- High-level brain waves remain the same → valid score 3
- Example: "baja" instead of "barata" → same meaning → high ISC

#### Score 2: Meaning Ambiguous or Incomplete

- Key idea omitted → semantic brain map **drastically shifts**
- ISC in language network drops automatically
- Example: "el carro tiene Pedro" instead of "la tarea tiene Carla" → different meanings → lower ISC

#### Score 1 or 0: Garbled/Unrelated

- Predicted brain activity resembles **idiosyncratic noise**
- No alignment to target's semantic template
- Example: Complete misproduction → near-zero ISC

### 5.3 The Key Innovation

**We're not comparing audio or text—we're comparing the "mental states" they would produce in a standard human brain.**

This solves the meaning-based rubric problem because:

1. **Phonetic errors don't matter**: If meaning is preserved, brain patterns match
2. **Speaker independence**: We're comparing meaning, not voice
3. **No transcription needed**: Process audio directly with TRIBE v2

---

## 6. Methodology

### 6.1 Data Flow

```text
AUDIO INPUTS
├── Target Prompt Audio (from EIT template or separate recording)
└── Student Response Audio (from EIT recording)
        │
        ▼
TRIBE v2 PROCESSING
├── Feature Extraction (Wav2Vec-BERT)
└── Brain Prediction (20,484 vertices × timesteps)
        │
        ▼
SIMILARITY METRICS
├── Whole-brain cosine similarity
├── Region-specific similarity (TPJ, Wernicke, Broca)
├── Temporal correlation (time-series alignment)
└── Frequency-band analysis (theta, alpha, gamma)
        │
        ▼
SCORING
├── Threshold-based classification (0-4)
└── Continuous proficiency score
```

### 6.2 Region-Specific Analysis

Based on ISC research, we focus on specific brain regions:

| Region | Role | What It Tells Us |
| :--- | :--- | :--- |
| **Temporoparietal Junction (TPJ)** | Semantic integration | Meaning preserved? |
| **Wernicke's Area** | Language comprehension | Understanding intact? |
| **Broca's Area (IFG)** | Language production | Grammatical encoding? |
| **Auditory Cortex** | Sound processing | Acoustic similarity? |
| **Premotor Cortex** | Speech planning | Production similarity? |

**Strategy**: Weight TPJ and Wernicke's higher for meaning-based scoring (Score 3), weight Auditory higher for form-based scoring (Score 4).

### 6.3 Expected Results

| Scenario | ISC Pattern | Predicted Score |
| :--- | :--- | :--- |
| Perfect imitation | Very high similarity across all regions | 4 |
| Meaning correct, grammar wrong | High semantic regions, lower production | 3 |
| Partial meaning | Moderate semantic regions | 2 |
| Wrong meaning | Low similarity, noise pattern | 1 or 0 |
| No response | Near-zero activity | 0 |

---

## 7. Implementation Phases

### Phase 1: Exploratory Analysis (Current)

- [x] Load audio files and generate waveforms/spectrograms
- [ ] Generate TRIBE v2 brain predictions for all audio
- [ ] Visualize brain activation patterns
- [ ] Compare similarity between files

### Phase 2: Segmentation

- [ ] Segment audio into prompt/response pairs
- [ ] Manual verification of segment boundaries (if needed)
- [ ] Generate brain predictions for each segment

### Phase 3: Validation

- [ ] Compare brain similarity to human scores
- [ ] Find optimal similarity thresholds
- [ ] Test on held-out participants

### Phase 4: Classifier Development

- [ ] Train classifier on brain pattern features
- [ ] Evaluate accuracy vs. human scoring
- [ ] Deploy for automated scoring

---

## 8. Research Questions

### Primary Question

Does TRIBE v2 brain pattern similarity between native speaker prompts and student responses correlate with human-evaluated EIT scores?

### Secondary Questions

1. **Which brain regions are most predictive of EIT accuracy?**
    - Hypothesis: TPJ (semantic) > Auditory (acoustic)
2. **Does the similarity threshold vary by proficiency level?**
    - Hypothesis: Higher proficiency = higher ISC
3. **Can we identify specific phonetic errors from brain pattern differences?**
    - Hypothesis: Certain errors map to specific region patterns
4. **How does the modality (audio only vs. video) affect prediction accuracy?**
    - Hypothesis: Video adds visual semantics → higher accuracy

---

## 9. Factors That Could Limit Similarity

| Factor | Effect | Mitigation Strategy |
| :--- | :--- | :--- |
| **L2 Proficiency** | Lower proficiency → different neural patterns, especially in frontal regions | Train threshold calibration per proficiency group |
| **Acoustic Differences** | Different voice pitch/timbre → low-level auditory differences | Focus analysis on high-level semantic regions |
| **Attention** | Distracted student → lower ISC | Add attention quality metrics |
| **Phonetic Errors** | Mispronunciation → different processing in auditory cortex | Weight semantic regions higher than acoustic |
| **Working Memory** | Complex sentences → different processing load | Stratify by sentence complexity |

---

## 10. Glossary

| Term | Definition |
| :--- | :--- |
| **ISC** | Intersubject Correlation - correlation between brain responses across individuals |
| **EIT** | Elicited Imitation Task - language assessment where students repeat heard sentences |
| **fMRI** | functional Magnetic Resonance Imaging - measures blood flow related to neural activity |
| **TRIBE v2** | Meta AI's tri-modal brain encoding foundation model |
| **Wav2Vec-BERT** | Self-supervised audio feature extractor (used by TRIBE v2) |
| **fsaverage5** | Standard brain cortical mesh (~20k vertices) |
| **Neural Synchrony** | Coupling/alignment of brain activity between individuals |
| **Hyperscanning** | Simultaneous brain recording from multiple people |
| **DMN** | Default Mode Network - high-level semantic processing regions |
| **TPJ** | Temporoparietal Junction - key region for semantic integration |
| **ISC Score** | Intersubject Correlation value (0-1) measuring brain pattern similarity |

---

## 11. References

1. **TRIBE v2 Paper**: "A foundation model of vision, audition, and language for in-silico neuroscience" (Meta AI, March 2026)
2. **ISC Methodology**: "Measuring shared responses across subjects using intersubject correlation" (bioRxiv)
3. **ECoG Language**: "Brain activity associated with specific words is mirrored between speaker and listener" (EurekAlert, 2024)
4. **LLM-Brain Alignment**: "Large language models explain brain data better than traditional linguistic models"
5. **Theta Synchrony**: "Dual-MEG interbrain synchronization during turn-taking verbal imitation"
6. **Shared Linguistic Space**: Research on "shared model-based linguistic space" using LLMs
7. **Speaker Independence**: Studies on modality-invariant conceptual representations

---

## 12. Conclusion

This framework provides a **neurobiologically-grounded** approach to solving the AutoEIT problem. By leveraging:

1. **Neural synchrony** (same sentences → same brain waves)
2. **TRIBE v2** (foundation model for brain prediction)
3. **ISC metrics** (quantifying brain pattern similarity)

...we can build an automated scoring system that:

- ✅ Doesn't require human transcription
- ✅ Understands meaning over form
- ✅ Is grounded in real neuroscience
- ✅ Scales to any language/dataset

The "same sentences = same waves" hypothesis isn't just a guess—it's proven neuroscience. TRIBE v2 gives us the tool to measure it.

---

*Document updated: April 2026*
*For: GSoC 2026 - AutoEIT Project*
*Author: Jb Anmol*
*Location: new-approach-tribe2/* ,

use [https://aidemos.atmeta.com/tribev2/](https://aidemos.atmeta.com/tribev2/) ,

Here is the fully corrected markdown with the conceptual errors fixed and the TRIBE v2 demo link incorporated:

---

# Theoretical Framework: TRIBE v2 for Automated EIT Scoring

## Project: AutoEIT + Brain Encoding


---

## 1. Executive Summary

This document provides the theoretical foundation for using **TRIBE v2** (Meta AI's brain encoding model) to automate the scoring of **Elicited Imitation Tasks (EIT)** in second language acquisition research.

### Core Hypothesis

> **Same sentence → Same brain activation pattern**
> If the native speaker prompt and the student's response produce similar brain activation patterns, we can score EIT responses without human transcription.

### The Idea

This isn't just another AI transcription tool. The goal is to leverage a fundamental neurobiological phenomenon—**neural synchrony**—to tackle the hardest problem in language assessment: scoring meaning‑preserving but grammatically imperfect responses.

---

## 2. Validating the Hypothesis: "Same Sentences = Same Waves"

### 2.1 The Document That Motivates This

The research document **"Brain Synchrony in Language Communication"** surveys evidence that when people process identical linguistic stimuli, their brains show highly similar neural responses:

> *"When individuals process identical linguistic stimuli (like repeating the same sentence), their brains actively couple and produce highly similar electrophysiological and hemodynamic fluctuations."*

This phenomenon is referred to as **neural synchrony** and is often quantified using **Intersubject Correlation (ISC)** in real brain recordings.

### 2.2 Why This Happens: The Four Pillars

#### Pillar 1: The Shared Linguistic Space

Human brains do not process language merely as acoustic signals. They map words to a **shared semantic space** where the neural code for a specific sentence's meaning is broadly consistent across individuals.

**Evidence** (ECoG, 2024):

- Word‑level content appears in the speaker's brain ~250 ms **before** articulation.
- The same content re‑emerges in the listener's brain ~250 ms **after** hearing the word.
- This timing pattern is a neural signature of shared meaning.

> [!TIP]
> **Key Insight**: In EIT, the instructor's sentence creates a neural template. The student either approximates that template or diverges from it.

#### Pillar 2: Sensorimotor Integration in EIT

EIT works because neural systems for speech perception and speech production **heavily overlap**.

When the student listens to the instructor's prompt, their brain effectively primes the neural assemblies required to reproduce that sentence.

MEG work on speech imitation shows:

- Strong functional connectivity between auditory cortex and ventral premotor cortex.
- **Representational parity**: perception and production share neural substrates.
- If a student accurately perceives the sentence, their motor system is already partially prepared to produce it.

#### Pillar 3: Speaker Independence

For our purposes, a critical finding is that **high‑level linguistic representations are largely speaker‑independent**.

- **Low‑level acoustic regions** (primary auditory cortex) vary with pitch, timbre, and voice.
- **High‑level cortical regions** (language network, Default Mode Network) align primarily on **meaning**.

Studies show:

- When participants hear the same sentence spoken by different speakers, patterns in DMN and language areas are similar.
- Decoders trained on one person's brain activity can often recognize content in another person's brain activity, given the same linguistic input.
- The brain maintains partly separate representations for *what* is being said (meaning) and *who* is speaking (identity).

> [!NOTE]
> **Implication for EIT**: The student does not need to sound like the instructor. What matters is whether the underlying meaning is preserved.

#### Pillar 4: Frequency‑Specific Synchrony (Motivation from EEG/MEG)

Electrophysiological work (EEG/MEG) decomposes neural activity into frequency bands that track different aspects of language processing:

| Band | Frequency | Role in Language |
| :--- | :--- | :--- |
| **Delta** | 0.5–4 Hz | Speech envelope, phrase‑level parsing |
| **Theta** | 4–8 Hz | Syllable‑rate processing, phonological encoding |
| **Alpha** | 8–14 Hz | Attention, motor prediction |
| **Beta** | 12–25 Hz | Syntactic unification, predictive processing |
| **Gamma** | 30–90 Hz | Lexical‑semantic retrieval |

In EIT‑like verbal imitation tasks, enhanced synchrony is often observed in **theta and alpha** bands, associated with phonological processing and motor planning.

> [!IMPORTANT]
> **Important limitation:** These frequency‑band findings come from **EEG/MEG**, which have millisecond‑level temporal resolution. **TRIBE v2 outputs fMRI‑like BOLD predictions**, with second‑level temporal resolution. Theta/alpha/gamma oscillations cannot be extracted directly from TRIBE v2 outputs.
>
> Here, frequency bands are **motivation**, not a method we apply to TRIBE v2 predictions.

---

## 3. Understanding TRIBE v2

### 3.1 What is TRIBE v2?

TRIBE v2 is a **tri‑modal (audio, video, text) foundation model** that predicts high‑resolution human brain activity (fMRI) from naturalistic stimuli.[^1]

Instead of modeling one narrow task, TRIBE v2 is trained on over **1,000 hours of fMRI** from **720 subjects**, across movies, podcasts, and experimental paradigms, to map modern AI embeddings directly to cortical space.[^1]

- **Code**: https://github.com/facebookresearch/tribev2
- **Demo**: https://aidemos.atmeta.com/tribev2/

### 3.2 Architecture Deep Dive

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                                INPUTS                                  │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                 │
│  │    Audio    │    │    Video    │    │    Text     │                 │
│  │ (Wav2Vec)   │    │ (V-JEPA2)   │    │ (LLaMA 3.2) │                 │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘                 │
│         │                  │                  │                        │
│         └──────────────────┼──────────────────┘                        │
│                            │                                           │
│                            ▼                                           │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │              UNIFIED TRANSFORMER ENCODER (~1B params)          │   │
│  │  • Fuses multimodal representations                            │   │
│  │  • Maps to brain space (20,484 cortical vertices)              │   │
│  │  • Trained on 700+ subjects                                    │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                            │                                           │
│                            ▼                                           │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                             OUTPUT                             │   │
│  │  Predicted fMRI response on fsaverage5 cortical mesh           │   │
│  │  Shape: (n_timesteps, 20,484 vertices)                         │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3.3 Why TRIBE v2 is Relevant for EIT

| Feature | EIT Application |
| :--- | :--- |
| **Wav2Vec‑BERT** | Processes raw audio — no text transcription required to get a representation. |
| **Predicted fMRI** | Predicted brain‑response pattern that acts as a **proxy** for representational structure in the brain. |
| **700+ Subjects** | Approximates an “average brain” that generalizes across individuals. |
| **Foundation Model** | Can predict brain‑like responses for arbitrary audio and/or text inputs. |
| **No real fMRI needed** | We only use TRIBE v2's predictions; no scanning of EIT participants is required. |

> [!NOTE]
> **Note**: TRIBE v2 outputs **predicted** BOLD activity. This is not the same as real fMRI used in classical ISC studies, but it can approximate how different stimuli are represented in a shared cortical space.[^1]

---

## 4. The GSoC AutoEIT Problem: Test II

### 4.1 The Challenge

Test II requires grading a student's spoken sentence on a **0–4 scale** based on **meaning preservation**, even when grammar or pronunciation is imperfect.

### 4.2 Why Standard AI Fails

| Approach | Problem |
| :--- | :--- |
| **String matching** | `"coltarme"` ≠ `"cortarme"` even when meaning is preserved. |
| **WER (Word Error Rate)** | Penalizes phonetic errors heavily; unfair and misaligned with the rubric. |
| **BLEU/ROUGE** | Require overlapping word sequences; fail on valid paraphrases or synonyms. |
| **ASR transcription** | Whisper “corrects” learner errors, erasing exactly the deviations we care about. |

### 4.3 The Idea: Semantic Brain‑State Comparison

Instead of comparing **text strings**, we compare **predicted brain‑state patterns** for:

- the **target prompt**, and
- the **learner’s response**.

---

## 5. Proposal: TRIBE v2 + Brain‑State Similarity Scoring

### 5.1 The Algorithm

```text
┌──────────────────────────────────────────────────────────────────────────┐
│                     SEMANTIC BRAIN-STATE COMPARISON                     │
└──────────────────────────────────────────────────────────────────────────┘

STEP 1: Generate "Ground Truth" Brain State
────────────────────────────────────────────
Target Prompt (Audio) → TRIBE v2 → Brain Pattern A (20k vertices)
                                     ↓
                     "Standard brain" response to the target meaning

STEP 2: Generate Learner's Brain State
───────────────────────────────────────
Student Response (Audio) → TRIBE v2 → Brain Pattern B (20k vertices)
                                     ↓
                     "Standard brain" response to student’s meaning

STEP 3: Measure Brain-State Similarity (Cross-Stimulus RSA)
────────────────────────────────────────────────────────────
                              ┌────────────────────────────┐
                              │ Spatial correlation        │
                              │ (e.g., cosine similarity)  │
                              │ + temporal alignment       │
                              │ + region-weighted focus    │
                              └────────────────────────────┘
                                           ↓
                              Similarity score (0.0–1.0)
                     (relative scale; thresholds calibrated
                           empirically against human scores)

STEP 4: Map to 0–4 Rubric
──────────────────────────
Use the similarity score and region-wise patterns to assign:

High similarity       → Score 4 (form + meaning preserved)  
Moderate–high         → Score 3 (meaning preserved, grammar altered)  
Moderate              → Score 2 (meaning ambiguous/incomplete)  
Low                   → Score 1 (partial meaning, significant errors)  
Near‑zero             → Score 0 (garbled/unrelated)
```

> [!IMPORTANT]
> **Important**: Although **ISC** is used in the literature as a cross‑subject metric on real fMRI/EEG, here we are doing **cross‑stimulus similarity** on **predicted** fMRI. Technically, this is closer to **Representational Similarity Analysis (RSA)** than classical ISC.

### 5.2 Why This Could Work for Meaning‑Based Scoring

#### Score 4: Exact Match

- Both form and meaning are preserved.
- Brain‑state similarity is high in both **low‑level auditory** and **high‑level semantic** regions.
- Example: Prompt *"Quiero cortarme el pelo"* → Response *"Quiero cortarme el pelo"*.

#### Score 3: Meaning Preserved, Grammar Altered

- TRIBE v2’s audio (and optionally text) embeddings capture **contextual meaning**.
- A student may use a synonym or make a morphological error, but high‑level semantic regions (e.g., TPJ, MTG, DMN) remain similar.
- Example: *"baja"* instead of *"barata"* → similar semantic pattern in high‑level regions → eligible for Score 3.

#### Score 2: Meaning Ambiguous or Incomplete

- Key semantic elements are missing or altered.
- Similarity in semantic regions drops; patterns shift to reflect a different or partial meaning.
- Example: *"el carro tiene Pedro"* instead of *"la tarea tiene Carla"* — different core proposition → lower similarity.

#### Score 1 or 0: Garbled/Unrelated

- Predicted activity for the learner’s response diverges strongly from the prompt pattern in language/semantic regions.
- The similarity score is low; patterns resemble idiosyncratic noise relative to the target.

### 5.3 The Key Idea

We are **not** comparing audio waveforms or text tokens directly. We are comparing **the brain‑like representations they would evoke in an “average” brain model**.

This addresses the meaning‑based rubric because:

1. **Phonetic errors matter less** when meaning stays intact; high‑level similarity remains.
2. **Speaker differences** (voice, accent) mainly affect low‑level auditory regions; semantic regions can still align.
3. **No human transcription is required** — we process raw audio with TRIBE v2.

---

## 6. Methodology

### 6.1 Data Flow

```text
AUDIO INPUTS
├── Target Prompt Audio (from EIT template or a clean recording)
└── Student Response Audio (from EIT recording)
        │
        ▼
TRIBE v2 PROCESSING
├── Audio → Wav2Vec-BERT features
└── Brain prediction → (n_timesteps, 20,484 vertices)
        │
        ▼
SIMILARITY METRICS
├── Whole-brain cosine similarity
├── Region-specific similarity (e.g., TPJ, Wernicke, Broca)
└── Temporal correlation (time-series alignment)
        │
        ▼
SCORING
├── Threshold-based mapping to 0–4 scale
└── Continuous proficiency score (optional)
```

> [!NOTE]
> **Note**: Frequency‑band analysis (theta/alpha/gamma) is **not** applied to TRIBE v2 outputs because they are fMRI‑like signals, not EEG/MEG.

### 6.2 Region‑Specific Analysis

Based on synchrony and language‑processing literature, we pay particular attention to:

| Region | Role | What It Tells Us |
| :--- | :--- | :--- |
| **Temporoparietal Junction (TPJ)** | Semantic integration | Meaning preserved? |
| **Wernicke’s Area** | Language comprehension | Understanding intact? |
| **Broca’s Area (IFG)** | Morphosyntax, production planning | Grammatical encoding effort? |
| **Auditory Cortex** | Low‑level sound processing | Acoustic similarity only |
| **Premotor Cortex** | Speech planning / articulatory code | Production similarity |

**Strategy**:

- Weight **TPJ** and **Wernicke’s** more heavily when judging **meaning preservation** (Scores 2–3–4).
- Use **auditory** and **premotor** regions as **supportive** signals for **form** and fluency (distinguishing 3 vs 4).

### 6.3 Expected Qualitative Patterns

| Scenario | Qualitative Pattern in Brain‑State Similarity | Expected Score |
| :--- | :--- | :--- |
| Perfect imitation | High similarity in auditory + semantic areas | 4 |
| Meaning correct, grammar wrong | High in semantic areas, reduced in production | 3 |
| Partial meaning | Moderate similarity in semantic areas | 2 |
| Wrong meaning | Low similarity, pattern mismatch | 1 or 0 |
| No response / unrelated | Near‑zero similarity | 0 |

---

## 7. Implementation Phases

### Phase 1: Exploratory Analysis (Current)

- [x] Load audio files and examine waveforms/spectrograms.
- [ ] Run TRIBE v2 on all prompt and response audio.
- [ ] Visualize predicted cortical activation patterns for selected items.
- [ ] Compute simple similarity scores between prompt/response pairs.

### Phase 2: Segmentation

- [ ] Segment the continuous audio into aligned **prompt/response** chunks (30 per participant).
- [ ] Manually verify several segment boundaries to ensure correctness.
- [ ] Generate TRIBE v2 predictions for each segment.

### Phase 3: Validation

- [ ] For each of the 120 items, compute similarity between prompt and response predictions.
- [ ] Correlate similarity scores with existing human/LLM scores (0–4).
- [ ] Explore region‑specific and global similarity metrics.
- [ ] Calibrate practical thresholds for mapping similarity → 0–4 scores.

### Phase 4: Classifier / Mapping Refinement

- [ ] Use similarity features (global + regional) as input to a simple model (e.g., logistic/ordinal regression).
- [ ] Evaluate agreement with human scores (e.g., accuracy, Spearman/Pearson correlations).
- [ ] Document failure modes (where brain‑state similarity and text‑based scores disagree).

---

## 8. Research Questions

### Primary Question

Does TRIBE v2 brain‑state similarity between native speaker prompts and student responses correlate with human‑evaluated EIT scores?

### Secondary Questions

1. **Which brain regions are most predictive of EIT accuracy?**
    - Hypothesis: High‑level semantic regions (e.g., TPJ) are more predictive than purely acoustic regions.
2. **Does the similarity threshold vary by proficiency level?**
    - Hypothesis: Higher proficiency learners show higher similarity scores for correct items and a clearer separation between correct/incorrect responses.
3. **Can specific phonetic or grammatical error patterns be inferred from region‑wise similarity differences?**
    - Hypothesis: Some error types preferentially affect auditory vs. frontal language regions.
4. **Does adding text to the audio input improve brain‑state similarity scoring?**
    - Hypothesis: Providing both audio and the text transcript of the prompt/response to TRIBE v2 (audio + text) yields more robust semantic representations than audio alone, improving discrimination between Score 2 vs 3 vs 4.

---

## 9. Factors That Could Limit Similarity

| Factor | Effect | Mitigation Strategy |
| :--- | :--- | :--- |
| **L2 Proficiency** | Lower proficiency → more effortful, frontal recruitment | Calibrate thresholds per proficiency band |
| **Acoustic Differences** | Different voices, accents, recording quality affect low‑level regions | Emphasize high‑level semantic regions in scoring |
| **Attention** | Inattentive students → weaker alignment to the instructor’s signal | Exclude or down‑weight items with very low scores |
| **Phonetic Errors** | Mispronunciation changes auditory patterns | Let semantic regions dominate for meaning‑based scores |
| **Working Memory / Complexity** | Long or complex sentences increase cognitive load | Stratify analyses by sentence length/complexity |

---

## 10. Glossary

| Term | Definition |
| :--- | :--- |
| **ISC** | Intersubject Correlation; correlation between different people’s brain responses to the same stimulus (on real fMRI/EEG). |
| **EIT** | Elicited Imitation Task; learners repeat heard sentences, scored on meaning. |
| **fMRI** | Functional Magnetic Resonance Imaging; measures BOLD signal as a proxy for neural activity. |
| **TRIBE v2** | Meta AI’s tri‑modal brain encoding foundation model for audio, video, and text. |
| **Wav2Vec‑BERT** | Self‑supervised audio feature extractor used inside TRIBE v2. |
| **fsaverage5** | Standard cortical surface mesh (~20k vertices) used to represent brain predictions. |
| **Neural Synchrony** | Alignment/coupling of brain activity across individuals processing the same stimulus. |
| **Hyperscanning** | Simultaneous recording of brain activity from multiple people. |
| **DMN** | Default Mode Network; high‑level semantic and narrative processing areas. |
| **TPJ** | Temporoparietal Junction; central to semantic integration and social cognition. |

---

## 11. References

1. **TRIBE v2 Paper**: *A foundation model of vision, audition, and language for in‑silico neuroscience* (Meta AI, March 2026).
2. **TRIBE v2 Demo**: https://aidemos.atmeta.com/tribev2/
3. **ISC Methodology**: *Measuring shared responses across subjects using intersubject correlation* (bioRxiv).
4. **ECoG Language**: *Brain activity associated with specific words is mirrored between speaker and listener* (2024).
5. **Theta/Alpha Synchrony**: *Dual‑MEG inter‑brain synchronization during turn‑taking verbal imitation*.
6. **Shared Linguistic Space**: Work on LLM‑based embeddings predicting shared neural representations.
7. **Speaker Independence \& Modality Invariance**: Studies on high‑level conceptual representations across modalities and speakers.

---

## 12. Conclusion

This framework outlines a **neurobiologically motivated, TRIBE v2–based approach** to the AutoEIT problem. By combining:

1. **Neural synchrony findings** (same sentences → similar brain patterns in real data),
2. **TRIBE v2** (a foundation model that predicts brain‑like activity for audio/text), and
3. **Brain‑state similarity metrics** on these predictions,

we can explore whether automated scoring can:

- Operate directly on **raw audio**, without human transcription,
- Focus on **meaning preservation** rather than surface form,
- Remain grounded in existing neuroscience, and
- Potentially generalize to other languages and datasets.

This is explicitly an **exploratory hypothesis**, not a solved method. The next step is empirical: run TRIBE v2 on the EIT audio, compute similarity measures, and see how well they align with the human and LLM‑as‑judge scores you already produced.

<div align="center">⁂</div>

[^1]: *TRIBE v2 Technical Report: A foundation model of vision, audition, and language for in‑silico neuroscience.* (Meta AI, 2026).
