import string
from itertools import product

import pygame
from pygame import Surface

from ai import AI
from boardstate import BoardState


def draw_board(screen: Surface, pos_x: int, pos_y: int, elem_size: int, board: BoardState):
    black = (0, 0, 0)
    white = (200, 200, 200)

    for y, x in product(range(8), range(8)):
        color = white if (x + y) % 2 == 0 else black
        position = pos_x + x * elem_size, pos_y + y * elem_size, elem_size, elem_size
        pygame.draw.rect(screen, color, position)

        figure = board.board[y, x]

        if figure == 0:
            continue

        if figure > 0:
            figure_color = 255, 255, 255
        else:
            figure_color = 100, 100, 100
        r = elem_size // 2 - 10

        pygame.draw.circle(screen, figure_color, (position[0] + elem_size // 2, position[1] + elem_size // 2), r)
        if abs(figure) == 2:
            r = 5
            negative_color = [255 - e for e in figure_color]
            pygame.draw.circle(screen, negative_color, (position[0] + elem_size // 2, position[1] + elem_size // 2), r)


def game_loop(screen: Surface, board: BoardState, ai: AI) -> int:
    grid_size = screen.get_size()[0] // 8

    while True:
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()

            if board.is_game_finished != 0:
                return board.is_game_finished

            # выход
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                return 0

            # новая игра
            if keys[pygame.K_SPACE]:
                new_board = board.initial_state()
                board = new_board

            # перемещение
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_click_position = event.pos
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                new_x, new_y = [p // grid_size for p in event.pos]
                old_x, old_y = [p // grid_size for p in mouse_click_position]

                if board.current_player * board.board[old_y, old_x] > 0:
                    new_board = board.do_move(old_x, old_y, new_x, new_y)
                    if new_board is not None:
                        board = new_board
                        draw_board(screen, 0, 0, grid_size, board)
                        pygame.display.flip()

            # смена фигур
            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                x, y = [p // grid_size for p in event.pos]
                board.board[y, x] = (board.board[y, x] + 1 + 2) % 5 - 2

            # ход ии
            if keys[pygame.K_UP] or ai.work_or_not == board.current_player:
                new_board = ai.next_move(board, board.current_player)
                if new_board is not None:
                    board = new_board

            # выход в меню
            if keys[pygame.K_DOWN]:
                pygame.display.flip()
                menu(screen, ai)

            # сохранение в файл
            if keys[pygame.K_LEFT]:
                board.save_state(board, 'saves.txt')

            # загрузка из файла
            if keys[pygame.K_RIGHT]:
                new_board = board.load_state(board, 'saves.txt')
                board = new_board

        draw_board(screen, 0, 0, grid_size, board)
        pygame.display.flip()


def menu(screen: Surface, ai: AI):

    pygame.draw.rect(screen, (0, 0, 0), (0, 0, 512, 512))
    flag_not_exit = True

    while flag_not_exit:
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()

            font = pygame.font.Font(None, 30)

            hello_color = (30, 120, 30)
            hello = font.render('Вас приветствуют шашки!', True, hello_color)
            made_by = font.render('Выполнено Савенковой Александрой', True, hello_color)

            tex_color = (30, 30, 120)

            start_game = font.render('Чтобы продолжить, нажмите на экран', True, tex_color)
            start_game_else = font.render('или воспользуйтесь кнопками 1 или 2', True, tex_color)
            save = font.render('Для сохранения в игре нажмите влево', True, tex_color)
            load = font.render('Для загрузки в игре нажмите вправо', True, tex_color)
            new_game = font.render('Для начала новой игры нажмите SPACE', True, tex_color)
            come_to_menu = font.render('Для возвращения в меню нажмите вниз', True, tex_color)
            exit_from_game = font.render('Для выхода из игры нажмите ESCAPE', True, tex_color)

            screen.blit(hello, (10, 50))
            screen.blit(made_by, (10, 90))
            screen.blit(start_game, (10, 150))
            screen.blit(start_game_else, (10, 180))
            screen.blit(save, (10, 250))
            screen.blit(load, (10, 270))
            screen.blit(new_game, (10, 290))
            screen.blit(come_to_menu, (10, 310))
            screen.blit(exit_from_game, (10, 330))

            pygame.display.update()

            # выход
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                flag_not_exit = False

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if 0 <= event.pos[0] <= 512 and 0 <= event.pos[1] <= 512:
                    flag_not_exit = False

            if keys[pygame.K_1] or keys[pygame.K_2]:
                flag_not_exit = False

    play = player(screen)
    if play == 1:
        ai.work_or_not = art_int(screen)
        ai.depth = difficulty(screen)


def player(screen: Surface):
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, 512, 512))
    flag_not_exit = True

    mode = -1

    while flag_not_exit:
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()

            [ai_x, ai_y, self_x, self_y] = [10, 200, 10, 250]
            choice(screen, 'Выберите тип игры', 'Против ии', 'За обе стороны', ai_x, ai_y, self_x, self_y)

            pygame.display.update()

            # выход
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                flag_not_exit = False

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if ai_x <= event.pos[0] <= ai_x + 300 and ai_y <= event.pos[1] <= ai_y + 50 or keys[pygame.K_1]:
                    mode = 1
                    flag_not_exit = False
                if self_x <= event.pos[0] <= self_x + 300 and self_y <= event.pos[1] <= self_y + 50:
                    mode = 0
                    flag_not_exit = False

            if keys[pygame.K_1]:
                mode = 1
                flag_not_exit = False
            if keys[pygame.K_2]:
                mode = 0
                flag_not_exit = False

    return mode


def art_int(screen: Surface) -> int:
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, 512, 512))
    color = 0
    flag_not_exit = True

    while flag_not_exit:
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()

            [black_x, black_y, white_x, white_y] = [10, 200, 10, 250]
            choice(screen, 'Выберите, за кого будет играть искусственный интеллект',
                   'Чёрные', 'Белые', black_x, black_y, white_x, white_y)

            color = 1
            pygame.display.update()

            # выход
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                flag_not_exit = False

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if black_x <= event.pos[0] <= black_x + 300 and black_y <= event.pos[1] <= black_y + 50:
                    color = -1
                    flag_not_exit = False
                if white_x <= event.pos[0] <= white_x + 300 and white_y <= event.pos[1] <= white_y + 50:
                    color = 1
                    flag_not_exit = False

            if keys[pygame.K_1]:
                color = -1
                flag_not_exit = False
            if keys[pygame.K_2]:
                color = 1
                flag_not_exit = False

    return color


def difficulty(screen: Surface) -> int:
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, 512, 512))
    diff = 0
    flag_not_exit = True

    while flag_not_exit:
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()

            [easy_x, easy_y, hard_x, hard_y] = [10, 200, 10, 250]
            choice(screen, 'Выберите уровень сложности', 'Лёгкий', 'Тяжёлый', easy_x, easy_y, hard_x, hard_y)

            diff = 1
            pygame.display.update()

            # выход
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                flag_not_exit = False

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if easy_x <= event.pos[0] <= easy_x + 300 and easy_y <= event.pos[1] <= easy_y + 50:
                    diff = 1
                    flag_not_exit = False
                if hard_x <= event.pos[0] <= hard_x + 300 and hard_y <= event.pos[1] <= hard_y + 50:
                    diff = 4
                    flag_not_exit = False

            if keys[pygame.K_1]:
                diff = 1
                flag_not_exit = False
            if keys[pygame.K_2]:
                diff = 4
                flag_not_exit = False

    return diff


def end(screen: Surface, winner: int):
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, 512, 512))
    flag_not_exit = True

    if winner == 0:
        flag_not_exit = False

    while flag_not_exit:
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()

            font = pygame.font.Font(None, 30)

            question_color = (100, 100, 100)
            question = font.render('Победители', True, question_color)
            easy = font.render('Чёрные', True, (20, 100, 200))
            hard = font.render('Белые', True, (100, 100, 20))
            screen.blit(question, (30, 150))

            [black_x, black_y, white_x, white_y] = [10, 200, 10, 250]

            if winner == -1:
                screen.blit(easy, (black_x, black_y))
            if winner == 1:
                screen.blit(hard, (white_x, white_y))

            pygame.display.update()

            # выход
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                flag_not_exit = False


def choice(screen: Surface, question: string, str1: string, str2: string, x1: int, y1: int, x2: int, y2: int):

    font = pygame.font.Font(None, 30)

    screen.blit(font.render(question, True, (100, 100, 100)), (30, 150))
    screen.blit(font.render(str1, True, (20, 100, 200)), (x1, y1))
    screen.blit(font.render(str2, True, (100, 100, 20)), (x2, y2))
