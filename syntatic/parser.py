from lexer.models import TokenType, Token
from typing import Optional, Union, List

from syntatic.ast_node import ASTNode


class Parser:
    """
    Класс Parser выполняет синтаксический анализ списка токенов, генерируемых лексером.

    Атрибуты:
        tokens (list[Token]): Список токенов для синтаксического анализа.
        current_token_index (int): Индекс текущего токена в списке.
        graph (graphviz.Digraph): Граф для визуализации синтаксического дерева.
        node_counter (int): Счетчик узлов для уникальных идентификаторов.

    Методы:
        current_token: Возвращает текущий токен или None, если достигнут конец списка токенов.
        eat(token_type): Проверяет, соответствует ли текущий токен ожидаемому типу, и переходит к следующему токену.
        error(expected_type): Вызывает исключение с сообщением об ошибке, указывающим ожидаемый и фактический типы токенов.
        parse(): Запускает процесс синтаксического анализа и возвращает AST.
        program(): Обрабатывает правило <Программа> и возвращает узел AST.
        variable_declaration(): Обрабатывает правило <Объявление переменных> и возвращает узел AST.
        identifier_list(): Обрабатывает список идентификаторов и возвращает узел AST.
        identifier(): Обрабатывает один идентификатор и возвращает узел AST.
        assignment_list(): Обрабатывает список присваиваний и возвращает узел AST.
        assignment(): Обрабатывает одно присваивание и возвращает узел AST.
        expression(): Обрабатывает выражение и возвращает узел AST.
        term(): Обрабатывает терм в выражении и возвращает узел AST.
        factor(): Обрабатывает фактор в выражении и возвращает узел AST.
        generate_syntax_graph(filename): Генерирует и сохраняет синтаксический граф.
    """

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current_token_index = 0
        self.node_counter = 0

    @property
    def __current_token(self) -> Optional[Token]:
        """
        Возвращает текущий токен или None, если достигнут конец списка токенов.

        Возвращает:
            Optional[Token]: Текущий токен или None.
        """
        if self.current_token_index < len(self.tokens):
            return self.tokens[self.current_token_index]
        return None

    def __eat(self, token_type: TokenType, value=None):
        """
        Проверяет, соответствует ли текущий токен ожидаемому типу, и переходит к следующему токену.

        Параметры:
            token_type (TokenType): Ожидаемый тип токена.

        Вызывает:
            Exception: Если текущий токен не соответствует ожидаемому типу или достигнут конец списка токенов.
        """
        if self.__current_token and self.__current_token.t_type == token_type:
            if value and self.__current_token.value != value:
                self.__error(token_type, value)
            self.current_token_index += 1
        else:
            self.__error(token_type)

    def __error(self, expected_type: Union[TokenType, str], value=None):
        """
        Вызывает исключение с сообщением об ошибке, указывающим ожидаемый и фактический типы токенов.

        Параметры:
            expected_type (Union[TokenType, str]): Ожидаемый тип токена.

        Вызывает:
            Exception: С сообщением об ошибке.
        """
        if self.__current_token is None:
            raise Exception(f'Error: expected {expected_type}, but got end of input')
        else:
            if self.__current_token.t_type == expected_type and value!=None:
                raise Exception(
                    f'Error: expected {value}, got {self.__current_token.value} on the line {self.__current_token.line}')
            raise Exception(
                f'Error: expected {expected_type}, got {self.__current_token.t_type} on the line {self.__current_token.line}')

    def parse(self) -> ASTNode:
        """
        Запускает процесс синтаксического анализа, начиная с правила <Программа>.

        Возвращает:
            ASTNode: Корневой узел AST для программы.
        """
        return self.__program()

    def __program(self) -> ASTNode:
        """
        Обрабатывает правило <Программа>.

        Правило:
            <Программа> ::= <Объявление переменных> <Описание вычислений>

        Возвращает:
            ASTNode: Узел AST для <Программа>.

        Вызывает:
            error: Если синтаксический анализ не соответствует правилу.
        """
        node = ASTNode('Program', line=1)
        self.__eat(TokenType.KEYWORD, value="Var")  # Var
        node.add_child(self.__variable_declaration())
        self.__eat(TokenType.NEWLINE)  # NewLine
        self.__eat(TokenType.KEYWORD, value="Begin")  # Begin
        self.__eat(TokenType.NEWLINE)  # NewLine
        node.add_child(self.__assignment_list())
        self.__eat(TokenType.KEYWORD, value="End")  # End
        return node

    def __variable_declaration(self) -> ASTNode:
        """
        Обрабатывает правило <Объявление переменных>.

        Правило:
            <Объявление переменных> ::= Var <Список переменных>

        Возвращает:
            ASTNode: Узел AST для <Объявление переменных>.

        Вызывает:
            error: Если синтаксический анализ не соответствует правилу.
        """
        node = ASTNode('VarDecl', line=self.__current_token.line)
        node.add_child(self.__identifier_list())
        return node

    def __identifier_list(self) -> ASTNode:
        """
        Обрабатывает список идентификаторов.

        Правило:
            <Список переменных> ::= <Идент> | <Идент>, <Список переменных> | <Идент>; <Список переменных>

        Возвращает:
            ASTNode: Узел AST для <Список переменных>.

        Вызывает:
            error: Если синтаксический анализ не соответствует правилу.
        """
        node = ASTNode('IdList', line=1)
        node.add_child(self.__identifier())
        while self.__current_token and self.__current_token.t_type == TokenType.COMMA:
            self.__eat(TokenType.COMMA)
            node.add_child(self.__identifier())
        self.__eat(TokenType.SEMICOLON)
        return node

    def __identifier(self) -> ASTNode:
        """
        Обрабатывает один идентификатор.

        Правило:
            <Идент> ::= <Буква> <Идент> | <Буква>

        Возвращает:
            ASTNode: Узел AST для <Идент>.

        Вызывает:
            error: Если синтаксический анализ не соответствует правилу.
        """
        node_id = f'Ident{self.node_counter}'
        self.node_counter += 1
        node = ASTNode('Ident', value=self.__current_token.value, line=self.__current_token.line)
        self.__eat(TokenType.IDENTIFIER)
        return node

    def __assignment_list(self) -> ASTNode:
        """
        Обрабатывает список присваиваний.

        Правило:
            <Список присваиваний> ::= <Присваивание> | <Присваивание> <Список присваиваний>

        Возвращает:
            ASTNode: Узел AST для <Список присваиваний>.

        Вызывает:
            error: Если синтаксический анализ не соответствует правилу.
        """
        node = ASTNode('AssignList', line=self.__current_token.line)
        node.add_child(self.__assignment())
        while self.__current_token and self.__current_token.t_type == TokenType.IDENTIFIER:
            node.add_child(self.__assignment())
        return node

    def __assignment(self) -> ASTNode:
        """
        Обрабатывает одно присваивание.

        Правило:
            <Присваивание> ::= <Идент> = <Выражение> ;

        Возвращает:
            ASTNode: Узел AST для <Присваивание>.

        Вызывает:
            error: Если синтаксический анализ не соответствует правилу.
        """
        self.node_counter += 1
        node = ASTNode('Assign', line=self.__current_token.line)
        node.add_child(self.__identifier())
        self.__eat(TokenType.EQUAL)
        node.add_child(self.__expression())
        self.__eat(TokenType.SEMICOLON)
        self.__eat(TokenType.NEWLINE)  # NewLine
        return node

    def __expression(self) -> ASTNode:
        """
        Обрабатывает выражение.

        Правило:
            <Выражение> ::= <Подвыражение> { ("+" | "-") <Подвыражение> }*

        Возвращает:
            ASTNode: Узел AST для <Выражение>.

        Вызывает:
            error: Если синтаксический анализ не соответствует правилу.
        """
        node = self.__term()
        while self.__current_token and self.__current_token.t_type in (
                TokenType.BINARY_OPERATOR,) and self.__current_token.value in ('+', '-'):
            op_node = ASTNode('BinOp', value=self.__current_token.value, line=self.__current_token.line)
            self.__eat(self.__current_token.t_type)
            op_node.add_child(node)
            op_node.add_child(self.__term())
            node = op_node
        return node

    def __term(self) -> ASTNode:
        """
        Обрабатывает терм в выражении.

        Правило:
            <Подвыражение> ::= <Фактор> { ("*" | "/") <Фактор> }*

        Возвращает:
            ASTNode: Узел AST для <Подвыражение>.

        Вызывает:
            error: Если синтаксический анализ не соответствует правилу.
        """
        node = self.__factor()
        while self.__current_token and self.__current_token.t_type in (
                TokenType.BINARY_OPERATOR,) and self.__current_token.value in ('*', '/'):
            op_node = ASTNode('BinOp', value=self.__current_token.value, line=self.__current_token.line)
            self.__eat(self.__current_token.t_type)
            op_node.add_child(node)
            op_node.add_child(self.__factor())
            node = op_node
        return node

    def __factor(self) -> ASTNode:
        """
        Обрабатывает фактор в выражении.

        Правило:
            <Фактор> ::= <Идент> | <Константа> | "(" <Выражение> ")" | <Ун.оп.> <Фактор>

        Возвращает:
            ASTNode: Узел AST для <Фактор>.

        Вызывает:
            error: Если синтаксический анализ не соответствует правилу.
        """
        if self.__current_token.t_type == TokenType.LPAREN:
            self.__eat(TokenType.LPAREN)
            node = self.__expression()
            self.__eat(TokenType.RPAREN)
            return node
        elif self.__current_token.t_type == TokenType.UNARY_OPERATOR:
            node = ASTNode('UnaryOp', value=self.__current_token.value, line=self.__current_token.line)
            self.__eat(TokenType.UNARY_OPERATOR)
            node.add_child(self.__factor())
            return node
        elif self.__current_token.t_type == TokenType.IDENTIFIER:
            node = ASTNode('Ident', value=self.__current_token.value, line=self.__current_token.line)
            self.__eat(TokenType.IDENTIFIER)
            return node
        elif self.__current_token.t_type == TokenType.CONSTANT:
            node = ASTNode('Constant', value=self.__current_token.value, line=self.__current_token.line)
            self.__eat(TokenType.CONSTANT)
            return node
        else:
            self.__error("IDENTIFIER or CONSTANT")
