from lexer.models import TokenType, Token
from typing import Optional, Union
import graphviz

class Parser:
    """
    Класс Parser выполняет синтаксический анализ списка токенов, генерируемых лексером.

    Атрибуты:
        tokens (list[Token]): Список токенов для синтаксического анализа.
        current_token_index (int): Индекс текущего токена в списке.
        graph (graphviz.Digraph): Граф для визуализации синтаксического дерева.

    Методы:
        current_token: Возвращает текущий токен или None, если достигнут конец списка токенов.
        eat(token_type): Проверяет, соответствует ли текущий токен ожидаемому типу, и переходит к следующему токену.
        error(expected_type): Вызывает исключение с сообщением об ошибке, указывающим ожидаемый и фактический типы токенов.
        parse(): Запускает процесс синтаксического анализа.
        program(): Обрабатывает правило <Программа>.
        variable_declaration(): Обрабатывает правило <Объявление переменных>.
        identifier_list(): Обрабатывает список идентификаторов.
        identifier(): Обрабатывает один идентификатор.
        assignment_list(): Обрабатывает список присваиваний.
        assignment(): Обрабатывает одно присваивание.
        expression(): Обрабатывает выражение.
        term(): Обрабатывает терм в выражении.
        factor(): Обрабатывает фактор в выражении.
        generate_syntax_graph(filename): Генерирует и сохраняет синтаксический граф.
    """

    def __init__(self, tokens: list[Token]):
        """
        Инициализирует объект Parser.

        Параметры:
            tokens (list[Token]): Список токенов для синтаксического анализа.
        """
        self.tokens = tokens
        self.current_token_index = 0
        self.graph = graphviz.Digraph(comment='Syntax Graph')
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

    def __eat(self, token_type: TokenType):
        """
        Проверяет, соответствует ли текущий токен ожидаемому типу, и переходит к следующему токену.

        Параметры:
            token_type (TokenType): Ожидаемый тип токена.

        Вызывает:
            Exception: Если текущий токен не соответствует ожидаемому типу или достигнут конец списка токенов.
        """
        if self.__current_token and self.__current_token.t_type == token_type:
            self.current_token_index += 1
        else:
            self.__error(token_type)

    def __error(self, expected_type: Union[TokenType, str]):
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
            raise Exception(
                f'Error: expected {expected_type}, got {self.__current_token.t_type} on the line {self.__current_token.line}')

    def parse(self):
        """
        Запускает процесс синтаксического анализа, начиная с правила <Программа>.

        Возвращает:
            Результат выполнения метода program().
        """
        return self.__program()

    def __program(self):
        """
        Обрабатывает правило <Программа>.

        Правило:
            <Программа> ::= <Объявление переменных> <Описание вычислений>

        Вызывает:
            error: Если синтаксический анализ не соответствует правилу.
        """
        self.graph.node('Program', '<Программа>')
        self.graph.edge('Program', 'Var')
        self.__eat(TokenType.KEYWORD)  # Var
        self.variable_declaration()
        self.__eat(TokenType.NEWLINE)  # NewLine
        self.graph.edge('Program', 'Begin')
        self.__eat(TokenType.KEYWORD)  # Begin
        self.__eat(TokenType.NEWLINE)  # NewLine
        self.assignment_list()
        self.__eat(TokenType.KEYWORD)  # End
        self.graph.edge('Program', 'End')

    def variable_declaration(self):
        """
        Обрабатывает правило <Объявление переменных>.

        Правило:
            <Объявление переменных> ::= Var <Список переменных>

        Вызывает:
            error: Если синтаксический анализ не соответствует правилу.
        """
        self.graph.node('VarDecl', '<Объявление переменных>')
        self.graph.edge('Var', 'VarDecl')
        self.identifier_list()

    def identifier_list(self):
        """
        Обрабатывает список идентификаторов.

        Правило:
            <Список переменных> ::= <Идент> | <Идент>, <Список переменных> | <Идент>; <Список переменных>

        Вызывает:
            error: Если синтаксический анализ не соответствует правилу.
        """
        self.graph.node('IdList', '<Список переменных>')
        self.graph.edge('VarDecl', 'IdList')
        self.identifier()
        while self.__current_token and self.__current_token.t_type == TokenType.COMMA:
            self.__eat(TokenType.COMMA)
            self.identifier()
        self.__eat(TokenType.SEMICOLON)

    def identifier(self):
        """
        Обрабатывает один идентификатор.

        Правило:
            <Идент> ::= <Буква> <Идент> | <Буква>

        Вызывает:
            error: Если синтаксический анализ не соответствует правилу.
        """
        node_id = f'Ident{self.node_counter}'
        self.graph.node(node_id, '<Идент>')
        self.graph.edge('IdList', node_id)
        self.node_counter += 1
        self.__eat(TokenType.IDENTIFIER)

    def assignment_list(self):
        """
        Обрабатывает список присваиваний.

        Правило:
            <Список присваиваний> ::= <Присваивание> | <Присваивание> <Список присваиваний>

        Вызывает:
            error: Если синтаксический анализ не соответствует правилу.
        """
        self.graph.node('AssignList', '<Список присваиваний>')
        self.graph.edge('Program', 'AssignList')
        self.assignment()
        while self.__current_token and self.__current_token.t_type == TokenType.IDENTIFIER:
            self.assignment()

    def assignment(self):
        """
        Обрабатывает одно присваивание.

        Правило:
            <Присваивание> ::= <Идент> := <Выражение> ;

        Вызывает:
            error: Если синтаксический анализ не соответствует правилу.
        """
        node_id = f'Assign{self.node_counter}'
        self.graph.node(node_id, '<Присваивание>')
        self.graph.edge('AssignList', node_id)
        self.node_counter += 1
        self.identifier()
        self.__eat(TokenType.EQUAL)
        self.expression()
        self.__eat(TokenType.SEMICOLON)
        self.__eat(TokenType.NEWLINE)  # NewLine

    def expression(self):
        """
        Обрабатывает выражение.

        Правило:
            <Выражение> ::= <Ун.оп.> <Подвыражение> | <Подвыражение>

        Вызывает:
            error: Если синтаксический анализ не соответствует правилу.
        """
        node_id = f'Expr{self.node_counter}'
        self.graph.node(node_id, '<Выражение>')
        self.graph.edge('Assign', node_id)
        self.node_counter += 1
        if self.__current_token and self.__current_token.t_type == TokenType.UNARY_OPERATOR:
            self.__eat(TokenType.UNARY_OPERATOR)
        self.term()

    def term(self):
        """
        Обрабатывает терм в выражении.

        Правило:
            <Подвыражение> ::= ( <Выражение> ) | <Операнд> | <Подвыражение> <Бин.оп.> <Подвыражение>

        Вызывает:
            error: Если синтаксический анализ не соответствует правилу.
        """
        node_id = f'Term{self.node_counter}'
        self.graph.node(node_id, '<Подвыражение>')
        self.graph.edge('Expr', node_id)
        self.node_counter += 1
        self.factor()
        while self.__current_token and self.__current_token.t_type in (TokenType.BINARY_OPERATOR,):
            self.__eat(self.__current_token.t_type)
            self.factor()

    def factor(self):
        """
        Обрабатывает фактор в выражении.

        Правило:
            <Операнд> ::= <Идент> | <Константа>

        Вызывает:
            error: Если синтаксический анализ не соответствует правилу.
        """
        node_id = f'Factor{self.node_counter}'
        self.graph.node(node_id, '<Операнд>')
        self.graph.edge('Term', node_id)
        self.node_counter += 1
        if self.__current_token.t_type == TokenType.LPAREN:
            self.__eat(TokenType.LPAREN)
            self.expression()
            self.__eat(TokenType.RPAREN)
        elif self.__current_token.t_type == TokenType.IDENTIFIER:
            self.__eat(TokenType.IDENTIFIER)
        elif self.__current_token.t_type == TokenType.CONSTANT:
            self.__eat(TokenType.CONSTANT)
        else:
            self.__error("IDENTIFIER or CONSTANT")

    def generate_syntax_graph(self, filename: str = 'syntax_graph'):
        """
        Генерирует и сохраняет синтаксический граф.

        Параметры:
            filename (str): Имя файла для сохранения графа.
        """
        self.parse()
        self.graph.render(filename, view=True)