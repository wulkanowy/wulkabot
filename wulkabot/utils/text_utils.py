POLISH_DIACRITICS = {
    "Ą": "A",
    "Ć": "C",
    "Ę": "E",
    "Ł": "L",
    "Ń": "N",
    "Ó": "O",
    "Ś": "S",
    "Ź": "Z",
    "Ż": "Z",
    "ą": "a",
    "ć": "c",
    "ę": "e",
    "ł": "l",
    "ń": "n",
    "ó": "o",
    "ś": "s",
    "ź": "z",
    "ż": "z",
}


def remove_diacritics(text: str, /) -> str:
    """
    Replaces Polish diacritics with their ASCII counterparts

    Żółć => Zolc
    Źdźbło => Zdzblo
    """
    for (diacritic, ascii) in POLISH_DIACRITICS.items():
        text = text.replace(diacritic, ascii)

    return text
