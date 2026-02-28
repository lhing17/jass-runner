"""
Tests for the JASS parser implementation.

This module contains tests for the parser that converts token streams
from the lexer into an Abstract Syntax Tree (AST).
"""

import pytest
from src.jass_runner.parser.parser import (
    Parser, AST, FunctionDecl, Parameter,
    ParseError, MissingKeywordError, UnexpectedTokenError, ParameterError
)


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


class TestParserErrorReporting:
    """Tests for enhanced error reporting in the parser."""

    def test_parser_collects_errors_instead_of_silent_failure(self):
        """Test that parser collects errors when parsing fails."""
        code = """
function missing_takes returns nothing
endfunction
"""
        parser = Parser(code)
        ast = parser.parse()

        # Should still return an AST (may be empty)
        assert isinstance(ast, AST)

        # Should have collected errors
        # This test will fail initially since error collection is not implemented
        assert hasattr(parser, 'errors')
        assert len(parser.errors) > 0

        # Check error details
        error = parser.errors[0]
        assert hasattr(error, 'message')
        assert hasattr(error, 'line')
        assert hasattr(error, 'column')
        assert "takes" in error.message.lower()  # Error about missing 'takes' keyword

    def test_parser_continues_parsing_after_error(self):
        """Test that parser continues after encountering an error."""
        code = """
function invalid takes // missing parameter list
endfunction

function valid takes nothing returns nothing
endfunction
"""
        parser = Parser(code)
        ast = parser.parse()

        # Should parse the valid function despite earlier error
        assert len(ast.functions) == 1
        assert ast.functions[0].name == "valid"

        # Should have collected error about invalid function
        assert len(parser.errors) >= 1

    def test_parser_provides_detailed_error_messages(self):
        """Test that parser provides detailed error messages with position."""
        code = """function test takes integer x real y returns nothing
endfunction"""
        parser = Parser(code)
        ast = parser.parse()

        # Should have error about missing comma
        assert len(parser.errors) >= 1

        # Find error about missing comma
        comma_errors = [e for e in parser.errors if "comma" in e.message.lower()]
        assert len(comma_errors) > 0, f"No comma error found in errors: {parser.errors}"
        error = comma_errors[0]

        # Error should have position information
        assert error.line == 1
        # Column should point to where comma is expected
        assert error.column > 0

        # Error message should be descriptive
        assert "comma" in error.message.lower() or "separator" in error.message.lower()

    def test_parser_handles_multiple_errors(self):
        """Test that parser can collect multiple errors."""
        code = """
function bad1 takes integer x real y returns nothing
endfunction

function bad2 takes nothing returns // missing return type
endfunction
"""
        parser = Parser(code)
        ast = parser.parse()

        # Should collect multiple errors
        assert len(parser.errors) >= 2


def test_parser_can_parse_local_declaration():
    """Test that parser can parse local variable declarations."""
    from jass_runner.parser.parser import Parser, LocalDecl

    code = """
    function test takes nothing returns nothing
        local integer x = 42
        local string name = "hello"
    endfunction
    """

    parser = Parser(code)
    ast = parser.parse()

    assert len(ast.functions) == 1
    func = ast.functions[0]
    assert func.name == 'test'
    assert func.body is not None
    assert len(func.body) == 2

    # Check first local declaration
    stmt1 = func.body[0]
    assert isinstance(stmt1, LocalDecl)
    assert stmt1.name == 'x'
    assert stmt1.type == 'integer'
    assert stmt1.value == 42

    # Check second local declaration
    stmt2 = func.body[1]
    assert isinstance(stmt2, LocalDecl)
    assert stmt2.name == 'name'
    assert stmt2.type == 'string'
    assert stmt2.value == 'hello'


def test_parse_simple_if_statement():
    """测试解析简单if语句"""
    from jass_runner.parser.parser import Parser, IfStmt

    code = """
    function main takes nothing returns nothing
        if true then
            call DisplayTextToPlayer("hello")
        endif
    endfunction
    """

    parser = Parser(code)
    ast = parser.parse()

    func = ast.functions[0]
    if_stmt = func.body[0]
    assert isinstance(if_stmt, IfStmt)
    assert if_stmt.condition == "true"
    assert len(if_stmt.then_body) == 1


def test_parse_if_else_statement():
    """测试解析if/else语句"""
    from jass_runner.parser.parser import Parser, IfStmt, NativeCallNode

    code = """
    function main takes nothing returns nothing
        if true then
            call A()
        else
            call B()
        endif
    endfunction
    """

    parser = Parser(code)
    ast = parser.parse()

    func = ast.functions[0]
    if_stmt = func.body[0]
    assert isinstance(if_stmt, IfStmt)
    assert if_stmt.condition == "true"
    assert len(if_stmt.then_body) == 1
    assert len(if_stmt.else_body) == 1

    # 验证then分支的调用
    then_call = if_stmt.then_body[0]
    assert isinstance(then_call, NativeCallNode)
    assert then_call.func_name == "A"

    # 验证else分支的调用
    else_call = if_stmt.else_body[0]
    assert isinstance(else_call, NativeCallNode)
    assert else_call.func_name == "B"


