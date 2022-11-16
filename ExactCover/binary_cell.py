class BinaryCell(object):
    def __init__(self, raw_line: str) -> None:
        self.len = raw_line.count("1")
        self.row_value = int(raw_line, base=2)

    def __len__(self):
        return self.len

    def __eq__(self, other) -> bool:
        if isinstance(other, BinaryCell):
            return self.row_value == other.row_value

        raise Exception(f"Can't compare BinaryCell to {type(other)}")

    def union(self, other):
        if isinstance(other, BinaryCell):
            union = self.row_value | other.row_value
            return BinaryCell("{0:b}".format(union))

        raise Exception(f"Can't compute union of BinaryCell and {type(other)}")

    def intersection(self, other):
        if isinstance(other, BinaryCell):
            union = self.row_value & other.row_value
            return BinaryCell("{0:b}".format(union))

        raise Exception(f"Can't compute union of BinaryCell and {type(other)}")

    def __str__(self):
        return "{0:b}".format(self.row_value)
        