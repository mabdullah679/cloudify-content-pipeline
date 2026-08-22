#!/usr/bin/env python3
"""
Generates narration audio via ElevenLabs text-to-speech.

Usage:
    python generate_voiceover.py --text "Cloudify Studio turns a prompt into..." --out narration.mp3
"""
import os
import sys
import argparse
import requests

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
if not ELEVENLABS_API_KEY:
    sys.exit("ELEVENLABS_API_KEY not set. Add it to your .env and export it before running.")

# Default voice — swap this for a cloned/custom voice ID later if you want
# a consistent "brand voice." "Adam" (pNInz6obpgDQGcFmaJgB) is a solid
# neutral, direct male voice good for founder-style narration.
DEFAULT_VOICE_ID = "pNInz6obpgDQGcFmaJgB"

def generate(text: str, out_path: str, voice_id: str = DEFAULT_VOICE_ID):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
        },
    }

    print(f"Generating narration: {text[:60]}...")
    resp = requests.post(url, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()

    with open(out_path, "wb") as f:
        f.write(resp.content)
    print(f"Saved: {out_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--voice-id", default=DEFAULT_VOICE_ID)
    args = parser.parse_args()
    generate(args.text, args.out, args.voice_id)
