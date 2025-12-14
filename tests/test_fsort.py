import random
from ssorted import fsort


class Obj:
    def __init__(self, v: int, name: str):
        self.v = v
        self.name = name

    def __repr__(self) -> str:
        return f"Obj(v={self.v}, name={self.name})"


def test_ints_up_to_1e18():
    rnd = random.Random(1)
    for _ in range(30):
        n = rnd.randrange(0, 5000)
        a = [rnd.randrange(-10**18, 10**18) for _ in range(n)]
        assert fsort(a) == sorted(a)


def test_reverse():
    a = [3, 1, 2]
    assert fsort(a, reverse=True) == [3, 2, 1]


def test_key_objects_stable():
    a = [Obj(3, "c"), Obj(1, "a"), Obj(2, "b"), Obj(1, "x")]
    out = fsort(a, key=lambda o: o.v)
    assert [o.v for o in out] == [1, 1, 2, 3]
    assert [o.name for o in out if o.v == 1] == ["a", "x"]


def test_mixed_types_no_crash():
    a = [1, "2", 3.0, None, (1, "x"), {"a": 1}, Obj(2, "x")]
    out = fsort(a)
    assert len(out) == len(a)
