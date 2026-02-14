import re


SYMBOL_TO_ORAL_NAME = {
    "~": "tilde",
    "!": "exclamation point",
    "@": "at",
    "#": "hash",
    "$": "dollar sign",
    "%": "percent",
    "^": "caret",
    "&": "and",
    "*": "star",
    "(": "left parenthesis",
    ")": "right parenthesis",
    "_": "underscore",
    "-": "dash",
    "=": "equals",
    "+": "plus",
    "[": "left bracket",
    "{": "left brace",
    "]": "right bracket",
    "}": "right brace",
    ":": "colon",
    ";": "semicolon",
    '"': "double quote",
    "'": "apostrophe",
    "\\": "backslash",
    "|": "pipe",
    "<": "less than",
    ">": "greater than",
    ",": "comma",
    ".": "dot",
    "?": "question mark",
    "/": "slash",
}


_SYMBOL_PATTERN = re.compile("[" + re.escape("".join(SYMBOL_TO_ORAL_NAME.keys())) + "]")


def verbalize_symbols(text: str) -> str:
    """Replace supported symbols with their oral names for more stable TTS pronunciation."""

    def replace_symbol(match: re.Match) -> str:
        return f" {SYMBOL_TO_ORAL_NAME[match.group(0)]} "

    verbalized_text = _SYMBOL_PATTERN.sub(replace_symbol, text)
    verbalized_text = re.sub(r"[ \t]+", " ", verbalized_text)
    verbalized_text = re.sub(r" *\n *", "\n", verbalized_text)
    return verbalized_text.strip()

