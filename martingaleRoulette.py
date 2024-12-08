import random

HEADS = "heads"
TAILS = "tails"
COIN_VALUES1 = [HEADS, TAILS]


def flip_coin():
    return random.choice(COIN_VALUES1)


def martingale(*, money: int, min_bet: int, max_bet: int) -> int:
    steps_to_loose = 0
    current_funds = money
    current_bet = min_bet
    
    while current_funds >= 0:
        steps_to_loose += 1
        current_funds -= current_bet
        if current_funds <= -1:
            break
        flipped_coin_value = flip_coin()
        
        if flipped_coin_value == HEADS:
            win = current_bet * 2
            current_funds += win 
            current_bet = min_bet
        else:
            current_bet *= 2
            if current_bet > max_bet:
                current_bet = min_bet
            if current_bet > current_funds:
                current_bet = current_funds

    return steps_to_loose


# print(martingale(money=100, min_bet=1, max_bet=100))


def simulate_martingale_for_n_players(*, money: int, min_bet: int, max_bet: int, n_games: int) -> float:
    total_steps_to_lose = 0
    for i in range (n_games):
        step_to_lose = martingale(money=money, min_bet=min_bet, max_bet=max_bet)
        total_steps_to_lose += step_to_lose
        
    return total_steps_to_lose / n_games
        

print(simulate_martingale_for_n_players(
    n_games=10,
    money=100000,
    min_bet=1,
    max_bet=100000,
))