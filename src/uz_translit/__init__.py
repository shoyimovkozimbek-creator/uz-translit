"""uz-translit: Uzbek Cyrillic <-> Latin conversion and passport-style romanisation.

Three public functions:

* ``cyr_to_lat(text)``      Uzbek Cyrillic -> official Uzbek Latin (1995 alphabet).
* ``normalize_latin(text)`` unify the many apostrophe variants in Uzbek Latin text.
* ``to_passport(text)``     any Uzbek text (Cyrillic or Latin) -> the upper-case
                            romanised form used in passports and visa forms
                            (e.g. "Qodirova" -> "KODIROVA", "Xo'jayev" -> "KHOJAYEV").
"""

from __future__ import annotations

import re

__all__ = ["cyr_to_lat", "normalize_latin", "to_passport", "__version__"]
__version__ = "0.1.0"

# Official Uzbek Latin uses U+02BB (modifier letter turned comma) after o/g
# and U+02BC (modifier letter apostrophe) for the glottal stop (tutuq belgisi).
OKINA = "ʻ"   # oʻ gʻ
TUTUQ = "ʼ"   # maʼno

# Every character people actually type in place of the two marks above.
_APOSTROPHES = "'`‘’ʻʼ´ʹ`"
_APOS_CLASS = "[" + re.escape(_APOSTROPHES) + "]"

_VOWELS_CYR = set("аеёиоуэюяўАЕЁИОУЭЮЯЎ")

# Uzbek Cyrillic -> Latin, lower-case keys. "е" and "ц" are context dependent
# and handled in cyr_to_lat().
_CYR_LAT = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "ё": "yo", "ж": "j",
    "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m", "н": "n",
    "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u", "ф": "f",
    "х": "x", "ч": "ch", "ш": "sh", "щ": "sh", "ъ": TUTUQ, "ы": "i", "ь": "",
    "э": "e", "ю": "yu", "я": "ya", "ў": "o" + OKINA, "қ": "q",
    "ғ": "g" + OKINA, "ҳ": "h",
}


def _apply_case(src: str, out: str, next_char: str, prev_char: str) -> str:
    """Give a (possibly multi-letter) Latin replacement the case of its source letter."""
    if not out or not src.isupper():
        return out
    # Inside an ALL-CAPS word every letter of a digraph is upper-case.
    if len(out) > 1 and (next_char.isupper() or (not next_char.isalpha() and prev_char.isupper())):
        return out.upper()
    return out[0].upper() + out[1:]


def cyr_to_lat(text: str) -> str:
    """Convert Uzbek Cyrillic text to the official Uzbek Latin alphabet.

    Characters that are not Uzbek Cyrillic (digits, punctuation, Latin) are kept.
    """
    result = []
    n = len(text)
    for i, ch in enumerate(text):
        low = ch.lower()
        prev = text[i - 1] if i > 0 else ""
        nxt = text[i + 1] if i + 1 < n else ""
        word_start = not prev.isalpha()

        if low == "е":
            # "ye" at the start of a word and after a vowel or a hard/soft sign.
            if word_start or prev in _VOWELS_CYR or prev.lower() in "ъь":
                out = "ye"
            else:
                out = "e"
        elif low == "ц":
            # "s" after a consonant or at the start of a word in Uzbek words
            # (sirk, sement), "ts" between vowels (militsiya).
            out = "ts" if prev in _VOWELS_CYR else "s"
        elif low in _CYR_LAT:
            out = _CYR_LAT[low]
        else:
            result.append(ch)
            continue
        result.append(_apply_case(ch, out, nxt, prev))
    return "".join(result)


def normalize_latin(text: str) -> str:
    """Unify apostrophe variants in Uzbek Latin text.

    ``o'``, ``o`` ``, ``o’``, ``oʼ`` ... become ``oʻ`` (and the same for ``g``);
    any other apostrophe after a letter becomes the tutuq sign ``ʼ``.
    """
    def fix(m: re.Match) -> str:
        letter = m.group(1)
        return letter + (OKINA if letter in "OoGg" else TUTUQ)

    return re.sub(r"(\w)" + _APOS_CLASS, fix, text)


def _is_cyrillic(text: str) -> bool:
    return any("Ѐ" <= c <= "ӿ" for c in text)


def to_passport(text: str) -> str:
    """Romanise Uzbek text the way it is written in passports and visa forms.

    Accepts Cyrillic or Latin input. Rules:

    * ``oʻ`` -> ``O``, ``gʻ`` -> ``G``; the tutuq sign ``ʼ`` is dropped
    * ``q`` -> ``K``  (Qodirova -> KODIROVA, Qoʻshtepa -> KOSHTEPA)
    * ``x`` -> ``KH`` (Xoʻjayev -> KHOJAYEV), ``h`` stays ``H``
    * everything is upper-case

    Always prefer the spelling already printed in the person's passport:
    this function is for names and places that have no official romanisation yet.
    """
    if _is_cyrillic(text):
        text = cyr_to_lat(text)
    text = normalize_latin(text)
    text = text.replace(OKINA, "").replace(TUTUQ, "")
    text = text.upper()
    text = text.replace("Q", "K").replace("X", "KH")
    return text
