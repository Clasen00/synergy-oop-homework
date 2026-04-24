Данный репозиторий - это набор лабораторных работы, которые относятся к различным урокам университета Синергия по предмету ЯП Python. 

 Файл [oop-homework1.py](https://github.com/Clasen00/synergy-oop-homework/blob/main/lesson_16/oop-homework1.py) - это задание №1 "Касса" из урока 16: "классы и объекты".

## Описание
```txt
Создайте класс Касса, который хранит текущее количество денег в кассе, у него есть методы:

top_up(X) - пополнить на X
count_1000() - выводит сколько целых тысяч осталось в кассе
take_away(X) - забрать X из кассы, либо выкинуть ошибку, что не достаточно денег
```
Файл [oop-homework2.py](https://github.com/Clasen00/synergy-oop-homework/blob/main/lesson_16/oop-homework2.py) это задание №2 "Черепашка".

## Описание
```txt
Создайте класс Черепашка, который хранит позиции x и y черепашки, а также s - количество клеточек, на которое она перемещается за ход

у этого класс есть методы:

go_up() - увеличивает y на s
go_down() - уменьшает y на s
go_left() - уменьшает x на s
go_right() - увеличивает y на s
evolve() - увеличивает s на 1
degrade() - уменьшает s на 1 или выкидывает ошибку, когда s может стать ≤ 0
count_moves(x2, y2) - возвращает минимальное количество действий, за которое черепашка сможет добраться до x2 y2 от текущей позиции
```

## Запуск

```bash
git clone https://github.com/Clasen00/synergy-oop-homework.git
cd synergy-oop-homework/lesson_16
python oop-homework1.py
python oop-homework2.py
```

Файл [Game.py](https://github.com/Clasen00/synergy-oop-homework/blob/main/lesson_23/Game.py) Содержит в себе код для игры из задания 23 "Проект создание Игры"

## Запуск

```bash
git clone https://github.com/Clasen00/synergy-oop-homework.git
cd synergy-oop-homework/lesson_23
python Game.py
```