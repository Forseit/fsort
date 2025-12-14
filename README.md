SSORTED

Package goal
fsort() is a drop-in replacement for Python sorted().

What it does
1) If data is huge numeric and looks random-ish, it may use NumPy for speed.
2) Otherwise it uses built-in sorted().
3) If elements are not mutually comparable, it falls back to a safe deterministic order.

Install from GitHub
pip install git+https://github.com/Forseit/fsort.git

Install from GitHub with NumPy acceleration
pip install "fsort[numpy] @ git+https://github.com/Forseit/fsort.git"

Usage
from fsort import fsort

print(fsort([3, 1, 2]))
print(fsort([3, 1, 2], reverse=True))
print(fsort(["b", "aa", "a"]))

Same signature as sorted()
fsort(iterable, *, key=None, reverse=False) -> list

Run tests locally
pip install -e ".[test]"
pytest -q
