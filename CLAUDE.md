# CLAUDE.md — cloudify-content-pipeline

Master rules: `~/.claude/CLAUDE.md` (read it; not copied here). This file is repo-specific.

**Public repo.** Nothing in here may contain client names, internal URLs, or credentials.

## What this is
Three small scripts for a short-video workflow: `generate_video.py` (fal.ai Kling clips),
`generate_voiceover.py` (ElevenLabs narration), `edit.sh` (ffmpeg stitch + captions).
`CLOUDIFY_FACTS.md` is the claims source of truth and is still an unfilled template (all `[TODO]`).
Publishing is done by Claude Code through the Zernio MCP, not by any script here.

## Layout
Everything is flat at the repo root. There is no `assets/`, `scripts/` or `output/` directory in git
(`output/` is git-ignored as the place finished media goes).

## Commands (all run on this tree)
- Syntax check: `python3 -m py_compile generate_video.py generate_voiceover.py`
- Shell lint: `shellcheck --severity=warning edit.sh` (the one `info` note, SC2012, is known and left alone)
- Secrets: `gitleaks detect --no-git --redact` (working tree)
- There are no unit tests. Running the generators spends real money on fal.ai / ElevenLabs. Never run them in CI or as a "test".

## Do not
- Commit `.env` (git-ignored; `.env.example` is the template). Never paste keys anywhere.
- Fill `CLOUDIFY_FACTS.md` with guesses: every video claim must trace to it.
- Rewrite history. Old history contains a deleted `.env` (see below). The owner decides on rotation.

## Known issue
Commit `8fb63cc` contains a `.env` with three API keys (fal.ai, ElevenLabs, Zernio). The file was deleted in `b982506`, but it is still in public history. The keys must be treated as compromised and rotated; that is not something this repo can fix.

## CI
`.github/workflows/ci.yml`: syntax check, shellcheck, gitleaks over the PR's commits only (full history would be red until the above is resolved).
