class Node(object):
    """ Node class used for LinkedList items. """
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList(object):
    def __init__(self):
        self.root = None
        self.__length = 0

    def append(self, value):
        """ Append a value to the linked list. """
        if self.root is None:
            self.root = Node(value)
        else:
            current_node = self.root
            while current_node.next is not None:
                current_node = current_node.next
            current_node.next = Node(value)

        self.__length += 1

    def remove(self, value):
        """ Remove a value from the linked list. """
        previous_node = None
        current_node = self.root

        found = False
        while current_node is not None:
            if current_node.value == value:
                found = True
                break
            previous_node = current_node
            current_node = current_node.next

        if found:
            if previous_node is None:
                self.root = current_node.next
            else:
                previous_node.next = current_node.next
            self.__length -= 1

    def modify(self, index, value):
        count = 0
        index = index - 1

        current = self.root

        while current is not None:
            if index == count:
                current.value = value
                return
            current = current.next
            count += 1

        raise KeyError("The specified index was not found.")


    def __len__(self):
        return self.__length

    def __iter__(self):
        self.__current = self.root
        return self

    def next(self):
        """ Allows for use of LinkedList as an iterator (for loops). """
        if self.__current is None:
            raise StopIteration
        else:
            next = self.__current
            self.__current = self.__current.next
            return next.value


class Stack(object):
    def __init__(self):
        self.__stack = []

    def push(self, value):
        """ Push an item to the top of the stack. """
        self.__stack.append(value)

    def pop(self):
        """ Take an item from the top of the stack. """
        value = self.__stack[len(self) - 1]
        del self.__stack[len(self) - 1]
        return value

    def remove(self, value):
        """ Remove a value from an array at the top of the stack. """
        array = self.__stack[len(self) - 1]
        if len(array) > 0:
            array.remove(value)

    @property
    def contents(self):
        return self.__stack

    def __len__(self):
        return len(self.__stack)
