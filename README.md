# Cloudify Studio Content Pipeline

Topic in → script + shot list (Claude Code, grounded in CLOUDIFY_FACTS.md) →
video clips (fal.ai/Kling) → narration (ElevenLabs) → edit/captions (ffmpeg) →
publish (Zernio MCP) to Instagram Reels, Facebook Reels, YouTube Shorts.

## One-time setup

1. Fill in `assets/facts/CLOUDIFY_FACTS.md` — every claim in every video traces
   back to this file. Nothing gets scripted that isn't listed here.
2. Copy `.env.example` to `.env`, fill in FAL_KEY and ELEVENLABS_API_KEY.
3. Connect Zernio's MCP server in Claude Code (see below) — this handles
   publishing, no API key needed in .env for that part.
4. `pip install requests --break-system-packages`
5. Confirm `ffmpeg` is installed (`ffmpeg -version`).

## Connecting Zernio MCP

In Claude Code settings, add a custom MCP connector:
    URL: https://mcp.zernio.com/mcp
Sign in via OAuth with your Zernio account. This gives Claude Code direct
tools to publish/schedule across Instagram, Facebook, and YouTube — no
manual API scripting needed for the publish step.

## Daily workflow

Tell Claude Code (in this project): "Today's topic is [X feature/angle]."

Claude Code will:
1. Pull the relevant fact(s) from CLOUDIFY_FACTS.md
2. Do a quick keyword pass (what would someone search to find this?)
3. Write a script (hook in first 2-3s, founder-voice direct-to-camera style,
   15-45s, one feature/problem per video) + shot list + caption + hashtags
4. Call generate_video.py per shot (stitching multiple 5-10s clips as needed)
5. Call generate_voiceover.py for narration
6. Run edit.sh to stitch + caption + finalize
7. Use the Zernio MCP tools to publish/schedule to all three platforms

## Files

- `assets/facts/CLOUDIFY_FACTS.md` — source of truth, edit this first
- `scripts/generate_video.py` — fal.ai/Kling clip generation
- `scripts/generate_voiceover.py` — ElevenLabs narration
- `scripts/edit.sh` — ffmpeg stitch + caption burn-in
- `output/` — finished videos land here before publishing

## Cost per video (budget tier, 1080p)

~$0.75–1.25 in fal.ai credits per 20-30s video (3-5 stitched clips).
ElevenLabs free tier covers narration at this volume.
Zernio: flat monthly per connected account, not per-post.
