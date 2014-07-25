import operator
import os

from structures import LinkedList, Stack


class KnightsTour(object):
    def __init__(self, board_size, initial_pos, verbose=False):
        self.board = Board(board_size)
        self.initial_pos = initial_pos
        self.current_pos = None

        # set to true for console output
        self.verbose = verbose

    def run(self):
        """ Runs Warnsdorff for 1/2 and brute force for 1/2. """
        self.current_pos = self.initial_pos

        self.warnsdorff(work_split=len(self.board) / 2)
        self.brute_force()

    def warnsdorff(self, work_split):
        """
        Use the Warnsdorff rule to search for a valid tour.
        Params: int work_split (amount of spaces to solve)
        """
        if len(self.board) > 76*76:
            raise ValueError("Warnsdorff heuristic can fail on boards"
                             " than 76x76.")
        if self.current_pos is None:
            self.current_pos = self.initial_pos

        x, y = self.current_pos

        for move in range(work_split):
            if self.verbose:
                print "| Tour (Warnsdorff): The current position is:", \
                        self.current_pos
                self.board.display()
            x, y = self.current_pos
            # choose best next move (with the least amount of next moves)
            move = self.choose_move(x, y)
            x, y = move
            self.board.visit(x, y)
            self.current_pos = move
            if self.board.completed:
                break
        if self.verbose:
            self.board.display()

    def brute_force(self):
        """ Brute force search for a valid tour. """
        if self.current_pos is None:
            self.current_pos = self.initial_pos

        stack = Stack()
        space = Space(self.current_pos)
        stack.push(space)

        if self.verbose:
            self.board.display()

        while not self.board.completed:
            # moves that are not in space.failures
            moves = []

            # find valid moves
            x, y = space.value
            available_moves = self.find_moves(x, y)

            # insert moves that have not failed
            for move in available_moves:
                if move not in space.failures:
                    moves.append(move)

            # if there are available moves
            if len(moves) is not 0:
                # try a move
                next_move = moves[0]
                x, y = next_move
                # visit the next move
                self.board.visit(x, y)
                # push the old value to the stack
                stack.push(space)
                # create a new space
                space = Space(next_move)
                # set the new current position
                self.current_pos = next_move
            else:
                space = stack.pop()
                space.failures.append(self.current_pos)
                x, y = self.current_pos
                self.current_pos = space.value

            if self.verbose:
                print "| Tour (brute-force): The current position:", self.current_pos
        if self.verbose:
            self.board.display()

    def choose_move(self, x, y):
        """ Used to pick a move based upon the Warnsdorff rule. """
        possible_moves = {}

        """
        Initialize a dict of each move's possible moves
        from the current position.
        """
        for move in self.find_moves(x, y):
            possible_moves[move] = 0

        """
        Count available moves for each available move from the
        current position.
        """
        for position, count in possible_moves.iteritems():
            x, y = position
            move_count = len(self.find_moves(x, y))
            possible_moves[position] = move_count

        sorted_moves = sorted(possible_moves.iteritems(),
                              key=operator.itemgetter(1))

        move = sorted_moves[0][0]
        if self.verbose:
            print "| Tour (Warnsdorff): The next move calculated was " + \
                    str(move) + " with " + str(possible_moves[move]) + \
                    " available moves from that point."
        return move

    def find_moves(self, x, y):
        """ Find positions in which the knight is allowed to move. """
        moves = [(x + 1, y + 2),
                 (x + 1, y - 2),
                 (x + 2, y + 1),
                 (x + 2, y - 1),
                 (x - 1, y + 2),
                 (x - 1, y - 2),
                 (x - 2, y + 1),
                 (x - 2, y - 1)]

        possible_moves = [move for move in moves if self.valid_move(move)]

        valid_moves = []
        for move in possible_moves:
            x, y = move
            if not self.board.been_visited(x, y):
                valid_moves.append(move)

        return valid_moves

    def valid_move(self, move):
        """ Determine if the move is within the boundaries of the board. """
        x, y = move
        max_x, max_y = self.board.size
        if not x < 0 and not x > max_x - 1 and \
                not y < 0 and not y > max_y - 1:
            return True
        else:
            return False


class Space(object):
    def __init__(self, value):
        self.value = value
        self.failures = []


class Board(object):
    def __init__(self, size):
        self.__board = []
        self.__size = size
        # number of locations visited
        self.__visited = 0
        # generate a board based upon a given size
        self.__generate()

        x, y = self.__size
        self.__len = x * y

    def visit(self, x, y):
        """ Visit a location on the board. """
        if self.__board[y][x] == 1:
            raise KeyError("The value: " + str(x) + ", " + str(y) + " has already been visited")
        self.__board[y][x] = 1
        self.__visited += 1

    def unvisit(self, x, y):
        """ Unvisit a location on the board. """
        self.__board[y][x] = -1
        self.__visited -= 1

    def been_visited(self, x, y):
        """ Check if a location has been visited. """
        if self.__board[y][x] == 1:
            return True
        else:
            return False

    def display(self):
        """ Print the board to the console. """
        print(" ======= Board Info ======")
        if len(self) < 2500:
            for x in self.__board:
                row = []
                for y in x:
                    if y is 1:
                        row.append("X")
                    else:
                        row.append("O")
                output = ' ' + ' '.join(str(point) for point in row)
                print output
            print(" =========================")
        else:
            print("| Failed. The board is too large to display efficiently.")

    def __generate(self):
        """ Generate a board based upon the input size. """
        x, y = self.__size
        for i in range(x):
            self.__board.append([])
            for j in range(y):
                self.__board[i].append(-1)

    @property
    def completed(self):
        """ Check whether or not all locations have been visited. """
        if self.__visited == len(self):
            return True
        else:
            return False

    @property
    def size(self):
        """ Return a tuple containing height and width of the board. """
        return self.__size

    def __len__(self):
        """ Return the number of positions on the board. """
        return self.__len


