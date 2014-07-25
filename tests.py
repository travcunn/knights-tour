import unittest

from main import Board, KnightsTour
from structures import LinkedList, Stack


class LinkedListTest(unittest.TestCase):
    def test_generator(self):
        linked_list = LinkedList()
        linked_list.append(34)
        linked_list.append(55)
        linked_list.append(33)

        values = [34, 55, 33]

        values_match = True
        for x in linked_list:
            if x not in values:
                values_match = False
                break
        self.assertTrue(values_match)

class StackTest(unittest.TestCase):
    def test_basics(self):
        stack = Stack()

        test_data1 = 123
        test_data2 = 456
        stack.push(test_data1)
        self.assertTrue(len(stack) is 1)
        stack.push(test_data2)
        self.assertTrue(len(stack) is 2)

        self.assertTrue(stack.pop() == test_data2)
        self.assertTrue(stack.pop() == test_data1)

    def test_array_removals(self):
        stack = Stack()

        test_values = [1, 2, 3, 4]
        stack.push(test_values)

        stack.remove(3)
        top = stack.pop()
        expected = [1, 2, 4]

        values_match = True
        for value in top:
            if value not in expected:
                values_match = False
                break
        self.assertTrue(values_match)

        values_match = True
        for value in stack.contents:
            if value not in expected:
                values_match = False
                break
        self.assertTrue(values_match)


class BoardTest(unittest.TestCase):
    def setUp(self):
        size = (8, 8)
        self.board = Board(size)

    def test_visits(self):
        self.assertTrue(not self.board.been_visited(3, 4))
        self.board.visit(3, 4)
        self.assertTrue(self.board.been_visited(3, 4))

    def test_completed(self):
        self.assertTrue(not self.board.completed)
        for x in range(8):
            for y in range(8):
                self.board.visit(x, y)
        self.assertTrue(self.board.completed)


class KnightsTourTest(unittest.TestCase):
    def test_invalid_moves(self):
        initial = (0, 0)
        size = (8, 8)
        kt = KnightsTour(size, initial)

        valid_moves = kt.find_moves(0, 0)
        self.assertTrue(len(valid_moves) == 2)
        self.assertTrue((1, 2) in valid_moves)
        self.assertTrue((2, 1) in valid_moves)

    def test_choose_move(self):
        initial = (0, 2)
        size = (8, 8)
        kt = KnightsTour(size, initial)

        self.assertTrue(kt.choose_move(0, 2) == (1, 0))

    def test_warnsdorff(self):
        initial = (0, 2)
        size = (8, 8)
        kt = KnightsTour(size, initial)

        # use warnsdorff on the entire board
        kt.warnsdorff(work_split=len(kt.board))

        visited_count = 0
        for position in range(len(kt.board)):
            x = position / 8
            y = position % 8
            if kt.board.been_visited(x, y):
                visited_count += 1

        self.assertTrue(visited_count is len(kt.board))

    def test_brute_force(self):
        initial = (0, 2)
        size = (8, 8)
        kt = KnightsTour(size, initial)

        kt.brute_force()

        self.assertTrue(kt.board.completed)

    def test_warnsdorff_and_brute_force(self):
        initial = (0, 2)
        size = (8, 8)
        kt = KnightsTour(size, initial)

        kt.run()

        self.assertTrue(kt.board.completed)

    def test_warnsdorff_max(self):
        initial = (0, 2)
        size = (400, 500)
        kt = KnightsTour(size, initial)

        with self.assertRaises(ValueError):
            kt.warnsdorff(work_split=len(kt.board))

if __name__ == '__main__':
    unittest.main()
