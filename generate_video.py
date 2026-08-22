#!/usr/bin/env python3
"""
Generates video clips via fal.ai's Kling 2.6 Pro endpoint.
Kling caps single generations at 5-10s, so a 20-30s short needs multiple
clips stitched together in the edit step (see edit.sh).

Usage:
    python generate_video.py --prompt "screen recording style, clean UI..." --duration 5 --out clip_01.mp4
"""
import os
import sys
import time
import argparse
import requests

FAL_KEY = os.environ.get("FAL_KEY")
if not FAL_KEY:
    sys.exit("FAL_KEY not set. Add it to your .env and export it before running.")

# Kling 2.6 Pro via fal.ai — 1080p, watermark-free, commercial use
MODEL_ENDPOINT = "https://fal.run/fal-ai/kling-video/v2.6/pro/text-to-video"

def generate(prompt: str, duration: int, out_path: str):
    headers = {
        "Authorization": f"Key {FAL_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "prompt": prompt,
        "duration": str(duration),  # "5" or "10"
        "aspect_ratio": "9:16",     # vertical for Reels/Shorts
    }

    print(f"Requesting generation: {prompt[:60]}...")
    resp = requests.post(MODEL_ENDPOINT, headers=headers, json=payload, timeout=120)
    resp.raise_for_status()
    result = resp.json()

    video_url = result.get("video", {}).get("url")
    if not video_url:
        sys.exit(f"No video URL in response: {result}")

    print(f"Downloading from {video_url}")
    video_data = requests.get(video_url, timeout=120)
    video_data.raise_for_status()

    with open(out_path, "wb") as f:
        f.write(video_data.content)
    print(f"Saved: {out_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--duration", type=int, default=5, choices=[5, 10])
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    generate(args.prompt, args.duration, args.out)
