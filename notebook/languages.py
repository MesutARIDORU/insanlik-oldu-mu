# -*- coding: utf-8 -*-
"""Notebook review · language rules the page builder needs

Only what matching sentences and words depends on: lowercasing (Turkish has a dotted and a
dotless i) and the abbreviations a period does not end a sentence after.
"""

import re

ABBREVIATIONS = {
    "en": {
        "mr", "mrs", "ms", "dr", "prof", "sr", "jr", "st", "vs", "etc", "e.g", "i.e", "inc", "ltd", "co", "corp",
        "no", "fig", "approx", "dept", "est", "al", "cf", "ca", "u.s", "u.k", "a.m", "p.m", "ph.d", "jan", "feb",
        "mar", "apr", "jun", "jul", "aug", "sep", "sept", "oct", "nov", "dec", "mon", "tue", "wed", "thu", "fri",
        "vol", "pp", "p", "ed", "eds", "rev", "gen", "col", "lt", "sgt", "mt", "ft", "min", "max", "tel", "ext",
    },
    "tr": {
        "dr", "prof", "doç", "av", "uzm", "öğr", "yrd", "müh", "vb", "vs", "örn", "bkz", "krş", "çev", "sok", "cad", "mah", "bulv", "apt", "no", "tel", "s", "ss", "c", "yy", "sn", "st", "dk", "alm", "ing",
        "fr", "t.c", "a.ş", "ltd", "şti",
    },
}


def lower(text, language):
    if language in ("tr", "az"):
        text = text.replace("I", "ı").replace("İ", "i")
    return text.lower()


def is_abbreviation(word, language):
    """True when a period after word does not end the sentence: "Dr.", "e.g.", or a lone initial ("J.")."""
    word = word.rstrip(".")
    if re.fullmatch(r"[A-ZÇĞİÖŞÜ]", word):
        return True
    return lower(word, language) in ABBREVIATIONS.get(language, set())
