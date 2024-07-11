from vision import parse_game, draw_path, get_image
from spellcast import Solver

# TODO:
if __name__ == "__main__":
    im = get_image()
    letters, bonuses = parse_game(im)

    solver = Solver(letters, bonuses)
    solver.solve()

    best = solver.find_best()
    print(f"\nBest word: {best[0].upper()} | Score: {best[1]} | Path: {best[2]}\n")

    draw_path(im, best[2])