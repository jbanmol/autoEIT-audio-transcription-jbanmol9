"""
Step 2: Score each transcription using the Groq API

This is the main workhorse - it takes each of the 120 items, sends it to 
the API with our scoring rubric, and records what comes back.

The API call includes:
- The model we're using (Llama 4 Scout)
- The prompt we built in prompt_builder.py  
- Settings like temperature (low = more consistent results)

We also do a consistency check - scoring some items twice to make sure
the system is reliable and not giving random answers.
"""

import os
import json
import time
import pandas as pd
from pathlib import Path
from typing import Optional, Tuple
import yaml
from utils.prompt_builder import build_judge_prompt
from utils.score_parser import parse_judge_response, validate_score

# Pull in the Groq library - this is what lets us talk to their API
try:
    from groq import Groq
except ImportError:
    print("Installing groq package...")
    import subprocess
    subprocess.check_call(["pip", "install", "groq"])
    from groq import Groq


def get_groq_client() -> Groq:
    """
    Set up the connection to the Groq API.
    
    We need an API key - it's stored in an environment variable.
    This is standard practice to keep secrets out of the code.
    
    Returns:
        A Groq client we can use to make API calls
    """
    api_key = os.environ.get("GROQ_API_KEY")
    
    # If the key isn't set, stop and tell the user what to do
    if not api_key or api_key == "your_groq_api_key_here":
        raise ValueError(
            "GROQ_API_KEY not set. Please set it in .env file or environment variable.\n"
            "Get your free API key at: https://console.groq.com/"
        )
    
    return Groq(api_key=api_key)


def score_single_item(client: Groq, item: dict, model: str, max_retries: int = 3) -> dict:
    """
    Score one transcription by calling the API.
    
    This takes a single item (stimulus + transcription), builds the prompt,
    sends it to the model, and parses the result.
    
    If something goes wrong (network blip, rate limit, etc), we try again
    a few times before giving up.
    
    Args:
        client: The Groq client
        item: Dict with 'stimulus' and 'transcription'
        model: Which model to use (Llama 4 Scout in our case)
        max_retries: How many times to retry if it fails
    
    Returns:
        Dict with the score, rationale, and any error info
    """
    # Build the prompt for this item using our builder function
    messages = build_judge_prompt(item)
    
    # Try to call the API - might fail the first time so we retry
    for attempt in range(max_retries):
        try:
            # Make the actual API call
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.1,  # Low temp = consistent results
                max_tokens=500,  # Enough space for a rationale
                timeout=30       # Don't wait forever
            )
            
            # Get the text response from the model
            response_text = response.choices[0].message.content
            
            # Pull out the score and explanation from the response
            score, rationale = parse_judge_response(response_text)
            
            # Double-check edge cases (empty transcription, etc)
            validated_score, note = validate_score(score, item.get('transcription', ''))
            
            # If we caught an edge case, update our values
            if validated_score is not None:
                score = validated_score
            elif note:
                rationale = note if not rationale else f"{rationale} {note}"
            
            # Success! Return what we got
            return {
                "score": score,
                "rationale": rationale,
                "raw_response": response_text,
                "success": True,
                "error": None
            }
            
        except Exception as e:
            # Something went wrong - wait a bit and try again
            error_msg = str(e)
            print(f"  Attempt {attempt + 1}/{max_retries} failed: {error_msg}")
            
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Wait longer each time (exponential backoff)
                print(f"  Waiting {wait_time}s before retry...")
                time.sleep(wait_time)
    
    # All retries failed - record the failure but don't crash
    return {
        "score": None,
        "rationale": f"Failed after {max_retries} attempts: {error_msg}",
        "raw_response": None,
        "success": False,
        "error": error_msg
    }


def run_consistency_check(client: Groq, items: list, model: str, sample_size: int = 24) -> dict:
    """
    Run a sanity check - score some items twice to verify we're getting consistent results.
    
    This is important because we don't have human scores to compare against.
    Instead, we check that the same input produces the same output - a good
    proxy for reliability.
    
    Args:
        client: Groq client
        items: All items to check
        model: Model name
        sample_size: How many items to test (we use 24 = 20%)
    
    Returns:
        Dict with agreement rate and other metrics
    """
    sample = items[:sample_size]
    print(f"\nRunning consistency check on {sample_size} items...")
    
    # First pass - score everything once
    first_run = []
    for item in sample:
        result = score_single_item(client, item, model)
        first_run.append(result)
        time.sleep(0.5)  # Be nice to the API
    
    # Second pass - score the same items again
    second_run = []
    for item in sample:
        result = score_single_item(client, item, model)
        second_run.append(result)
        time.sleep(0.5)
    
    # Compare the two passes - count how many times they agree
    disagreements = 0
    for i in range(len(sample)):
        if first_run[i]['score'] != second_run[i]['score']:
            disagreements += 1
    
    agreement_rate = (sample_size - disagreements) / sample_size * 100
    
    print(f"  Agreement rate: {agreement_rate:.1f}% ({sample_size - disagreements}/{sample_size})")
    
    return {
        "sample_size": sample_size,
        "agreements": sample_size - disagreements,
        "disagreements": disagreements,
        "agreement_rate": agreement_rate
    }


