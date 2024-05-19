import unittest

from lexer.tokenizer import Tokenizer
from parser import Parser


class TestParser(unittest.TestCase):
    """
    Набор тестов для проверки синтаксического анализатора (Parser).
    Эти тесты охватывают различные сценарии, включая успешный разбор,
    синтаксические ошибки и ошибки, связанные с неожиданным окончанием входных данных.
    """

    @classmethod
    def setUpClass(cls):
        cls.tokenizer = Tokenizer()

    def test_variable_declaration(self):
        """
        Проверяет обработку объявления переменных.
        Код: "Var x, y;"
        Ожидаемый результат: Ошибка, так как ожидается новая строка после объявления переменных.
        Сообщение об ошибке: "Error: expected TokenType.NEWLINE, but got end of input"
        """
        code = "Var x, y;"
        tokens = self.tokenizer.tokenize(code)
        parser = Parser(tokens)
        with self.assertRaises(Exception) as cm:
            parser.parse()
        self.assertEqual(str(cm.exception), "Error: expected TokenType.NEWLINE, but got end of input")

    def test_assignment(self):
        """
        Проверяет обработку присваивания переменной.
        Код:
        Var x;
        Begin
            x := 5;
        End
        Ожидаемый результат: Успешный разбор без ошибок.
        """
        code = """
        Var x;
        Begin
            x := 5;
        End
        """
        tokens = self.tokenizer.tokenize(code)
        parser = Parser(tokens)
        try:
            parser.parse()
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Parser raised an exception unexpectedly: {e}")

    def test_expression(self):
        """
        Проверяет обработку выражения с унарным оператором и сложным арифметическим выражением.
        """
        code = """
        Var x;
        Begin
            x := -5 + (10 * 3);
        End
        """
        tokens = self.tokenizer.tokenize(code)
        parser = Parser(tokens)
        try:
            parser.parse()
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Parser raised an exception unexpectedly: {e}")

    def test_nested_expression(self):
        """
        Проверяет обработку вложенных выражений и использование переменных.
        """
        code = """
        Var x, y;
        Begin
            x := 5;
            y := -(x + 10) * 2;
        End
        """
        tokens = self.tokenizer.tokenize(code)
        parser = Parser(tokens)
        try:
            parser.parse()
            self.assertTrue(True)
        except Exception as e:
            print(e)
            self.fail(f"Parser raised an exception unexpectedly: {e}")

    def test_syntax_error(self):
        """
        Проверяет, что парсер правильно обрабатывает синтаксическую ошибку, связанную с отсутствием точки с запятой.
        """
        code = """
        Var x;
        Begin
            x := 5
        End
        """
        tokens = self.tokenizer.tokenize(code)
        parser = Parser(tokens)
        with self.assertRaises(Exception) as cm:
            parser.parse()
        self.assertEqual(str(cm.exception), "Error: expected TokenType.SEMICOLON, got TokenType.NEWLINE on the line 3")

    def test_end_of_input_error(self):
        """
        Проверяет обработку ситуации, когда конец ввода достигается раньше, чем ожидалось.
        """
        code = """
        Var x;
        Begin
            x := 5;
        """
        tokens = self.tokenizer.tokenize(code)
        parser = Parser(tokens)
        with self.assertRaises(Exception) as cm:
            parser.parse()
        self.assertEqual(str(cm.exception), "Error: expected TokenType.KEYWORD, but got end of input")

    def test_empty_program(self):
        """
        Проверяет обработку пустой программы.
        """
        code = ""
        tokens = self.tokenizer.tokenize(code)
        parser = Parser(tokens)
        with self.assertRaises(Exception) as cm:
            parser.parse()
        self.assertEqual(str(cm.exception), "Error: expected TokenType.KEYWORD, but got end of input")

    def test_missing_begin(self):
        """
        Проверяет обработку ситуации, когда отсутствует ключевое слово Begin.
        """
        code = """
        Var x;
        x := 5;
        End
        """
        tokens = self.tokenizer.tokenize(code)
        parser = Parser(tokens)
        with self.assertRaises(Exception) as cm:
            parser.parse()
        self.assertEqual(str(cm.exception), "Error: expected TokenType.KEYWORD, got TokenType.IDENTIFIER on the line 2")

    def test_missing_end(self):
        """
        Проверяет обработку ситуации, когда отсутствует ключевое слово End.
        """
        code = """
        Var x;
        Begin
            x := 5;
        """
        tokens = self.tokenizer.tokenize(code)
        parser = Parser(tokens)
        with self.assertRaises(Exception) as cm:
            parser.parse()
        self.assertEqual(str(cm.exception), "Error: expected TokenType.KEYWORD, but got end of input")

    def test_missing_var(self):
        """
        Проверяет обработку ситуации, когда отсутствует ключевое слово Var в начале программы.
        """
        code = """
        x := 5;
        Begin
            x := 5;
        End
        """
        tokens = self.tokenizer.tokenize(code)
        parser = Parser(tokens)
        with self.assertRaises(Exception) as cm:
            parser.parse()
        self.assertEqual(str(cm.exception), "Error: expected TokenType.KEYWORD, got TokenType.IDENTIFIER on the line 1")


if __name__ == '__main__':
    unittest.main()
