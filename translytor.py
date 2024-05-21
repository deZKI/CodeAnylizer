from lexer.tokenizer import Tokenizer
from parser.parser import Parser, ASTNode
from semantic.analyzer import SemanticAnalyzer


class CodeGenerator:
    """
    Класс CodeGenerator выполняет генерацию кода на целевом языке на основе AST.

    Атрибуты:
        ast (ASTNode): Корневой узел AST.
        code (List[str]): Список строк сгенерированного кода.

    Методы:
        generate(): Запускает процесс генерации кода.
        visit(node): Посещает узел AST и вызывает соответствующий метод для узла.
        generic_visit(node): Посещает все дочерние узлы.
        visit_Program(node): Обрабатывает узел <Program>.
        visit_VarDecl(node): Обрабатывает узел <VarDecl>.
        visit_IdList(node): Обрабатывает узел <IdList>.
        visit_AssignList(node): Обрабатывает узел <AssignList>.
        visit_Assign(node): Обрабатывает узел <Assign>.
        visit_Expr(node): Обрабатывает узел <Expr>.
        visit_Term(node): Обрабатывает узел <Term>.
        visit_Factor(node): Обрабатывает узел <Factor>.
    """
    def __init__(self, ast: ASTNode):
        self.ast = ast
        self.code = []

    def generate(self) -> str:
        """
        Запускает процесс генерации кода.

        Возвращает:
            str: Сгенерированный код.
        """
        self.visit(self.ast)
        return '\n'.join(self.code)

    def visit(self, node: ASTNode):
        """
        Посещает узел AST и вызывает соответствующий метод для узла.

        Параметры:
            node (ASTNode): Узел AST.
        """
        method_name = 'visit_' + node.node_type
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node: ASTNode):
        """
        Посещает все дочерние узлы.

        Параметры:
            node (ASTNode): Узел AST.
        """
        for child in node.children:
            self.visit(child)

    def visit_Program(self, node: ASTNode):
        """
        Обрабатывает узел <Program>.

        Параметры:
            node (ASTNode): Узел <Program>.
        """
        self.generic_visit(node)

    def visit_VarDecl(self, node: ASTNode):
        """
        Обрабатывает узел <VarDecl>.

        Параметры:
            node (ASTNode): Узел <VarDecl>.
        """
        self.code.append('Var ')
        self.visit(node.children[0])
        self.code[-1] += ';'  # Добавляем точку с запятой в конце объявления переменных

    def visit_IdList(self, node: ASTNode):
        """
        Обрабатывает узел <IdList>.

        Параметры:
            node (ASTNode): Узел <IdList>.
        """
        idents = []
        for child in node.children:
            if child.node_type == 'Ident':
                idents.append(child.value)
            elif child.node_type == 'IdList':
                idents.append(self.visit(child))
        self.code[-1] += ', '.join(idents)  # Добавляем идентификаторы в строку объявления переменных

    def visit_AssignList(self, node: ASTNode):
        """
        Обрабатывает узел <AssignList>.

        Параметры:
            node (ASTNode): Узел <AssignList>.
        """
        self.generic_visit(node)

    def visit_Assign(self, node: ASTNode):
        """
        Обрабатывает узел <Assign>.

        Параметры:
            node (ASTNode): Узел <Assign>.
        """
        self.visit(node.children[0])
        self.code.append(' = ')
        self.visit(node.children[1])
        self.code[-1] += ';'

    def visit_Expr(self, node: ASTNode):
        """
        Обрабатывает узел <Expr>.

        Параметры:
            node (ASTNode): Узел <Expr>.
        """
        if len(node.children) == 2:
            self.visit(node.children[0])
            self.visit(node.children[1])
        else:
            self.visit(node.children[0])

    def visit_Term(self, node: ASTNode):
        """
        Обрабатывает узел <Term>.

        Параметры:
            node (ASTNode): Узел <Term>.
        """
        if len(node.children) == 3:
            self.visit(node.children[0])
            self.code.append(' ')
            self.code.append(node.value)
            self.code.append(' ')
            self.visit(node.children[2])
        else:
            self.visit(node.children[0])

    def visit_Factor(self, node: ASTNode):
        """
        Обрабатывает узел <Factor>.

        Параметры:
            node (ASTNode): Узел <Factor>.
        """
        if node.children[0].node_type == 'Ident':
            self.code.append(node.children[0].value)
        elif node.children[0].node_type == 'Constant':
            self.code.append(node.children[0].value)
        elif node.children[0].node_type == 'Expr':
            self.code.append('(')
            self.visit(node.children[0])
            self.code.append(')')

# Пример использования лексера, парсера, семантического анализатора и генератора кода
code = """
Var x, y;
Begin
    x := -5 + (10 * 3);
    y := x - 2;
End
"""

tokens = Tokenizer().tokenize(code)
parser = Parser(tokens)
ast = parser.parse()

semantic_analyzer = SemanticAnalyzer(ast)
semantic_analyzer.analyze()

code_generator = CodeGenerator(ast)
generated_code = code_generator.generate()
print(generated_code)

