# Игра Snake

## Игровой процесс

Вы управляете змеёй используя клавиши стрелок. На поле появляются яблоки: обычное - увеличивает длину на 1 и золотое -
увеличивает длину на 3. При завершении игры выводится итоговый счёт, и при нажатии на любую клавишу игры начинается
заново.

## Основные классы

### Класс Snake
Используется для создания, обработки и рисования змеи.

### Класс Food
Использутся для создания яблок.

### Класс Game
Основной класс игры. Обрабатывает все события. Запускает, перезапускает и завершает игру.

## Установка
Установка программы не требуется, однако для ее работы требуется установить библиотеку Pygame.
Сделать это можно с помощью [pip](https://pip.pypa.io/en/stable/).

```bash
pip install Pygame
```

## Запуск программы
Запуск программы осуществляется путем запуска главного файла программы Snake.py либо "двойным" кликом по нему, либо из
любой IDE. Кроме того, можно использовать и командную строку

```bash
python Snake.py
```

