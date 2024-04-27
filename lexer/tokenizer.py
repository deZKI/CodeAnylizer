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
                    raise RuntimeError(f'Не допустимое значение {value!r} на строке {current_line}')
                case 'SKIP':
                    continue
                case 'NEWLINE':
                    tokens.append(Token(TokenType[kind], value, current_line))
                    current_line += 1
                case _:
                    tokens.append(Token(TokenType[kind], value, current_line, ))
        return tokens
