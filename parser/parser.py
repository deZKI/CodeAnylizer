from lexer.models import TokenType, Token
from typing import Optional, Union


class Parser:
    """
    Класс Parser выполняет синтаксический анализ списка токенов, генерируемых лексером.

    Атрибуты:
        tokens (list[Token]): Список токенов для синтаксического анализа.
        current_token_index (int): Индекс текущего токена в списке.

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
    """

    def __init__(self, tokens: list[Token]):
        """
        Инициализирует объект Parser.

        Параметры:
            tokens (list[Token]): Список токенов для синтаксического анализа.
        """
        self.tokens = tokens
        self.current_token_index = 0

    @property
    def current_token(self) -> Optional[Token]:
        """
        Возвращает текущий токен или None, если достигнут конец списка токенов.

        Возвращает:
            Optional[Token]: Текущий токен или None.
        """
        if self.current_token_index < len(self.tokens):
            return self.tokens[self.current_token_index]
        return None

    def eat(self, token_type: TokenType):
        """
        Проверяет, соответствует ли текущий токен ожидаемому типу, и переходит к следующему токену.

        Параметры:
            token_type (TokenType): Ожидаемый тип токена.

        Вызывает:
            Exception: Если текущий токен не соответствует ожидаемому типу или достигнут конец списка токенов.
        """
        if self.current_token and self.current_token.t_type == token_type:
            self.current_token_index += 1
        else:
            self.error(token_type)

    def error(self, expected_type: Union[TokenType, str]):
        """
        Вызывает исключение с сообщением об ошибке, указывающим ожидаемый и фактический типы токенов.

        Параметры:
            expected_type (Union[TokenType, str]): Ожидаемый тип токена.

        Вызывает:
            Exception: С сообщением об ошибке.
        """
        if self.current_token is None:
            raise Exception(f'Error: expected {expected_type}, but got end of input')
        else:
            raise Exception(
                f'Error: expected {expected_type}, got {self.current_token.t_type} on the line {self.current_token.line}')

    def parse(self):
        """
        Запускает процесс синтаксического анализа, начиная с правила <Программа>.

        Возвращает:
            Результат выполнения метода program().
        """
        return self.program()

    def program(self):
        """
        Обрабатывает правило <Программа>.

        Правило:
            <Программа> ::= <Объявление переменных> <Описание вычислений>

        Вызывает:
            error: Если синтаксический анализ не соответствует правилу.
        """
        self.eat(TokenType.KEYWORD)  # Var
        self.variable_declaration()
        self.eat(TokenType.NEWLINE)  # NewLine
        self.eat(TokenType.KEYWORD)  # Begin
        self.eat(TokenType.NEWLINE)  # NewLine
        self.assignment_list()
        self.eat(TokenType.KEYWORD)  # End

    def variable_declaration(self):
        """
        Обрабатывает правило <Объявление переменных>.

        Правило:
            <Объявление переменных> ::= Var <Список переменных>

        Вызывает:
            error: Если синтаксический анализ не соответствует правилу.
        """
        self.identifier_list()

    def identifier_list(self):
        """
        Обрабатывает список идентификаторов.

        Правило:
            <Список переменных> ::= <Идент> | <Идент>, <Список переменных> | <Идент>; <Список переменных>

        Вызывает:
            error: Если синтаксический анализ не соответствует правилу.
        """
        self.identifier()
        while self.current_token and self.current_token.t_type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            self.identifier()
        self.eat(TokenType.SEMICOLON)

    def identifier(self):
        """
        Обрабатывает один идентификатор.

        Правило:
            <Идент> ::= <Буква> <Идент> | <Буква>

        Вызывает:
            error: Если синтаксический анализ не соответствует правилу.
        """
        self.eat(TokenType.IDENTIFIER)

    def assignment_list(self):
        """
        Обрабатывает список присваиваний.

        Правило:
            <Список присваиваний> ::= <Присваивание> | <Присваивание> <Список присваиваний>

        Вызывает:
            error: Если синтаксический анализ не соответствует правилу.
        """
        self.assignment()
        while self.current_token and self.current_token.t_type == TokenType.IDENTIFIER:
            self.assignment()

    def assignment(self):
        """
        Обрабатывает одно присваивание.

        Правило:
            <Присваивание> ::= <Идент> := <Выражение> ;

        Вызывает:
            error: Если синтаксический анализ не соответствует правилу.
        """
        self.identifier()
        self.eat(TokenType.EQUAL)
        self.expression()
        self.eat(TokenType.SEMICOLON)
        self.eat(TokenType.NEWLINE)  # NewLine

    def expression(self):
        """
        Обрабатывает выражение.

        Правило:
            <Выражение> ::= <Ун.оп.> <Подвыражение> | <Подвыражение>

        Вызывает:
            error: Если синтаксический анализ не соответствует правилу.
        """
        if self.current_token and self.current_token.t_type == TokenType.UNARY_OPERATOR:
            self.eat(TokenType.UNARY_OPERATOR)
        self.term()

    def term(self):
        """
        Обрабатывает терм в выражении.

        Правило:
            <Подвыражение> ::= ( <Выражение> ) | <Операнд> | <Подвыражение> <Бин.оп.> <Подвыражение>

        Вызывает:
            error: Если синтаксический анализ не соответствует правилу.
        """
        self.factor()
        while self.current_token and self.current_token.t_type in (TokenType.BINARY_OPERATOR,):
            self.eat(self.current_token.t_type)
            self.factor()

    def factor(self):
        """
        Обрабатывает фактор в выражении.

        Правило:
            <Операнд> ::= <Идент> | <Константа>

        Вызывает:
            error: Если синтаксический анализ не соответствует правилу.
        """
        if self.current_token.t_type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            self.expression()
            self.eat(TokenType.RPAREN)
        elif self.current_token.t_type == TokenType.IDENTIFIER:
            self.eat(TokenType.IDENTIFIER)
        elif self.current_token.t_type == TokenType.CONSTANT:
            self.eat(TokenType.CONSTANT)
        else:
            self.error("IDENTIFIER or CONSTANT")
