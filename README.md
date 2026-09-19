# MediaLibraries

Media helpers shared by the Studio and other apps. Companion to `Libraries`.

- `Media.py`: ffmpeg and ID3 helpers, cover images, durations, standard video sizes.
- `Services.py`: ElevenLabs voice services (text-to-speech, speech-to-speech, forced/word alignment).

## Requirements

`ffmpeg` (system), and Python packages `elevenlabs`, `ffmpeg-python`, `mutagen`, `Pillow`.

`Services.py` reads the API key from `elevenlabs.txt` in the current working directory. Never commit that file (it is in `.gitignore`).

## Usage

Add the folder to `PYTHONPATH`, next to `Libraries`:

    export PYTHONPATH=/root/WORK/Libraries:/root/WORK/MediaLibraries
