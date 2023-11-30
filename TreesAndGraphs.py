'''
Завдання 1:

Для графа, заданого булевою матрицею суміжності (табл. 1 – 4), перевірятиметься
його орієнтованість (використовуючи означення, якщо матриця суміжності
несиметрична, то граф однозначно вважати орієнтованим, у разі якщо задана
матриця виявиться симетричною – виводити повідомлення, що граф може бути як
неорієнтованим, так і орієнтованим).
'''


def define_graph_orientation(matrix):
    matlen = len(matrix)
    flag = True
    oriented = "однозначно орієнтований"
    not_oriented_fully = "може бути як неорієнтованим, так і орієнтованим"

    for i in range(matlen):
        for j in range(matlen):
            if matrix[i][j] and not matrix[j][i]:
                flag = False
                break

    return f"Заданий вами граф-матриця — {oriented if flag else not_oriented_fully}"


'''
Завдання 2:

Побудувати бінарне дерево для заданого арифметичного виразу згідно варіанту
(табл. 5 – 9).
'''


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def infix_to_postfix(infix_expression):
    # Пріоритети операторів
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}

    # Функція для перевірки, чи є токен оператором
    def is_operator(token):
        return token in precedence

    # Функція для порівняння пріоритетів двох операторів
    def higher_precedence(op1, op2):
        return precedence[op1] > precedence[op2]

    # Стек для зберігання операторів
    stack = []
    # Список для зберігання постфіксного виразу
    postfix = []
    # Розділення вхідного інфіксного виразу на токени
    tokens = infix_expression.split()

    # Проходимо всі токени вхідного виразу
    for token in tokens:
        if token.isalnum():  # Якщо токен є операндом (буквою або цифрою), додаємо його до постфіксного виразу
            postfix.append(token)
        elif is_operator(token):  # Якщо токен є оператором
            # Поки стек не пустий і верхній оператор у стеку має вищий або рівний пріоритет, додаємо його до постфіксного виразу
            while stack and is_operator(stack[-1]) and higher_precedence(stack[-1], token):
                postfix.append(stack.pop())
            # Додаємо поточний оператор до стеку
            stack.append(token)
        elif token == '(':  # Якщо токен — ліва дужка, додаємо його до стеку
            stack.append(token)
        elif token == ')':  # Якщо токен — права дужка
            # Поки стек не пустий і верхній елемент у стеку не є лівою дужкою
            while stack and stack[-1] != '(':
                # Додаємо оператори зі стеку до постфіксного виразу
                postfix.append(stack.pop())
            # Видаляємо ліву дужку зі стеку
            stack.pop()

    # Додаємо залишок операторів зі стеку до постфіксного виразу
    while stack:
        postfix.append(stack.pop())

    # Повертаємо постфіксний вираз у вигляді рядка
    return ' '.join(postfix)



def build_expression_tree(postfix_expression):
    stack = []

    operators = {'+', '-', '*', '/', '^'}

    for token in postfix_expression.split():
        node = Node(token)

        if token in operators:
            node.right = stack.pop()
            node.left = stack.pop()

        stack.append(node)

    return stack.pop()


def print_tree(root, level=0, prefix="", is_left=None):
    if root:
        if is_left is None:
            connector = "   "
        elif is_left:
            connector = "  ├── "
        else:
            connector = "  └── "

        print("   " * level + prefix + connector + str(root.value))
        print_tree(root.left, level + 1, "", is_left=True)
        print_tree(root.right, level + 1, "", is_left=False)

'''
Завдання 3:

Зробити прямий та зворотній обходи отриманого в п.b дерева, вивести та покроково
обчислити отриманий у прямому та зворотному польському записах вираз.
'''


def preorder_traversal(node):
    if node:
        print(node.value, end=" ")
        preorder_traversal(node.left)
        preorder_traversal(node.right)


def postorder_traversal(node):
    if node:
        postorder_traversal(node.left)
        postorder_traversal(node.right)
        print(node.value, end=" ")


def evaluate_postfix(postfix_expression):
    stack = []
    i = 0

    for token in postfix_expression.split():
        if token.isnumeric():
            # Якщо токен є числом, то додаємо його до стеку як операнд
            stack.append(int(token))
        else:
            i += 1
            # Якщо токен є оператором, вилучаємо два останніх операнди зі стеку
            operand2 = stack.pop()
            operand1 = stack.pop()

            # Обчислення результату відповідно до знака оператора
            if token == '+':
                result = operand1 + operand2
            elif token == '-':
                result = operand1 - operand2
            elif token == '*':
                result = operand1 * operand2
            elif token == '/':
                result = operand1 / operand2
            elif token == '^':
                result = operand1 ** operand2

            # Додаємо отриманий результат обчислення назад до стеку
            stack.append(result)

            # Виведення кроку обчислення
            print(f"{i}: {operand1} {token} {operand2} = {result}")

    return stack.pop()


'''
РЕАЛІЗАЦІЯ ЗАВДАНЬ
'''

# Завдання 1

matrix = [
    [0, 0, 1, 1, 0],
    [0, 1, 0, 1, 1],
    [0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0]
]


print(define_graph_orientation(matrix))


# Завдання 2

expression = "( ( 6 - 1 ) / 5 * 2 + 2 ) * 4 ^ 3"
postfix_expression = infix_to_postfix(expression)
expression_tree = build_expression_tree(postfix_expression)

print(f"\nДерево для виразу {expression} має вигляд:")
print_tree(expression_tree)

# Завдання 3
print("\nПрямий обхід: ")
preorder_traversal(expression_tree)
print()
print("Зворотній обхід:")
postorder_traversal(expression_tree)
print()
print("Етапи обчислення заданого виразу:")
evaluate_postfix(postfix_expression)
