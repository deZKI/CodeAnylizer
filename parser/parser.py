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
        self.__eat(TokenType.KEYWORD)  # Var
        self.variable_declaration()
        self.__eat(TokenType.NEWLINE)  # NewLine
        self.__eat(TokenType.KEYWORD)  # Begin
        self.__eat(TokenType.NEWLINE)  # NewLine
        self.__assignment_list()
        self.__eat(TokenType.KEYWORD)  # End

    def variable_declaration(self):
        """
        Обрабатывает правило <Объявление переменных>.

        Правило:
            <Объявление переменных> ::= Var <Список переменных>

        Вызывает:
            error: Если синтаксический анализ не соответствует правилу.
        """
        self.__identifier_list()

    def __identifier_list(self):
        """
        Обрабатывает список идентификаторов.

        Правило:
            <Список переменных> ::= <Идент> | <Идент>, <Список переменных> | <Идент>; <Список переменных>

        Вызывает:
            error: Если синтаксический анализ не соответствует правилу.
        """
        self.__identifier()
        while self.__current_token and self.__current_token.t_type == TokenType.COMMA:
            self.__eat(TokenType.COMMA)
            self.__identifier()
        self.__eat(TokenType.SEMICOLON)

    def __identifier(self):
        """
        Обрабатывает один идентификатор.

        Правило:
            <Идент> ::= <Буква> <Идент> | <Буква>

        Вызывает:
            error: Если синтаксический анализ не соответствует правилу.
        """
        self.__eat(TokenType.IDENTIFIER)

    def __assignment_list(self):
        """
        Обрабатывает список присваиваний.

        Правило:
            <Список присваиваний> ::= <Присваивание> | <Присваивание> <Список присваиваний>

        Вызывает:
            error: Если синтаксический анализ не соответствует правилу.
        """
        self.__assignment()
        while self.__current_token and self.__current_token.t_type == TokenType.IDENTIFIER:
            self.__assignment()

    def __assignment(self):
        """
        Обрабатывает одно присваивание.

        Правило:
            <Присваивание> ::= <Идент> := <Выражение> ;

        Вызывает:
            error: Если синтаксический анализ не соответствует правилу.
        """
        self.__identifier()
        self.__eat(TokenType.EQUAL)
        self.__expression()
        self.__eat(TokenType.SEMICOLON)
        self.__eat(TokenType.NEWLINE)  # NewLine

    def __expression(self):
        """
        Обрабатывает выражение.

        Правило:
            <Выражение> ::= <Ун.оп.> <Подвыражение> | <Подвыражение>

        Вызывает:
            error: Если синтаксический анализ не соответствует правилу.
        """
        if self.__current_token and self.__current_token.t_type == TokenType.UNARY_OPERATOR:
            self.__eat(TokenType.UNARY_OPERATOR)
        self.__term()

    def __term(self):
        """
        Обрабатывает терм в выражении.

        Правило:
            <Подвыражение> ::= ( <Выражение> ) | <Операнд> | <Подвыражение> <Бин.оп.> <Подвыражение>

        Вызывает:
            error: Если синтаксический анализ не соответствует правилу.
        """
        self.__factor()
        while self.__current_token and self.__current_token.t_type in (TokenType.BINARY_OPERATOR,):
            self.__eat(self.__current_token.t_type)
            self.__factor()

    def __factor(self):
        """
        Обрабатывает фактор в выражении.

        Правило:
            <Операнд> ::= <Идент> | <Константа>

        Вызывает:
            error: Если синтаксический анализ не соответствует правилу.
        """
        if self.__current_token.t_type == TokenType.LPAREN:
            self.__eat(TokenType.LPAREN)
            self.__expression()
            self.__eat(TokenType.RPAREN)
        elif self.__current_token.t_type == TokenType.IDENTIFIER:
            self.__eat(TokenType.IDENTIFIER)
        elif self.__current_token.t_type == TokenType.CONSTANT:
            self.__eat(TokenType.CONSTANT)
        else:
            self.__error("IDENTIFIER or CONSTANT")
