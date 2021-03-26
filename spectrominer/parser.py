import pandas


class Parser:

    def __init__(self, filepath: str, delimiter: str = ',', quotechar: str = '"') -> None:
        self.df = pandas.read_csv(
            filepath,
            delimiter=delimiter,
            quotechar=quotechar,
            header=[0, 1]
        )

