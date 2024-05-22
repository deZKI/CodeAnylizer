import unittest

from lexer.tokenizer import Tokenizer
from syntatic.parser import Parser
from semantic.analyzer import SemanticAnalyzer
from codegenerator.translytor import CodeGenerator


class TestCodeGenerator(unittest.TestCase):
    """
    Набор тестов для проверки генератора кода (CodeGenerator).
    Эти тесты охватывают различные сценарии, включая успешную генерацию кода,
    ошибки при семантическом анализе и корректность преобразования в целевой язык.
    """

    @classmethod
    def setUpClass(cls):
        cls.tokenizer = Tokenizer()

    def test_variable_declaration_and_usage(self):
        """
        Проверяет, что объявленные переменные могут быть использованы без ошибок,
        и генерируется правильный код.
        Ожидаемый результат: Правильный код на целевом языке.
        """
        code = """
        Var x, y;
        Begin
            x := 5;
            y := x + 10;
        End
        """
        expected_code = "Var x, y;\nx = 5;\ny = x + 10;\n"

        tokens = self.tokenizer.tokenize(code)
        parser = Parser(tokens)
        ast = parser.parse()
        semantic_analyzer = SemanticAnalyzer(ast)
        semantic_analyzer.analyze()
        code_generator = CodeGenerator(ast)
        generated_code = code_generator.generate()

        self.assertEqual(generated_code, expected_code)

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
        self.assertEqual(str(cm.exception), 'Semantic Error: variable y not declared on line 3')

    def test_constant_usage(self):
        """
        Проверяет, что использование константы в выражении работает корректно и генерируется правильный код.
        Ожидаемый результат: Правильный код на целевом языке.
        """
        code = """
        Var x;
        Begin
            x := 10 + 1;
        End
        """
        expected_code = "Var x;\nx = 10 + 1;\n"

        tokens = self.tokenizer.tokenize(code)
        parser = Parser(tokens)
        ast = parser.parse()
        semantic_analyzer = SemanticAnalyzer(ast)
        semantic_analyzer.analyze()
        code_generator = CodeGenerator(ast)
        generated_code = code_generator.generate()

        self.assertEqual(generated_code, expected_code)


if __name__ == '__main__':
    unittest.main()
