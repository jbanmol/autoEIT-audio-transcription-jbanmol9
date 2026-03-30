import os
import json
import pandas as pd
from pathlib import Path

def prepare_audit_csv():
    """
    Creates a chronologically ordered draft CSV to facilitate manual review, 
    merging target stimuli with the raw ASR output.
    
    WARNING: THIS DOES NOT GUARANTEE EXACT 30-ITEM ALIGNMENT.
    The item indices are provisional drafts. You MUST manually verify the 
    transcript against the Audacity waveform.
    """
    print("Preparing draft review CSV files...")
    
    import yaml
    config_path = Path("config/test1_metadata.yaml")
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
        
    excel_template = Path("data/working/AutoEIT Sample Audio for Transcribing_WORKING.xlsx")
    if not excel_template.exists():
        raise FileNotFoundError(f"Template not found at {excel_template}")
        
    xl = pd.ExcelFile(excel_template)
    
    json_dir = Path("outputs/whisper_json")
    csv_dir = Path("outputs/review_csv")
    csv_dir.mkdir(parents=True, exist_ok=True)
    
    for file_meta in config.get("files", []):
        participant_id = file_meta["participant_id"]
        sheet_name = file_meta["sheet_name"]
        
        json_path = json_dir / f"{participant_id}_raw.json"
        if not json_path.exists():
            print(f"Skipping {participant_id}: JSON output not found at {json_path}")
            continue
            
        # Load the raw ASR segments
        with open(json_path, "r", encoding="utf-8") as f:
            asr_data = json.load(f)
        segments = asr_data.get("segments", [])
        
        if sheet_name not in xl.sheet_names:
            print(f"Skipping {participant_id}: Sheet {sheet_name} not found in workbook.")
            continue
            
        # Load the target stimuli from Excel
        df_sheet = xl.parse(sheet_name)
        # Expected exact structure: Column A = Sentence (Item #), Column B = Stimulus
        # Some empty rows might exist, dropna specifically on Sentence
        df_sheet = df_sheet.dropna(subset=['Sentence'])
        
        # We only expect 30 items
        target_stimuli = df_sheet['Stimulus'].tolist()[:30]
        
        # Create the CSV rows.
        # Since we don't do complex temporal alignment in this 24hr sprint,
        # we do a naive pairing: 30 items chronologically linked to the first 30 segments.
        # This is strictly a DRAFT matrix. The reviewer will fix drift manually.
        audit_rows = []
        for i in range(30):
            item_number = i + 1
            target_phrase = target_stimuli[i] if i < len(target_stimuli) else ""
            
            # Grab corresponding segment if it exists
            seg_start = ""
            seg_end = ""
            asr_text = ""
            
            if i < len(segments):
                seg = segments[i]
                seg_start = seg["start"]
                seg_end = seg["end"]
                asr_text = seg["text"]
                
            audit_rows.append({
                "participant_id": participant_id,
                "sheet_name": sheet_name,
                "item_number": item_number,
                "stimulus_target": target_phrase,
                "asr_start_time": seg_start,
                "asr_end_time": seg_end,
                "draft_asr_text": asr_text,
                "FINAL_AUDIT_TRANSCRIPTION": "", # BLANK for reviewer
                "notes": ""
            })
            
        # If there are trailing segments (e.g. ASR picked up breathing or background noise at end), 
        # append them as unassigned items so reviewer sees them.
        for j in range(30, len(segments)):
            seg = segments[j]
            audit_rows.append({
                "participant_id": participant_id,
                "sheet_name": sheet_name,
                "item_number": f"UNASSIGNED_{j+1}",
                "stimulus_target": "",
                "asr_start_time": seg["start"],
                "asr_end_time": seg["end"],
                "draft_asr_text": seg["text"],
                "FINAL_AUDIT_TRANSCRIPTION": "",
                "notes": "Extra segment picked up by ASR"
            })
            
        audit_df = pd.DataFrame(audit_rows)
        out_csv = csv_dir / f"{participant_id}_audit.csv"
        audit_df.to_csv(out_csv, index=False)
        print(f"Generated {out_csv} with {len(audit_df)} rows for {participant_id}.")

if __name__ == "__main__":
    prepare_audit_csv()
