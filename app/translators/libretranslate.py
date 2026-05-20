import os
import requests


class LibreTranslate:
    def __init__(self, api_key: str = "") -> None:
        base = os.environ.get("LIBRETRANSLATE_URL", "https://libretranslate.com").rstrip("/")
        self.url = f"{base}/translate"
        self.api_key = api_key

    def translate(self, text: list[str]) -> list[str]:
        try:
            results = []
            for phrase in text:
                payload: dict = {
                    "q": phrase,
                    "source": "ja",
                    "target": "en",
                    "format": "text",
                }
                if self.api_key:
                    payload["api_key"] = self.api_key
                response = requests.post(self.url, data=payload, timeout=30)
                response.raise_for_status()
                results.append(response.json().get("translatedText", ""))
            return results
        except Exception as e:
            print(f"libretranslate error: {e}")
            return []
