from vision import *
from spellcast import Solver

if __name__ == "__main__":
    im = get_image()
    if im is None:
        print("No image found in clipboard. Exiting...")
        exit()
    letters, bonuses = parse_game(im)

    solver = Solver(letters, bonuses)
    solver.solve()

    best = solver.find_best()
    print(f"\nBest word: {best[0].upper()} | Score: {best[1]} | Path: {best[2]}\n")

    draw_path(im, best[2])

    generate_video(im, solver.possible_words)

    cv2.destroyAllWindows()