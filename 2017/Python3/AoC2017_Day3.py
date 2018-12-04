import itertools

def Day3a(n):
    """
    Each square on the grid is allocated in a spiral pattern starting at a 
    location marked 1 and then counting up while spiraling outward. For 
    example, the first few squares are allocated like this:
    
    17  16  15  14  13
    18   5   4   3  12
    19   6   1   2  11
    20   7   8   9  10
    21  22  23---> ...
    
    While this is very space-efficient (no squares are skipped), requested 
    data must be carried back to square 1 (the location of the only access 
    port for this memory system) by programs that can only move up, down, 
    left, or right. They always take the shortest path: the Manhattan 
    Distance between the location of the data and square 1.
    
    For example:
    
    Data from square 1 is carried 0 steps, since it's at the access port.
    Data from square 12 is carried 3 steps, such as: down, left, left.
    Data from square 23 is carried only 2 steps: up twice.
    Data from square 1024 must be carried 31 steps.
    
    How many steps are required to carry the data from the square identified 
    in your puzzle input all the way to the access port?
    """
    digitpos = list(spiralizer(n))
    return sum([abs(x) for x in digitpos[0]])


def spiralizer(n):
    # Set up the moves
    north = lambda x, y: (x, y+1)
    south = lambda x, y: (x, y-1)
    east = lambda x, y: (x+1, y)
    west = lambda x, y: (x-1, y)
    movecycle = itertools.cycle([east, north, west, south])

    # Set initial parameters
    step = 1
    pos = [0, 0]
    nmoves = 1

    while True:
        # Iterate over the next 2 moves
        for _ in range(2): 
            move = next(movecycle)
            for _ in range(nmoves):
                if step >= n:
                    yield pos
                    return
                pos = move(*pos)  # Apply the move lambda
                step += 1
        nmoves += 1
