"""Given the list of letters from the NY Times "Letterboxed" game,
generate some possible solutions. Note that the file in WORDLIST
contains many words not recognized as such by the game, which you can
add after the letter list to omit from consideration.

NOTE: the letters must be given in this order:
1. Start at the upper left-hand corner.
2. Proceed clockwise around the square.
"""

from collections import Counter
from itertools import chain, combinations, permutations
from pathlib import Path
import re
import sys

# WORDLIST = "/home/mark/word.list"
NOTAWORDLIST = "data/notaword.list"
WORDLIST = "/home/mark/nwl2023_words.list"
WORDS = Path(WORDLIST).read_text().splitlines()

# Get command-line arguments
letters = list(sys.argv[1])

# Find all the words that use only the given letters
pat = re.compile(f"^[{''.join(letters)}]+$")
allwords = [w for w in WORDS if pat.search(w)]

matchescnt = len(allwords)

# Remove words with doubled letters, as these can't be played
words = [word for word in allwords if not re.search(r"([a-z])\1", word)]
doublescnt = len(allwords) - len(words)

# Remove words that have sequences of letters
# that appear on the same side of the square.
sides = [letters[0:3], letters[3:6], letters[6:9], letters[9:12]]
patstr = ["|".join(["".join(l) for l in permutations(side, 2)]) for side in sides]
pat = re.compile("|".join(patstr))
words = [word for word in words if not pat.search(word)]

pairingscnt = len(allwords) - len(words) - doublescnt

# Remove words not recognized by the NYT editor
nonwords = Path(NOTAWORDLIST).read_text().splitlines()
words = list(set(words) - set(nonwords))

# Find the 2-word combinations that use all the given letters
combos = [(w1, w2) for w1, w2 in combinations(words, 2) if len(set(w1 + w2)) == 12]

# Filter to just the word sequences with connecting last/first letters
solutions = []
for w1, w2 in combos:
    if w1[-1] == w2[0]:
        solutions.append((w1, w2))
    elif w2[-1] == w1[0]:
        solutions.append((w2, w1))

# Print the solutions. You'll have to try questionable words
# manually in the puzzle to see if they're "valid".
print("Solutions sorted by letter length")
for s in sorted(solutions, key=lambda s: len(s[0] + s[1]), reverse=True):
    print(f"{s!r:30s} {len(s[0] + s[1]) - 1:2d}")

# Find the 'pencil-line' length for each solution
coords = (
    (0.2, 1.0),
    (0.5, 1.0),
    (0.8, 1.0),
    (1.0, 0.8),
    (1.0, 0.5),
    (1.0, 0.2),
    (0.8, 0.0),
    (0.5, 0.0),
    (0.2, 0.0),
    (0.0, 0.2),
    (0.0, 0.5),
    (0.0, 0.8),
)

lettercoords = {l: c for l, c in zip(letters, coords)}

totaldists = {}
traces = []
for s in solutions:
    trace = s[0] + s[1][1:]
    traces.append(trace)
    totaldist = 0
    for l0, l1 in zip(trace[0:-1], trace[1:]):
        c0x, c0y = lettercoords[l0]
        c1x, c1y = lettercoords[l1]
        d = ((c1x - c0x) ** 2 + (c1y - c0y) ** 2) ** 0.5
        totaldist += d
    totaldists[s] = totaldist

totaldists = {
    sol: pld
    for sol, pld in sorted(totaldists.items(), key=lambda item: item[1], reverse=True)
}

print("\nSolutions sorted by pencil-line distance")
for sol, pld in totaldists.items():
    print(f"{sol!r:30s} {pld:5.2f}")

# Get a list of the unique words used in all the solutions
flatsols = list(chain(*solutions))

# Get a count of all the 2-letter combinations in the solutions
lettercombos = Counter()
for t in traces:
    for l0, l1 in zip(t[0:-1], t[1:]):
        lettercombos[(l0, l1)] += 1

print()
print(f"There are {matchescnt} possible words from these letters.")
print(f"That drops to {matchescnt - doublescnt} when doubled letters are removed.")
print(
    f"That drops to {matchescnt - doublescnt - pairingscnt} when disallowed pairings are removed."
)
