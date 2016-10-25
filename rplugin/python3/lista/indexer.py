class Indexer:
    """An indexer class."""
    def __init__(self, candidates, index):
        """Constructor.

        Args:
            candidates (Sequence): A candidates.
        """
        self.candidates = candidates
        self.index = index

    @property
    def index(self):
        """int: A current index.

        Example:
            >>> indexer = Indexer("abcde")
            >>> indexer.index
            0
            >>> indexer.index = 1
            >>> indexer.index
            1
            >>> indexer.index = 4
            >>> indexer.index
            4
            >>> indexer.index = 5
            >>> indexer.index
            0
            >>> indexer.index = 6
            >>> indexer.index
            1
            >>> indexer.index = -1
            >>> indexer.index
            4
            >>> indexer.index = -2
            >>> indexer.index
            3
        """
        return self._index

    @index.setter
    def index(self, value):
        value = value % len(self.candidates)
        self._index = value

    @property
    def current(self):
        """Any: A current candidate.

        Example:
            >>> indexer = Indexer("abcde")
            >>> indexer.current
            'a'
            >>> indexer.index = 1
            >>> indexer.current
            'b'
        """
        return self.candidates[self.index]

    def next(self, offset):
        """Select next candidate and return.

        Example:
            >>> indexer = Indexer("abcde")
            >>> indexer.current
            'a'
            >>> indexer.next()
            'b'
            >>> indexer.next()
            'c'
            >>> indexer.next()
            'd'
            >>> indexer.next()
            'e'
            >>> indexer.next()
            'a'
        """
        self.index += offset
        return self.current

    def previous(self, offset):
        """Select previous candidate and return.

        Example:
            >>> indexer = Indexer("abcde")
            >>> indexer.current
            'a'
            >>> indexer.previous()
            'e'
            >>> indexer.previous()
            'd'
            >>> indexer.previous()
            'c'
            >>> indexer.previous()
            'b'
            >>> indexer.previous()
            'a'
        """
        self.index -= offset
        return self.current
