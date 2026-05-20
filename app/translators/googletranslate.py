from googleapiclient.discovery import build


class GoogleTranslate:
    def __init__(self, api_key: str) -> None:
        self.service = build("translate", "v2", developerKey=api_key)

    def translate(self, text: list[str]) -> list[str]:
        try:
            response = self.service.translations().list(source="ja", target="en", format="text", q=text).execute()
            return [result["translatedText"] for result in response["translations"]]
        except Exception as e:
            print(f"google translate error: {e}")
            return []
