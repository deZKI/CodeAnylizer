from syntatic.parser import ASTNode

class SemanticAnalyzer:
    """
    Класс SemanticAnalyzer выполняет семантический анализ AST.

    Атрибуты:
        ast (ASTNode): Корневой узел AST.
        symbol_table (Dict[str, bool]): Таблица символов для хранения объявленных и инициализированных переменных.

    Методы:
        analyze(): Запускает процесс семантического анализа.
        visit(node): Посещает узел AST и вызывает соответствующий метод для узла.
        generic_visit(node): Посещает все дочерние узлы.
        visit_Program(node): Обрабатывает узел <Program>.
        visit_VarDecl(node): Обрабатывает узел <VarDecl>.
        visit_IdList(node): Обрабатывает узел <IdList>.
        visit_Ident(node): Обрабатывает узел <Ident>.
        visit_AssignList(node): Обрабатывает узел <AssignList>.
        visit_Assign(node): Обрабатывает узел <Assign>.
        visit_Expr(node): Обрабатывает узел <Expr>.
        visit_Term(node): Обрабатывает узел <Term>.
        visit_Factor(node): Обрабатывает узел <Factor>.
    """

    def __init__(self, ast: ASTNode):
        self.ast = ast
        self.symbol_table = {}
        self.initialized_vars = set()

        self.var_Visited = False  # переменная для отслеживания что посетили узел объявления переменных

    def analyze(self):
        """
        Запускает процесс семантического анализа.
        """
        self.visit(self.ast)

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
        self.generic_visit(node)
        self.var_Visited = True

    def visit_IdList(self, node: ASTNode):
        """
        Обрабатывает узел <IdList>.

        Параметры:
            node (ASTNode): Узел <IdList>.
        """
        for child in node.children:
            if child.value in self.symbol_table:
                raise Exception(f'Semantic Error: variable {child.value} redeclared on line {child.line}')
            self.symbol_table[child.value] = None  # Переменная объявлена, но не инициализирована
            self.visit(child)

    def visit_Ident(self, node: ASTNode):
        """
        Обрабатывает узел <Ident>.

        Параметры:
            node (ASTNode): Узел <Ident>.
        """
        if node.value not in self.symbol_table:
            raise Exception(f'Semantic Error: variable {node.value} not declared on line {node.line}')

        if node.value not in self.initialized_vars and self.var_Visited:
            raise Exception(f'Semantic Error: variable {node.value} not initialized on line {node.line}')

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
        ident_node = node.children[0]
        if ident_node.value not in self.symbol_table:
            raise Exception(f'Semantic Error: variable {ident_node.value} not declared on line {ident_node.line}')
        self.initialized_vars.add(ident_node.value)
        self.generic_visit(node)

    def visit_Expr(self, node: ASTNode):
        """
        Обрабатывает узел <Expr>.

        Параметры:
            node (ASTNode): Узел <Expr>.
        """
        self.generic_visit(node)

    def visit_Term(self, node: ASTNode):
        """
        Обрабатывает узел <Term>.

        Параметры:
            node (ASTNode): Узел <Term>.
        """
        self.generic_visit(node)

    def visit_Factor(self, node: ASTNode):
        """
        Обрабатывает узел <Factor>.

        Параметры:
            node (ASTNode): Узел <Factor>.
        """
        child = node.children[0]
        if child.node_type == 'Ident':
            if child.value not in self.symbol_table:
                raise Exception(f'Semantic Error: variable {child.value} not declared')
        self.generic_visit(node)
