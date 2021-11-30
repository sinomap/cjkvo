import re
import typing as t

import romkan # type: ignore


def normalize_katakana_size(s: str) -> str:
    ret = ''
    for c in s:
        if c in 'ァィゥェォッャュョヮ':
            ret += chr(ord(c) + 1)
        else:
            ret += c
    return ret


def normalize_romaji(s: str) -> str:
    '''Handle a couple apparent quirks of romkan's kunrei romaji'''
    return s.replace('dyi', 'di').replace('fu', 'hu')


def normalize_glides(s: str) -> str:
    return s.replace('uw', 'w').replace('iy', 'y')


def parse_romaji(s: str) -> t.Sequence[t.Optional[str]]:
    initials = 'kgsztdnhbmr'
    initial_pattern = '(%s)' % '|'.join(initials)
    medial_pattern = '(wy|w|y)'
    nucleus = 'aiueo'
    nucleus_pattern = '(%s)' % '|'.join(nucleus)
    finals = ['i', 'u', 'ki', 'ku', 'ti', 'tu', 'hu', 'mu', 'n']
    final_pattern = '(%s)' % '|'.join(finals)
    m: t.Optional[t.Match[str]] = re.match('^%s?%s?%s%s?$' % (initial_pattern, medial_pattern, nucleus_pattern, final_pattern), s)
    if not m:
        raise ValueError('Unable to parse romaji: %s' % s)
    return m.groups()


def parse_japanese(s: str) -> t.Sequence[t.Optional[str]]:
    romaji = romkan.to_kunrei(s)
    normalized_romaji = normalize_glides(normalize_romaji(romaji))
    return parse_romaji(normalized_romaji)
