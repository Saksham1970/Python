"""
Project Euler Problem 66: https://projecteuler.net/problem=66

Consider quadratic Diophantine equations of the form:

x2 - Dy2 = 1

For example, when D=13, the minimal solution in x is 6492 - 13*1802 = 1.

It can be assumed that there are no solutions in positive integers when D is square.

By finding minimal solutions in x for D = {2, 3, 5, 6, 7}, we obtain the following:

32 - 2*22 = 1
22 - 3*12 = 1
92 - 5*42 = 1
52 - 6*22 = 1
82 - 7*32 = 1

Hence, by considering minimal solutions in x for D ≤ 7, the largest x is obtained
when D=5.

Find the value of D ≤ 1000 in minimal solutions of x for which the largest value
of x is obtained.

"""

from math import floor, log10, sqrt


# Modified form of continuous_fraction_period from /project_eular/problem_064/sol1.py
def sqrt_continued_fraction(num: int) -> list[int]:
    """
    Returns the continued fraction of square root of a number num.

    >>> sqrt_continued_fraction(2)
    [1, 2]
    >>> sqrt_continued_fraction(5)
    [2, 4]
    >>> sqrt_continued_fraction(7)
    [2, 1, 1, 1, 4]
    >>> sqrt_continued_fraction(11)
    [3, 3, 6]
    >>> sqrt_continued_fraction(13)
    [3, 1, 1, 1, 1, 6]
    """
    continued_fraction_list: list[int] = []
    numerator = 0.0
    denominator = 1.0
    ROOT = int(sqrt(num))
    integer_part = ROOT
    continued_fraction_list.append(integer_part)
    while integer_part != 2 * ROOT:
        numerator = denominator * integer_part - numerator
        denominator = (num - numerator**2) / denominator
        integer_part = int((ROOT + numerator) / denominator)
        continued_fraction_list.append(integer_part)
    return continued_fraction_list


def sqrt_convergent_numerator(series: list[int], index: int) -> int:
    """
    Returns the numerator of (index+1)th convergent of
    reapeating square root style continued fraction series.

    >>> sqrt_convergent_numerator([0,1,5,2,2],0)
    0
    >>> sqrt_convergent_numerator([0,1,5,2,2],2)
    5
    >>> sqrt_convergent_numerator([0,1,5,2,2],4)
    27
    >>> sqrt_convergent_numerator([1,1,2],1)
    2
    >>> sqrt_convergent_numerator([1,1,2],7)
    97
    """

    a = [1, series[0]]
    repeat = series[1:]
    period = len(repeat)

    i = 1
    while len(a) - 2 < index:
        a.append(repeat[(i - 1) % period] * a[i] + a[i - 1])
        i += 1
    return a[index + 1]


def solution(num: int = 1000) -> int:
    """
    Solution works on the fact that Diophantine equations fundamental solutions
    are the h_(r-1) (if r is even) or h_2r-1 (if r is odd) terms of
    continued fraction series of sqrt of D.
    Here h is the numerator of convergent of the series.
    r is the repeating period.

    Returns the D where x is maximum

    >>> solution(7)
    5
    >>> solution(10)
    10
    """

    max_val: float = 0  # Storing the max value of log(x)
    index = 0  # Storing the index of x which is maximum
    for i in range(2, num + 1):
        sr = sqrt(i)
        if sr - floor(sr) != 0:  # Equation not valid for a perfect square
            continued_fraction_series = sqrt_continued_fraction(i)
            max_element = max(continued_fraction_series)
            period = len(continued_fraction_series) - 1
            if period % 2 != 0:
                period = 2 * period

            # Estimating Max value a series can achieve without
            # actually calculating to save computation
            if (period) * log10(2 * max_element) >= max_val:

                # Checking actual value of series with max value
                value = log10(
                    sqrt_convergent_numerator(continued_fraction_series, period - 1)
                )
                if value >= max_val:
                    max_val = value
                    index = i
    return index


if __name__ == "__main__":
    print(f"{solution() = }")
