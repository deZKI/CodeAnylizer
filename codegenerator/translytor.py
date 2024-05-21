from syntatic.ast_node import ASTNode


class CodeGenerator:
    def __init__(self, ast: ASTNode):
        self.ast = ast
        self.generated_code = ""

    def generate(self) -> str:
        """
        Генерирует код на основе абстрактного синтаксического дерева.

        Возвращает:
            str: Сгенерированный код.
        """
        self._generate_node(self.ast)
        return self.generated_code

    def _generate_node(self, node: ASTNode):
        """
        Рекурсивно обходит узлы абстрактного синтаксического дерева и генерирует код.

        Параметры:
            node (ASTNode): Узел абстрактного синтаксического дерева.
        """
        if node.node_type == 'Program':
            for child in node.children:
                self._generate_node(child)
        elif node.node_type == 'VarDecl':
            self.generated_code += "Var "
            self._generate_node(node.children[0])  # IdentifierList
            self.generated_code = self.generated_code.rstrip(', ')
        elif node.node_type == 'IdList':
            for child in node.children:
                self._generate_node(child)  # Identifier
                self.generated_code += ", "
            self.generated_code = self.generated_code.rstrip(', ')
            self.generated_code += ";\n"
        elif node.node_type == 'Ident':
            self.generated_code += node.value
        elif node.node_type == 'AssignList':
            for child in node.children:
                self._generate_node(child)  # Assignment
        elif node.node_type == 'Assign':
            self._generate_node(node.children[0])  # Identifier
            self.generated_code += " = "
            self._generate_node(node.children[1])  # Expression
            self.generated_code += ";\n"
        elif node.node_type in ('BinOp', 'UnaryOp'):
            self._generate_node(node.children[0])
            if node.node_type == 'BinOp':
                self.generated_code += " " + node.value + " "
            if len(node.children) == 2:
                self._generate_node(node.children[1])
        elif node.node_type == 'Constant':
            self.generated_code += node.value
        else:
            raise ValueError("Unsupported node type: {}".format(node.node_type))
