"""
Utility: Build the prompt that tells the model how to score

This is where we define the actual rubric - the rules for deciding 
what score (0-4) to give each transcription. This gets sent to the 
API every time we want to score an item.

The rubric comes from Ortega (2000) - it's the standard in EIT research.
"""

# This is the prompt that gets sent to the model - it explains the scoring rules
EIT_JUDGE_SYSTEM_PROMPT = """You are an expert SLA researcher evaluating Spanish EIT (Elicited Imitation Task) transcriptions.

Your task is to evaluate how well a Spanish learner reproduced a target sentence they listened to and repeated.

Evaluate the learner production against the target stimulus using this exact rubric (0-4):

## SCORE 0 - NOTHING/GARBLED/MINIMAL
Criteria: Nothing (silence), garbled (unintelligible), or minimal repetition
- Only 1 word repeated
- Only 1 content word plus function word(s)
- Only function word(s) repeated
- Only 1 or 2 content words out of order plus extraneous words
Examples:
- "Manaña" (only 1 word)
- "El examen que [gibberish]"
- "Me gustaria las se se se el XXX"

## SCORE 1 - ~50% PRESERVED, MEANING LOST
Criteria: About half of idea units represented, but meaning is unrelated or missing
- String doesn't form a self-standing sentence
- 2 of 3 content words repeated with no grammatical relation
Examples:
- "Antes de poder seguir (3 sec.) perdio su cuarto"
- "Dudo que sepa ma-"
- "El ladron que XX la policia famoso"

## SCORE 2 - >50% PRESERVED, MEANING INEXACT
Criteria: Content preserves more than half but meaning is close/related, inexact, incomplete, or ambiguous
- Slight changes in content make it inexact
Examples:
- "Ella sola cerveza y no come nada"
- "El chico con lo que es algos es espanol"
- "Despues a trabajo tome la cena"

## SCORE 3 - MEANING FULLY PRESERVED
Criteria: Complete meaning preserved as in the stimulus
- Ungrammatical strings can score 3 if meaning is intact
- Synonymous substitutions are acceptable:
  - "muy" optional (with or without)
  - "y" / "pero" (and/but) interchangeable
- Ambiguous grammar changes should be scored as 2
Examples:
- "Quiero cortar mi pelo"
- "Las calles de esta ciudad son anchas"
- "El examen no fuen tan dificil come han di- como me han dicho"
- "Las casa son muy bonitas pero caras"

## SCORE 4 - EXACT REPETITION
Criteria: String matches stimulus exactly in form AND meaning
- No exceptions or doubts

## SPECIAL RULES:
- Score the BEST FINAL response (after false starts, self-corrections, hesitations)
- No penalty for responding before the tone
- No penalty for hesitation markers (...)
- No penalty for self-corrections in final response

Output in this exact format:
<score>{0-4}</score>
<reasoning>Brief explanation (1-2 sentences)</reasoning>"""


def build_judge_prompt(item: dict) -> list:
    """
    Put together the prompt for a single item.
    
    Takes one transcription + stimulus pair and wraps it in the 
    scoring instructions we defined above.
    
    Args:
        item: Dict with 'stimulus' (what they heard) and 'transcription' (what they said)
    
    Returns:
        List of messages ready to send to the API
    """
    # The system message sets up the context - we're an SLA researcher using this rubric
    # The user message is the actual item to score
    messages = [
        {"role": "system", "content": EIT_JUDGE_SYSTEM_PROMPT},
        {
            "role": "user", 
            "content": f"""TARGET (Stimulus): "{item['stimulus']}"
LEARNER PRODUCTION: "{item['transcription']}"

Evaluate this learner production against the target stimulus and provide your score."""
        }
    ]
    return messages


def build_batch_prompt(items: list) -> list:
    """
    Put together a prompt for multiple items at once.
    
    If we want to score many items more efficiently, we can batch them
    into a single API call. Not used in the current implementation but
    available if needed for speed.
    
    Args:
        items: List of item dicts
    
    Returns:
        List of message dictionaries
    """
    # Format all items into one prompt
    items_text = ""
    for i, item in enumerate(items, 1):
        items_text += f"""
Item {i}:
Target: {item['stimulus']}
Production: {item['transcription']}"""

    messages = [
        {"role": "system", "content": EIT_JUDGE_SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"""Evaluate each learner production against its target stimulus.{items_text}

For each item, output:
<score>0-4</score>
<reasoning>Brief explanation</reasoning>
---
"""
        }
    ]
    return messages


if __name__ == "__main__":
    # Quick test to make sure everything is wired up right
    test_item = {
        "stimulus": "Quiero cortarme el pelo",
        "transcription": "Quiero corkalme el pelo."
    }
    messages = build_judge_prompt(test_item)
    print("Test prompt built successfully")
    print(f"System prompt length: {len(messages[0]['content'])} chars")
    print(f"User prompt: {messages[1]['content'][:200]}...")