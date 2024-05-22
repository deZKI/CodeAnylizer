from lexer.tokenizer import Tokenizer
from syntatic.parser import Parser
from semantic.analyzer import SemanticAnalyzer
from codegenerator.translytor import CodeGenerator

code = """
Var x, y, f;
Begin
    f := 54;
    x := 5; y := (x + 10) * 5 + f * 2;
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

    code = CodeGenerator(ast).generate()
    print(code)
