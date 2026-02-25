"""
Tests for the JASS parser implementation.

This module contains tests for the parser that converts token streams
from the lexer into an Abstract Syntax Tree (AST).
"""

import pytest
from src.jass_runner.parser.parser import Parser, AST, FunctionDecl, Parameter


class TestParserBasic:
    """Basic parser functionality tests."""

    def test_parser_can_parse_function_declaration(self):
        """Test that parser can parse a simple function declaration."""
        code = """
function main takes nothing returns nothing
endfunction
"""
        parser = Parser(code)
        ast = parser.parse()

        assert isinstance(ast, AST)
        assert len(ast.functions) == 1

        func = ast.functions[0]
        assert func.name == "main"
        assert func.return_type == "nothing"
        assert len(func.parameters) == 0
        assert func.line == 2  # function starts on line 2
        assert func.column == 1

    def test_parser_can_parse_function_with_parameters(self):
        """Test that parser can parse a function with parameters."""
        code = """
function add takes integer x, real y returns integer
endfunction
"""
        parser = Parser(code)
        ast = parser.parse()

        assert len(ast.functions) == 1

        func = ast.functions[0]
        assert func.name == "add"
        assert func.return_type == "integer"
        assert len(func.parameters) == 2

        param1 = func.parameters[0]
        assert param1.name == "x"
        assert param1.type == "integer"
        assert param1.line == 2
        assert param1.column == 20  # "integer" token starts at column 20

        param2 = func.parameters[1]
        assert param2.name == "y"
        assert param2.type == "real"
        assert param2.line == 2
        assert param2.column == 31  # "real" token starts at column 31

    def test_parser_can_parse_multiple_functions(self):
        """Test that parser can parse multiple function declarations."""
        code = """
function func1 takes nothing returns nothing
endfunction

function func2 takes integer x returns integer
endfunction
"""
        parser = Parser(code)
        ast = parser.parse()

        assert len(ast.functions) == 2

        func1 = ast.functions[0]
        assert func1.name == "func1"
        assert func1.return_type == "nothing"
        assert len(func1.parameters) == 0

        func2 = ast.functions[1]
        assert func2.name == "func2"
        assert func2.return_type == "integer"
        assert len(func2.parameters) == 1
        assert func2.parameters[0].name == "x"
        assert func2.parameters[0].type == "integer"

    def test_parser_handles_empty_code(self):
        """Test that parser handles empty code input."""
        parser = Parser("")
        ast = parser.parse()

        assert isinstance(ast, AST)
        assert len(ast.functions) == 0

    def test_parser_handles_code_with_only_comments(self):
        """Test that parser handles code containing only comments."""
        code = """
// This is a comment
/* This is a
   multiline comment */
"""
        parser = Parser(code)
        ast = parser.parse()

        assert isinstance(ast, AST)
        assert len(ast.functions) == 0


class TestParserErrorHandling:
    """Parser error handling and recovery tests."""

    def test_parser_skips_invalid_syntax_and_continues(self):
        """Test that parser skips invalid syntax and continues to next function."""
        code = """
function invalid takes // missing parameter list
endfunction

function valid takes nothing returns nothing
endfunction
"""
        parser = Parser(code)
        ast = parser.parse()

        # Should parse only the valid function
        assert len(ast.functions) == 1
        assert ast.functions[0].name == "valid"

    def test_parser_handles_missing_keywords(self):
        """Test that parser handles missing required keywords."""
        code = """
function missing_takes returns nothing
endfunction
"""
        parser = Parser(code)
        ast = parser.parse()

        # Should skip the invalid function
        assert len(ast.functions) == 0

    def test_parser_handles_malformed_parameter_list(self):
        """Test that parser handles malformed parameter lists."""
        code = """
function bad_params takes integer x real y returns nothing
endfunction
"""
        parser = Parser(code)
        ast = parser.parse()

        # Should skip the invalid function
        assert len(ast.functions) == 0


class TestParserEdgeCases:
    """Parser edge case tests."""

    def test_parser_handles_function_with_single_parameter(self):
        """Test that parser handles function with single parameter (no comma)."""
        code = """
function single takes integer x returns nothing
endfunction
"""
        parser = Parser(code)
        ast = parser.parse()

        assert len(ast.functions) == 1
        func = ast.functions[0]
        assert len(func.parameters) == 1
        assert func.parameters[0].name == "x"
        assert func.parameters[0].type == "integer"

    def test_parser_preserves_position_information(self):
        """Test that parser preserves line and column information in AST nodes."""
        code = """function test takes integer a, real b returns string
endfunction"""
        parser = Parser(code)
        ast = parser.parse()

        func = ast.functions[0]
        assert func.line == 1
        assert func.column == 1  # "function" starts at column 1

        param1 = func.parameters[0]
        assert param1.line == 1
        assert param1.column == 21  # "integer" token starts at column 21

        param2 = func.parameters[1]
        assert param2.line == 1
        assert param2.column == 32  # "real" token starts at column 32