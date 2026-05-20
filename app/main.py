from alive_progress import alive_bar
from dotenv import load_dotenv
from globals import GITHUB_CLARITY_GLOSSARY_URL
from translate import Translator

import deepl
import glob
import json
import os
import random
import requests
import sys


def load_env():
    """Load global environment variables and download our glossary."""
    global DEEPL_KEYS
    global GLOSSARY

    load_dotenv()

    DEEPL_KEYS = [x for x in json.loads(os.environ.get("DEEPL_KEYS", "[]")) if x]
    GLOSSARY = requests.get(GITHUB_CLARITY_GLOSSARY_URL)
    if GLOSSARY.status_code != 200:
        print("Did not get 200 from Github glossary URL.")
        sys.exit(1)
    GLOSSARY = [x for x in GLOSSARY.content.decode().split("\n") if x]

    if not os.environ.get("TRANSLATE_SERVICE"):
        print("TRANSLATE_SERVICE is not set in .env.")
        sys.exit(1)


def get_remaining_limit(api_key: str) -> int:
    """Returns remaining characters for a specified api key."""
    translator = deepl.Translator(api_key)
    usage = translator.get_usage()
    remaining_chars = usage._character.limit - usage._character.count
    return remaining_chars


def get_remaining_keys_all():
    """Parses all keys configured in DEEPL_KEYS and returns the remaining num of characters."""
    for key in DEEPL_KEYS:
        remaining = get_remaining_limit(key)
        print(f"Key {key[0:5]}.. has {remaining} remaining characters.")


def read_file(file: str) -> dict:
    """Returns data from a json file."""
    with open(file, encoding="utf-8") as f:
        data = json.loads(f.read())
    return data


def estimate_characters(data: dict) -> int:
    characters = ""
    for id in data:
        ja = next(iter(data.get(id).keys()))
        en = data[id][ja]
        if not en:
            characters += ja
    return len(characters)


if __name__ == "__main__":
    load_env()

    translator = Translator(glossary_lines=GLOSSARY)

    for file in glob.glob("files/*"):
        if DEEPL_KEYS:
            get_remaining_keys_all()

        data = read_file(file)
        num_entries = len(data)
        estimated_chars = estimate_characters(data)

        print(f"Translating {os.path.basename(file)} with an estimated {estimated_chars} characters needed to be translated.")
        with alive_bar(total=num_entries, title="Translating..", theme="musical", length=20) as bar:
            for id in data:
                bar()
                ja = next(iter(data.get(id).keys()))
                en = data[id][ja]
                if not ja:
                    continue
                if not en:
                    output = translator.translate(ja)
                    data[id][ja] = output
                    with open(file, "wb") as f:
                        f.write(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=False).encode("utf-8"))

        if DEEPL_KEYS:
            get_remaining_keys_all()
