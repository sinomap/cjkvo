import re
import unicodedata as ud
import typing as t


UNICODE_TONE = {
    '\u0301': 's',
    '\u0300': 'f',
    '\u0309': 'r',
    '\u0303': 'x',
    '\u0323': 'j',
}

TONE_UNICODE = {v: k for (k, v) in UNICODE_TONE.items()}

DIPTHONG_TELEX = {
    'iê': 'ia',
    'yê': 'ia',
    'ya': 'ia',
    'ưa': 'uwa',
    'ươ': 'uwa',
    'uô': 'ua' 
}

VOWEL_TELEX = {
    'ă': 'aw',
    'â': 'aa',
    'ơ': 'ow',
    'ư': 'uw',
    'ê': 'ee',
    'ô': 'oo'
}

NUCLEUS_TELEX = {'y': 'i'}
NUCLEUS_TELEX.update(DIPTHONG_TELEX)
NUCLEUS_TELEX.update(VOWEL_TELEX)

TELEX_VOWEL = {v: k for (k, v) in VOWEL_TELEX.items()}


class Syllable:

    def __init__(self, initial: t.Optional[str], glide: t.Optional[str],
            nucleus: t.Optional[str], coda: t.Optional[str], tone: t.Optional[str]):
        self.initial = initial
        self.glide = glide
        self.nucleus = nucleus
        self.coda = coda
        self.tone = tone

    def tuple(self) -> tuple:
        return (self.initial, self.glide, self.nucleus, self.coda, self.tone)


def extract_tone(s: str) -> t.Tuple[t.Optional[str], str]:
    tone = None
    rest = ''
    for c in s:
        norm = ud.normalize('NFD', c)
        toneless = ''
        for cn in norm:
            if cn in UNICODE_TONE:
                tone = UNICODE_TONE[cn]
            else:
                toneless += cn
        rest += ud.normalize('NFC', toneless)
    return tone, rest


def add_tone(tone: t.Optional[str], rest: str, at_beginning: bool=False) -> str:
    '''Add tone mark at end of string (unless at_beginning is True)'''
    if tone and at_beginning:
        return ud.normalize('NFC', rest[0] + TONE_UNICODE[tone] + rest[1:])
    elif tone:
        return ud.normalize('NFC', rest + TONE_UNICODE[tone])
    else:
        return rest


def extract_semivowel(s: str) -> t.Tuple[t.Optional[str], str]:
    if 1 < len(s) and s[-1] in 'iouy':
        return s[-1], s[:-1]
    else:
        return None, s


def extract_glide(s: str) -> t.Tuple[t.Optional[str], str]:
    _, toneless = extract_tone(s)
    if toneless in ['oa', 'oă', 'oe', 'uy', 'uê', 'uơ', 'uâ']:
        return s[0], s[1]
    else:
        return None, s


def maybe_groups(match: t.Match) -> t.Tuple[t.Optional[str], ...]:
    return tuple(g or None for g in match.groups())


def segment(s: str) -> Syllable:
    '''This function nondestructively breaks a quoc ngu syllable into initial/glide/nucleus/coda'''
    # Note: Including all tone options for gi, as only it can combine initial/tone
    initial_str = 'b|ch|c|d|đ|gh|gi|gí|gì|gỉ|gĩ|gị|g|h|kh|k|l|m|ngh|ng|nh|n|ph|qu|r|s|th|tr|t|v|x'
    coda_str = 'c|ch|ng|nh|n|t|p|m'
    match_str = '^(%s)?(.*?)(%s)?$' % (initial_str, coda_str)
    match = re.search(match_str, s)
    if not match:
        raise ValueError('Error segmenting Vietnamese syllable "%s"' % s)
    initial, rest, coda = maybe_groups(match)
    glide = None
    if rest:
        _, toneless = extract_tone(rest)
        if toneless[:2] == 'uy':
            glide, rest = rest[0], rest[1:]
        if not coda:
            coda, rest = extract_semivowel(rest)
        if not glide:
            glide, rest = extract_glide(rest)
    return Syllable(initial, glide, rest, coda, None)


def norm_tone(s: Syllable) -> None:
    if s.nucleus:
        tone, rest = extract_tone(s.nucleus)
        s.tone = tone
        s.nucleus = rest
    # Sometimes tone indicated on glide as in hỏa
    if not s.tone and s.glide:
        tone, rest = extract_tone(s.glide)
        if tone:
            s.tone = tone
            s.glide = rest


def denorm_tone(s: Syllable) -> None:
    if s.nucleus and s.tone:
        at_beginning = not s.coda
        s.nucleus = add_tone(s.tone, s.nucleus, at_beginning)
        s.tone = None


def norm_initial(s: Syllable) -> None:
    alternates = {
        'ngh': 'ng',
        'c': 'k',
        'q': 'k',
        'gh': 'g',
        'đ': 'dd'
    }
    if s.initial in alternates:
        s.initial = alternates[s.initial]


