import pygame as pg


class Plotting:
    def __init__(self, Nx, grid_size, margin_x, margin_y, Lx, Ly, man_value, king_value, FLIP, WINDOWS, operations):
        self.Nx = Nx
        self.grid_size = grid_size
        self.man_value = man_value
        self.king_value = king_value
        self.margin_x = margin_x
        self.margin_y = margin_y
        self.Lx = Lx
        self.Ly = Ly
        self.FLIP = FLIP
        self.WINDOWS = WINDOWS
        self.operations = operations

    def SHOW_TEXT(self, font, text, x, y):
        x = x
        y = y
        text = font.render(text, True, (0, 0, 0))
        self.WINDOWS.blit(text, (x+self.margin_x+2, y+self.margin_y))
        pg.display.update()

    def SHOW_SCORE(self, text, x, y):
        x = x
        y = y
        font = pg.font.Font("font/l_10646.ttf", 24)
        text = font.render(text, True, (0, 0, 0))
        self.WINDOWS.blit(text, (x+self.margin_x+2, y+self.margin_y))
        pg.display.update()

    def WINDOWS_PLOT(self, WINDOWS, FLIP):
        BOARD = pg.image.load('images/board.png')
        BOARD = pg.transform.smoothscale(
            BOARD, (self.grid_size*self.Nx, self.grid_size*self.Nx))

        BOARD_IMAGE = BOARD.get_rect()
        BOARD_IMAGE.topleft = (self.margin_x, self.margin_y)

        #ACKGROUND = pg.Surface(WINDOWS.get_size())
        BACKGROUND = pg.image.load('images/background.jpg')
        BACKGROUND = pg.transform.smoothscale(BACKGROUND, (self.Lx, self.Ly))
        BACKGROUND = BACKGROUND.convert()

        self.WINDOWS.blit(BACKGROUND, (0, 0))
        self.WINDOWS.blit(BOARD, BOARD_IMAGE)

        font = pg.font.Font("font/l_10646.ttf", 10)
        for i in range(0, 64):
            if self.FLIP:
                text = f"{self.Nx**2-1-i}"
            else:
                text = f"{i}." + self.operations[i]
            if i == 0:
                text = "Game Score:"
            text_x = i % self.Nx
            text_y = i//self.Nx
            self.SHOW_TEXT(font, text, text_x*self.grid_size,
                           text_y*self.grid_size)

    def CHECKER_PLOT(self, list_of_checkers, WINDOWS, FLIP):
        shift_x = 12
        shift_y = 12

        for index, element in enumerate(list_of_checkers):
            if element == -self.man_value:
                CHECKER = pg.image.load('images/CHECKER_RED.png')
            elif element == self.man_value:
                CHECKER = pg.image.load('images/CHECKER_WHITE.png')
            elif element == -self.king_value:
                CHECKER = pg.image.load('images/CHECKER_RED_KING.png')
            elif element == self.king_value:
                CHECKER = pg.image.load('images/CHECKER_WHITE_KING.png')

            checker_x = index % self.Nx
            checker_y = index//self.Nx
            if FLIP:
                checker_x = self.Nx-1-checker_x
                checker_y = self.Nx-1-checker_y
            if (element != 0):
                CHECKER = pg.transform.smoothscale(
                    CHECKER, (2*self.grid_size, 2*self.grid_size))
                self.WINDOWS.blit(
                    CHECKER, (checker_x*self.grid_size+shift_x, checker_y*self.grid_size+shift_y))

    def MOVE_HINT(self, available_move):
        available_start = []
        available_stop = []
        for i in available_move:
            available_start.append(i[0])
            # remove the repeating elements
            available_start = list(set(available_start))
            available_stop.append(i[1])
            # remove the repeating elements
            available_stop = list(set(available_stop))
        return (available_start, available_stop)
