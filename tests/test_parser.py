import pandas

from spectrominer.parser import Parser

RAW_DATA_FILEPATH = './tests/data/raw.csv'


def test_parser():
    result = Parser(RAW_DATA_FILEPATH, delimiter=';')

    assert type(result.df) == pandas.DataFrame
    assert not result.df.empty
    # Asserting the column format
    assert len(result.df.columns) == 248
    assert len(result.df.columns[0]) == 2
    # Asserting that two-index column selection works
    assert type(result.df[('Lactic acid M+0 Results', 'RT')]) == pandas.Series
