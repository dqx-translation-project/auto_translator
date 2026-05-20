import deepl


class DeepLTranslate:
    def __init__(self, api_key: str) -> None:
        deepl.http_client.max_network_retries = 1
        deepl.http_client.min_connection_timeout = 3
        self.translator = deepl.DeepLClient(auth_key=api_key, send_platform_info=False)

    def translate(self, text: list[str]) -> list[str]:
        try:
            response = self.translator.translate_text(
                text=text,
                source_lang="ja",
                target_lang="en-us",
                preserve_formatting=True,
                model_type="prefer_quality_optimized",
                custom_instructions=[
                    "You are an expert translator and cultural localization specialist with deep knowledge of video game localization. Preserve the original tone, humor, personality, and emotional nuances of the dialogue, considering the unique style and atmosphere of Dragon Quest X.",  # noqa: E501
                    "Adapt idioms, cultural references, and wordplay to resonate naturally with native English speakers while maintaining the fantasy RPG context. Avoid the overuse of profanity. Don't use the same word over and over.",  # noqa: E501
                    "Maintain consistency in character voices, terminology, and naming conventions specific to Dragon Quest X throughout the translation.",  # noqa: E501
                    "Avoid literal translations that may lose the original intent or impact, especially for game-specific terms or lore elements. Any text that's returned should only include ASCII character codes 33 through 127.",  # noqa: E501
                    "Ensure the translation flows naturally and reads as if it were originally written in English, while staying true to the game's narrative style.",  # noqa: E501
                    "Consider the context and subtext of the dialogue, including any references to the game's lore, world, or ongoing storylines.",  # noqa: E501
                    "If a word, phrase, or name has been translated in a specific way, maintain that translation consistently unless the context demands otherwise, respecting established localization choices for Dragon Quest X.",  # noqa: E501
                    "Pay attention to formal/informal speech patterns and adjust accordingly for the target language and cultural norms, considering the speaker's role and status within the game world.",  # noqa: E501
                    "Be mindful of character limits or text box constraints that may be present in the game, adapting the translation to fit if necessary.",  # noqa: E501
                    "Preserve any game-specific jargon, spell names, or technical terms according to the official localization guidelines for Dragon Quest X.",  # noqa: E501
                ],
            )
            return [result.text for result in response]
        except Exception as e:
            print(f"deepl error: {e}")
            return []
