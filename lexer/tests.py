import unittest

from lexer.tokenizer import Tokenizer
from lexer.models import Token, TokenType


class TestLexer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Настройка перед каждым тестом."""
        cls.lexer = Tokenizer()

    def test_basic_tokenization(self):
        """Тестирование базовой токенизации."""
        code = "Var x = 5;"
        expected_tokens = [
            Token(TokenType.KEYWORD, 'Var', 1),
            Token(TokenType.SKIP, ' ', 1),
            Token(TokenType.IDENTIFIER, 'x', 1),
            Token(TokenType.SKIP, ' ', 1),
            Token(TokenType.OPERATOR, '=', 1),
            Token(TokenType.SKIP, ' ', 1),
            Token(TokenType.CONSTANT, '5', 1),
            Token(TokenType.SEMICOLON, ';', 1)
        ]
        tokens = self.lexer.tokenize(code)
        self.assertEqual(tokens, expected_tokens)

    def test_error_handling(self):
        """Тестирование обработки ошибок при неверном символе."""
        code = "Var $x = 5;"
        with self.assertRaises(RuntimeError) as cm:
            self.lexer.tokenize(code)
        the_exception = cm.exception
        self.assertEqual(str(the_exception), 'Не допустимое значение \'$\' на строке 1')

    def test_line_counting(self):
        """Тестирование подсчета строк."""
        code = "Var x = 5;\nVar y = 10;"
        tokens = self.lexer.tokenize(code)
        last_token = tokens[-1]
        self.assertEqual(last_token.line, 2)  # Проверяем, что последний токен на второй строке

    def test_complex_expressions(self):
        """Тестирование обработки сложных арифметических выражений с учетом пробелов."""
        code = 'Var result = 15 + (42 / 6) - 7;'
        expected_tokens = [
            Token(TokenType.KEYWORD, 'Var', 1),
            Token(TokenType.SKIP, ' ', 1),  # Пробел после 'Var'
            Token(TokenType.IDENTIFIER, 'result', 1),
            Token(TokenType.SKIP, ' ', 1),  # Пробел перед '='
            Token(TokenType.OPERATOR, '=', 1),
            Token(TokenType.SKIP, ' ', 1),  # Пробел после '='
            Token(TokenType.CONSTANT, '15', 1),
            Token(TokenType.SKIP, ' ', 1),  # Пробел перед '+'
            Token(TokenType.OPERATOR, '+', 1),
            Token(TokenType.SKIP, ' ', 1),  # Пробел после '+'
            Token(TokenType.LPAREN, '(', 1),
            Token(TokenType.CONSTANT, '42', 1),
            Token(TokenType.SKIP, ' ', 1),  # Пробел перед '/'
            Token(TokenType.OPERATOR, '/', 1),
            Token(TokenType.SKIP, ' ', 1),  # Пробел после '/'
            Token(TokenType.CONSTANT, '6', 1),
            Token(TokenType.RPAREN, ')', 1),
            Token(TokenType.SKIP, ' ', 1),  # Пробел перед '-'
            Token(TokenType.OPERATOR, '-', 1),
            Token(TokenType.SKIP, ' ', 1),  # Пробел после '-'
            Token(TokenType.CONSTANT, '7', 1),
            Token(TokenType.SEMICOLON, ';', 1)
        ]
        tokens = self.lexer.tokenize(code)
        self.assertEqual(tokens, expected_tokens)

    def test_unary_operators(self):
        code = "Var a = -5; b = -(10 + 3);"
        expected_tokens = [
            Token(TokenType.KEYWORD, 'Var', 1),
            Token(TokenType.SKIP, ' ', 1),
            Token(TokenType.IDENTIFIER, 'a', 1),
            Token(TokenType.SKIP, ' ', 1),
            Token(TokenType.OPERATOR, '=', 1),
            Token(TokenType.SKIP, ' ', 1),
            Token(TokenType.OPERATOR, '-', 1),  # Унарный минус перед числом
            Token(TokenType.CONSTANT, '5', 1),
            Token(TokenType.SEMICOLON, ';', 1),
            Token(TokenType.SKIP, ' ', 1),
            Token(TokenType.IDENTIFIER, 'b', 1),
            Token(TokenType.SKIP, ' ', 1),
            Token(TokenType.OPERATOR, '=', 1),
            Token(TokenType.SKIP, ' ', 1),
            Token(TokenType.OPERATOR, '-', 1),  # Унарный минус перед скобкой
            Token(TokenType.LPAREN, '(', 1),
            Token(TokenType.CONSTANT, '10', 1),
            Token(TokenType.SKIP, ' ', 1),
            Token(TokenType.OPERATOR, '+', 1),
            Token(TokenType.SKIP, ' ', 1),
            Token(TokenType.CONSTANT, '3', 1),
            Token(TokenType.RPAREN, ')', 1),
            Token(TokenType.SEMICOLON, ';', 1)
        ]

        result_tokens = self.lexer.tokenize(code)
        self.assertEqual(result_tokens, expected_tokens)

    def test_multi_line_program(self):
        code = """
           Var x = 10;
           Begin
               x = -x + 1;
           End
           """
        expected_tokens_types = [
            TokenType.NEWLINE,
            TokenType.SKIP,
            TokenType.KEYWORD,
            TokenType.SKIP,
            TokenType.IDENTIFIER,
            TokenType.SKIP,
            TokenType.OPERATOR,
            TokenType.SKIP,
            TokenType.CONSTANT,
            TokenType.SEMICOLON,
            TokenType.NEWLINE,
            TokenType.SKIP,
            TokenType.KEYWORD,
            TokenType.NEWLINE,
            TokenType.SKIP,
            TokenType.IDENTIFIER,
            TokenType.SKIP,
            TokenType.OPERATOR,
            TokenType.SKIP,
            TokenType.OPERATOR,
            TokenType.IDENTIFIER,
            TokenType.SKIP,
            TokenType.OPERATOR,
            TokenType.SKIP,
            TokenType.CONSTANT,
            TokenType.SEMICOLON,
            TokenType.NEWLINE,
            TokenType.SKIP,
            TokenType.KEYWORD,
            TokenType.NEWLINE,
            TokenType.SKIP
        ]
        result_tokens_types = [token.t_type for token in self.lexer.tokenize(code)]
        self.assertEqual(result_tokens_types, expected_tokens_types)

# Запуск тестов
if __name__ == '__main__':
    unittest.main()
