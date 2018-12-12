import re
from collections import deque
from pathlib import Path

def play_game(n_players: int, n_marbles: int) -> int:
    """
    Play the elf puzzle game!
    
    The current marble is the rightmost in the deque
    """
    scores = [0]*n_players
    marble_circle = deque([0])
    for marble in range(1, n_marbles + 1):
        if marble % 23 == 0:
            # Player scores! 
            # Player gets the current marble + the marble 7 spots counter-clockwise
            current_player = (marble - 1) % n_players
            marble_circle.rotate(7)
            scores[current_player] += (marble_circle.pop() + marble)
            
            # Shift current marble to the right of the one that was popped
            marble_circle.rotate(-1)
        else:
            marble_circle.rotate(-1)
            marble_circle.append(marble)
            
    return max(scores)
            

puzzle_input_file = Path('../../Inputs/puzzle_input_d9.txt')
with puzzle_input_file.open(mode="r") as f:
    exp = r"(\d+) players; last marble is worth (\d+) points"
    match = re.search(exp, f.read())
    n_players, n_marbles = map(int, match.groups())
    
print(play_game(n_players, n_marbles))
print(play_game(n_players, n_marbles*100))