# Whisper Annotation Tool

This tool allows you to run whisper, and manually edit WebVTT files and convert them back to JSON format for corrected transcriptions. It's designed to be human-friendly while preserving the essential transcription data.

## Overview

The workflow consists of three simple steps:
1. **Download the audio files**, and place them in a newly created audio/ folder in the dataset
2. **Run Whisper**: `./whisper_run_batch.bash <DATASET_NAME>` .  Replace `<DATASET_NAME>` with the actual dataset name.
3. **Edit** the `.vtt` file manually with your corrections.
4. **Run** the converter script `vtt_to_json_converter.py --vtt-file <NAME_OF_THE VTT_FILE.vtt>` (no dependencies on original JSON!)

## Files

- `vtt_to_json_converter.py` - The main conversion script
- `episode_000000.vtt` - WebVTT file (human-editable)
- `episode_000000_human_fixed.json` - Generated corrected JSON file (output)
