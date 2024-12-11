def change(coins, amount):
  
  if amount == 0:
    return 0
  else:
    min_coins = float("inf")
    for coin in coins:
      if amount >= coin:
        sub_coins = change(coins, amount - coin)
        min_coins = min(min_coins, sub_coins + 1)
    return min_coins


if __name__ == "__main__":
  coins = [1, 10]
  amount = 11
  print(f'Total need {change(coins, amount)} coins')