# Пример кода на вашем языке
from lexer.tokenizer import Tokenizer
from parser.parser import Parser

code = """
Var x, y;
Begin
    x := 5;
    y := x + 10;
End
"""

if __name__ == '__main__':

    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(code)

    # Парсинг токенов
    parser = Parser(tokens)
    parser.generate_syntax_graph('syntax_graph')
