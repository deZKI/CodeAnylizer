import dataclasses
from enum import Enum


class TokenType(Enum):
    KEYWORD = r'\b(Var|Begin|End)\b'  # Ключевые слова
    IDENTIFIER = r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'  # Идентификаторы
    EQUAL = r'='  # Присваивание
    UNARY_OPERATOR = r'-'  # Унарный оператор
    BINARY_OPERATOR = r'\+|-|\*|/'  # Бинарные операторы
    SEMICOLON = r';'  # Точка с запятой
    COMMA = r','  # Запятая
    LPAREN = r'\('  # Левая скобка
    RPAREN = r'\)'  # Правая скобка
    CONSTANT = r'\b\d+\b'  # Константа
    SKIP = r'[ \t]+'  # Пробелы и табуляция
    NEWLINE = r'\n'  # Новая строка
    MISMATCH = r'.'  # Любой другой символ

    def __eq__(self, other):
        return self.value == other.value

    @classmethod
    def build_regex(cls):
        """Собирает регулярное выражение из всех элементов перечисления."""
        return '|'.join(f'(?P<{member.name}>{member.value})' for member in cls)


@dataclasses.dataclass(slots=True)
class Token:
    t_type: TokenType
    value: str
    line: int

    def __str__(self):
        return f'Токен типа: {self.t_type.name} со значением: {self.value} на строке номер: {self.line}'

    def __eq__(self, other):
        return (self.t_type.name == other.t_type.name and
                self.value == other.value and
                self.line == other.line)
