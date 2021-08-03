import pytest

from lam4vb3.cell_parser import LITERAL_VALUE, VALUES, COMMENT, MIN_COUNT, MAX_COUNT, CONTROLLED_LIST, parse_cell


def test_multiline_value_parser():
    example1 = """eurovoc:1452
eurovoc:4347 | this is an optional comment"""

    result = parse_cell(example1)

    assert LITERAL_VALUE not in result
    assert VALUES in result
    assert "1452" in str(result[VALUES][0])
    assert "4347" in str(result[VALUES][1])
    assert COMMENT in result
    assert "this is an optional comment" in result[COMMENT]
    assert MIN_COUNT in result
    assert result[MIN_COUNT] == 1

    example2 = """
eurovoc:1452

eurovoc:4347 


          | this is an optional comment tolerating empty new lines and spaces"""

    result = parse_cell(example2)

    assert LITERAL_VALUE not in result
    assert VALUES in result
    assert "1452" in str(result[VALUES][0])
    assert "4347" in str(result[VALUES][1])
    assert COMMENT in result
    assert "this is an optional comment tolerating empty new lines and spaces" in result[COMMENT]
    assert MIN_COUNT in result
    assert result[MIN_COUNT] == 1

    counter_example1 = """eurovoc:1452,
eurovoc:4347, | no comments | with | extra pipes|"""

    with pytest.raises(ValueError):
        parse_cell(counter_example1)

    counter_example2 = """eurovoc:1452 | bad intermediary comment
eurovoc:4347 | good final comment"""

    with pytest.raises(ValueError):
        parse_cell(counter_example2)

    counter_example3 = """ | no empty list of values with a dangling comment"""

    with pytest.raises(ValueError):
        parse_cell(counter_example3)


def test_cardinality_value_parser():
    example1 = """O|Under Internal reference the reference to the procedure is doubled (as it is specifically under procedure)"""
    result = parse_cell(example1)

    assert LITERAL_VALUE not in result
    assert VALUES not in result
    assert COMMENT in result
    assert "Under Internal reference the reference" in result[COMMENT]
    assert MIN_COUNT in result
    assert result[MIN_COUNT] == 1

    example2 = ""

    result = parse_cell(example2)

    assert LITERAL_VALUE not in result
    assert VALUES not in result
    assert COMMENT not in result
    assert MIN_COUNT in result
    assert result[MIN_COUNT] == 1

    counter_example1 = """XYZ | cardinality specifications that are not in the foreseen controlled list"""

    with pytest.raises(ValueError):
        parse_cell(counter_example1)

    counter_example2 = """YU | comment | with pipe (|) separators | inside |"""

    with pytest.raises(ValueError):
        parse_cell(counter_example2)

    counter_example3 = """ | no empty cardinality spec with a dangling comment"""

    with pytest.raises(ValueError):
        parse_cell(counter_example3)


def test_literal_value_parser():
    example1 = """Council Common Position (CFSP number)"""

    result = parse_cell(example1)

    assert LITERAL_VALUE in result
    assert "Council Common Position (CFSP number)" in result[LITERAL_VALUE]
    assert VALUES not in result
    assert COMMENT not in result
    assert MIN_COUNT not in result
    assert MAX_COUNT not in result

    counter_example = """text with | pipe | separator inside"""

    with pytest.raises(ValueError):
        parse_cell(counter_example)
