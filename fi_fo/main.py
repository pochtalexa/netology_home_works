class Stack:
    def __init__(self):
        self.stack = []

    def is_empty(self):
        if len(self.stack) == 0:
            return True
        else:
            return False

    def push(self, el):
        self.stack.append(el)
        return True

    def pop(self):
        el = self.stack.pop()
        return el

    def peek(self):
        el = self.stack[-1]
        return el

    def size(self):
        return len(self.stack)


def check_brackets_balance(bracket_el):
    bracket_stack = Stack()

    pair_bracket_dict = {
        '(': ')',
        '{': '}',
        '[': ']',
    }

    bracket_kind = {
        '(': 'open',
        '{': 'open',
        '[': 'open',
        ')': 'close',
        '}': 'close',
        ']': 'close'
    }

    len_list = len(bracket_el)
    if len_list % 2 != 0 or bracket_kind[bracket_el[0]] == 'close':
        return 'Несбалансированно'

    for el in bracket_el:
        if bracket_kind[el] == 'open':
            bracket_stack.push(el)
        elif bracket_kind[el] == 'close':
            if pair_bracket_dict[bracket_stack.pop()] == el:
                continue
            else:
                return 'Несбалансированно'
    return 'Сбалансированно'


if __name__ == '__main__':
    brackets_list = [
        '(((([{}]))))',
        '[([])((([[[]]])))]{()}',
        '{{[()]}}',
        '}{}',
        '{{[(])]}}',
        '[[{())}]'
    ]

    for el in brackets_list:
        result = check_brackets_balance(el)
        print(f'{el} - {result}')
