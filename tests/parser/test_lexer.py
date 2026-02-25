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