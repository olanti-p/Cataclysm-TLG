#!/usr/bin/env python3
import os
import regex
from spellchecker import SpellChecker


Tokenizer = regex.compile(
    r"(?<="
        r"(?:" # a word can be after...
            r"^" # ...the start of text...
        r"|" # ...or...
            r"""[\s\-'‘"“«\*&\(\[\{/>]""" # ...a valid starting delimiter
        r")"
        r"[…]*" # ignore possible punctuations before a word
    r")"
    # a single letter is always considered a valid word and therefore not
    # tokenized
    r"\pL" # a word always starts with an letter...
    r"(?:\pL|['‘’])*" # ...can contain letters and apostrophes...
    r"\pL" # ...and always ends with an letter
    # exclude suffix `'s` and match the apostrophe as a delimiter later
    r"(?<!'[sS])"
    # note: staring and ending apostrophe cannot be distinguished from
    # starting and ending single quote so the former is not considered.
    r"(?="
        r"[,\.\?!:;…]*" # ignore any punctuations after a word
        r"(?:" # a word can be before...
            r"$" # ...the end of text...
        r"|" # ...or...
            r"""[\s\-'’"”»\*\)\]\}/<]""" # ...a valid ending delimiter
        r")"
    r")"
)
DefaultKnownWords = set()
KnownWords = set()


def init_known_words(DefaultKnownWords, KnownWords):
    default_dict = SpellChecker(case_sensitive=True).word_frequency

    custom_dict = set()
    dict_path = os.path.join(os.path.dirname(__file__), 'dictionary.txt')
    with open(dict_path, 'r', encoding='utf-8') as fp:
        for line in fp:
            line = line.rstrip('\n').rstrip('\r')
            custom_dict.add(line)

    for dictionary, knownwords in [
            (default_dict, DefaultKnownWords), (custom_dict, KnownWords)]:
        for word in dictionary:
            # For words in full lower case, allow capitalization and all caps
            # (e.g. word, Word, & WORD); for other words, allow the word itself and
            # all caps (e.g. George & GEORGE or pH & PH)
            knownwords.add(word)
            if word == word.lower():
                knownwords.add(word.capitalize())
            knownwords.add(word.upper())

    KnownWords |= DefaultKnownWords


if not KnownWords:
    init_known_words(DefaultKnownWords, KnownWords)


def unit_test__tokenizer():
    text_and_results = [
        ("I'm a test", ["I'm", "test"]),
        ("\"This'll do!\"", ["This'll", "do"]),
        ("Someone's test case", ["Someone", "test", "case"]),
        ("SOMEONE'S VERY IMPORTANT TEST", ["SOMEONE", "VERY", "IMPORTANT", "TEST"]),
        ("tic-tac-toe", ["tic", "tac", "toe"]),
        ("Ünicodé", ["Ünicodé"]),
        ("This apostrophe’s weird", ["This", "apostrophe’s", "weird"]),
        ("Foo i18n l10n bar", ["Foo", "bar"]),
        ("Lorem 123 ipsum -- dolor ||| sit", ["Lorem", "ipsum", "dolor", "sit"]),
        ("Lorem", ["Lorem"]),
        ("Lorem ipsum dolor sit amet",
            ["Lorem", "ipsum", "dolor", "sit", "amet"]),
        ("'Lorem ipsum dolor sit amet, consectetur adipiscing elit'",
            ["Lorem", "ipsum", "dolor", "sit", "amet", "consectetur",
                "adipiscing","elit"]),
        ("Lorem, ipsum.  dolor?  sit!  amet.", ["Lorem", "ipsum", "dolor", "sit", "amet"]),
        ("Lorem ipsum, 'dolor?'  sit!?", ["Lorem", "ipsum", "dolor", "sit"]),
        ("Lorem: ipsum; dolor…", ["Lorem", "ipsum", "dolor"]),
        ('"Lorem"', ["Lorem"]),
        ("Lorem-ipsum", ["Lorem", "ipsum"]),
        ("«Lorem ipsum»", ["Lorem", "ipsum"]), # used in some NPC dialogue
        ("*Lorem ipsum*", ["Lorem", "ipsum"]),
        ("&Lorem ipsum", ["Lorem", "ipsum"]), # used in some NPC dialogue
        ("…Lorem", ["Lorem"]),
        ("'…Lorem ipsum…'", ["Lorem", "ipsum"]),
        ("Lorem <ipsum> <color_yellow>dolor</color>", ["Lorem", "dolor"]),
        ("<global_val:<u_val:foobar>>", []),
        ("Lorem (ipsum) [dolor sit] {amet}", ["Lorem", "ipsum", "dolor", "sit", "amet"]),
        ("Lorem ipsum/dolor/sit amet", ["Lorem", "ipsum", "dolor", "sit", "amet"]),
        ("Lorem.ipsum.dolor", []),
        ("Lorem %1$s ipsum %2$d dolor!", ["Lorem", "ipsum", "dolor"])
    ]

    fail = False
    for text, expected in text_and_results:
        result = list(Tokenizer.findall(text))
        if result != expected:
            print(f"test case: {text}\nexpected: {expected}\nresult: {result}\n")
            fail = True

    if fail:
        raise RuntimeError("tokenizer test failed")
