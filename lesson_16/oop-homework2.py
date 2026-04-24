class Turtle:
    def __init__(self, x=0, y=0, s=1):
        """Инициализация черепашки с начальными координатами и шагом"""
        self.x = x
        self.y = y
        self.s = s

    def go_up(self):
        """Перемещение вверх"""
        self.y += self.s
        print(f"Перемещение вверх на {self.s}. Текущая позиция: ({self.x}, {self.y})")

    def go_down(self):
        """Перемещение вниз"""
        self.y -= self.s
        print(f"Перемещение вниз на {self.s}. Текущая позиция: ({self.x}, {self.y})")

    def go_left(self):
        """Перемещение влево"""
        self.x -= self.s
        print(f"Перемещение влево на {self.s}. Текущая позиция: ({self.x}, {self.y})")

    def go_right(self):
        """Перемещение вправо"""
        self.x += self.s
        print(f"Перемещение вправо на {self.s}. Текущая позиция: ({self.x}, {self.y})")

    def evolve(self):
        """Увеличивает шаг на 1"""
        self.s += 1
        print(f"Эволюция! Шаг увеличен до {self.s}")

    def degrade(self):
        """Уменьшает шаг на 1, если это возможно"""
        if self.s <= 1:
            raise Exception("Ошибка: Невозможно уменьшить шаг - он уже минимальный (1)")
        self.s -= 1
        print(f"Деградация! Шаг уменьшен до {self.s}")

    def count_moves(self, x2, y2):
        """
        Возвращает минимальное количество действий для достижения цели
        Действия: перемещение на s клеток или изменение s
        """
        # Вычисляем разницу по осям
        dx = abs(x2 - self.x)
        dy = abs(y2 - self.y)

        # Если черепашка уже на месте
        if dx == 0 and dy == 0:
            print(f"Черепашка уже в точке ({x2}, {y2})")
            return 0

        # Сначала пробуем достичь цели текущим шагом
        # Количество ходов по горизонтали и вертикали
        moves_x = dx // self.s if dx % self.s == 0 else dx // self.s + 1
        moves_y = dy // self.s if dy % self.s == 0 else dy // self.s + 1

        # Общее количество ходов (можно двигаться по диагонали, но так как
        # ходы только по осям, то нужно суммировать)
        total_moves = moves_x + moves_y

        # Проверяем, не выгоднее ли изменить шаг
        # Оптимальный шаг для достижения цели - это наибольший общий делитель?
        # Для простоты считаем, что изменение шага стоит 1 действие

        # Если расстояние маленькое, возможно выгоднее уменьшить шаг
        min_distance = min(dx, dy) if dx > 0 and dy > 0 else max(dx, dy)

        # Эвристика: если цель очень далеко, выгоднее увеличить шаг
        optimal_moves = total_moves

        # Пробуем варианты с изменением шага (упрощенная версия)
        for new_s in range(1, max(dx, dy) + 1):
            if new_s == self.s:
                continue

            # Стоимость изменения шага (сколько нужно эволюций/деградаций)
            change_cost = abs(new_s - self.s)

            # Количество ходов с новым шагом
            new_moves_x = dx // new_s if dx % new_s == 0 else dx // new_s + 1
            new_moves_y = dy // new_s if dy % new_s == 0 else dy // new_s + 1
            new_total_moves = new_moves_x + new_moves_y

            # Общая стоимость
            total_cost = change_cost + new_total_moves

            if total_cost < optimal_moves:
                optimal_moves = total_cost

        print(f"Минимальное количество действий для достижения ({x2}, {y2}): {optimal_moves}")
        return optimal_moves

# Пример использования
if __name__ == "__main__":
    turtle = Turtle(0, 0, 1)

    turtle.go_right()  # (1, 0)
    turtle.go_up()     # (1, 1)
    turtle.evolve()    # s = 2
    turtle.go_right()  # (3, 1)
    turtle.go_up()     # (3, 3)

    turtle.count_moves(10, 10)  # Минимальное количество действий

    # Демонстрация degrade с проверкой ошибки
    turtle = Turtle(0, 0, 1)
    try:
        turtle.degrade()  # Вызовет ошибку
    except Exception as e:
        print(e)

    # Демонстрация работы count_moves
    print("\n--- Демонстрация count_moves ---")
    t = Turtle(0, 0, 2)
    print(f"Старт: позиция ({t.x}, {t.y}), шаг {t.s}")
    t.count_moves(10, 0)  # Нужно 5 ходов вправо (по 2 клетки)

    t = Turtle(0, 0, 1)
    t.count_moves(5, 5)   # Нужно 10 ходов (5 вправо + 5 вверх)