import os
import json
import yaml
from pathlib import Path

def run_whisper_pipeline():
    """
    Executes the baseline ASR inference on the EIT audio files.
    This script is designed to run in a Colab GPU environment using faster-whisper.
    """
    print("Initializing ASR Pipeline...")
    
    # Load configuration
    config_path = Path("config/test1_metadata.yaml")
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found at {config_path}")
        
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
        
    raw_audio_dir = Path("data/raw_audio")
    output_json_dir = Path("outputs/whisper_json")
    output_txt_dir = Path("outputs/whisper_txt")
    
    output_json_dir.mkdir(parents=True, exist_ok=True)
    output_txt_dir.mkdir(parents=True, exist_ok=True)

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("WARNING: faster-whisper not installed. Please run `pip install faster-whisper` before executing.")
        print("In Colab, GPU execution is required for optimal speed.")
        return

    # Load model (large-v3 is recommended for accuracy, using float16 for GPU speed)
    print("Loading faster-whisper model (large-v3)...")
    # Setting device to 'auto' so it works on GPU if available, else CPU
    model = WhisperModel("large-v3", device="auto", compute_type="default")
    
    # Process each file
    for file_meta in config.get("files", []):
        participant_id = file_meta["participant_id"]
        audio_file = file_meta["audio_filename"]
        start_offset = file_meta["start_offset_sec"]
        
        audio_path = raw_audio_dir / audio_file
        
        if not audio_path.exists():
            print(f"Skipping {participant_id}: Audio file {audio_path} not found.")
            continue
            
        print(f"\nProcessing {participant_id}: {audio_file} (Skipping first {start_offset}s)")
        
        # We explicitly set initial_prompt to encourage exact reproduction of words.
        # However, as warned, Whisper is heavily biased to auto-correct ungrammatical Spanish.
        segments, info = model.transcribe(
            str(audio_path),
            language="es",
            condition_on_previous_text=False,
            word_timestamps=True,
            initial_prompt="A continuación, el alumno intentará repetir la oración exactamente, con pausas, errores y falsos comienzos."
        )
        
        print(f"Detected language '{info.language}' with probability {info.language_probability:.2f}")
        
        # Filter segments that occur AFTER our manual start offset
        transcribed_data = []
        raw_text_accumulation = []
        
        for segment in segments:
            # Shift the printed start/end time by subtracting the offset if needed,
            # or keep absolute time. If we pass the full audio into transcribe, the 
            # timestamps are absolute. We'll simply ignore any segments before the offset.
            if segment.start < start_offset:
                continue
                
            seg_dict = {
                "id": segment.id,
                "start": round(segment.start, 2),
                "end": round(segment.end, 2),
                "text": segment.text.strip(),
                "words": [{"word": w.word, "start": w.start, "end": w.end, "probability": w.probability} for w in segment.words]
            }
            transcribed_data.append(seg_dict)
            raw_text_accumulation.append(f"[{segment.start:.2f} - {segment.end:.2f}] {segment.text.strip()}")
            
        # Write JSON
        json_out = output_json_dir / f"{participant_id}_raw.json"
        with open(json_out, "w", encoding="utf-8") as f:
            json.dump({"participant_id": participant_id, "segments": transcribed_data}, f, indent=2, ensure_ascii=False)
            
        # Write TXT
        txt_out = output_txt_dir / f"{participant_id}_raw.txt"
        with open(txt_out, "w", encoding="utf-8") as f:
            f.write("\n".join(raw_text_accumulation))
            
        print(f"Saved outputs for {participant_id}")

if __name__ == "__main__":
    run_whisper_pipeline()
