import csv
from importlib import resources

from cjkvo.ja import parse_japanese


def test_parse() -> None:
    with open(resources.files('cjkvo') / 'data' / 'test_ja.tsv') as f:
        r = csv.reader(f, delimiter='\t')
        for row in r:
            actual = parse_japanese(row[0])
            expected = tuple(s or None for s in row[1].split('_'))
            assert actual == expected
