#! python


class Node:
    def __init__(self, cargo=None, next=None):
        self.cargo = cargo
        self.next = next

    def __str__(self):
        return str(self.cargo)

    def printBackward(self):
        if self.next is not None:
            tail = self.next
            tail.printBackward()
        print(self.cargo, end='')

# Cannot call methods on None which is why these must be functions


def printList(node):
    nodelist = []
    while node:
        nodelist.append(node.cargo)
        node = node.next
    print(nodelist)


def printBackward(list):
    if list is None:
        return
    head = list
    tail = list.next
    printBackward(tail)
    print(head, end=' ')


def removeSecond(list):
    if list is None:
        return
    first = list
    second = list.next
    # Make first node refer to third
    first.next = second.next
    # separate the second node from the rest of the list
    second.next = None
    return second


def printBackwardNicely(list):
    print('[ ', end='')
    printBackward(list)
    print(']', end='')


class LinkedList:
    def __init__(self):
        self.length = 0
        self.head = None

    def printBackward(self):
        print('[', end='')
        if self.head is not None:
            self.head.printBackward()
        print(']', end='')

    def addFirst(self, cargo):
        node = Node(cargo)
        node.next = self.head
        self.head = node
        self.length += 1


node1 = Node(1)
node2 = Node(2)
node3 = Node(3)

node1.next = node2
node2.next = node3

printBackward(node1)