def denorm_initial(s: Syllable) -> None:
    if not s.nucleus:
        raise ValueError('Vietnamese syllable must have a nucleus')
    if not s.initial:
        return
    if s.initial == 'g' and s.nucleus[0] in 'ieê':
        s.initial = 'gh'
    elif s.initial == 'ng' and s.nucleus[0] in 'ieê':
        s.initial = 'ngh'
    elif s.initial == 'k' and s.glide:
        s.initial = 'q'
    elif s.initial == 'k' and s.nucleus[0] not in 'yieê':
        s.initial = 'c'
    elif s.initial == 'dd':
        s.initial = 'đ'


def norm_nucleus(s: Syllable) -> None:
    if s.nucleus in NUCLEUS_TELEX:
        s.nucleus = NUCLEUS_TELEX[s.nucleus]


def denorm_nucleus(s: Syllable) -> None:
    if s.nucleus in TELEX_VOWEL:
        s.nucleus = TELEX_VOWEL[s.nucleus]
    elif s.nucleus == 'ia' and ((s.glide and s.coda) or not s.initial):
        s.nucleus = 'yê'
    elif s.nucleus == 'ia' and s.glide:
        s.nucleus = 'ya'
    elif s.nucleus == 'ia' and s.coda:
        s.nucleus = 'iê'
    elif s.nucleus == 'uwa' and s.coda:
        s.nucleus = 'ươ'
    elif s.nucleus == 'uwa':
        s.nucleus = 'ưa'
    elif s.nucleus == 'ua' and s.coda:
        s.nucleus = 'uô'
    # Note: 'y' used exclusively if 'y' is the complete syllable, or in '-uy-' syllables,
    # otherwise it is very rare (just a few occurrences of hy/ly/ky) but according to this
    # Wiktionary editor the "standard" in those cases is 'i':
    # https://en.wiktionary.org/wiki/User:Fumiko_Take
    elif s.nucleus == 'i' and (not (s.initial or s.coda) or s.glide):
        s.nucleus = 'y'

def norm_glide(s: Syllable) -> None:
    if s.glide:
        s.glide = 'w'


def denorm_glide(s: Syllable) -> None:
    if not s.nucleus:
        raise ValueError('Vietnamese syllable must have a nucleus')
    if s.glide and s.nucleus in 'aăe':
        s.glide = 'o'
    if s.glide and s.nucleus[0] in 'yêơâ':
        s.glide = 'u'


def norm_coda(s: Syllable) -> None:
    alternates = {
        'y': 'i',
        'o': 'u'
    }
    if s.coda in alternates:
        s.coda = alternates[s.coda]


def denorm_coda(s: Syllable) -> None:
    if s.coda == 'i' and s.nucleus in ['aw', 'aa']:
        s.coda = 'y'
    elif s.coda == 'u' and s.nucleus in ['e', 'a']:
        s.coda = 'o'


def duplicate_i(s: Syllable) -> None:
    if s.initial:
        tone, initial = extract_tone(s.initial)
        if s.nucleus == None and initial == 'gi':
            s.nucleus = 'i'
            s.initial = 'gi'
            s.tone = tone


def deduplicate_i(s: Syllable) -> None:
    if s.initial == 'gi' and s.nucleus == 'i':
        s.initial = add_tone(s.tone, 'gi')
        s.nucleus = s.tone = None


def add_short_a(s: Syllable) -> None:
    if s.nucleus == 'a' and s.coda and s.coda in 'yu':
        s.nucleus = 'ă'


def remove_short_a(s: Syllable) -> None:
    if s.nucleus == 'ă' and s.coda and s.coda in 'yu':
        s.nucleus = 'a'


def norm_q(s: Syllable) -> None:
    if s.initial == 'qu':
        s.initial = 'q'
        s.glide = 'w'


def denorm_q(s: Syllable) -> None:
    if s.initial == 'q' and s.glide:
        s.initial = 'qu'
        s.glide = None


def normalize(s: Syllable) -> None:
    norm_tone(s)
    duplicate_i(s)
    if not s.nucleus:
        # By now there must be a nucleus
        raise ValueError('No nucleus in Vietnamese syllable %r' % s)
    norm_q(s)
    add_short_a(s)
    norm_initial(s)
    norm_glide(s)
    norm_nucleus(s)
    norm_coda(s)


def denormalize(s: Syllable) -> None:
    denorm_coda(s)
    denorm_nucleus(s)
    denorm_glide(s)
    denorm_initial(s)
    remove_short_a(s)
    denorm_q(s)
    deduplicate_i(s)
    denorm_tone(s)


def parse_vietnamese(s: str) -> t.Tuple[t.Optional[str], ...]:
    syllable = segment(s.lower())
    normalize(syllable)
    return syllable.tuple()


def emit_vietnamese(tup: t.Tuple[t.Optional[str], ...]) -> str:
    syllable = Syllable(*tup)
    denormalize(syllable)
    return ''.join(seg or '' for seg in syllable.tuple())

