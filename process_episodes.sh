#!/bin/bash

# Script to process multiple episodes with VTT to JSON converter
# Usage: ./process_episodes.sh <source_directory>

set -e  # Exit on any error

# Check if source directory is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <source_directory>"
    echo "Example: $0 /path/to/vtt/files"
    exit 1
fi

SOURCE_DIR="$1"

# Check if source directory exists
if [ ! -d "$SOURCE_DIR" ]; then
    echo "Error: Source directory '$SOURCE_DIR' does not exist"
    exit 1
fi

# List of episode numbers to process (modify this list as needed)
# These will be formatted as episode_XXXXXX (6-digit zero-padded)
EPISODE_NUMBERS=(
    0
    1
    2
    5
    9
    10
)

# Optional parameters (modify as needed)

# Track processing results
PROCESSED=0
SKIPPED=0
ERRORS=0

echo "🚀 Starting VTT to JSON conversion process"
echo "📁 Source directory: $SOURCE_DIR"
echo "📋 Episode numbers to process: ${#EPISODE_NUMBERS[@]}"
echo ""

# Change to source directory
cd "$SOURCE_DIR"

# Process each episode
for episode_num in "${EPISODE_NUMBERS[@]}"; do
    # Format episode number with zero-padding (6 digits)
    EPISODE=$(printf "episode_%06d" "$episode_num")
    VTT_FILE="${EPISODE}.vtt"
    
    echo "🔄 Processing: $EPISODE (episode $episode_num)"
    
    # Check if VTT file exists
    if [ ! -f "$VTT_FILE" ]; then
        echo "⚠️  Skipping $EPISODE: VTT file '$VTT_FILE' not found"
        ((SKIPPED++))
        echo ""
        continue
    fi
    
    # Run the converter
    echo "   📥 Input: $VTT_FILE"
    
    if python vtt_to_json_converter.py --vtt-file "$VTT_FILE"; then
        echo "   ✅ Successfully processed $EPISODE"
        ((PROCESSED++))
    else
        echo "   ❌ Error processing $EPISODE"
        ((ERRORS++))
    fi
    
    echo ""
done

# Summary
echo "📊 Processing Summary:"
echo "   ✅ Successfully processed: $PROCESSED"
echo "   ⚠️  Skipped (file not found): $SKIPPED"
echo "   ❌ Errors: $ERRORS"
echo "   📋 Total episodes in list: ${#EPISODE_NUMBERS[@]}"

if [ $ERRORS -eq 0 ]; then
    echo ""
    echo "🎉 All available episodes processed successfully!"
    exit 0
else
    echo ""
    echo "⚠️  Some episodes had errors. Check the output above for details."
    exit 1
fi 