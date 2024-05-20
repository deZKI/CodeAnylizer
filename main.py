# Пример кода на вашем языке
from lexer.tokenizer import Tokenizer
from parser.parser import Parser
from semantic.analyzer import SemanticAnalyzer

code = """
Var x, y;
Begin
    x := 5;
    y := (x + 10) * 5 + 2 * 2;
End
"""

if __name__ == '__main__':

    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(code)

    # Парсинг токенов
    parser = Parser(tokens)
    ast = parser.parse()
    print(ast)

    semantic_analyzer = SemanticAnalyzer(ast)
    semantic_analyzer.analyze()