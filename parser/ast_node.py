from typing import Optional


class ASTNode:
    """
    Класс ASTNode представляет узел абстрактного синтаксического дерева.

    Атрибуты:
        node_type (str): Тип узла (например, 'Program', 'VarDecl').
        value (Optional[str]): Значение узла (например, имя переменной).
        children (List[ASTNode]): Список дочерних узлов.
    """

    def __init__(self, node_type: str, line: int, value: Optional[str] = None):
        self.node_type = node_type
        self.line = line
        self.value = value
        self.children = []

    def add_child(self, node: 'ASTNode'):
        self.children.append(node)

    def __str__(self):
        return self._print_tree()

    def _print_tree(self, level=0):
        result = '  ' * level + f'{self.node_type}'
        if self.value:
            result += f' ({self.value})'
        result += '\n'
        for child in self.children:
            result += child._print_tree(level + 1)
        return result

    def __repr__(self):
        return self.__str__()
