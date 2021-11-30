# CJKVO

CJKVO is a parser/emitter for CJKV phonetic orthography. It supportsparsing/emitting CJKV syllables written in a common phonetic script into a phonological representation.
The written form is translated into a tuple of initial, medial, vowel, coda, tone, a model typically used in Chinese
and Sinoxenic phonology. (Tone is currently only included for Vietnamese.)

CJKVO currently supports parsing/emitting Vietnamese (Chữ Quốc Ngữ) and parsing Japanese (ひらがな or カタカナ).

## Notation

### Japanese
The parsed Japanese notation is Japanese readings are approximately based on
[Nihon-shiki Romanization](https://en.wikipedia.org/wiki/Nihon-shiki_romanization) as applied to the
[Historical Kana Orthography](https://en.wikipedia.org/wiki/Historical_kana_orthography).
Vowels between initials and glides are generally omitted (e.g. "kwaku" instead of "kuwaku").
The convention of Tōdō Akiyasu's _Shin Kanwa Daijiten_ (新漢和大字典) is supported, which is sometimes based on
even older kana usage than "standard" historical kana (e.g. "kuwiyaku"/"kwyaku" instead of "kuwaku"/"kwaku").

### Vietnamese
For ease of typing in an ASCII environment, Vietnamese text is parsed into a format based on the Telex input system. As with Japanese,
medials are somewhat simplified compared to the Quốc Ngữ form. For example, "hoa" becomes `('h', 'w', 'a', None, None)`.

## Usage

Here is a simple example of importing/using the library. See the tests for more sample cases.

```
>>> from cjkvo.vi import parse_vietnamese, emit_vietnamese
>>> from cjkvo.ja import parse_japanese
>>> parse_japanese('キャク')
('k', 'y', 'a', 'ku')
>>> parse_vietnamese('nguyễn')
('ng', 'w', 'ia', 'n', 'x')
>>> emit_vietnamese(('ng', 'w', 'ia', 'n', 'x'))
'nguyễn'
```
