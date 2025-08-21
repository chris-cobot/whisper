#!/bin/bash

# Directory containing the input files
INPUT_DIR="./data/sandbox"
DATASET_NAME=$1

# Output directory
OUTPUT_DIR="$HOME/.cache/openpi/ai-demo-coach-practice/pi0_finetuning/datasets/cobot/$DATASET_NAME/audio/"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Model to use
MODEL="medium.en"

# Counter starts at 0
i=0

while true; do
    # Format number with leading zeros (6 digits)
    filename=$(printf "episode_%06d.m4a" "$i")
    filepath="$INPUT_DIR/$filename"

    # Check if the file exists
    if [[ ! -f "$filepath" ]]; then
        echo "No more files found. Stopping."
        break
    fi

    echo "Processing $filepath..."
    whisper "$filepath" --model "$MODEL" --output_dir "$OUTPUT_DIR" --word_timestamps True

    # Increment counter
    ((i++))
done
