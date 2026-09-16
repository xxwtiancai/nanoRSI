# Ported from ShinkaEvolve https://github.com/SakanaAI/ShinkaEvolve (Apache-2.0, Copyright Sakana AI 2025)
# Source file: examples/sine_approx_headless/initial.py (verbatim below this header).
# Only adaptation: this header. Direct sine implementations are blocked by the evaluator.
# EVOLVE-BLOCK-START
def approximate(x: float) -> float:
    # Odd polynomial fit approximating sin(x) on [-pi, pi]
    x2 = x * x
    # Higher-order odd polynomial (Taylor series truncated after x^13):
    # sin(x) ~ x - x^3/3! + x^5/5! - x^7/7! + x^9/9! - x^11/11! + x^13/13!
    # Max truncation error on [-pi, pi] is ~pi^15/15! ~ 2.3e-10.
    c3 = -1.0 / 6.0
    c5 = 1.0 / 120.0
    c7 = -1.0 / 5040.0
    c9 = 1.0 / 362880.0
    c11 = -1.0 / 39916800.0
    c13 = 1.0 / 6227020800.0
    return x * (1.0 + x2 * (c3 + x2 * (c5 + x2 * (c7 + x2 * (c9 + x2 * (c11 + x2 * c13))))))


# EVOLVE-BLOCK-END
