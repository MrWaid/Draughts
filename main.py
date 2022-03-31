from gui import*

ai = AI(search_depth=1, work=0)

pygame.init()
screen: Surface = pygame.display.set_mode([512, 512])

menu(screen, ai)
end(screen, game_loop(screen, BoardState.initial_state(BoardState), ai))

pygame.quit()
