"""
JASS parser implementation.

This module implements a recursive descent parser for JASS code.
It converts token streams from the lexer into an Abstract Syntax Tree (AST).
"""

from dataclasses import dataclass
from typing import List, Optional
from .lexer import Lexer, Token


@dataclass
class Parameter:
    """Function parameter node."""
    name: str
    type: str
    line: int  # Line number from token
    column: int  # Column number from token


@dataclass
class FunctionDecl:
    """Function declaration node."""
    name: str
    parameters: List[Parameter]
    return_type: str
    line: int
    column: int


@dataclass
class AST:
    """Abstract Syntax Tree root node."""
    functions: List[FunctionDecl]


class Parser:
    """Recursive descent parser for JASS code."""

    def __init__(self, code: str):
        """Initialize parser with JASS code.

        Args:
            code: JASS source code to parse
        """
        self.lexer = Lexer(code)
        self.tokens: List[Token] = []
        self.current_token: Optional[Token] = None
        self.token_index = 0

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
                self.skip_to_next_function()
                return None

            func_name = self.current_token.value
            self.next_token()

            # Match 'takes' keyword
            if not self.match_keyword('takes'):
                self.skip_to_next_function()
                return None

            # Parse parameter list
            parameters = self.parse_parameter_list()

            # Match 'returns' keyword
            if not self.match_keyword('returns'):
                self.skip_to_next_function()
                return None

            # Parse return type
            if self.current_token is None:
                self.skip_to_next_function()
                return None

            return_type = self.current_token.value
            self.next_token()

            # Create function declaration
            return FunctionDecl(
                name=func_name,
                parameters=parameters,
                return_type=return_type,
                line=start_line,
                column=start_column
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

        return parameters

    def parse_parameter(self) -> Optional[Parameter]:
        """Parse a single parameter.

        Returns:
            Parameter if successful, None if parsing failed
        """
        if self.current_token is None:
            return None

        # Parameter type
        param_type = self.current_token.value
        type_line = self.current_token.line
        type_column = self.current_token.column
        self.next_token()

        # Parameter name
        if (self.current_token is None
                or self.current_token.type != 'IDENTIFIER'):
            return None

        param_name = self.current_token.value
        self.next_token()

        return Parameter(
            name=param_name,
            type=param_type,
            line=type_line,
            column=type_column
        )

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
