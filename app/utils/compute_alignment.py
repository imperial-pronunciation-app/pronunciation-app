from typing import Callable, List, Optional, Tuple, TypeVar

import numpy as np


T = TypeVar("T")

def compute_alignment(
    expected: List[T],
    actual: List[T],
    similarity_func: Callable[[T, T], float],
    deletion_penalty: float = -1.0,
    insertion_penalty: float = -0.5
) -> Tuple[List[Tuple[Optional[T], Optional[T]]], int]:
    """
    Generalized function to align two sequences using dynamic programming.
    Developed with assistance of ChatGPT (OpenAI).

    :param expected: List of expected items.
    :param actual: List of actual items.
    :param similarity_func: Function to compute similarity between items of type `T`.
    :param deletion_penalty: Penalty for missing an expected item.
    :param insertion_penalty: Penalty for adding an extra item.
    :return: Tuple of aligned sequences and a score (0-100).
    """

    if not expected:
        raise ValueError("Expected list must not be empty.")

    if not actual:
        return [(item, None) for item in expected], 0  # All expected items are missing.

    n, m = len(expected), len(actual)
    dp = np.zeros((n + 1, m + 1))
    backtrace = np.zeros((n + 1, m + 1), dtype=int)

    # Initialize DP table
    for i in range(1, n + 1):
        dp[i][0] = dp[i - 1][0] + deletion_penalty  # Deletion penalty
        backtrace[i][0] = 2  # Indicates deletion

    for j in range(1, m + 1):
        dp[0][j] = dp[0][j - 1] + insertion_penalty  # Insertion penalty
        backtrace[0][j] = 3  # Indicates insertion

    # Fill DP table
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            match_score = similarity_func(expected[i - 1], actual[j - 1])
            choices = [
                (dp[i - 1][j - 1] + match_score, 1),  # Match or substitution
                (dp[i - 1][j] + deletion_penalty, 2),  # Deletion
                (dp[i][j - 1] + insertion_penalty, 3)  # Insertion
            ]
            dp[i][j], backtrace[i][j] = max(choices, key=lambda x: x[0])

    # Backtracking to extract alignment
    i, j = n, m
    alignment: List[Tuple[Optional[T], Optional[T]]] = []
    while i > 0 or j > 0:
        if j > 0 and backtrace[i][j] == 3:  # Insertion
            alignment.append((None, actual[j - 1]))
            j -= 1
        elif i > 0 and backtrace[i][j] == 2:  # Deletion
            alignment.append((expected[i - 1], None))
            i -= 1
        elif i > 0 and j > 0 and backtrace[i][j] == 1:  # Match or substitution
            alignment.append((expected[i - 1], actual[j - 1]))
            i -= 1
            j -= 1
        else:
            # Fallback to avoid infinite loop
            break  

    alignment.reverse()
    final_score = int((dp[n][m] / max(1, n)) * 100)  # Normalize to 0-100

    return alignment, max(0, min(100, final_score))  # Clamp score between 0-100
