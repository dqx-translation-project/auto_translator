import html
import re
import requests


class GoogleTranslateFree:
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.108 Mobile Safari/537.36"  # noqa: E501
    }

    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update(GoogleTranslateFree.headers)

    def __parse_response(self, response: str) -> str:
        match = re.search(r'<div class="result-container">(.*?)</div>', response, re.DOTALL)
        if not match:
            return ""
        return html.unescape(match.group(1).strip())

    def translate(self, text: list[str]) -> list[str]:
        try:
            results = []
            for phrase in text:
                response = self.session.get(f"https://translate.google.com/m?hl=en&sl=ja&tl=en&q={phrase}")
                response.raise_for_status()
                results.append(self.__parse_response(response.text))
            return results
        except Exception as e:
            print(f"google translate free error: {e}")
            return []
