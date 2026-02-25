"""
JASS parser implementation.

This module implements a recursive descent parser for JASS code.
It converts token streams from the lexer into an Abstract Syntax Tree (AST).
"""

from dataclasses import dataclass
from typing import List, Optional, Any
from .lexer import Lexer, Token


@dataclass
class ParseError:
    """Base class for parser errors."""
    message: str
    line: int
    column: int

    def __str__(self) -> str:
        return f"{self.message} at line {self.line}, column {self.column}"


@dataclass
class MissingKeywordError(ParseError):
    """Error when a required keyword is missing."""
    keyword: str

    def __str__(self) -> str:
        return (f"Missing keyword '{self.keyword}' {self.message} "
                f"at line {self.line}, column {self.column}")


@dataclass
class UnexpectedTokenError(ParseError):
    """Error when an unexpected token is encountered."""
    expected: str
    actual: str

    def __str__(self) -> str:
        return (f"Expected {self.expected}, got '{self.actual}' {self.message} "
                f"at line {self.line}, column {self.column}")


@dataclass
class ParameterError(ParseError):
    """Error in parameter list parsing."""
    pass


@dataclass
class Parameter:
    """Function parameter node."""
    """Function parameter node."""
    name: str
    type: str
    line: int  # Line number from token
    column: int  # Column number from token


@dataclass
class LocalDecl:
    """Represents a local variable declaration."""
    name: str
    type: str
    value: Any


@dataclass
class FunctionDecl:
    """Function declaration node."""
    name: str
    parameters: List[Parameter]
    return_type: str
    line: int
    column: int
    body: Optional[List[Any]] = None  # Now will contain statements


@dataclass
class AST:
    """Abstract Syntax Tree root node."""
    functions: List[FunctionDecl]


