class Solver:
    def __init__(self, letters, bonuses):
        self.WORDS, self.SCORES = self.init_consts()
        self.game, self.possible_words = self.init_game(letters)
        self.x2 = bonuses["x2"]
        self.dl = bonuses["dl"]
        self.tl = bonuses["tl"]

    def init_consts(self):
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

        return WORDS, SCORES

    def init_game(self, letters: str):
        pos: list[tuple] = []
        for i in range(1, 6):
            for j in range(1, 6):
                pos.append((i, j))

        game = dict(zip(pos, letters))

        possible_words = []

        return game, possible_words

    def find_words(self, position: tuple[int], word: str, score: int, path: list[tuple]) -> None:
        path.append(position)

        letter = self.game[position]
        word += letter.lower()

        if self.dl == position:
            score += 2 * self.SCORES[letter]
        elif self.tl == position:
            score += 3 * self.SCORES[letter]
        else:
            score += self.SCORES[letter]

        if word in self.WORDS[0]: # base case
            finalscore = score
            if self.x2 in path: # double word bonus
                finalscore = 2 * score
            if len(word) >= 6: # long word bonus
                finalscore += 10
            self.possible_words.append((word, finalscore, path))
        
        if word in self.WORDS[len(word)] and len(word) < 25: # if it could be the start of a word
            # check surroundings
            r, c = position
            surroundings = []
            for i in (-1, 0, 1):
                for j in (-1, 0, 1):
                    if 1 <= r + i <= 5 and 1 <= c + j <= 5 and not (i == 0 and j == 0) and not (r + i, c + j) in path:
                        surroundings.append((r + i, c + j))

            for pos in surroundings:
                self.find_words(pos, word, score, path.copy())
        else:
            return

    def solve(self):
        for pos in self.game:
            self.find_words(pos, "", 0, [])

    def find_best(self):
        best = max(sorted(self.possible_words, key=lambda x: x[1], reverse=True), key=lambda x: x[1])
        return best

