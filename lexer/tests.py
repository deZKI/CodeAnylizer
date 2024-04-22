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


# Запуск тестов
if __name__ == '__main__':
    unittest.main()
