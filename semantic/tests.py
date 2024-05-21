import unittest
from lexer.tokenizer import Tokenizer
from syntatic.parser import Parser

from semantic.analyzer import SemanticAnalyzer


class TestSemanticAnalyzer(unittest.TestCase):
    """
    Набор тестов для проверки семантического анализатора (SemanticAnalyzer).
    Эти тесты охватывают различные сценарии, включая успешный семантический анализ,
    ошибки при повторном объявлении переменных и использование необъявленных переменных.
    """

    @classmethod
    def setUpClass(cls):
        cls.tokenizer = Tokenizer()

    def test_variable_declaration_and_usage(self):
        """
        Проверяет, что объявленные переменные могут быть использованы без ошибок.
        Ожидаемый результат: Успешный разбор без ошибок.
        """
        code = """
        Var x, y;
        Begin
            x := 5;
            y := x + 10;
        End
        """
        tokens = self.tokenizer.tokenize(code)
        parser = Parser(tokens)
        ast = parser.parse()
        semantic_analyzer = SemanticAnalyzer(ast)
        try:
            semantic_analyzer.analyze()
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Semantic analyzer raised an exception unexpectedly: {e}")

    def test_undeclared_variable_usage(self):
        """
        Проверяет, что использование необъявленной переменной вызывает ошибку.
        Ожидаемый результат: Ошибка семантического анализа, так как переменная 'y' не объявлена.
        """
        code = """
        Var x;
        Begin
            y := 10;
        End
        """
        tokens = self.tokenizer.tokenize(code)
        parser = Parser(tokens)
        ast = parser.parse()
        semantic_analyzer = SemanticAnalyzer(ast)
        with self.assertRaises(Exception) as cm:
            semantic_analyzer.analyze()
        self.assertEqual(str(cm.exception), 'Semantic Error: variable y not declared on line 1')

    def test_redeclaration_of_variable(self):
        """
        Проверяет, что повторное объявление переменной вызывает ошибку.
        Ожидаемый результат: Ошибка семантического анализа, так как переменная 'x' объявлена дважды.
        """
        code = """
        Var x, x;
        Begin
            x := 10;
        End
        """
        tokens = self.tokenizer.tokenize(code)
        parser = Parser(tokens)
        ast = parser.parse()
        semantic_analyzer = SemanticAnalyzer(ast)
        with self.assertRaises(Exception) as cm:
            semantic_analyzer.analyze()
        self.assertEqual(str(cm.exception), 'Semantic Error: variable x redeclared on line 1')

    def test_constant_usage(self):
        """
        Проверяет, что использование константы в выражении работает корректно.
        Ожидаемый результат: Успешный разбор без ошибок.
        """
        code = """
        Var x;
        Begin
            x := 10;
        End
        """
        tokens = self.tokenizer.tokenize(code)
        parser = Parser(tokens)
        ast = parser.parse()
        semantic_analyzer = SemanticAnalyzer(ast)
        try:
            semantic_analyzer.analyze()
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Semantic analyzer raised an exception unexpectedly: {e}")


if __name__ == '__main__':
    unittest.main()
