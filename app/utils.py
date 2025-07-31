from functools import lru_cache

def pow_op(a: float, b: float) -> float:
    return a ** b

@lru_cache(maxsize=256)
def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

def fact(n: int) -> int:
    res = 1
    for i in range(2, n + 1):
        res *= i
    return res
