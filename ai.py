from itertools import product
from typing import Optional

from boardstate import BoardState


def draught(board: BoardState, current_player: int) -> int:

    draughts = 0
    if board is None:
        return 0
    for x, y in product(range(8), range(8)):
        if board.board[y, x] * current_player > 0:
            draughts += 1
        if board.board[y, x] * current_player < 0:
            draughts -= 1
    return draughts


class AI:
    def __init__(self, search_depth: int, work: int):
        self.depth: int = search_depth
        self.work_or_not = work

    def next_move(self, board_st: BoardState, current_player: int) -> Optional[BoardState]:

        draughts = -13
        max_number = board_st.copy()
        flag_eat = False
        if self.depth > 0:
            for x, y in product(range(8), range(8)):
                if board_st.board[y, x] * board_st.current_player > 0:
                    eat = board_st.get_possible_eat(x, y)
                    if eat is not None:
                        flag_eat = True
                        for i in eat:
                            if i is not None and type(i) is not list:
                                if draughts <= draught(i, current_player):
                                    [max_number, draughts] = grade(self, i, current_player, draughts, max_number)
                                else:
                                    continue
            if flag_eat:
                for x, y in product(range(8), range(8)):
                    if board_st.board[y, x] != max_number.board[y, x] and max_number.board[y, x] < 0:
                        if eat is not None:
                            for i in eat:
                                if i is not None and type(i) is not list:
                                    if draughts <= draught(i, current_player):
                                        [max_number, draughts] = grade(self, i, current_player, draughts, max_number)
                return max_number

            for x, y in product(range(8), range(8)):
                if board_st.board[y, x] * board_st.current_player > 0:
                    move = board_st.get_possible_moves(x, y)
                    if move is not None:
                        for i in move:
                            if i is not None and type(i) is not list:
                                if draughts <= draught(i, current_player):
                                    [max_number, draughts] = grade(self, i, current_player, draughts, max_number)
                                else:
                                    continue

        return max_number


def grade(ai: AI, i: BoardState, current_player: int, draughts: int, max_number: BoardState) -> [BoardState, int]:

    ai.depth -= 1
    i.current_player *= -1
    tmp = ai.next_move(i, current_player)
    tmp_number = draught(tmp, current_player)
    if draughts <= tmp_number:
        draughts = tmp_number
        max_number = i
    ai.depth += 1

    return [max_number, draughts]
