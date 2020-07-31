
from pullenti.morph.internal.UnicodeInfo import UnicodeInfo


UnicodeInfo.initialize()
VALID = {_.uni_char for _ in UnicodeInfo.ALL_CHARS}


def preprocess(text):
    return ''.join(_ for _ in text if _ in VALID)
