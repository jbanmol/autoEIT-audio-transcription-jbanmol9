"""
Utility: Pull out the score and explanation from the model's response

The API returns a bunch of text, but we really just need two things:
1. The score (a number from 0-4)
2. The explanation (what the model was thinking)

This tries a few different ways to find these in the response, since
the model might format things slightly different each time.
"""

import re
from typing import Optional, Tuple


def parse_judge_response(response_text: str) -> Tuple[Optional[int], Optional[str]]:
    """
    Pull out score and reasoning from the model's output.
    
    The model is supposed to format its response with <score> and <reasoning>
    tags, but sometimes it might do something slightly different. We try
    a few patterns to be robust.
    
    Args:
        response_text: Whatever the model returned to us
    
    Returns:
        Tuple of (the score number, the explanation text)
    """
    # First, look for our preferred format: <score>3</score>
    score_match = re.search(r'<score>(\d)</score>', response_text)
    
    # If that didn't work, maybe they wrote "score: 3" instead
    if not score_match:
        score_match = re.search(r'score[:\s]*(\d)', response_text, re.IGNORECASE)
    
    # Last resort - just find any number 0-4 in the text
    if not score_match:
        score_match = re.search(r'\b([0-4])\b', response_text)
    
    # Convert to an integer if we found something
    score = int(score_match.group(1)) if score_match else None
    
    # Now find the reasoning - look for the reasoning tag
    reasoning_match = re.search(r'<reasoning>(.*?)</reasoning>', response_text, re.DOTALL)
    
    # Maybe they did "reasoning:" instead
    if not reasoning_match:
        reasoning_match = re.search(r'reasoning[:\s]*(.+?)(?:\n\n|\Z)', response_text, re.IGNORECASE | re.DOTALL)
    
    # Get the text and clean it up a bit
    rationale = reasoning_match.group(1).strip() if reasoning_match else None
    
    return score, rationale


def validate_score(score: Optional[int], transcription: str) -> Tuple[int, str]:
    """
    Check for edge cases - things where we know the score should be different.
    
    Sometimes the model might miss something obvious, like an empty transcription.
    We have a few rules to catch these and correct them before we save the results.
    This is kinda like a safety net.
    
    Args:
        score: What the model gave us (might be None if parsing failed)
        transcription: The actual text that was transcribed
    
    Returns:
        Tuple of (validated_score, any note about what we changed)
    """
    # If there's nothing there at all, that's a 0
    if not transcription or transcription.strip() == "":
        return 0, "Empty transcription - scored 0"
    
    # Check for explicit "no response" markers
    if "[no response]" in transcription.lower():
        return 0, "No response - scored 0"
    
    # Unintelligible stuff gets 0 too
    if "[unintelligible]" in transcription.lower() or "xxx" in transcription.lower():
        return 0, "Unintelligible - scored 0"
    
    # If we couldn't even find a score, just return None so we can handle it later
    if score is None:
        return None, "Could not extract score from LLM response"
    
    # Make sure the score is actually in range - sometimes models mess this up
    if score < 0 or score > 4:
        return None, f"Invalid score {score} - not in range 0-4"
    
    return score, ""


def parse_batch_response(response_text: str, num_items: int) -> list:
    """
    Parse a response that contains multiple item scores.
    
    This was meant for batching multiple items in one API call.
    Not currently used but keeping it around in case we want to 
    optimize for speed later.
    
    Args:
        response_text: The full response with multiple scores
        num_items: How many items we expected
    
    Returns:
        List of dicts with 'score' and 'rationale' for each item
    """
    results = []
    
    # Split up the response by item markers
    items = re.split(r'Item \d+:', response_text)
    
    # First element is probably empty or just intro text
    items = items[1:] if items[0].strip() == "" else items
    
    # Parse each one
    for item_text in items[:num_items]:
        score, rationale = parse_judge_response(item_text)
        
        # Validate format
        if score is not None and (score < 0 or score > 4):
            score = None
            rationale = "Invalid score in response"
        
        results.append({
            "score": score,
            "rationale": rationale
        })
    
    return results


if __name__ == "__main__":
    # Quick test to make sure the parsing works
    
    test_responses = [
        """<score>3</score>
<reasoning>The meaning is preserved even though "corkalme" is phonetically incorrect. The learner clearly intended "cortarme".</reasoning>""",
        
        """<score>4</score>
<reasoning>Exact match with stimulus.</reasoning>""",
        
        """<score>0</score>""",
    ]
    
    for resp in test_responses:
        score, rationale = parse_judge_response(resp)
        print(f"Score: {score}, Rationale: {rationale[:50] if rationale else 'None'}...")
        print("---")