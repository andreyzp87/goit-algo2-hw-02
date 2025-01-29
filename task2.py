from typing import List, Dict

def rod_cutting_memo(length: int, prices: List[int]) -> Dict:
    """
    Знаходить оптимальний спосіб розрізання через мемоізацію

    Args:
        length: довжина стрижня
        prices: список цін, де prices[i] — ціна стрижня довжини i+1

    Returns:
        Dict з максимальним прибутком та списком розрізів
    """
    memo = {}
    cuts_memo = {}

    def solve(n):
        if n == 0:
            return 0, []
        if n in memo:
            return memo[n], cuts_memo[n]

        max_profit = float('-inf')
        best_cuts = []

        for i in range(n):
            current_profit, current_cuts = solve(i)
            if current_profit + prices[n - 1 - i] > max_profit:
                max_profit = current_profit + prices[n - 1 - i]
                best_cuts = current_cuts + [n - i]

        memo[n] = max_profit
        cuts_memo[n] = best_cuts
        return max_profit, best_cuts

    max_profit, cuts = solve(length)
    cuts.sort(reverse=True)

    return {
        "max_profit": max_profit,
        "cuts": cuts,
        "number_of_cuts": len(cuts) - 1 if cuts else 0
    }


def rod_cutting_table(length: int, prices: List[int]) -> Dict:
    """
    Знаходить оптимальний спосіб розрізання через табуляцію

    Args:
        length: довжина стрижня
        prices: список цін, де prices[i] — ціна стрижня довжини i+1

    Returns:
        Dict з максимальним прибутком та списком розрізів
    """

    table = [0] * (length + 1)
    cuts = [[] for _ in range(length + 1)]

    # Заповнення таблиці
    for i in range(1, length + 1):
        max_profit = float('-inf')
        best_cuts = []

        for j in range(1, i + 1):
            current_profit = prices[j - 1] + table[i - j]
            if current_profit > max_profit:
                max_profit = current_profit
                best_cuts = cuts[i - j] + [j]

        table[i] = max_profit
        cuts[i] = best_cuts

    final_cuts = cuts[length]
    final_cuts.sort(reverse=True)

    return {
        "max_profit": table[length],
        "cuts": final_cuts,
        "number_of_cuts": len(final_cuts) - 1 if final_cuts else 0
    }


def run_tests():
    """Функція для запуску всіх тестів"""
    test_cases = [
        # Тест 1: Базовий випадок
        {
            "length": 5,
            "prices": [2, 5, 7, 8, 10],
            "name": "Базовий випадок"
        },
        # Тест 2: Оптимально не різати
        {
            "length": 3,
            "prices": [1, 3, 8],
            "name": "Оптимально не різати"
        },
        # Тест 3: Всі розрізи по 1
        {
            "length": 4,
            "prices": [3, 5, 6, 7],
            "name": "Рівномірні розрізи"
        }
    ]

    for test in test_cases:
        print(f"\nТест: {test['name']}")
        print(f"Довжина стрижня: {test['length']}")
        print(f"Ціни: {test['prices']}")

        # Тестуємо мемоізацію
        memo_result = rod_cutting_memo(test['length'], test['prices'])
        print("\nРезультат мемоізації:")
        print(f"Максимальний прибуток: {memo_result['max_profit']}")
        print(f"Розрізи: {memo_result['cuts']}")
        print(f"Кількість розрізів: {memo_result['number_of_cuts']}")

        # Тестуємо табуляцію
        table_result = rod_cutting_table(test['length'], test['prices'])
        print("\nРезультат табуляції:")
        print(f"Максимальний прибуток: {table_result['max_profit']}")
        print(f"Розрізи: {table_result['cuts']}")
        print(f"Кількість розрізів: {table_result['number_of_cuts']}")

        print("\nПеревірка пройшла успішно!")

if __name__ == "__main__":
    run_tests()
