#!/bin/bash
# Stitches generated clips, overlays narration, and burns in captions.
# Requires ffmpeg and (for auto-captions) whisper installed.
#
# Usage: ./edit.sh <clips_dir> <narration.mp3> <captions.srt> <output.mp4>

set -e

CLIPS_DIR="$1"
NARRATION="$2"
CAPTIONS="$3"
OUTPUT="$4"

if [ -z "$OUTPUT" ]; then
    echo "Usage: ./edit.sh <clips_dir> <narration.mp3> <captions.srt> <output.mp4>"
    exit 1
fi

WORKDIR=$(mktemp -d)

# 1. Concatenate clips in order (clip_01.mp4, clip_02.mp4, ...)
ls "$CLIPS_DIR"/clip_*.mp4 | sort | sed "s/^/file '/;s/$/'/" > "$WORKDIR/concat_list.txt"
ffmpeg -y -f concat -safe 0 -i "$WORKDIR/concat_list.txt" -c copy "$WORKDIR/stitched.mp4"

# 2. Overlay narration (replaces any generated audio, syncs to video length)
ffmpeg -y -i "$WORKDIR/stitched.mp4" -i "$NARRATION" \
    -c:v copy -map 0:v:0 -map 1:a:0 -shortest "$WORKDIR/with_audio.mp4"

# 3. Burn in captions (word-by-word animated style performs best per 2026 trend data —
# for now this does standard SRT burn-in; swap for ASS format for animated word-pop style)
ffmpeg -y -i "$WORKDIR/with_audio.mp4" \
    -vf "subtitles=$CAPTIONS:force_style='FontName=Arial Bold,FontSize=16,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,BorderStyle=3,Outline=2,Alignment=2,MarginV=80'" \
    -c:a copy "$OUTPUT"

rm -rf "$WORKDIR"
echo "Final video: $OUTPUT"
