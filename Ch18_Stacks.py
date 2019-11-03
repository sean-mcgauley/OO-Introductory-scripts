#! python


class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def isEmpty(self):
        return (self.items == [])


''' tokenlist == the expression to be evaluated, separated by any character
    that is not an integer, if the token == integer it is pushed onto the
    stack, when an operator is picked up the stack takes the top two values
    in the stack and performs the operator then returns the result to the
    top of the stack. (52 + 47)*26 == 52 47 + 26 *. 52 added to stack,
    47 added to stack, + found, 52 + 47 = 99, return 99 to top of stack.
    26 added to stack, * found, 99 * 26 = 2574. return 2574 to stack.
    no more tokens, return stack.pop()'''


def evalPostfix(expr):
    import re
    tokenList = re.split('([^0-9])', expr)
    stack = Stack()
    for token in tokenList:
        if token == '' or token == ' ':
            continue
        if token == '+':
            sum = stack.pop() + stack.pop()
            stack.push(sum)
        elif token == '-':
            sub = stack.pop() - stack.pop()
            stack.push(sub)
        elif token == '/':
            div = stack.pop() / stack.pop()
            stack.push(div)
        elif token == '*':
            product = stack.pop() * stack.pop()
            stack.push(product)
        else:
            stack.push(int(token))
    return stack.pop()

    '''returns value that would be popped from stack
       i.e. the final value in stack'''


print(evalPostfix('2 6 27 46 + * /'))
