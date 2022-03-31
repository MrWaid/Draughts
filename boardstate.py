from itertools import product

import numpy as np
from typing import Optional


class BoardState:

    def __init__(self, board: np.ndarray, current_player: int = 1):
        self.board: np.ndarray = board
        self.current_player: int = current_player

    def __eq__(self, other) -> bool:
        for x, y in product(range(8), range(8)):
            if self.board[y, x] != other.board[y, x]:
                return False
        return True

    def copy(self) -> 'BoardState':
        return BoardState(self.board.copy(), self.current_player)

    def do_move(self, from_x, from_y, to_x, to_y) -> Optional['BoardState']:
        # Возвращает новое состояние доски. Если что-то не так, None

        # Проверка ходов на адекватность
        if from_x == to_x and from_y == to_y:
            return None

        if (to_x + to_y) % 2 == 0:
            return None

        # Проверка на дамки
        result = self.copy()
        result.board[to_y, to_x] = result.board[from_y, from_x]
        if result.board[to_y, to_x] == 1 and to_y == 7:
            result.board[to_y, to_x] = 2
        if result.board[to_y, to_x] == -1 and to_y == 0:
            result.board[to_y, to_x] = -2
        result.board[from_y, from_x] = 0

        # Проверка на возможность кого-то съесть
        eat = self.get_possible_eat(from_x, from_y)
        if eat is not None:
            for i in eat:
                if i is not None and type(i) is not list:
                    if result.board[to_y, to_x] == i.board[to_y, to_x]:
                        if i.get_possible_eat(to_x, to_y) is None:
                            i.current_player *= -1
                        return i

        flag_not_eat = True
        for x, y in product(range(8), range(8)):
            if self.board[y, x] * self.current_player > 0:
                if self.get_possible_eat(x, y) is not None:
                    flag_not_eat = False

        if flag_not_eat:
            moves = self.get_possible_moves(from_x, from_y)
            if moves is not None:
                for i in moves:
                    if i is not None and type(i) is not list:
                        if result.board[to_y, to_x] * i.board[to_y, to_x] > 0:
                            i.current_player *= -1
                            return i

        return None

    def get_possible_moves(self, from_x, from_y) -> Optional['BoardState']:
        result = []

        # ход белой шашки
        if self.board[from_y, from_x] == 1:
            # вправо
            if from_y + 1 < 8 and from_x + 1 < 8:
                if self.board[from_y + 1, from_x + 1] == 0:
                    tmp = self.copy()
                    tmp.board[from_y + 1, from_x + 1] = tmp.board[from_y, from_x]
                    tmp.board[from_y, from_x] = 0
                    if from_y + 1 == 7:
                        tmp.board[from_y + 1, from_x + 1] = 2
                    result.append(tmp)

            # влево
            if from_y + 1 < 8 and from_x - 1 > -1:
                if self.board[from_y + 1, from_x - 1] == 0:
                    tmp = self.copy()
                    tmp.board[from_y + 1, from_x - 1] = tmp.board[from_y, from_x]
                    tmp.board[from_y, from_x] = 0
                    if from_y + 1 == 7:
                        tmp.board[from_y + 1, from_x - 1] = 2
                    result.append(tmp)

        # ход черной шашки
        if self.board[from_y][from_x] == -1:
            # вправо
            if from_y - 1 > -1 and from_x + 1 < 8:
                if self.board[from_y - 1, from_x + 1] == 0:
                    tmp = self.copy()
                    tmp.board[from_y - 1, from_x + 1] = tmp.board[from_y, from_x]
                    tmp.board[from_y, from_x] = 0
                    if from_y - 1 == 0:
                        tmp.board[from_y - 1, from_x + 1] = -2
                    result.append(tmp)

            # влево
            if from_y - 1 > -1 and from_x - 1 > -1:
                if self.board[from_y - 1, from_x - 1] == 0:
                    tmp = self.copy()
                    tmp.board[from_y - 1, from_x - 1] = tmp.board[from_y, from_x]
                    tmp.board[from_y, from_x] = 0
                    if from_y - 1 == 0:
                        tmp.board[from_y - 1, from_x - 1] = -2
                    result.append(tmp)

        # ход дамки
        if abs(self.board[from_y, from_x]) == 2:
            # вперед вправо
            for i in range(1, 8):
                if from_y + i < 8 and from_x + i < 8:
                    if self.board[from_y + i, from_x + i] == 0:
                        tmp = self.copy()
                        tmp.board[from_y + i, from_x + i] = tmp.board[from_y, from_x]
                        tmp.board[from_y, from_x] = 0
                        result.append(tmp)
                    else:
                        break

            # вперед влево
            for i in range(1, 8):
                if from_y + i < 8 and from_x - i > -1:
                    if self.board[from_y + i, from_x - i] == 0:
                        tmp = self.copy()
                        tmp.board[from_y + i, from_x - i] = tmp.board[from_y, from_x]
                        tmp.board[from_y, from_x] = 0
                        result.append(tmp)
                    else:
                        break

            # назад вправо
            for i in range(1, 8):
                if from_y - i < 8 and from_x + i < 8:
                    if self.board[from_y - i, from_x + i] == 0:
                        tmp = self.copy()
                        tmp.board[from_y - i, from_x + i] = tmp.board[from_y, from_x]
                        tmp.board[from_y, from_x] = 0
                        # print("forward right")
                        result.append(tmp)
                    else:
                        break

            # назад влево
            for i in range(1, 8):
                if from_y - i < 8 and from_x - i > -1:
                    if self.board[from_y - i, from_x - i] == 0:
                        tmp = self.copy()
                        tmp.board[from_y - i, from_x - i] = tmp.board[from_y, from_x]
                        tmp.board[from_y, from_x] = 0
                        result.append(tmp)
                    else:
                        break

        if not result:
            return None
        return result

    def get_possible_eat(self, from_x: int, from_y: int) -> Optional['BoardState']:
        result = []

        # ест шашка
        if abs(self.board[from_y, from_x]) == 1:
            # ест вперед вправо
            if from_y + 2 < 8 and from_x + 2 < 8:
                if self.board[from_y + 1, from_x + 1] * self.board[from_y, from_x] < 0:
                    if self.board[from_y + 2, from_x + 2] == 0:
                        tmp = self.copy()
                        tmp.board[from_y + 2, from_x + 2] = tmp.board[from_y, from_x]
                        tmp.board[from_y, from_x] = 0
                        tmp.board[from_y + 1, from_x + 1] = 0
                        if from_y + 2 == 7 and self.board[from_y + 2, from_x + 2] == 1:
                            tmp.board[from_y + 2, from_x + 2] = 2
                        result.append(tmp)

            # ест вперед влево
            if from_y + 2 < 8 and from_x - 2 > -1:
                if self.board[from_y + 1, from_x - 1] * self.board[from_y, from_x] < 0:
                    if self.board[from_y + 2, from_x - 2] == 0:
                        tmp = self.copy()
                        tmp.board[from_y + 2, from_x - 2] = tmp.board[from_y, from_x]
                        tmp.board[from_y, from_x] = 0
                        tmp.board[from_y + 1, from_x - 1] = 0
                        if from_y + 2 == 7 and self.board[from_y + 2, from_x - 2] == 1:
                            tmp.board[from_y + 2, from_x - 2] = 2
                        result.append(tmp)

            # ест назад вправо
            if from_y - 2 > -1 and from_x + 2 < 8:
                if self.board[from_y - 1, from_x + 1] * self.board[from_y, from_x] < 0:
                    if self.board[from_y - 2, from_x + 2] == 0:
                        tmp = self.copy()
                        tmp.board[from_y - 2, from_x + 2] = tmp.board[from_y, from_x]
                        tmp.board[from_y, from_x] = 0
                        tmp.board[from_y - 1, from_x + 1] = 0
                        if from_y - 2 == 0 and self.board[from_y - 2, from_x + 2] == -1:
                            tmp.board[from_y - 2, from_x + 2] = -2
                        result.append(tmp)

            # ест назад влево
            if from_y - 2 > -1 and from_x - 2 > -1:
                if self.board[from_y - 1, from_x - 1] * self.board[from_y, from_x] < 0:
                    if self.board[from_y - 2, from_x - 2] == 0:
                        tmp = self.copy()
                        tmp.board[from_y - 2, from_x - 2] = tmp.board[from_y, from_x]
                        tmp.board[from_y, from_x] = 0
                        tmp.board[from_y - 1, from_x - 1] = 0
                        if from_y - 2 == 0 and self.board[from_y - 2, from_x - 2] == -1:
                            tmp.board[from_y - 2, from_x - 2] = -2
                        result.append(tmp)

        # ест дамка
        if abs(self.board[from_y, from_x]) == 2:
            # вперед вправо
            if from_y != 7 and from_x != 7:
                i = 1
                while from_y + i + 1 < 8 and from_x + i + 1 < 8 and self.board[from_y + i, from_x + i] == 0:
                    i += 1
                if self.board[from_y + i, from_x + i] * self.board[from_y, from_x] < 0:
                    j = 1
                    while from_y + i + j < 8 and from_x + i + j < 8:
                        if self.board[from_y + i + j, from_x + i + j] == 0:
                            tmp = self.copy()
                            tmp.board[from_y + i + j, from_x + i + j] = tmp.board[from_y, from_x]
                            tmp.board[from_y + i, from_x + i] = 0
                            tmp.board[from_y, from_x] = 0
                            result.append(tmp)
                        else:
                            break
                        j += 1

            # вперед влево
            if from_y != 7 and from_x != 0:
                i = 1
                while from_y + i + 1 < 8 and from_x - i - 1 > -1 and self.board[from_y + i, from_x - i] == 0:
                    i += 1
                if self.board[from_y + i, from_x - i] * self.board[from_y, from_x] < 0:
                    j = 1
                    while from_y + i + j < 8 and from_x - i - j > -1:
                        if self.board[from_y + i + j, from_x - i - j] == 0:
                            tmp = self.copy()
                            tmp.board[from_y + i + j, from_x - i - j] = tmp.board[from_y, from_x]
                            tmp.board[from_y + i, from_x - i] = 0
                            tmp.board[from_y, from_x] = 0
                            result.append(tmp)
                        else:
                            break
                        j += 1

            # назад вправо
            if from_y != 0 and from_x != 7:
                i = 1
                while from_y - i - 1 > -1 and from_x + i + 1 < 8 and self.board[from_y - i, from_x + i] == 0:
                    i += 1
                if self.board[from_y - i, from_x + i] * self.board[from_y, from_x] < 0:
                    j = 1
                    while from_y - i - j > -1 and from_x + i + j < 8:
                        if self.board[from_y - i - j, from_x + i + j] == 0:
                            tmp = self.copy()
                            tmp.board[from_y - i - j, from_x + i + j] = tmp.board[from_y, from_x]
                            tmp.board[from_y - i, from_x + i] = 0
                            tmp.board[from_y, from_x] = 0
                            result.append(tmp)
                        else:
                            break
                        j += 1

            # назад влево
            if from_y != 0 and from_x != 0:
                i = 1
                while from_y - i - 1 > -1 and from_x - i - 1 > -1 and self.board[from_y - i, from_x - i] == 0:
                    i += 1
                if self.board[from_y - i, from_x - i] * self.board[from_y, from_x] < 0:
                    j = 1
                    while from_y - i - j > -1 and from_x - i - j > -1:
                        if self.board[from_y - i - j, from_x - i - j] == 0:
                            tmp = self.copy()
                            tmp.board[from_y - i - j, from_x - i - j] = tmp.board[from_y, from_x]
                            tmp.board[from_y - i, from_x - i] = 0
                            tmp.board[from_y, from_x] = 0
                            result.append(tmp)
                        else:
                            break
                        j += 1

        if not result:
            return None
        return result

    @property
    def is_game_finished(self) -> int:
        flag_white = False
        flag_black = False
        for x, y in product(range(8), range(8)):
            if self.board[y, x] > 0:
                flag_white = True
            if self.board[y, x] < 0:
                flag_black = True
        if not flag_black:
            return 1
        if not flag_white:
            return -1

        return 0

    def initial_state(self) -> 'BoardState':
        #  1 - Шашка белая
        #  2 - Дамка белая
        # -1 - Шашка черная
        # -2 - Дамка черная

        self.board = np.zeros(shape=(8, 8), dtype=np.int8)

        self.board[7, 0] = -1
        self.board[7, 2] = -1
        self.board[7, 4] = -1
        self.board[7, 6] = -1
        self.board[6, 1] = -1
        self.board[6, 3] = -1
        self.board[6, 5] = -1
        self.board[6, 7] = -1
        self.board[5, 0] = -1
        self.board[5, 2] = -1
        self.board[5, 4] = -1
        self.board[5, 6] = -1

        self.board[0, 1] = 1
        self.board[0, 3] = 1
        self.board[0, 5] = 1
        self.board[0, 7] = 1
        self.board[1, 0] = 1
        self.board[1, 2] = 1
        self.board[1, 4] = 1
        self.board[1, 6] = 1
        self.board[2, 1] = 1
        self.board[2, 3] = 1
        self.board[2, 5] = 1
        self.board[2, 7] = 1

        return BoardState(self.board, 1)

    @staticmethod
    def save_state(self, name: str):
        if name == 'saves.txt':
            f = open(name, 'w')
        else:
            f = open(name, 'a')
        for y, x in product(range(8), range(8)):
            f.write(str(self.board[y][x] + 2))
        f.write(str(self.current_player + 1))
        f.write("\n")
        f.close()

    @staticmethod
    def load_state(self, name: str) -> 'BoardState':
        f = open(name, 'r')
        value = ""
        for line in f:
            value = ""
            for char in line:
                value += char
        i = 0
        if len(value) > 0:
            for y, x in product(range(8), range(8)):
                self.board[y][x] = int(value[i]) - 2
                i += 1
            self.current_player = int(value[i]) - 1

        f.close()

        return BoardState(self.board, self.current_player)
