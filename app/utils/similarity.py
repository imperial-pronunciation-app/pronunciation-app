# From https://www.geeksforgeeks.org/edit-distance-dp-5/
def edit_dist(s1: str, s2: str) -> int:
    m, n = len(s1), len(s2)
    prev = 0  # Stores dp[i-1][j-1]
    curr = list(range(n + 1))  # Stores dp[i][j-1] and dp[i][j]

    for i in range(1, m + 1):
        prev = curr[0]
        curr[0] = i
        for j in range(1, n + 1):
            temp = curr[j]
            if s1[i - 1] == s2[j - 1]:
                curr[j] = prev
            else:
                curr[j] = 1 + min(curr[j - 1], prev, curr[j])
            prev = temp
    return curr[n]


def similarity(target: str, transcribed: str) -> int:
    return int((1 - edit_dist(target, transcribed) / len(target)) * 100)
