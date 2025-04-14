# /// script
# dependencies = [
#   "typer",
#   "openai",
#   "pydub",
#   "audioop-lts",
# ]
# ///

import typer
from openai import OpenAI
from pydub import AudioSegment
import os

app = typer.Typer()

MAX_DURATION_SECONDS = 1250  # Maximum allowed duration by the model


def chunk_audio(file_path: str):
    audio = AudioSegment.from_file(file_path)
    chunks = []

    for i in range(0, len(audio), MAX_DURATION_SECONDS * 1000):
        chunk = audio[i:i + MAX_DURATION_SECONDS * 1000]
        chunk_file = f"chunk_{i // 1000}.mp3"
        chunk.export(chunk_file, format="mp3")
        chunks.append(chunk_file)

    return chunks


@app.command()
def transcribe(
    file: str,
    model: str = typer.Option("gpt-4o-transcribe", help="Model to use for transcription."),
    response_format: str = typer.Option("text", help="Output format: text, json, verbose_json, srt, vtt"),
    prompt: str = typer.Option(None, help="Optional prompt to improve transcription.")
):
    """Transcribe an audio file, automatically chunking if necessary."""
    client = OpenAI()
    audio = AudioSegment.from_file(file)

    if len(audio) / 1000 <= MAX_DURATION_SECONDS:
        chunks = [file]
    else:
        typer.echo("Audio too long, splitting into chunks...")
        chunks = chunk_audio(file)

    full_transcription = ""

    for chunk_file in chunks:
        with open(chunk_file, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model=model,
                file=audio_file,
                response_format=response_format,
                prompt=prompt
            )

            chunk_text = transcription if response_format == "text" else transcription.text
            full_transcription += chunk_text + "\n"

        if chunk_file.startswith("chunk_"):
            os.remove(chunk_file)

    typer.echo(full_transcription)


@app.command()
def translate(
    file: str,
    response_format: str = typer.Option("text", help="Output format: text or json")
):
    """Translate an audio file into English."""
    client = OpenAI()

    with open(file, "rb") as audio_file:
        translation = client.audio.translations.create(
            model="whisper-1",
            file=audio_file,
            response_format=response_format
        )

    typer.echo(translation.text if response_format == "text" else translation)


if __name__ == "__main__":
    app()
