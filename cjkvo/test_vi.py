from cjkvo.vi import parse_vietnamese, emit_vietnamese


def assert_parsed_and_emitted(cases):
    for s, expected in cases:
        parsed = parse_vietnamese(s)
        assert parsed == expected
        emitted = emit_vietnamese(parsed)
        assert emitted == s.lower()


def test_glide():
    assert_parsed_and_emitted([
        ('qua', ('k', 'w', 'a', None, None)),
        ('hoa', ('h', 'w', 'a', None, None)),
        ('hoay', ('h', 'w', 'aw', 'i', None)),
        ('khoẻ', ('kh', 'w', 'e', None, 'r')),
        ('nhoà', ('nh', 'w', 'a', None, 'f')),
        ('nguy', ('ng', 'w', 'i', None, None)),
        ('thuê', ('th', 'w', 'ee', None, None)),
        ('thuở', ('th', 'w', 'ow', None, 'r')),
        ('khuấy', ('kh', 'w', 'aa', 'i', 's')),
        ('khuya', ('kh', 'w', 'ia', None, None)),
        ('quyển', ('k', 'w', 'ia', 'n', 'r')),
        ('hoằng', ('h', 'w', 'aw', 'ng', 'f')),
        ('huỷ', ('h', 'w', 'i', None, 'r'))
        ])


def test_i():
    assert_parsed_and_emitted([
        ('Ý', (None, None, 'i', None, 's')),
        ('khỉ', ('kh', None, 'i', None, 'r'))
        ])


def test_k():
    assert_parsed_and_emitted([
        ('ca', ('k', None, 'a', None, None)),
        ('qua', ('k', 'w', 'a', None, None)),
        ('kia', ('k', None, 'ia', None, None))
        ])


def test_ng():
    assert_parsed_and_emitted([
        ('nga', ('ng', None, 'a', None, None)),
        ('nghe', ('ng', None, 'e', None, None)),
        ('nghiêm', ('ng', None, 'ia', 'm', None))
        ])


def test_g():
    assert_parsed_and_emitted([
        ('ga', ('g', None, 'a', None, None)),
        ('ghét', ('g', None, 'e', 't', 's'))
        ])


def test_dipthongs():
    assert_parsed_and_emitted([
        ('kia', ('k', None, 'ia', None, None)),
        ('thiên', ('th', None, 'ia', 'n', None)),
        ('muốn', ('m', None, 'ua', 'n', 's')),
        ('nước', ('n', None, 'uwa', 'c', 's')),
        ('bữa', ('b', None, 'uwa', None, 'x'))
        ])


def test_final_semivowels():
    assert_parsed_and_emitted([
        ('tay', ('t', None, 'aw', 'i', None)),
        ('ai', (None, None, 'a', 'i', None)),
        ('heo', ('h', None, 'e', 'u', None)),
        ('táo', ('t', None, 'a', 'u', 's')),
        ('đâu', ('dd', None, 'aa', 'u', None))
        ])


def test_short_vowels():
    assert_parsed_and_emitted([
        ('tay', ('t', None, 'aw', 'i', None))
        ])


def test_dipthong_y():
    assert_parsed_and_emitted([
        ('yêu', (None, None, 'ia', 'u', None))
        ])


def test_gi():
    assert_parsed_and_emitted([
        ('gì', ('gi', None, 'i', None, 'f')),
        ('giường', ('gi', None, 'uwa', 'ng', 'f'))
        ])


def test_nonstandard():
    examples = [
        ('hỏa', ('h', 'w', 'a', None, 'r'), 'hoả'),
        ('túy', ('t', 'w', 'i', None, 's'), 'tuý'),
        ('ký', ('k', None, 'i', None, 's'), 'kí'),
    ]
    for s, expected_parsed, expected_emitted in examples:
        parsed = parse_vietnamese(s)
        assert parsed == expected_parsed
        emitted = emit_vietnamese(parsed)
        assert emitted == expected_emitted
