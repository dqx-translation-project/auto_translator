import os
import re
import textwrap
import unicodedata


class Translator:
    service = None
    api_key = None
    glossary = None

    def __init__(self, glossary_lines: list[str] | None = None):
        if Translator.service is None:
            Translator.service = os.environ["TRANSLATE_SERVICE"]
            Translator.api_key = os.environ.get("TRANSLATE_KEY", "")

        if Translator.glossary is None and glossary_lines is not None:
            glossary = {}
            for line in glossary_lines:
                k, v = line.split(",", 1)
                if v == '""':
                    v = ""
                glossary[k] = v
            Translator.glossary = glossary

    def __glossify(self, text: str) -> str:
        if not Translator.glossary:
            return text
        for ja, en in Translator.glossary.items():
            text = text.replace(ja, f" {en} ")
        text = text.replace("  ", " ")
        return text.lstrip()

    def __normalize_text(self, text: str) -> str:
        return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()

    def __swap_placeholder_tags(self, text: str, swap_back: bool = False) -> str:
        if not swap_back:
            text = text.replace("<pc_hiryu>", "<&13_aaaaaaa>")
            text = text.replace("<cs_pchero_hiryu>", "<&13_aaaaaab>")
            text = text.replace("<cs_pchero_race>", "<&8_aaa>")
            text = text.replace("<cs_pchero>", "<&13_aaaaaac>")
            text = text.replace("<kyodai_rel1>", "<&7_aa>")
            text = text.replace("<kyodai_rel2>", "<&7_ab>")
            text = text.replace("<kyodai_rel3>", "<&7_ac>")
            text = text.replace("<pc_hometown>", "<&8_aab>")
            text = text.replace("<pc_race>", "<&8_aac>")
            text = text.replace("<%sM_real_race>", "<&8_aad>")
            text = text.replace("<pc_rel1>", "<&7_ad>")
            text = text.replace("<pc_rel2>", "<&7_ae>")
            text = text.replace("<pc_rel3>", "<&7_af>")
            text = text.replace("<kyodai>", "<&13_aaaaaad>")
            text = text.replace("<pc>", "<&13_aaaaaae>")
            text = text.replace("<client_pcname>", "<&13_aaaaaaf>")
            text = text.replace("<heart>", "<&2a>")
            text = text.replace("<diamond>", "<&2b>")
            text = text.replace("<spade>", "<&2c>")
            text = text.replace("<clover>", "<&2d>")
            text = text.replace("<r_triangle>", "<&2e>")
            text = text.replace("<l_triangle>", "<&2f>")
            text = text.replace("<half_star>", "<&2g>")
            text = text.replace("<null_star>", "<&2h>")
            text = text.replace("<npc>", "<&13_aaaaaag>")
            text = text.replace("<pc_syokugyo>", "<&13_aaaaaah>")
            text = text.replace("<pc_original>", "<&13_aaaaaai>")
            text = text.replace("<log_pc>", "<&13_aaaaaaj>")
            text = text.replace("<%sM_NAME>", "<&13_aaaaaak>")
            text = text.replace("<%sM_BEFORE_NAME>", "<&13_aaaaaal>")
            text = text.replace("<%sM_OWNER_OTHER>", "<&13_aaaaaam>")
            text = text.replace("<%sM_OWNER>", "<&13_aaaaaan>")
            text = text.replace("<%sM_SAMA>", "<&6_a>")
            text = text.replace("<1st_title>", "<&20_aaaaaaaaaaaaaa>")
            text = text.replace("<2nd_title>", "<&20_aaaaaaaaaaaaab>")
            text = text.replace("<3rd_title>", "<&20_aaaaaaaaaaaaac>")
            text = text.replace("<4th_title>", "<&20_aaaaaaaaaaaaad>")
            text = text.replace("<5th_title>", "<&20_aaaaaaaaaaaaae>")
            text = text.replace("<6th_title>", "<&20_aaaaaaaaaaaaaf>")
            text = text.replace("<7th_title>", "<&20_aaaaaaaaaaaaag>")
        else:
            text = text.replace("<&13_aaaaaaaa>", "<pc_hiryu>")
            text = text.replace("<&13_aaaaaaa>", "<pc_hiryu>")
            text = text.replace("<&13_aaaaaa>", "<pc_hiryu>")
            text = text.replace("<&13_aaaaaaab>", "<cs_pchero_hiryu>")
            text = text.replace("<&13_aaaaaab>", "<cs_pchero_hiryu>")
            text = text.replace("<&13_aaaaab>", "<cs_pchero_hiryu>")
            text = text.replace("<&8_aaa>", "<cs_pchero_race>")
            text = text.replace("<&13_aaaaaaac>", "<cs_pchero>")
            text = text.replace("<&13_aaaaaac>", "<cs_pchero>")
            text = text.replace("<&13_aaaaac>", "<cs_pchero>")
            text = text.replace("<&7_aa>", "<kyodai_rel1>")
            text = text.replace("<&7_ab>", "<kyodai_rel2>")
            text = text.replace("<&7_ac>", "<kyodai_rel3>")
            text = text.replace("<&8_aab>", "<pc_hometown>")
            text = text.replace("<&8_aac>", "<pc_race>")
            text = text.replace("<&8_aad>", "<%sM_real_race>")
            text = text.replace("<&7_ad>", "<pc_rel1>")
            text = text.replace("<&7_ae>", "<pc_rel2>")
            text = text.replace("<&7_af>", "<pc_rel3>")
            text = text.replace("<&13_aaaaaaad>", "<kyodai>")
            text = text.replace("<&13_aaaaaad>", "<kyodai>")
            text = text.replace("<&13_aaaaad>", "<kyodai>")
            text = text.replace("<&13_aaaaaaae>", "<pc>")
            text = text.replace("<&13_aaaaaae>", "<pc>")
            text = text.replace("<&13_aaaaae>", "<pc>")
            text = text.replace("<&13_aaaaaaaf>", "<client_pcname>")
            text = text.replace("<&13_aaaaaaf>", "<client_pcname>")
            text = text.replace("<&13_aaaaaf>", "<client_pcname>")
            text = text.replace("<&2a>", "<heart>")
            text = text.replace("<&2b>", "<diamond>")
            text = text.replace("<&2c>", "<spade>")
            text = text.replace("<&2d>", "<clover>")
            text = text.replace("<&2e>", "<r_triangle>")
            text = text.replace("<&2f>", "<l_triangle>")
            text = text.replace("<&2g>", "<half_star>")
            text = text.replace("<&2h>", "<null_star>")
            text = text.replace("<&13_aaaaaaag>", "<npc>")
            text = text.replace("<&13_aaaaaag>", "<npc>")
            text = text.replace("<&13_aaaaag>", "<npc>")
            text = text.replace("<&13_aaaaaaah>", "<pc_syokugyo>")
            text = text.replace("<&13_aaaaaah>", "<pc_syokugyo>")
            text = text.replace("<&13_aaaaah>", "<pc_syokugyo>")
            text = text.replace("<&13_aaaaaaai>", "<pc_original>")
            text = text.replace("<&13_aaaaaai>", "<pc_original>")
            text = text.replace("<&13_aaaaai>", "<pc_original>")
            text = text.replace("<&13_aaaaaaaj>", "<log_pc>")
            text = text.replace("<&13_aaaaaaj>", "<log_pc>")
            text = text.replace("<&13_aaaaaj>", "<log_pc>")
            text = text.replace("<&13_aaaaaaak>", "<%sM_NAME>")
            text = text.replace("<&13_aaaaaak>", "<%sM_NAME>")
            text = text.replace("<&13_aaaaak>", "<%sM_NAME>")
            text = text.replace("<&13_aaaaaaal>", "<%sM_BEFORE_NAME>")
            text = text.replace("<&13_aaaaaal>", "<%sM_BEFORE_NAME>")
            text = text.replace("<&13_aaaaal>", "<%sM_BEFORE_NAME>")
            text = text.replace("<&13_aaaaaaam>", "<%sM_OWNER_OTHER>")
            text = text.replace("<&13_aaaaaam>", "<%sM_OWNER_OTHER>")
            text = text.replace("<&13_aaaaam>", "<%sM_OWNER_OTHER>")
            text = text.replace("<&13_aaaaaaan>", "<%sM_OWNER>")
            text = text.replace("<&13_aaaaaan>", "<%sM_OWNER>")
            text = text.replace("<&13_aaaaan>", "<%sM_OWNER>")
            text = text.replace("<&6_a>", "<%sM_SAMA>")
            text = text.replace("<&20_aaaaaaaaaaaaaaa>", "<1st_title>")
            text = text.replace("<&20_aaaaaaaaaaaaaa>", "<1st_title>")
            text = text.replace("<&20_aaaaaaaaaaaaa>", "<1st_title>")
            text = text.replace("<&20_aaaaaaaaaaaaaab>", "<2nd_title>")
            text = text.replace("<&20_aaaaaaaaaaaaab>", "<2nd_title>")
            text = text.replace("<&20_aaaaaaaaaaaab>", "<2nd_title>")
            text = text.replace("<&20_aaaaaaaaaaaaaac>", "<3rd_title>")
            text = text.replace("<&20_aaaaaaaaaaaaac>", "<3rd_title>")
            text = text.replace("<&20_aaaaaaaaaaaac>", "<3rd_title>")
            text = text.replace("<&20_aaaaaaaaaaaaaad>", "<4th_title>")
            text = text.replace("<&20_aaaaaaaaaaaaad>", "<4th_title>")
            text = text.replace("<&20_aaaaaaaaaaaad>", "<4th_title>")
            text = text.replace("<&20_aaaaaaaaaaaaaae>", "<5th_title>")
            text = text.replace("<&20_aaaaaaaaaaaaae>", "<5th_title>")
            text = text.replace("<&20_aaaaaaaaaaaae>", "<5th_title>")
            text = text.replace("<&20_aaaaaaaaaaaaaaf>", "<6th_title>")
            text = text.replace("<&20_aaaaaaaaaaaaaf>", "<6th_title>")
            text = text.replace("<&20_aaaaaaaaaaaaf>", "<6th_title>")
            text = text.replace("<&20_aaaaaaaaaaaaaag>", "<7th_title>")
            text = text.replace("<&20_aaaaaaaaaaaaag>", "<7th_title>")
            text = text.replace("<&20_aaaaaaaaaaaag>", "<7th_title>")
        return text

    def __wrap_text(self, text: str, width: int, max_lines=None) -> str:
        return textwrap.fill(text, width=width, max_lines=max_lines, replace_whitespace=False)

    def __add_line_endings(self, text: str) -> str:
        count_list = [i for i in range(3, 500, 4)]
        split_text = text.split("\n")
        try:
            for i in count_list:
                _ = split_text[i]
                split_text.insert(i, "<br>")
        except IndexError:
            split_text = [x for x in split_text if x]
            return "\n".join(split_text)

    def __api_translate(self, text: list) -> list:
        for i, phrase in enumerate(text):
            text[i] = self.__glossify(phrase)

        service = Translator.service
        api_key = Translator.api_key

        if service == "deepl":
            from translators.deepl import DeepLTranslate
            return DeepLTranslate(api_key).translate(text)

        elif service == "google":
            from translators.googletranslate import GoogleTranslate
            return GoogleTranslate(api_key).translate(text)

        elif service == "googlefree":
            from translators.googletranslatefree import GoogleTranslateFree
            return GoogleTranslateFree().translate(text)

        elif service == "googletranslatepa":
            from translators.googletranslatepa import GoogleTranslatePa
            return GoogleTranslatePa().translate(text)

        elif service == "chatgpt":
            from translators.chatgpt import ChatGPTTranslate
            return ChatGPTTranslate(api_key).translate(text)

        elif service == "ollama":
            from translators.ollama import OllamaTranslate
            return OllamaTranslate().translate(text)

        elif service == "yandex":
            from translators.yandex import YandexTranslate
            return YandexTranslate().translate(text)

        elif service == "libretranslate":
            from translators.libretranslate import LibreTranslate
            return LibreTranslate(api_key).translate(text)

        return []

    def translate(self, text: str, wrap_width: int = 46, max_lines=None, add_brs: bool = True) -> str:
        output = text.replace("<br>", "　")

        alignments = ["<center>", "<right>", "<left>"]
        for alignment in alignments:
            output = output.replace(alignment, "")

        ellipses = [
            "…………………………………………",
            "………………………………………",
            "……………………………………",
            "…………………………………",
            "………………………………",
            "……………………………",
            "…………………………",
            "………………………",
            "……………………",
            "…………………",
            "………………",
            "……………",
            "…………",
            "………",
            "……",
        ]
        for ellipse in ellipses:
            output = output.replace(ellipse, "…")

        oddities = ["「", "～", "♪"]
        for oddity in oddities:
            output = output.replace(oddity, "")

        output = output.replace("…。", ".")
        output = output.replace("。", ".")
        output = output.replace("\n　", "\n")

        name_tags = ["<pc>", "<cs_pchero>", "<kyodai>"]
        honorifics = ["さま", "君", "どの", "ちゃん", "くん", "様", "さーん", "殿", "さん"]
        for tag in name_tags:
            for honorific in honorifics:
                output = output.replace(f"{tag}{honorific}", tag)

        output = re.sub(r"<color_(\w+)>", r"<&color_\1>", output)
        output = self.__swap_placeholder_tags(output)
        output = self.__glossify(output)

        pristine_str = output

        tag_re = re.compile("(<[^%&]*?>)")
        select_re = re.compile(r"(<select.*>)")
        str_split = [x for x in re.split(tag_re, output) if x]

        count = 0
        str_attrs = {}

        for string in str_split:
            if not re.match(tag_re, string):
                if string == "\n":
                    continue

                pristine_str = pristine_str.replace(string, f"<replace_me_index_{count}>")

                if string.startswith("\n"):
                    lookback = str_split.index(string) - 1
                    if re.match(select_re, str_split[lookback]):
                        str_attrs[count] = {
                            "text": string,
                            "is_list": True,
                            "prepend_newline": False,
                            "append_newline": False,
                        }
                        count += 1
                        continue

                append_newline = string.endswith("\n")
                prepend_newline = string.startswith("\n")

                string = string.replace("\n", "")
                string = string.strip()

                str_attrs[count] = {
                    "text": string,
                    "is_list": False,
                    "prepend_newline": prepend_newline,
                    "append_newline": append_newline,
                }

                count += 1

        to_translate = []
        for i in str_attrs:
            if not str_attrs[i]["is_list"]:
                to_translate.append(str_attrs[i]["text"])
            else:
                for line in str_attrs[i]["text"].splitlines():
                    if line:
                        to_translate.append(line)

        translated_list = self.__api_translate(text=to_translate)

        if not translated_list or len(translated_list) != len(to_translate):
            print(f"{Translator.service} translation failed.")
            return ""

        for count, i in enumerate(translated_list):
            if not str_attrs[count]["is_list"]:
                str_attrs[count]["text"] = i
            else:
                joined_list = "\n".join(translated_list[count:])
                str_attrs[count]["text"] = joined_list + "\n"
                break

        for count in range(len(str_attrs)):
            str_text = str_attrs[count]["text"]
            str_text = str_text.replace("　 ", " ")
            str_text = str_text.replace(" 　", " ")
            str_text = str_text.replace("　", " ")
            str_text = str_text.replace("  ", " ")
            str_text = str_text.replace("..................", "...")
            str_text = str_text.replace("...............", "...")
            str_text = str_text.replace("............", "...")
            str_text = str_text.replace(".........", "...")
            str_text = str_text.replace("......", "...")
            str_text = str_text.replace("....", "...")
            str_text = str_text.replace("’", "'")
            updated_str = str_text.replace("—", "--")
            updated_str = self.__normalize_text(updated_str)

            if str_attrs[count]["is_list"]:
                updated_str = self.__swap_placeholder_tags(updated_str, swap_back=True)
                updated_str = re.sub(r"<&color_(\w+)>", r"<color_\1>", updated_str)
                updated_str = re.sub(r"(?<![<])&color_(\w+)>", r"<color_\1>", updated_str)
                updated_str = updated_str.replace("\n ", "\n")
                updated_str = updated_str.replace("\n　", "\n")
                pristine_str = pristine_str.replace(f"<replace_me_index_{count}>", updated_str)
            else:
                updated_str = self.__wrap_text(updated_str, width=wrap_width, max_lines=max_lines)
                updated_str = self.__swap_placeholder_tags(updated_str, swap_back=True)
                updated_str = re.sub(r"<&color_(\w+)>", r"<color_\1>", updated_str)
                updated_str = re.sub(r"(?<![<])&color_(\w+)>", r"<color_\1>", updated_str)

                if add_brs:
                    updated_str = self.__add_line_endings(updated_str)
                if str_attrs[count]["prepend_newline"]:
                    updated_str = "\n" + updated_str
                if str_attrs[count]["append_newline"]:
                    updated_str += "\n"

                voice_re = re.compile("<voice.*>")
                if re.search(voice_re, pristine_str) and "IEV_GS" not in pristine_str:
                    tag_list = re.findall(tag_re, pristine_str)
                    cur_index = tag_list.index(f"<replace_me_index_{count}>")
                    if len(tag_list) - 1 != cur_index:
                        lookback_index = cur_index - 1
                        if lookback_index > -1 and re.match(voice_re, tag_list[lookback_index]):
                            if not updated_str.endswith("<br>"):
                                updated_str += "<br>\n"

                pristine_str = pristine_str.replace(f"<replace_me_index_{count}>", updated_str)

        return pristine_str
