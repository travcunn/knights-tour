import cProfile

from main import KnightsTour


size = (8, 8)
initial = (2, 3)

def brute_force():
    kt = KnightsTour(size, initial)
    kt.brute_force()

    if not kt.board.completed:
        raise ValueError

def warnsdorff():
    kt = KnightsTour(size, initial)
    kt.warnsdorff(len(kt.board))

    if not kt.board.completed:
        raise ValueError

def both():
    kt = KnightsTour(size, initial)
    kt.run()

    if not kt.board.completed:
        raise ValueError


cProfile.run('both()')
cProfile.run('brute_force()')
cProfile.run('warnsdorff()')