def score_all_items(items: list, model: str, batch_delay: float = 1.0) -> list:
    """
    Go through all 120 items and score them one by one.
    
    This loops through every item in our dataset, calls the API for each one,
    and collects all the results. We add a small delay between calls to avoid
    hitting rate limits on the free tier.
    
    Args:
        items: List of all items to score (from step 1)
        model: Which model to use
        batch_delay: Seconds to wait between API calls
    
    Returns:
        List of results for each item
    """
    client = get_groq_client()
    
    results = []
    
    print(f"\nScoring {len(items)} items with {model}...")
    
    # Loop through everything
    for i, item in enumerate(items):
        print(f"  Item {i+1}/{len(items)}: {item['participant']} - Item {item['item_number']}")
        
        # Score this one item
        result = score_single_item(client, item, model)
        
        # Add metadata so we know which participant/item this belongs to
        result['participant'] = item['participant']
        result['item_number'] = item['item_number']
        result['stimulus'] = item['stimulus']
        result['transcription'] = item['transcription']
        
        results.append(result)
        
        # Print progress every 10 items
        if (i + 1) % 10 == 0:
            success_count = sum(1 for r in results if r['success'])
            print(f"  Progress: {i+1}/{len(items)} ({success_count} successful)")
        
        # Be gentle with the API - wait 2 seconds between calls
        # Free tier allows 30 per minute, but this is safer
        time.sleep(2)
    
    print(f"\n✅ Scoring complete!")
    
    # Quick summary
    success_count = sum(1 for r in results if r['success'])
    print(f"  Successful: {success_count}/{len(results)}")
    
    return results


def save_results(results: list, output_path: Path):
    """Write the results to a JSON file for safekeeping."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"Results saved to: {output_path}")


def load_items_from_json(json_path: Path) -> list:
    """Load the items we extracted in step 1."""
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    """
    Main entry point - runs the whole scoring pipeline.
    
    1. Load config
    2. Load the items we extracted in step 1
    3. Run consistency check on 20% of items
    4. Score all 120 items
    5. Save results to JSON
    """
    # Load configuration
    config_path = Path(__file__).parent.parent / "config" / "test2_config.yaml"
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    
    # Where to find input and where to save output
    extracted_data_path = Path(__file__).parent.parent / "outputs" / "scores" / "extracted_data.json"
    scores_output_path = Path(__file__).parent.parent / "outputs" / "scores" / "all_scores.json"
    
    # Make sure we have data to work with
    if not extracted_data_path.exists():
        print("Extracted data not found. Running Step 1...")
        exec(open(Path(__file__).parent / "01_extract_data.py").read())
    
    items = load_items_from_json(extracted_data_path)
    print(f"Loaded {len(items)} items for scoring")
    
    # Which model are we using?
    model = config['MODEL']
    print(f"Using model: {model}")
    
    # Run the consistency check first - important validation
    print("\n" + "="*50)
    print("STEP 1: Consistency Check (20% sample)")
    print("="*50)
    
    # Create a client for the check
    try:
        check_client = get_groq_client()
    except ValueError as e:
        print(f"\n❌ Error: {e}")
        print("\nTo fix:")
        print("1. Get a free API key at: https://console.groq.com/")
        print("2. Set GROQ_API_KEY environment variable")
        print("3. Or add to .env file")
        return
    
    # Run the check
    consistency_results = run_consistency_check(
        check_client,
        items, 
        model,
        config['CONSISTENCY_CHECK_SAMPLE_SIZE']
    )
    
    # Now do the main scoring
    print("\n" + "="*50)
    print("STEP 2: Full Scoring")
    print("="*50)
    
    # Create fresh client for main run
    client = get_groq_client()
    results = score_all_items(items, model)
    
    # Save everything
    save_results(results, scores_output_path)
    
    # Print final summary
    print("\n" + "="*50)
    print("SCORING SUMMARY")
    print("="*50)
    
    scores = [r['score'] for r in results if r['score'] is not None]
    if scores:
        print(f"Total scored: {len(scores)}/{len(results)}")
        print(f"Score distribution:")
        for s in range(5):
            count = scores.count(s)
            pct = count / len(scores) * 100
            print(f"  Score {s}: {count} ({pct:.1f}%)")
        print(f"Mean score: {sum(scores)/len(scores):.2f}")
    
    print(f"\nResults saved to: {scores_output_path}")


if __name__ == "__main__":
    main()