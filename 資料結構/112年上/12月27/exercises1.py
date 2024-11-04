def partition_equal_sum(A):

  n = len(A)
  sum_A = sum(A)
  dp = [[False for _ in range(sum_A + 1)] for _ in range(n + 1)]

  for i in range(n + 1):
    for j in range(sum_A + 1):
      if j == 0:
        dp[i][j] = True
      elif i == 0:
        dp[i][j] = False
      elif i >= j:
        dp[i][j] = dp[i][j - 1]
      else:
        dp[i][j] = dp[i][j - 1] or dp[i - A[i - 1]][j - 1]

  return dp[n][sum_A]


A = [5, 4, 9]
print(partition_equal_sum(A))