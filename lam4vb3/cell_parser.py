"""
This module implements Excel cell parsing as define in the excel srtucture specification document.

cases:

1. Literal values
2. Cardinality values with comments
3. Multi line reference values with comments

"""
LITERAL_VALUE = "literal_value"
VALUES = "values"
COMMENT = "comment"
MIN_COUNT = "min_count"
MAX_COUNT = "max_count"

CONTROLLED_LIST = [
    "Y",
    "YU",
    "",
    "OU",
    "O",
    "N"
]

def parse_cell(cell_value: str) -> dict:
    ...

