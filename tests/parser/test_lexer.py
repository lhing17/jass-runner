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