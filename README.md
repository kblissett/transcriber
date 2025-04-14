*This script was largely written by ChatGPT 4.5 with my assistance.*

# Speech-to-Text CLI

A command-line interface (CLI) tool for transcribing and translating audio files using OpenAI's Audio API. It automatically handles long audio files by splitting them into manageable chunks.

## Features

- **Transcription**: Convert audio into text.
- **Translation**: Convert audio from any supported language into English text.
- **Automatic Chunking**: Splits long audio files exceeding the model's maximum duration (1250 seconds).
- **Multiple Output Formats**: Supports `text`, `json`, `verbose_json`, `srt`, and `vtt` formats.

## Installation & Requirements

Ensure you have [uv](https://github.com/astral-sh/uv) installed for automatic dependency management.

Run the script using `uv`:

```bash
uv run transcriber.py transcribe <audio_file_path>
```

Dependencies (handled automatically by `uv`):

- `typer`
- `openai`
- `pydub`
- `audioop-lts`

## Usage

### Transcription

To transcribe an audio file:

```bash
uv run transcriber.py transcribe audio.mp3
```

Additional options:

- `--model`: Model to use (default: `gpt-4o-transcribe`)
- `--response-format`: Output format (`text`, `json`, `verbose_json`, `srt`, `vtt`)
- `--prompt`: Optional prompt to improve accuracy

Example with additional options:

```bash
uv run transcriber.py transcribe audio.mp3 --model whisper-1 --response-format json --prompt "Lecture on AI developments."
```

### Translation

Translate audio content to English:

```bash
uv run transcriber.py translate audio.mp3
```

Specify output format (default is `text`):

```bash
uv run transcriber.py translate audio.mp3 --response-format json
```

## Notes

- Temporary chunk files are cleaned up automatically after processing.
- The script automatically detects and handles long audio files.

## License

This project is licensed under the MIT License.
