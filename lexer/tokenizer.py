import re
from lexer.models import Token, TokenType


class Tokenizer:

    @staticmethod
    def tokenize(code: str) -> list[Token]:
        tokens: list[Token] = []
        current_line = 1
        for mo in re.finditer(TokenType.build_regex(), code):
            kind = mo.lastgroup
            value = mo.group(kind)
            match kind:
                case 'MISMATCH':
                    raise RuntimeError(f'Недопустимое значение {value!r} на строке {current_line}')
                case 'SKIP':
                    continue
                case 'NEWLINE':
                    tokens.append(Token(TokenType[kind], value, current_line))
                    current_line += 1
                case 'UNARY_OPERATOR':
                    # Проверьте, является ли этот унарный оператор или бинарный
                    if (len(tokens) == 0 or
                        tokens[-1].t_type in [TokenType.SEMICOLON, TokenType.COMMA,
                                             TokenType.LPAREN, TokenType.BINARY_OPERATOR,
                                             TokenType.KEYWORD, TokenType.NEWLINE, TokenType.EQUAL]):
                        tokens.append(Token(TokenType.UNARY_OPERATOR, value, current_line))
                    else:
                        tokens.append(Token(TokenType.BINARY_OPERATOR, value, current_line))
                case _:
                    tokens.append(Token(TokenType[kind], value, current_line))
        return tokens
