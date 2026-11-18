# Cloudify Studio Content Pipeline

Three small scripts that turn a topic into a vertical short video: AI clips, narration, then an ffmpeg edit with burned-in captions. Claude Code drives them; publishing is done separately through the Zernio MCP.

```
topic ──> Claude Code (script + shot list, from CLOUDIFY_FACTS.md)
            ├─> generate_video.py     ──> clip_01.mp4 ...   (fal.ai, Kling 2.6 Pro)   [external, paid]
            ├─> generate_voiceover.py ──> narration.mp3     (ElevenLabs)              [external, paid/free tier]
            └─> edit.sh (ffmpeg)      ──> final.mp4         (local)
final.mp4 ──> Zernio MCP in Claude Code ──> Instagram / Facebook / YouTube            [external, not in this repo]
```

Not local: video generation (fal.ai), narration (ElevenLabs) and publishing (Zernio) are hosted services you must have accounts and keys for. Only the ffmpeg edit runs on your machine. No Zernio call exists in this repo's code.

## Prerequisites
- Python 3 with `requests` (`pip install requests`)
- `ffmpeg` on PATH
- A fal.ai key (`FAL_KEY`) and an ElevenLabs key (`ELEVENLABS_API_KEY`)
- Not needed: Node, Docker, a database, any server.

## Run it
1. `cp .env.example .env`, fill in both keys. `.env` is git-ignored.
2. Load them: `set -a; source .env; set +a` (macOS/Linux).
3. Fill in `CLOUDIFY_FACTS.md`. It is currently an unfilled template (every field is `[TODO]`); nothing should be scripted until it is real.
4. Generate clips (name them `clip_01.mp4`, `clip_02.mp4`, ... so they sort in order):
   `python3 generate_video.py --prompt "..." --duration 5 --out clip_01.mp4`
5. Generate narration: `python3 generate_voiceover.py --text "..." --out narration.mp3`
6. Provide your own `.srt` caption file, then: `./edit.sh <clips_dir> narration.mp3 captions.srt final.mp4`
7. Publish with the Zernio MCP from Claude Code (add the connector at `https://mcp.zernio.com/mcp`, sign in with OAuth). This step is manual and outside the scripts.

If a key is missing, each generator exits immediately with a "not set" message and makes no request. If `edit.sh` is run without 4 arguments it prints its usage and stops.

## What it does
| Action | Result |
|---|---|
| `generate_video.py` with `--duration 5` or `10` | One 9:16 clip saved to `--out` (fal.ai Kling 2.6 Pro) |
| `generate_voiceover.py` | One mp3 saved to `--out`; default voice id is set in the file, override with `--voice-id` |
| `edit.sh` | Concatenates `clip_*.mp4` in sorted order, replaces audio with the narration (cut to the shorter of the two), burns in the `.srt` |

## Tests
There are none. The generators call paid APIs, so they are not run in CI. CI (`.github/workflows/ci.yml`) runs a Python syntax check, `shellcheck --severity=warning`, and a gitleaks scan of the commits in each PR. None of that exercises the generators or ffmpeg.

## Layout
| Path | Role |
|---|---|
| [generate_video.py](generate_video.py) | fal.ai clip generation |
| [generate_voiceover.py](generate_voiceover.py) | ElevenLabs narration |
| [edit.sh](edit.sh) | ffmpeg stitch + captions |
| [CLOUDIFY_FACTS.md](CLOUDIFY_FACTS.md) | claims source of truth (template, unfilled) |
| [.env.example](.env.example) | the two keys the scripts read |
| [CLAUDE.md](CLAUDE.md) | notes for Claude Code sessions, incl. the known key-in-history issue |
| [.github/workflows/ci.yml](.github/workflows/ci.yml) | CI |

## Design notes
- Clips are stitched, not generated long: Kling caps a single generation at 5 or 10 seconds, so a 20-30 s short needs several clips.
- Facts live in one file so a script can be traced to a listed claim rather than invented.
- Cost per video (about 0.75-1.25 USD of fal.ai credit for 3-5 clips) is the owner's estimate, not measured here.
