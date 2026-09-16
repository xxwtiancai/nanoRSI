# Ported from OpenEvolve https://github.com/codelion/openevolve (Apache-2.0, Copyright Asankhaya Sharma 2025)
# Source file: examples/function_minimization/initial_program.py (verbatim below this header).
# Only adaptation: this header; evaluation seeds the numpy global RNG per trial for reproducibility.
# The fixed (non-evolved) part must keep evaluate_function() unchanged.
# EVOLVE-BLOCK-START
"""Function minimization example for OpenEvolve"""
import numpy as np


def search_algorithm(iterations=1000, bounds=(-5, 5)):
    """
    Hybrid global-local search: uniform exploration followed by iterative
    local refinement (adaptive pattern search) around the best point found.

    Args:
        iterations: Number of iterations to run
        bounds: Bounds for the search space (min, max)

    Returns:
        Tuple of (best_x, best_y, best_value)
    """
    lo, hi = bounds
    span = hi - lo
    best_x = np.random.uniform(lo, hi)
    best_y = np.random.uniform(lo, hi)
    best_value = evaluate_function(best_x, best_y)

    # Global exploration phase (batched random sampling)
    n_global = max(1, int(iterations * 0.5))
    xs = np.random.uniform(lo, hi, size=n_global)
    ys = np.random.uniform(lo, hi, size=n_global)
    for x, y in zip(xs, ys):
        value = evaluate_function(x, y)
        if value < best_value:
            best_value = value
            best_x, best_y = x, y

    # Local refinement phase: pattern search with shrinking step,
    # restarting from the best points seen during exploration.
    remaining = max(0, iterations - n_global)
    candidates = [(best_x, best_y, best_value)]
    # keep a few promising samples as restart points
    vals = [evaluate_function(x, y) for x, y in zip(xs, ys)]
    order = np.argsort(vals)[: min(5, len(vals))]
    candidates += [(xs[i], ys[i], vals[i]) for i in order if vals[i] < float("inf")]

    per_candidate = max(1, remaining // max(1, len(candidates)))
    for cx, cy, cv in candidates:
        x, y, value = cx, cy, cv
        step = span / 4.0
        used = 0
        while used < per_candidate and step > 1e-12:
            improved = False
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1),
                           (0.7, 0.7), (-0.7, 0.7), (0.7, -0.7), (-0.7, -0.7)):
                if used >= per_candidate:
                    break
                nx = min(max(x + dx * step, lo), hi)
                ny = min(max(y + dy * step, lo), hi)
                nv = evaluate_function(nx, ny)
                used += 1
                if nv < value:
                    x, y, value = nx, ny, nv
                    improved = True
            if not improved:
                step *= 0.5
        if value < best_value:
            best_value = value
            best_x, best_y = x, y

    return best_x, best_y, best_value


# EVOLVE-BLOCK-END


# This part remains fixed (not evolved)
def evaluate_function(x, y):
    """The complex function we're trying to minimize"""
    return np.sin(x) * np.cos(y) + np.sin(x * y) + (x**2 + y**2) / 20


def run_search():
    x, y, value = search_algorithm()
    return x, y, value


if __name__ == "__main__":
    x, y, value = run_search()
    print(f"Found minimum at ({x}, {y}) with value {value}")
