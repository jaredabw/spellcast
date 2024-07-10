from vision import parse_game
from spellcast import Solver

## TODO: allow for direct screenshot input
## draw path on screen

if __name__ == "__main__":
    letters, bonuses = parse_game("img/image.png")

    solver = Solver(letters, bonuses)
    solver.solve()

    best = solver.find_best()
    print(f"\nBest word: {best[0].upper()} | Score: {best[1]} | Path: {best[2]}\n")