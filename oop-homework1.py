class CashBox:
    def __init__(self, initial_amount=0):
        """Инициализация кассы с начальной суммой"""
        self.money = initial_amount

    def top_up(self, X):
        """Пополнить кассу на X рублей"""
        if X <= 0:
            raise ValueError("Сумма пополнения должна быть положительной")
        self.money += X
        print(f"Касса пополнена на {X} руб. Текущий баланс: {self.money} руб.")

    def count_1000(self):
        """Выводит количество целых тысяч в кассе"""
        thousands = self.money // 1000
        print(f"В кассе {thousands} целых тысяч")
        return thousands

    def take_away(self, X):
        """Забрать X рублей из кассы"""
        if X > self.money:
            raise Exception(f"Ошибка: Недостаточно денег в кассе! "
                          f"Требуется {X} руб., доступно {self.money} руб.")
        self.money -= X
        print(f"Из кассы забрали {X} руб. Остаток: {self.money} руб.")
        return X

# Пример использования
if __name__ == "__main__":
    cash = CashBox(5000)
    cash.count_1000()  # 5 тысяч

    cash.top_up(2500)
    cash.count_1000()  # 7 тысяч

    cash.take_away(3200)
    cash.count_1000()  # 4 тысячи

    try:
        cash.take_away(10000)  # Вызовет ошибку
    except Exception as e:
        print(e)