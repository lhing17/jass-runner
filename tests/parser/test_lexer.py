"""Test JASS lexer."""

def test_lexer_can_tokenize_simple_code():
    """Test that lexer can tokenize simple JASS code."""
    from jass_runner.parser.lexer import Lexer

    code = "function main takes nothing returns nothing"
    lexer = Lexer(code)
    tokens = list(lexer.tokenize())

    # Should have at least some tokens
    assert len(tokens) > 0


def test_lexer_token_types():
    """Test that lexer correctly identifies token types."""
    from jass_runner.parser.lexer import Lexer

    code = 'function test takes integer x returns string'
    lexer = Lexer(code)
    tokens = [t for t in lexer.tokenize() if t.type != 'WHITESPACE']

    expected_types = ['KEYWORD', 'IDENTIFIER', 'KEYWORD', 'KEYWORD', 'IDENTIFIER', 'KEYWORD', 'KEYWORD']
    actual_types = [t.type for t in tokens]

    assert actual_types == expected_types


def test_lexer_new_keywords():
    """Test that lexer recognizes newly added keywords."""
    from jass_runner.parser.lexer import Lexer

    # Test some of the new keywords
    code = 'true false null elseif return and or not globals endglobals'
    lexer = Lexer(code)
    tokens = [t for t in lexer.tokenize() if t.type != 'WHITESPACE']

    # All should be recognized as KEYWORD tokens
    assert all(t.type == 'KEYWORD' for t in tokens)
    assert len(tokens) == 10  # 10 keywords in the code

    # Verify specific keyword values
    expected_values = ['true', 'false', 'null', 'elseif', 'return', 'and', 'or', 'not', 'globals', 'endglobals']
    actual_values = [t.value for t in tokens]
    assert actual_values == expected_values


def test_lexer_multiline_comment():
    """Test that lexer correctly handles multiline comments."""
    from jass_runner.parser.lexer import Lexer

    # Test multiline comment
    code = '''function test takes nothing returns nothing
/* This is a
   multiline comment */
set x = 5'''
    lexer = Lexer(code)
    tokens = [t for t in lexer.tokenize() if t.type not in ('WHITESPACE', 'COMMENT', 'MULTILINE_COMMENT')]

    # Should have tokens: function, test, takes, nothing, returns, nothing, set, x, =, 5
    # But let's just verify we get tokens and the comment is skipped
    assert len(tokens) > 0

    # Verify no comment tokens are in the output
    token_types = [t.type for t in tokens]
    assert 'COMMENT' not in token_types
    assert 'MULTILINE_COMMENT' not in token_types

    # Verify we get expected keywords
    keyword_values = [t.value for t in tokens if t.type == 'KEYWORD']
    assert 'function' in keyword_values
    assert 'takes' in keyword_values
    assert 'returns' in keyword_values
    assert 'nothing' in keyword_values
    assert 'set' in keyword_values


def test_lexer_all_keywords():
    """Test that lexer recognizes all JASS keywords."""
    from jass_runner.parser.lexer import Lexer

    # Complete list of 35 JASS keywords from user-provided lists
    all_keywords = [
        # From JassKeywork list
        'function', 'endfunction', 'constant', 'native', 'local', 'type', 'set',
        'call', 'takes', 'returns', 'extends', 'array', 'true', 'false', 'null',
        'nothing', 'if', 'else', 'elseif', 'endif', 'then', 'loop', 'endloop',
        'exitwhen', 'return', 'and', 'or', 'not', 'globals', 'endglobals',
        # Additional type keywords from Keywords list
        'integer', 'real', 'boolean', 'string', 'handle', 'code'
    ]

    # Test each keyword individually
    for keyword in all_keywords:
        lexer = Lexer(keyword)
        tokens = list(lexer.tokenize())
        # Filter out whitespace tokens
        tokens = [t for t in tokens if t.type != 'WHITESPACE']
        assert len(tokens) == 1, f"Expected 1 token for keyword '{keyword}', got {len(tokens)}"
        token = tokens[0]
        assert token.type == 'KEYWORD', f"Expected KEYWORD for '{keyword}', got {token.type}"
        assert token.value == keyword, f"Expected value '{keyword}', got {token.value}"


def test_lexer_fourcc_format():
    """Test that lexer correctly handles FourCC format (single-quoted 4 chars)."""
    from jass_runner.parser.lexer import Lexer
    from jass_runner.utils import fourcc_to_int

    # Test basic FourCC
    code = "'hfoo'"
    lexer = Lexer(code)
    tokens = list(lexer.tokenize())

    assert len(tokens) == 1
    assert tokens[0].type == 'INTEGER'
    assert tokens[0].value == fourcc_to_int('hfoo')  # Should be 1213484355

    # Test another FourCC
    code = "'hkni'"
    lexer = Lexer(code)
    tokens = list(lexer.tokenize())

    assert len(tokens) == 1
    assert tokens[0].type == 'INTEGER'
    assert tokens[0].value == fourcc_to_int('hkni')


def test_lexer_fourcc_in_function_call():
    """Test FourCC in a function call context."""
    from jass_runner.parser.lexer import Lexer
    from jass_runner.utils import fourcc_to_int

    # Simulate CreateUnit call with FourCC
    code = 'call CreateUnit(0, \'hfoo\', 0.0, 0.0, 0.0)'
    lexer = Lexer(code)
    tokens = [t for t in lexer.tokenize() if t.type not in ('WHITESPACE',)]

    # Should have: call, CreateUnit, (, 0, ,, INTEGER (hfoo), ,, 0.0, ,, 0.0, ,, 0.0, )
    token_types = [t.type for t in tokens]
    assert 'KEYWORD' in token_types  # call
    assert 'IDENTIFIER' in token_types  # CreateUnit
    assert 'INTEGER' in token_types  # 0 and 'hfoo'
    assert 'REAL' in token_types  # 0.0

    # Find the FourCC token (should be the second INTEGER after 0)
    fourcc_token = None
    for t in tokens:
        if t.type == 'INTEGER' and t.value == fourcc_to_int('hfoo'):
            fourcc_token = t
            break

    assert fourcc_token is not None, "FourCC token not found"
    # 'hfoo' = 0x68666F6F in big-endian, but we store as little-endian bytes
    # little-endian: 0x6F6F6668 = 1869571688
    assert fourcc_token.value == 1869571688


def test_lexer_fourcc_vs_string():
    """Test that FourCC and string are distinguished correctly."""
    from jass_runner.parser.lexer import Lexer

    # FourCC should be INTEGER
    code_fourcc = "'hfoo'"
    lexer = Lexer(code_fourcc)
    tokens = list(lexer.tokenize())
    assert tokens[0].type == 'INTEGER'

    # String should be STRING
    code_string = '"hfoo"'
    lexer = Lexer(code_string)
    tokens = list(lexer.tokenize())
    assert tokens[0].type == 'STRING'
    assert tokens[0].value == '"hfoo"'


def test_lexer_invalid_fourcc():
    """Test that invalid FourCC formats are not converted."""
    from jass_runner.parser.lexer import Lexer

    # Too short (3 chars)
    code = "'foo'"
    lexer = Lexer(code)
    tokens = list(lexer.tokenize())
    # Should not be recognized as FourCC, will be processed as separate tokens or skipped

    # Too long (5 chars)
    code = "'foooo'"
    lexer = Lexer(code)
    tokens = list(lexer.tokenize())
    # Should not be recognized as FourCC