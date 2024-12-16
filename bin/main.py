"""Given the list of letters from the NY Times "Letterboxed" game,
generate some possible solutions. Note that the file in WORDLIST
contains many words not recognized as such by the game, which you can
add after the letter list to omit from consideration.
"""

from itertools import combinations, permutations
from pathlib import Path
import re
import sys

WORDLIST = "/home/mark/word.list"
WORDS = Path(WORDLIST).read_text().splitlines()

# Remove words with doubled letters
fwords = [word for word in WORDS if not re.search(r"([a-z])\1", word)]

# Get command-line arguments
letters, nonwords = list(sys.argv[1]), sys.argv[2:]

# Find all the words that use only the given letters
pat = re.compile(f"^[{''.join(letters)}]+$")
matches = [w for w in fwords if pat.search(w)]

# Remove words that have sequences of letters
# that appear on the same side of the square.
sides = [letters[0:3], letters[3:6], letters[6:9], letters[9:12]]
patstr = ["|".join(["".join(l) for l in permutations(side, 2)]) for side in sides]
pat = re.compile("|".join(patstr))
matches = [word for word in matches if not pat.search(word)]

matches = [word for word in matches if word not in nonwords]

# Find the 2-word combinations that use all the given letters
combos = [(w1, w2) for w1, w2 in combinations(matches, 2) if len(set(w1 + w2)) == 12]

# Filter to just the word sequences with connecting last/first letters
solutions = []
for w1, w2 in combos:
    if w1[-1] == w2[0]:
        solutions.append((w1, w2))
    elif w2[-1] == w1[0]:
        solutions.append((w2, w1))

# Print the solutions. You'll have to try questionable words
# manually in the puzzle to see if they're "valid".
for s in sorted(solutions, key=lambda s: len(s[0] + s[1]), reverse=True):
    print(s)
