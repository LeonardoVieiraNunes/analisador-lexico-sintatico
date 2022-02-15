WHITE_SPACE = ' \n\t'


class Node:
    parent_node: any
    node_left: any
    node_right: any
    data: str
    nullable: None
    first_pos: None
    last_pos: None
    open_parenthesis = False
    is_root = False

    def __init__(self, data_value: str):
        self.data = data_value

    def __repr__(self):
        if self.data == '*':
            # return '*'
            if hasattr(self, 'node_right'):
                return f"({self.node_right.data})*"
            else:
                return ')*'
        elif self.data == '|':
            if not hasattr(self, 'node_left') and not hasattr(self, 'node_right'):
                return '|'
            elif not hasattr(self, 'node_left'):
                return f"|{self.node_right}"
            else:
                return f"{self.node_left}|{self.node_right}"
        elif self.data == 'concat':
            if not hasattr(self, 'node_left') and not hasattr(self, 'node_right'):
                return 'º'
            elif not hasattr(self, 'node_left'):
                return f"º{self.node_right}"
            else:
                return f"{self.node_left}º{self.node_right}"
        else:
            if self.data not in ['*', '|', 'concat', '(', ')']:
                return self.data
            else:
                return ""


class Tree:
    root_node = None
    current_node = None

    def __init__(self, text: str):
        self.root_node = Node('#')
        self.root_node.is_root = True
        self.current_node = self.root_node
        self.current_char = None
        self.text = reversed(text)
        self.advance()
        self.next_()

    def advance(self):
        try:
            self.current_char = next(self.text)
        except StopIteration:
            self.current_char = None

    def next_(self):
        while self.current_char is not None:
            if self.current_char in WHITE_SPACE:
                self.advance()
            elif self.current_char == '(':
                self.operate_close_parenthesis()
            else:
                print("antes", self.current_char)
                self.process_input()
                self.advance()

    def process_input(self):
        if self.current_node.data == '#':
            self.operate_hashtag()
        elif self.current_node.data == '*':
            self.operate_star()
        elif self.current_node.data == 'concat':
            self.operate_concat()
        elif self.current_node.data == '|':
            self.operate_union()
        else:
            self.operate_char()

    def operate_hashtag(self):
        if self.current_char == ')':
            new_node = Node('concat')
            new_node.is_root = True
            new_node.open_parenthesis = True
            new_node.node_right = self.current_node
            self.current_node.parent_node = new_node
            self.current_node = new_node
            self.root_node = new_node
        elif self.current_char == '*':
            new_node = Node('concat')
            new_node.is_root = True
            new_node.node_right = self.current_node
            self.current_node.parent_node = new_node
            self.current_node = new_node
            self.root_node = new_node
            new_node = Node('*')
            new_node.parent_node = self.current_node
            self.current_node.node_left = new_node
            self.current_node = new_node
        else:
            new_node = Node('concat')
            new_node.is_root = True
            new_node.node_right = self.current_node
            self.current_node.parent_node = new_node
            self.current_node = new_node
            self.root_node = new_node
            new_node = Node(self.current_char)
            new_node.parent_node = self.current_node
            self.current_node.node_left = new_node
            self.current_node = new_node

    def operate_star(self):
        if self.current_char == ')':
            self.current_node.open_parenthesis = True
        else:
            if not self.current_node.open_parenthesis and not hasattr(self.current_node, 'node_right'):
                new_node = Node(self.current_char)
                self.current_node.node_right = new_node
                new_node.parent_node = self.current_node
            elif self.current_node.open_parenthesis and not hasattr(self.current_node, 'node_right'):
                new_node = Node(self.current_char)
                new_node.parent_node = self.current_node
                self.current_node.node_right = new_node
                self.current_node = new_node
            else:
                new_node = Node('concat')
                new_node.parent_node = self.current_node.parent_node
                new_node.node_right = self.current_node
                self.update_parent_son(self.current_node.parent_node, new_node)
                self.current_node.parent_node = new_node
                self.current_node = new_node
                new_node2 = Node(self.current_char)
                new_node2.parent_node = self.current_node
                self.current_node.node_left = new_node2
                self.current_node = new_node2

    def operate_concat(self):
        if self.current_char == '*':
            if not hasattr(self.current_node, 'node_left'):
                new_node = Node('*')
                new_node.parent_node = self.current_node
                self.current_node.node_left = new_node
                self.current_node = new_node
            else:
                new_node = Node('concat')
                new_node.node_right = self.current_node.node_left
                new_node.parent_node = self.current_node
                self.current_node.node_left = new_node
                self.current_node = new_node
                new_node2 = Node('*')
                new_node2.parent_node = self.current_node
                self.current_node.node_left = new_node2
                self.current_node = new_node2
        elif self.current_char == ')':
            self.current_node.open_parenthesis = True
            return ""
        elif self.current_char == '|':
            new_node = Node('|')
            while not self.current_node.open_parenthesis or not self.current_node.is_root:
                self.current_node = self.current_node.parent_node
            new_node.node_right = self.current_node.node_left
            self.current_node.node_left = new_node
            self.current_node = new_node
            self.update_parent_son(self.current_node.node_left, self.current_node)
        else:
            if not hasattr(self.current_node, 'node_left'):
                new_node = Node(self.current_char)
                new_node.parent_node = self.current_node
                self.current_node.node_left = new_node
                self.current_node = new_node
            else:
                new_node = Node('concat')
                new_node.node_right = self.current_node.node_left
                self.current_node.node_left = new_node
                self.current_node = new_node
                self.update_parent_son(self.current_node.node_right, self.current_node)
                new_node2 = Node(self.current_char)
                new_node2.parent_node = self.current_node
                self.current_node.node_left = new_node2
                self.current_node = new_node2

    def update_parent_son(self, child: Node, parent: Node):
        child.parent_node = parent

    def update__own_son(self, current_node: Node, child: Node):
        current_node.node_left = child

    def operate_union(self):
        if self.current_char == '*':
            if not hasattr(self.current_node, 'node_left'):
                new_node = Node('*')
                new_node.parent_node = self.current_node
                self.current_node.node_left = new_node
                self.current_node = new_node
            else:
                new_node = Node('concat')
                new_node.node_right = self.current_node.node_left
                new_node.parent_node = self.current_node
                self.current_node.node_left = new_node
                self.current_node = new_node
                self.update_parent_son(self.current_node.node_left, self.current_node)
                new_node2 = Node('*')
                new_node2.parent_node = self.current_node
                self.current_node.node_left = new_node2
                self.current_node = new_node2
        elif self.current_char == ')':
            self.current_node.open_parenthesis = True
        else:
            if not hasattr(self.current_node, 'node_left'):
                new_node = Node(self.current_char)
                new_node.parent_node = self.current_node
                self.current_node.node_left = new_node
                self.current_node = new_node
            else:
                new_node = Node('concat')
                new_node.node_right = self.current_node.node_left
                self.current_node.node_left = new_node
                self.current_node = new_node
                self.update_parent_son(self.current_node.node_left, self.current_node)
                new_node2 = Node(self.current_char)
                new_node2.parent_node = self.current_node
                self.current_node.node_left = new_node2
                self.current_node = new_node2

    def operate_close_parenthesis(self):
        while not self.current_node.open_parenthesis:
            self.current_node = self.current_node.parent_node

    def operate_char(self):
        if self.current_char == '*':
            new_node = Node('concat')
            new_node.node_right = self.current_node
            new_node.parent_node = self.current_node.parent_node
            self.update_parent_son(self.current_char, new_node)
            self.current_node = new_node
            new_node = Node('*')
            new_node.parent_node = self.current_node
            self.current_node.node_left = new_node
            self.current_node = new_node
        elif self.current_char == '|':
            new_node = Node('|')
            while not (self.current_node.open_parenthesis or self.current_node.is_root):
                self.current_node = self.current_node.parent_node
            new_node.node_right = self.current_node.node_left
            new_node.parent_node = self.current_node
            self.current_node.node_left = new_node
            self.current_node = new_node
            self.update_parent_son(self.current_node.parent_node, self.current_node)
        else:
            new_node = Node('concat')
            new_node.node_right = self.current_node
            new_node.parent_node = self.current_node.parent_node
            self.update__own_son(self.current_node.parent_node, new_node)
            self.current_node = new_node
            self.update_parent_son(self.current_node.node_right, self.current_node)
            new_node2 = Node(self.current_char)
            new_node2.parent_node = self.current_node
            self.current_node.node_left = new_node2
            self.current_node = new_node2


# class RegularExpressionToDeterministicFiniteAutomata:
#     tree = None
#
#     def __init__(self):
#         tree = Tree()
#
#     def transform_to_automata(self, regex_input: str):
#         return print()

if __name__ == "__main__":
    current_input = 'a|(a|bb)*'
    print(current_input)
    text_reversed = reversed(current_input)
    print(list(text_reversed))
    tree = Tree(current_input)
    print(tree.root_node)
