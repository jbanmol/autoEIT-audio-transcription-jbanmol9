"""
Step 1: Pull data out of the Excel file

This reads the Test I output (where we already transcribed the audio) and 
extracts what we need for scoring - the target sentence they heard and 
what they actually said.

Input: Excel with columns for sentence number, stimulus, transcription
Output: JSON file with all 120 items (4 participants x 30 sentences)
"""

import json
import pandas as pd
from pathlib import Path
import yaml

def extract_data():
    """Main function to pull data from Excel into a usable format."""
    
    # Read the config file to know which file to process
    config_path = Path(__file__).parent.parent / "config" / "test2_config.yaml"
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    
    # Figur out where input and output files are
    input_file = Path(__file__).parent.parent / config['INPUT_FILE']
    output_dir = Path(__file__).parent.parent / "outputs" / "scores"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Reading from: {input_file}")
    
    # Open the Excel file - it has one sheet per participant
    xl = pd.ExcelFile(input_file)
    
    all_items = []
    
    # Loop through each participant's sheet
    for participant in config['PARTICIPANTS']:
        if participant not in xl.sheet_names:
            print(f"Warning: Sheet '{participant}' not found, skipping...")
            continue
            
        df = xl.parse(participant)
        
        # Go through each row and pull out the info we need
        for idx, row in df.iterrows():
            sentence_num = row.get('Sentence')
            stimulus = row.get('Stimulus')
            transcription = row.get('Transcription')
            
            # Skip empty rows
            if pd.isna(sentence_num):
                continue
            
            # Clean up the stimulus - remove the difficulty number at the end
            # e.g., "Quiero cortarme el pelo (7)" -> "Quiero cortarme el pelo"
            stimulus_clean = str(stimulus).strip() if pd.notna(stimulus) else ""
            if stimulus_clean and stimulus_clean[-1] == ')':
                space_idx = stimulus_clean.rfind(' ')
                if space_idx > 0:
                    stimulus_clean = stimulus_clean[:space_idx]
            
            # Clean up transcription
            transcription_clean = str(transcription).strip() if pd.notna(transcription) else ""
            
            # Save this item
            item = {
                "participant": participant,
                "item_number": int(sentence_num),
                "stimulus": stimulus_clean,
                "transcription": transcription_clean
            }
            all_items.append(item)
            
        print(f"Extracted {len(df)} items from {participant}")
    
    # Write everything to a JSON file for the next step
    output_file = output_dir / "extracted_data.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_items, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Total items extracted: {len(all_items)}")
    print(f"Saved to: {output_file}")
    
    return all_items

if __name__ == "__main__":
    extract_data()