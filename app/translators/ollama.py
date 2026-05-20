import os
import requests


_PROMPT_TEMPLATE = (
    "Translate the following Dragon Quest X dialogue from Japanese to English. "
    'Keep it localized and immersive. Return only the translated text.\n\n"{text}"'
)


class OllamaTranslate:
    def __init__(self, api_key: str = "") -> None:
        self.url = os.environ.get("OLLAMA_URL", "http://localhost:11434").rstrip("/") + "/api/generate"
        self.model = os.environ.get("OLLAMA_MODEL", "llama3")

    def translate(self, text: list[str]) -> list[str]:
        try:
            results = []
            for phrase in text:
                payload = {
                    "model": self.model,
                    "prompt": _PROMPT_TEMPLATE.format(text=phrase),
                    "temperature": 0.1,
                    "stream": False,
                }
                response = requests.post(self.url, json=payload, timeout=60)
                response.raise_for_status()
                translated = response.json().get("response", "").strip().strip('"')
                results.append(translated)
            return results
        except Exception as e:
            print(f"ollama error: {e}")
            return []
