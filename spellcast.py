import argparse
parser = argparse.ArgumentParser()
parser.add_argument("letters", nargs=25)
parser.add_argument("-x", action="store", default="99", help="Double word location (row, column) eg `-x 42`")
parser.add_argument("-d", action="store", default="99", help="Double letter location (row, column) eg `-d 34`")
parser.add_argument("-t", action="store", default="99", help="Triple bonus location (row, column) eg `-t 01`")

args = parser.parse_args()

board = [c.upper() for c in args.letters]
x2 = (int(args.x[:1]), int(args.x[1:]))
dl = (int(args.d[:1]), int(args.d[1:]))
tl = (int(args.t[:1]), int(args.t[1:]))

def init_game():
    pos: list[tuple] = []
    for i in range(int(len(board)**0.5)):
        for j in range(int(len(board)**0.5)):
            pos.append((i, j))

    game = dict(zip(pos, board))

    WORDS: list[set[str]] = []
    WORDS.append(set())
    with open("dictionary.txt", "r") as f:
        for line in f:
            WORDS[0].add(line.strip().lower())

    for i in range(1, 26):
        WORDS.append(set())
        for word in WORDS[0]:
            if len(word) >= i:
                WORDS[i].add(word[:i])

    SCORES = {
        "A": 1,
        "B": 4,
        "C": 5,
        "D": 3,
        "E": 1,
        "F": 5,
        "G": 3,
        "H": 4,
        "I": 1,
        "J": 7,
        "K": 6,
        "L": 3,
        "M": 4,
        "N": 2,
        "O": 1,
        "P": 4,
        "Q": 8,
        "R": 2,
        "S": 2,
        "T": 2,
        "U": 4,
        "V": 5,
        "W": 5,
        "X": 7,
        "Y": 4,
        "Z": 8 
    }

    possible_words = []

    return WORDS, SCORES, game, possible_words

def find_words(game: dict[tuple, str], position: tuple[int], word: str, score: int, path: list[tuple]) -> None:
    path.append(position)

    letter = game[position]
    word += letter.lower()

    if dl == position:
        score += 2 * SCORES[letter]
    elif tl == position:
        score += 3 * SCORES[letter]
    else:
        score += SCORES[letter]

    if word in WORDS[0]: # base case
        finalscore = score
        if x2 in path: # double word bonus
            finalscore = 2 * score
        if len(word) >= 6: # long word bonus
            finalscore += 10
        possible_words.append((word, finalscore, path))
    
    if word in WORDS[len(word)] and len(word) < 25: # if it could be the start of a word
        # check surroundings
        r, c = position
        surroundings = []
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                if 0 <= r + i <= 4 and 0 <= c + j <= 4 and not (i == 0 and j == 0) and not (r + i, c + j) in path:
                    surroundings.append((r + i, c + j))

        for pos in surroundings:
            find_words(game, pos, word, score, path.copy())
    else:
        return

WORDS, SCORES, game, possible_words = init_game()
for position in game:
    find_words(game, position, "", 0, [])

best = max(possible_words, key=lambda x: x[1])
print(f"\nBest word: {best[0].upper()} | Score: {best[1]} | Path: {best[2]}")
