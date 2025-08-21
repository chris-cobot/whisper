#!/usr/bin/env python3
"""
VTT to JSON Converter for Human Annotation Fixes

This script reads a WebVTT file with human edits and creates a simplified JSON file
that preserves the essential transcription data (start, end, text) while dropping
the detailed word-level timing and other whisper-specific metadata.

Usage:
    python vtt_to_json_converter.py episode_000000.vtt [--language en] [--output episode_000000_human_fixed.json]
    
Output:
    Creates a human-fixed JSON file with the updated data
"""

import re
import json
import sys
import os
from typing import List, Dict, Any
import tyro

def parse_vtt_timestamp(timestamp: str) -> float:
    """Convert VTT timestamp format (HH:MM:SS.mmm or MM:SS.mmm) to seconds"""
    # Handle both HH:MM:SS.mmm and MM:SS.mmm formats
    parts = timestamp.split(':')
    
    if len(parts) == 3:  # HH:MM:SS.mmm
        hours, minutes, seconds = parts
        return float(hours) * 3600 + float(minutes) * 60 + float(seconds)
    elif len(parts) == 2:  # MM:SS.mmm
        minutes, seconds = parts
        return float(minutes) * 60 + float(seconds)
    else:
        raise ValueError(f"Invalid timestamp format: {timestamp}")


def parse_vtt_file(vtt_path: str) -> List[Dict[str, Any]]:
    """Parse WebVTT file and extract segments"""
    segments = []
    
    with open(vtt_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Split by double newlines to get individual cues
    cues = re.split(r'\n\s*\n', content.strip())
    
    # Skip the WEBVTT header
    cues = [cue for cue in cues if not cue.startswith('WEBVTT') and cue.strip()]
    
    segment_id = 0
    for cue in cues:
        lines = cue.strip().split('\n')
        if len(lines) < 2:
            continue
            
        # Find the timestamp line (contains -->)
        timestamp_line = None
        text_lines = []
        
        for line in lines:
            if '-->' in line:
                timestamp_line = line
            elif line.strip() and not line.strip().isdigit():  # Skip cue numbers
                text_lines.append(line.strip())
        
        if timestamp_line and text_lines:
            # Parse timestamps
            timestamp_match = re.match(r'(\S+)\s+-->\s+(\S+)', timestamp_line.strip())
            if timestamp_match:
                start_time = parse_vtt_timestamp(timestamp_match.group(1))
                end_time = parse_vtt_timestamp(timestamp_match.group(2))
                text = ' '.join(text_lines)
                
                segments.append({
                    'id': segment_id,
                    'start': start_time,
                    'end': end_time,
                    'text': text
                })
                segment_id += 1
    
    return segments


def create_human_fixed_json(vtt_segments: List[Dict[str, Any]], language: str = 'en') -> Dict[str, Any]:
    """Create a human-fixed JSON structure based on VTT segments"""
    
    # Combine all segment texts for the overall text
    combined_text = ' '.join(segment['text'] for segment in vtt_segments)
    
    # Create the new JSON structure
    human_fixed_data = {
        'text': combined_text,
        'segments': [],
        'language': language
    }
    
    # Convert VTT segments to JSON format
    for segment in vtt_segments:
        json_segment = {
            'id': segment['id'],
            'start': segment['start'],
            'end': segment['end'],
            'text': segment['text'],
        }
        human_fixed_data['segments'].append(json_segment)
    
    return human_fixed_data


def main(
    vtt_file: str,
    language: str = "en",
    output_postfix: str = "_human_fixed",
):
    if not os.path.exists(vtt_file):
        print(f"Error: VTT file '{vtt_file}' not found")
        sys.exit(1)
    
    # Generate output filename if not provided
    base_name = os.path.splitext(vtt_file)[0]
    output_file = f"{base_name}{output_postfix}.json"
    
    try:
        # Parse the VTT file
        print(f"Parsing VTT file: {vtt_file}")
        vtt_segments = parse_vtt_file(vtt_file)
        print(f"Found {len(vtt_segments)} segments in VTT file")
        
        # Create human-fixed JSON
        print(f"Creating human-fixed JSON with language: {language}")
        human_fixed_data = create_human_fixed_json(vtt_segments, language)
        
        # Write the output
        print(f"Writing human-fixed JSON: {output_file}")
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(human_fixed_data, file, indent=2, ensure_ascii=False)
        
        print(f"✅ Successfully created {output_file}")
        print(f"📊 Summary:")
        print(f"   - Segments: {len(human_fixed_data['segments'])}")
        print(f"   - Duration: {human_fixed_data['segments'][-1]['end']:.2f} seconds" if human_fixed_data['segments'] else "   - Duration: 0.00 seconds")
        print(f"   - Language: {human_fixed_data['language']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    tyro.cli(main)