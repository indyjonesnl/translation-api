import os
import ollama
from fastapi import FastAPI, HTTPException
from typing import Dict

app = FastAPI(title="Multi-Lang TranslateGemma API")

MODEL = os.getenv("MODEL_NAME", "translategemma:4b")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://host.docker.internal:11434")

# Mapping short codes to full names for the AI
LANG_MAP = {
    "cs": "Czech",
    "da": "Danish",
    "de": "German",
    "en": "English",
    "es": "Spanish",
    "fi": "Finnish",
    "fr": "French",
    "it": "Italian"
    "nl": "Dutch",
    "pl": "Polish",
    "pt": "Portuguese",
    "ru": "Russian",
    "sv": "Swedish",
}

@app.post("/translate")
async def translate_all(request: Dict[str, str]):
    if not request:
        raise HTTPException(status_code=400, detail="JSON body is empty")

    # Extract the first key and value
    key = list(request.keys())[0]
    source_text = request[key]

    results = {}
    client = ollama.Client(host=OLLAMA_HOST)

    try:
        for code, lang_name in LANG_MAP.items():
            # Construct the specific TranslateGemma prompt
            prompt = f"Translate the following text to {lang_name}:\n{source_text}\nTranslation:"

            # Request translation
            response = client.generate(
                model=MODEL,
                prompt=prompt,
                keep_alive="1m" # Keep in VRAM for 1 min during the loop for speed
            )

            # Clean up the response (removing potential whitespace)
            translated_value = response['response'].strip()

            results[code] = {key: translated_value}

        # Final cleanup: force unload from GPU after the loop is done
        client.generate(model=MODEL, keep_alive=0)

        return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))