def test_parse_if_elseif_else_statement():
    """测试解析if/elseif/else语句"""
    from jass_runner.parser.parser import Parser, IfStmt, NativeCallNode

    code = """
    function main takes nothing returns nothing
        if x > 0 then
            call A()
        elseif x < 0 then
            call B()
        else
            call C()
        endif
    endfunction
    """

    parser = Parser(code)
    ast = parser.parse()

    func = ast.functions[0]
    if_stmt = func.body[0]
    assert isinstance(if_stmt, IfStmt)
    assert if_stmt.condition == "x > 0"
    assert len(if_stmt.then_body) == 1
    assert len(if_stmt.elseif_branches) == 1
    assert len(if_stmt.else_body) == 1

    # 验证elseif分支
    elseif_branch = if_stmt.elseif_branches[0]
    assert elseif_branch["condition"] == "x < 0"
    assert len(elseif_branch["body"]) == 1
    elseif_call = elseif_branch["body"][0]
    assert isinstance(elseif_call, NativeCallNode)
    assert elseif_call.func_name == "B"

    # 验证else分支的调用
    else_call = if_stmt.else_body[0]
    assert isinstance(else_call, NativeCallNode)
    assert else_call.func_name == "C"


def test_parse_nested_if_statement():
    """测试解析嵌套if语句"""
    from jass_runner.parser.parser import Parser, IfStmt, NativeCallNode

    code = """
    function main takes nothing returns nothing
        if x > 0 then
            if y > 0 then
                call A()
            endif
        endif
    endfunction
    """

    parser = Parser(code)
    ast = parser.parse()

    func = ast.functions[0]
    outer_if = func.body[0]
    assert isinstance(outer_if, IfStmt)
    assert outer_if.condition == "x > 0"

    # 验证内层if语句
    inner_if = outer_if.then_body[0]
    assert isinstance(inner_if, IfStmt)
    assert inner_if.condition == "y > 0"
    assert len(inner_if.then_body) == 1

    # 验证内层if中的调用
    inner_call = inner_if.then_body[0]
    assert isinstance(inner_call, NativeCallNode)
    assert inner_call.func_name == "A"


def test_parse_loop_statement():
    """测试解析loop语句"""
    from jass_runner.parser.parser import Parser, LoopStmt, NativeCallNode

    code = """
    function main takes nothing returns nothing
        loop
            call A()
        endloop
    endfunction
    """

    parser = Parser(code)
    ast = parser.parse()

    func = ast.functions[0]
    loop_stmt = func.body[0]
    assert isinstance(loop_stmt, LoopStmt)
    assert len(loop_stmt.body) == 1

    # 验证循环体内的调用
    call_stmt = loop_stmt.body[0]
    assert isinstance(call_stmt, NativeCallNode)
    assert call_stmt.func_name == "A"


def test_parse_loop_with_multiple_statements():
    """测试解析包含多个语句的loop"""
    from jass_runner.parser.parser import Parser, LoopStmt, NativeCallNode, SetStmt

    code = """
    function main takes nothing returns nothing
        loop
            call A()
            call B()
            set x = 1
        endloop
    endfunction
    """

    parser = Parser(code)
    ast = parser.parse()

    func = ast.functions[0]
    loop_stmt = func.body[0]
    assert isinstance(loop_stmt, LoopStmt)
    assert len(loop_stmt.body) == 3

    # 验证语句类型
    assert isinstance(loop_stmt.body[0], NativeCallNode)
    assert loop_stmt.body[0].func_name == "A"
    assert isinstance(loop_stmt.body[1], NativeCallNode)
    assert loop_stmt.body[1].func_name == "B"
    assert isinstance(loop_stmt.body[2], SetStmt)


def test_parse_nested_loop():
    """测试解析嵌套loop语句"""
    from jass_runner.parser.parser import Parser, LoopStmt, NativeCallNode

    code = """
    function main takes nothing returns nothing
        loop
            loop
                call A()
            endloop
        endloop
    endfunction
    """

    parser = Parser(code)
    ast = parser.parse()

    func = ast.functions[0]
    outer_loop = func.body[0]
    assert isinstance(outer_loop, LoopStmt)
    assert len(outer_loop.body) == 1

    # 验证内层loop
    inner_loop = outer_loop.body[0]
    assert isinstance(inner_loop, LoopStmt)
    assert len(inner_loop.body) == 1

    # 验证内层loop中的调用
    inner_call = inner_loop.body[0]
    assert isinstance(inner_call, NativeCallNode)
    assert inner_call.func_name == "A"