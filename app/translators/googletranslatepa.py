import requests


class GoogleTranslatePa:
    _URL = "https://translate.googleapis.com/translate_a/single"

    def __init__(self, api_key: str = "") -> None:
        self.session = requests.Session()

    def translate(self, text: list[str]) -> list[str]:
        try:
            results = []
            for phrase in text:
                response = self.session.get(
                    self._URL,
                    params={"client": "gtx", "sl": "ja", "tl": "en", "dt": "t", "q": phrase},
                )
                response.raise_for_status()
                data = response.json()
                translated = "".join(segment[0] for segment in data[0] if segment[0])
                results.append(translated)
            return results
        except Exception as e:
            print(f"google translate pa error: {e}")
            return []
