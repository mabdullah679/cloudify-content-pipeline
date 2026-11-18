CLOUDIFY STUDIO CONTENT PIPELINE (plain-language version)

What it is
Three small scripts that help make a short vertical video. One asks fal.ai to make video clips. One asks ElevenLabs to read a script aloud. One uses ffmpeg on your own computer to join the clips, lay the voice over them and burn in subtitles. Claude Code is the one that runs them. Posting the finished video to Instagram, Facebook and YouTube is done separately through a service called Zernio, connected inside Claude Code. No code in this repo talks to Zernio.

What is not on your computer
Making the clips (fal.ai), making the voice (ElevenLabs) and posting (Zernio) all happen on other companies' servers and need your accounts. Only the final edit is local.

What you need
Python 3 with the "requests" package, ffmpeg, a fal.ai key and an ElevenLabs key. No server, database or Docker.

How to run it
1. Copy .env.example to .env and put your two keys in. The .env file is ignored by git so it is not uploaded.
2. Load the keys into your terminal: set -a; source .env; set +a
3. Fill in CLOUDIFY_FACTS.md. Right now it is an empty template, every field says TODO. Do not script videos until it is real.
4. Make clips, named clip_01.mp4, clip_02.mp4 and so on: python3 generate_video.py --prompt "..." --duration 5 --out clip_01.mp4 (duration is 5 or 10).
5. Make the voice: python3 generate_voiceover.py --text "..." --out narration.mp3
6. Write or obtain your own subtitle file (.srt), then: ./edit.sh <clips folder> narration.mp3 captions.srt final.mp4
7. Post it using the Zernio connector in Claude Code. This is manual.

If something is missing
If a key is not set, the generator stops right away with a message and spends nothing. If edit.sh does not get all 4 inputs it prints how to use it and stops.

What each script does
generate_video.py makes one vertical 9:16 clip. generate_voiceover.py makes one mp3 (you can pick another voice with --voice-id). edit.sh joins the clips in name order, swaps the sound for the narration (the result is as long as the shorter of the two) and burns in the subtitles.

Tests
There are none. The generators cost real money, so they are never run automatically. Automatic checks on each pull request cover only: Python syntax, shell script lint, and a scan of new commits for leaked passwords or keys. They do not prove the generators or ffmpeg work.

Files
generate_video.py, generate_voiceover.py, edit.sh, CLOUDIFY_FACTS.md (empty template), .env.example (the two keys), CLAUDE.md (notes for Claude Code), .github/workflows/ci.yml (automatic checks).

Why it is built this way
Kling can only make 5 or 10 second clips, so a 20 to 30 second video needs several clips joined. All claims in videos must come from one facts file so nothing is invented. The cost estimate of about 0.75 to 1.25 USD per video is the owner's guess, not measured here.

Important security note
An old commit in this public repo contains a .env file with three real API keys (fal.ai, ElevenLabs, Zernio). The file was later deleted, but it is still in the history that anyone can read. Those keys should be treated as exposed and replaced with new ones.
