#! python

# Ch20 Trees


class Tree:
    def __init__(self, cargo, left=None, right=None):
        self.cargo = cargo
        self.left = left
        self.right = right

    def __str__(self):
        return str(self.cargo)

    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right

    def getCargo(self):
        return self.cargo

    def setLeft(self, arg):
        self.left = arg

    def setRight(self, arg):
        self.right = arg

    def setCargo(self, arg):
        self.cargo = arg
# How do I traverse it?


def total(tree):
    if tree is None:
        return 0
    return total(tree.left) + total(tree.right) + tree.cargo


def printTree(tree):
    if tree is None:
        return
    print(tree.cargo, end=' ')
    printTree(tree.left)
    printTree(tree.right)


def printTreePostorder(tree):
    if tree is None:
        return
    printTreePostorder(tree.left)
    printTreePostorder(tree.right)
    print(tree.cargo, end=' ')


def printTreeInorder(tree):
    if tree is None:
        return
    printTreeInorder(tree.left)
    print(tree.cargo, end=' ')
    printTreeInorder(tree.right)


def printTreeIndented(tree, level=0):
    if tree is None:
        return
    printTreeIndented(tree.right, level + 1)
    print(' '*level + str(tree.cargo))
    printTreeIndented(tree.left, level + 1)


def getToken(tokenList, expected):
    if tokenList[0] == expected:
        del tokenList[0]
        return True
    else:
        return False


def getNumber(tokenList):
    if getToken(tokenList, '('):
        x = getSum(tokenList)
        if not getToken(tokenList, ')'):
            raise ValueError('Missing parenthesis')
        return x
    else:
        x = tokenList[0]
        if not isinstance(x, int):
            return None
        tokenList[0:1] = []
        return Tree(x, None, None)


def getProduct(tokenList):
    a = getNumber(tokenList)
    if getToken(tokenList, '*'):
        b = getProduct(tokenList)
        return Tree('*', a, b)
    else:
        return a


def getSum(tokenList):
    a = getProduct(tokenList)
    if getToken(tokenList, '+'):
        b = getSum(tokenList)
        return Tree('+', a, b)
    else:
        return a

# Requires getLeft/Right and setLeft/Right
def animal():
    root = Tree('bird')

    # Loop until user quits
    while True:
        print()
        if not yes('Are you thinking of an animal? '):
            break
        # Walk the tree
        tree = root
        while tree.getLeft() is not None:
            prompt = tree.getCargo() + '? '
            if yes(prompt):
                tree = tree.getRight()
            else:
                tree = tree.getLeft()

        # Make a guess
        guess = tree.getCargo()
        prompt = 'Is it a ' + guess + '? '
        if yes(prompt):
            print('I rule!')
            continue

        # Get new info
        prompt = "What is the animal's name? "
        animal = input(prompt)
        # Question should ask what previous animal can do
        prompt = "What question would distinguish a %s from a %s? "
        question = input(prompt % (animal, guess))

        # Add new info to tree
        tree.setCargo(question)
        prompt = "If the animal were %s the answer would be? "
        if yes(prompt % animal):
            tree.setLeft(Tree(guess))
            tree.setRight(Tree(animal))
        else:
            tree.setLeft(Tree(animal))
            tree.setRight(Tree(guess))


def yes(ques):
    ans = (input(ques)).lower()
    return (ans[0] == 'y')

animal()
# printTree(tree)
# output: + 1 * 2 3 = (2 * 3) + 1
# printTreePostorder(tree)
# output: 1 2 3 * + = (2 * 3) + 1
# printTreeInorder(tree)
# output: 1 + 2 * 3
# printTreeIndented(tree)