class KnightManager(object):
    def __init__(self, knights):
        self.__knights = knights

    def main_menu(self):
        """ Main KnightManager menu. """
        while True:
            self.clear_screen()
            print(" ======= Manage Knights - KnightsTour =======")
            print("|")
            print("| 1) Add a knight")
            print("| 2) Delete a knight")
            print("| 3) Modify a knight")
            print("| 4) List all knights")
            print("| 5) back to main menu")
            selection = raw_input(">> ")
            if selection == "":
                break
            try:
                selection = int(selection)
            except ValueError:
                continue

            if selection is 1:
                self.add()
            elif selection is 2:
                self.delete()
            elif selection is 3:
                self.modify()
            elif selection is 4:
                self.list()
            elif selection is 5:
                break

    def add(self):
        print(" ======== Add Knights - KnightsTour ========")
        print("| Enter 'd' when done.")
        print("| Enter the comma separated starting position of your knight.")
        print("| (example: 4, 5)")
        while True:
            response = raw_input(">> ")

            # if the user is done entering knight locations
            if response == "d" or response == "":
                break

            # split the input into 2 values
            stripped_response = response.replace(" ", "")
            values = stripped_response.split(',')
            if len(values) is not 2:
                print("| Error: Not a valid input.")
                continue
            x, y = values
            x = int(x)
            y = int(y)
            values = x, y

            # add the knight coordinate to the linked list
            self.__knights.append(values)

    def delete(self):
        print(" ======= Delete Knights - KnightsTour =======")
        print("| Enter 'd' when done.")
        print("| Enter the comma seperated position to delete.")
        print("| (example: 4, 5)")
        while True:
            response = raw_input(">> ")

             # if the user is done entering knight locations
            if response == "d" or response == "":
                break

            # split the input into 2 values
            stripped_response = response.replace(" ", "")
            values = stripped_response.split(',')
            if len(values) is not 2:
                print("| Error: Not a valid input.")
                continue
            x, y = values
            x = int(x)
            y = int(y)
            values = x, y

            # delete knight from the linked list
            self.__knights.remove(values)

    def modify(self):
        print(" ====== Modify Knights - KnightsTour ======")
        print("| Enter 'd' when done ")
        print("| Enter the ID of a knight to modify.")
        print("| (ID's can be found on the knight listing)")
        while True:
            response = raw_input(">> ")

            # if the user is done entering knight locations
            if response == "d" or response == "":
                break

            response = int(response)

            print("| Enter a new comma seperated value:")
            new_value = raw_input(">> ")

            # if the user is done entering knight locations
            if response == "d" or response == "":
                break

            # split the input into 2 values
            stripped_response = new_value.replace(" ", "")
            values = stripped_response.split(',')
            if len(values) is not 2:
                print("| Error: Not a valid input.")
                continue
            x, y = values
            x = int(x)
            y = int(y)
            values = x, y

            # add the knight coordinate to the linked list
            self.__knights.modify(response, values)

    def list(self):
        print(" ======= List Knights - KnightsTour =======")
        if len(self.__knights) is 0:
            print("| There are 0 knights to list.")
        for x, knight in enumerate(self.__knights):
            print("| %s) %s" % (x + 1, knight))

        print("| ")
        raw_input("| Press enter to continue.")

    def clear_screen(self):
        """ Clear the screen. """
        os.system('cls' if os.name == 'nt' else 'clear')


class KnightSolver(object):
    def __init__(self, knights):
        self.__knights = knights

    def main_menu(self):
        print(" ====== Solve Knight Tours - KnightsTour ======")
        if len(self.__knights) is 0:
            print("| There are no knight tours to solve.")
            print "| Press enter to continue."
            raw_input(">> ")
        for knight in self.__knights:
            print "| Press enter to solve for:", knight
            raw_input(">> ")

            # solve for the current knight in the linked list
            try:
                self.solve(knight)
            except ValueError:
                raise
                print "| Failed: The knight position was invalid at:", knight
            else:
                print "| Tour completed for", knight
            print "| =================================="

        print "| Done computing knight tours. Press enter to continue."
        raw_input(">> ")

    def solve(self, position):
        board_size = (8, 8)
        tour = KnightsTour(board_size=board_size, initial_pos=position,
                           verbose=True)

        if tour.valid_move(position):
            tour.run()
        else:
            raise ValueError("The position for the knight is invalid.")


class UserControl(object):
    def __init__(self):
        self.knights = LinkedList()
        self.run()

    def run(self):
        """ Main program with user controls. """
        while True:
            selection = self.main_menu()
            if selection is 1:
                km = KnightManager(self.knights)
                km.main_menu()
            elif selection is 2:
                ks = KnightSolver(self.knights)
                ks.main_menu()
            elif selection is 3:
                self.quit_message()
                break

    def main_menu(self):
        """ Main menu method """
        while True:
            self.clear_screen()
            print(" ================ KnightsTour ================")
            print("|")
            print("| Menu:")
            print("| 1) Manage knight starting positions")
            print("| 2) Solve the knights tour for all knights")
            print("| 3) Quit")

            try:
                return int(raw_input(">> "))
            except ValueError:
                continue

    @classmethod
    def clear_screen(self):
        """ Clear the screen. """
        os.system('cls' if os.name == 'nt' else 'clear')

    def quit_message(self):
        """ Display the quit message. """
        print("| Goodbye...")


if __name__ == "__main__":
    UserControl()