class Parser:
    """Recursive descent parser for JASS code."""

    # JASS type keywords that can appear in parameter lists
    TYPE_KEYWORDS = {
        'integer', 'real', 'string', 'boolean', 'code', 'handle', 'nothing'
    }

    def __init__(self, code: str):
        """Initialize parser with JASS code.

        Args:
            code: JASS source code to parse
        """
        self.lexer = Lexer(code)
        self.tokens: List[Token] = []
        self.current_token: Optional[Token] = None
        self.token_index = 0
        self.errors: List[ParseError] = []

    def parse(self) -> AST:
        """Parse the JASS code and return an AST.

        Returns:
            AST containing all parsed function declarations
        """
        # Get all tokens from lexer, filtering out whitespace and comments
        self.tokens = [
            token for token in self.lexer.tokenize()
            if token.type not in ('WHITESPACE', 'COMMENT', 'MULTILINE_COMMENT')
        ]

        if not self.tokens:
            return AST(functions=[])

        self.token_index = 0
        self.current_token = self.tokens[0] if self.tokens else None

        functions: List[FunctionDecl] = []

        # Main parsing loop: look for function declarations
        while self.current_token is not None:
            if (self.current_token.type == 'KEYWORD'
                    and self.current_token.value == 'function'):
                func = self.parse_function_declaration()
                if func is not None:
                    functions.append(func)
            else:
                self.next_token()

        return AST(functions=functions)

    def parse_function_declaration(self) -> Optional[FunctionDecl]:
        """Parse a function declaration.

        Returns:
            FunctionDecl if successful, None if parsing failed
        """
        # Store position for error reporting
        start_line = self.current_token.line
        start_column = self.current_token.column

        try:
            # Match 'function' keyword
            if not self.match_keyword('function'):
                return None

            # Parse function name
            if (self.current_token is None
                    or self.current_token.type != 'IDENTIFIER'):
                # Create error message
                if self.current_token is None:
                    error = UnexpectedTokenError(
                        message="Expected function name identifier, got end of input",
                        expected="identifier",
                        actual="end of input",
                        line=start_line,
                        column=start_column + len('function ')  # Approximate position
                    )
                else:
                    error = UnexpectedTokenError(
                        message="Expected function name identifier",
                        expected="identifier",
                        actual=self.current_token.value,
                        line=self.current_token.line,
                        column=self.current_token.column
                    )
                self.add_error(error)
                self.skip_to_next_function()
                return None

            func_name = self.current_token.value
            self.next_token()

            # Match 'takes' keyword
            if not self.match_keyword('takes'):
                # Create error for missing 'takes' keyword
                error_line = self.current_token.line if self.current_token else start_line
                error_column = self.current_token.column if self.current_token else start_column + len('function ') + len(func_name)
                error = MissingKeywordError(
                    message="Missing 'takes' keyword in function declaration",
                    keyword='takes',
                    line=error_line,
                    column=error_column
                )
                self.add_error(error)
                self.skip_to_next_function()
                return None

            # Parse parameter list
            parameters = self.parse_parameter_list()

            # Match 'returns' keyword
            if not self.match_keyword('returns'):
                # Create error for missing 'returns' keyword
                error_line = self.current_token.line if self.current_token else start_line
                # Approximate column: after function name, takes, and parameters
                error_column = self.current_token.column if self.current_token else start_column + len('function ') + len(func_name) + len(' takes ')  # Approximation
                error = MissingKeywordError(
                    message="Missing 'returns' keyword in function declaration",
                    keyword='returns',
                    line=error_line,
                    column=error_column
                )
                self.add_error(error)
                self.skip_to_next_function()
                return None

            # Parse return type
            if self.current_token is None:
                # Create error for missing return type
                error_line = start_line
                error_column = start_column + len('function ') + len(func_name) + len(' takes ')  # Approximation
                error = UnexpectedTokenError(
                    message="Expected return type, got end of input",
                    expected="return type (nothing, integer, real, string, boolean, code, handle)",
                    actual="end of input",
                    line=error_line,
                    column=error_column
                )
                self.add_error(error)
                self.skip_to_next_function()
                return None

            return_type = self.current_token.value
            self.next_token()

            # Parse function body
            body = []
            while self.current_token and not (self.current_token.type == 'KEYWORD' and self.current_token.value == 'endfunction'):
                statement = self.parse_statement()
                if statement:
                    body.append(statement)

            if self.current_token and self.current_token.value == 'endfunction':
                self.next_token()

            # Create function declaration
            return FunctionDecl(
                name=func_name,
                parameters=parameters,
                return_type=return_type,
                line=start_line,
                column=start_column,
                body=body
            )

        except Exception:
            # If any error occurs, skip to next function
            self.skip_to_next_function()
            return None

    def parse_parameter_list(self) -> List[Parameter]:
        """Parse a parameter list.

        Returns:
            List of Parameter objects
        """
        parameters: List[Parameter] = []

        # Check for 'nothing'
        if (self.current_token is not None
                and self.current_token.value == 'nothing'):
            self.next_token()
            return parameters

        # Parse first parameter
        param = self.parse_parameter()
        if param is not None:
            parameters.append(param)

        # Parse additional parameters separated by commas
        while (self.current_token is not None and
               self.current_token.value == ','):
            self.next_token()  # Skip comma
            param = self.parse_parameter()
            if param is not None:
                parameters.append(param)

        # Check for missing comma: if next token looks like a type keyword
        # (but not 'nothing' since that's handled above)
        if (self.current_token is not None and
                self.current_token.value in self.TYPE_KEYWORDS and
                self.current_token.value != 'nothing'):
            # Missing comma error
            error = ParseError(
                message=f"Missing comma between parameters, got '{self.current_token.value}'",
                line=self.current_token.line,
                column=self.current_token.column
            )
            self.add_error(error)
            # Try to recover by parsing this as another parameter
            # (skip the type token and expect a name, which will likely fail)
            # For now, just continue and let the parser handle it

        return parameters

    def parse_parameter(self) -> Optional[Parameter]:
        """Parse a single parameter.

        Returns:
            Parameter if successful, None if parsing failed
        """
        if self.current_token is None:
            # This shouldn't happen in normal parsing, but add error for safety
            self.add_error(ParseError(
                message="Unexpected end of input while parsing parameter",
                line=0,  # Unknown line
                column=0  # Unknown column
            ))
            return None

        # Parameter type
        param_type = self.current_token.value
        type_line = self.current_token.line
        type_column = self.current_token.column
        self.next_token()

        # Parameter name
        if (self.current_token is None
                or self.current_token.type != 'IDENTIFIER'):
            # Create error for missing parameter name
            if self.current_token is None:
                error = UnexpectedTokenError(
                    message="Expected parameter name, got end of input",
                    expected="identifier",
                    actual="end of input",
                    line=type_line,
                    column=type_column + len(param_type)  # Approximate position after type
                )
            else:
                error = UnexpectedTokenError(
                    message="Expected parameter name after type",
                    expected="identifier",
                    actual=self.current_token.value,
                    line=self.current_token.line,
                    column=self.current_token.column
                )
            self.add_error(error)
            return None

        param_name = self.current_token.value
        self.next_token()

        return Parameter(
            name=param_name,
            type=param_type,
            line=type_line,
            column=type_column
        )

    def add_error(self, error: ParseError) -> None:
        """Add an error to the error list."""
        self.errors.append(error)

    def match_keyword(self, keyword: str) -> bool:
        """Check if current token matches the given keyword.

        Args:
            keyword: Keyword to match

        Returns:
            True if matches, False otherwise
        """
        if (self.current_token is not None and
                self.current_token.type == 'KEYWORD' and
                self.current_token.value == keyword):
            self.next_token()
            return True
        return False

    def next_token(self) -> None:
        """Advance to the next token."""
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        else:
            self.current_token = None

    def skip_to_next_function(self) -> None:
        """Skip tokens until next function declaration or end of tokens."""
        while self.current_token is not None:
            if (self.current_token.type == 'KEYWORD'
                    and self.current_token.value == 'function'):
                return
            self.next_token()

    def parse_statement(self) -> Optional[Any]:
        """Parse a statement."""
        if not self.current_token:
            return None

        # Parse local declaration
        if self.current_token.type == 'KEYWORD' and self.current_token.value == 'local':
            return self.parse_local_declaration()

        # Skip other tokens for now
        self.next_token()
        return None

    def parse_local_declaration(self) -> Optional[LocalDecl]:
        """Parse a local variable declaration."""
        try:
            # Skip 'local' keyword
            self.next_token()

            # Get variable type (can be keyword like 'integer' or identifier)
            if not self.current_token:
                return None
            var_type = self.current_token.value
            self.next_token()

            # Get variable name
            if not self.current_token or self.current_token.type != 'IDENTIFIER':
                return None
            var_name = self.current_token.value
            self.next_token()

            # Check for assignment
            value = None
            if self.current_token and self.current_token.value == '=':
                self.next_token()
                # Parse expression (simplified)
                if self.current_token:
                    if self.current_token.type == 'NUMBER':
                        value = int(self.current_token.value)
                    elif self.current_token.type == 'STRING':
                        value = self.current_token.value[1:-1]  # Remove quotes
                    self.next_token()

            # Skip semicolon if present
            if self.current_token and self.current_token.value == ';':
                self.next_token()

            return LocalDecl(name=var_name, type=var_type, value=value)

        except Exception:
            return None
