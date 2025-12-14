from __future__ import annotations

from typing import Any, Callable, Iterable, List, Optional, TypeVar

T = TypeVar("T")


def fsort(iterable: Iterable[T], /, *, key: Optional[Callable[[T], Any]] = None, reverse: bool = False) -> List[T]:
    a: List[T] = iterable if isinstance(iterable, list) else list(iterable)

    if key is not None:
        return sorted(a, key=key, reverse=reverse)

    if _should_try_numpy(a):
        out = _numpy_sort(a, reverse=reverse)
        if out is not None:
            return out

    try:
        return sorted(a, reverse=reverse)
    except TypeError:
        return sorted(a, key=_safe_total_key, reverse=reverse)


def _safe_total_key(x: Any) -> Any:
    t = type(x)
    if x is None:
        return ("NoneType", 0)
    if isinstance(x, (int, float, str, bytes, bool)):
        return (t.__name__, x)
    if isinstance(x, (tuple, list)):
        return (t.__name__, tuple(_safe_total_key(v) for v in x))
    return (t.__name__, repr(x))


def _should_try_numpy(a: List[Any]) -> bool:
    n = len(a)
    if n < 80_000:
        return False

    import random

    step = max(1, n // 64)
    seen = 0
    for i in range(0, n, step):
        x = a[i]
        if not isinstance(x, (int, float, bool)):
            return False
        seen += 1
        if seen >= 64:
            break

    rng = random.Random(12345)
    samples = 48
    desc = 0
    total = 0

    try:
        for _ in range(samples):
            i = rng.randrange(0, n - 1)
            if a[i] > a[i + 1]:
                desc += 1
            total += 1
    except TypeError:
        return False

    frac = desc / total if total else 0.0
    if frac < 0.05 or frac > 0.95:
        return False

    return True


def _numpy_sort(a: List[T], *, reverse: bool) -> Optional[List[T]]:
    try:
        import numpy as np
    except Exception:
        return None

    try:
        arr = np.array(a)
    except Exception:
        return None

    if arr.dtype == object:
        return None

    try:
        arr.sort(kind="quicksort")
    except Exception:
        return None

    if reverse:
        arr = arr[::-1]

    out = arr.tolist()
    return out
