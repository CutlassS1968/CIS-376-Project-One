import random

import pygame
import numpy


ON = 1
OFF = 0


class Board:
    def __init__(self, cell_count, cell_size, width, height):
        self.cell_count = cell_count
        self.cell_size = cell_size
        self.width = width
        self.height = height
        self.cells = []
        self.gen()

    def process_inputs(self):
        pass

    def update(self):
        pass

    def process_outputs(self):
        pass

    def neighbor_count(self, i, j):
        adj_table = [[-1, -1], [0, -1], [1, -1],
                     [-1,  0],          [1,  0],
                     [-1,  1], [0,  1], [1,  1]]
        c = 0
        for x, y in adj_table:
            ix = (i + x) % self.cell_count
            jy = (j + y) % self.cell_count
            c += self.cells[ix][jy].get_state()
        return c

    def gen(self):
        for c in range(self.cell_count):
            temp = []
            for r in range(self.cell_count):
                cell = Cell(c*self.cell_size, r*self.cell_size, self.cell_size)
                cell.set_state(OFF)
                temp.append(cell)
            self.cells.append(temp)

    # Draw each cell to the surface
    def draw(self):
        screen = pygame.display.get_surface()
        line_width = 1
        for c in range(self.cell_count):
            for r in range(self.cell_count):
                cell = self.cells[c][r]
                pygame.draw.rect(screen, cell.get_color(), cell.get_rect())
        for i in range(self.cell_count + 1):
            p1 = i * self.cell_size, 0
            p2 = i * self.cell_size, self.height
            pygame.draw.line(screen, (15, 15, 15), p1, p2, line_width)
        for i in range(self.cell_count + 1):
            p1 = 0, i * self.cell_size
            p2 = self.width, i * self.cell_size
            pygame.draw.line(screen, (15, 15, 15), p1, p2, line_width)

    def debug(self):
        screen = pygame.display.get_surface()
        font = pygame.font.SysFont('Helvetica.ttf', 32)
        for c in range(self.cell_count):
            for r in range(self.cell_count):
                cell = self.cells[c][r]
                count = self.neighbor_count(c, r)
                color = (((255/8) * count), ((255/8) * count), ((255/8) * count))
                pos = c * self.cell_size, r * self.cell_size
                text = font.render(str(count), True, (127, 127, 127))
                pygame.draw.rect(screen, color, cell.get_rect())
                # screen.blit(text, pos)


class Cell:
    def __init__(self, row, col, size):
        self.row = row
        self.col = col
        self.size = size
        self.rect = pygame.Rect(row, col, size, size)
        self.color = (0, 0, 0)
        self.state = OFF

    def get_rect(self):
        return self.rect

    def set_state(self, state):
        self.state = state
        self.update_color()

    def get_state(self):
        return self.state

    def get_color(self):
        return self.color

    def update_color(self):
        if self.state == ON:
            self.color = (255, 255, 255)
        elif self.state == OFF:
            self.color = (0, 0, 0)


class Mazectric(Board):
    def __init__(self, cell_count, cell_size, width, height):
        super().__init__(cell_count, cell_size, width, height)

    def generate_board(self):
        pass

    def update(self):
        temp_cells = self.cells.copy()
        adj_display = []
        for i in range(self.cell_count):
            t = []
            for j in range(self.cell_count):
                c = self.neighbor_count(i, j)
                if self.cells[i][j].get_state() == ON:
                    if c < 1 or c > 3:
                        temp_cells[i][j].set_state(OFF)
                else:
                    if c == 3:
                        temp_cells[i][j].set_state(ON)
                t.append(c)
            adj_display.append(t)
        self.cells = temp_cells

    def process_inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.gen()

    def draw(self):
        screen = pygame.display.get_surface()
        line_width = 1
        for c in range(self.cell_count):
            for r in range(self.cell_count):
                cell = self.cells[c][r]
                pygame.draw.rect(screen, cell.get_color(), cell.get_rect())
        # for i in range(self.cell_count + 1):
        #     p1 = i * self.cell_size, 0
        #     p2 = i * self.cell_size, self.height
        #     pygame.draw.line(screen, (15, 15, 15), p1, p2, line_width)
        # for i in range(self.cell_count + 1):
        #     p1 = 0, i * self.cell_size
        #     p2 = self.width, i * self.cell_size
        #     pygame.draw.line(screen, (15, 15, 15), p1, p2, line_width)

    def debug(self):
        screen = pygame.display.get_surface()
        font = pygame.font.SysFont('Helvetica.ttf', 32)
        for c in range(self.cell_count):
            for r in range(self.cell_count):
                cell = self.cells[c][r]
                count = self.neighbor_count(c, r)
                color = ((32 * count), (32 * count), (32 * count))
                pos = c * self.cell_size, r * self.cell_size
                text = font.render(str(count), True, (127, 127, 127))
                pygame.draw.rect(screen, color, cell.get_rect())
                # screen.blit(text, pos)

    def gen(self):
        self.cells.clear()
        for c in range(self.cell_count):
            temp = []
            for r in range(self.cell_count):
                cell = Cell(c*self.cell_size, r*self.cell_size, self.cell_size)
                cell.set_state(random.randint(0, 1))
                temp.append(cell)
            self.cells.append(temp)


class GameOfLife(Board):
    def __init__(self, cell_count, cell_size, width, height):
        super().__init__(cell_count, cell_size, width, height)

    def generate_board(self):
        pass

    def update(self):
        pass

    def process_inputs(self):
        temp_cells = self.cells.copy()
        for i in range(self.cell_count):
            for j in range(self.cell_count):
                c = self.neighbor_count(i, j)
                if self.cells[i][j].get_state() == ON:
                    if c < 2:
                        temp_cells[i][j].set_state(OFF)
                    if c == 2 or c == 3:
                        temp_cells[i][j].set_state(ON)
                    if c > 3:
                        temp_cells[i][j].set_state(OFF)
                else:
                    if c == 3:
                        temp_cells[i][j].set_state(ON)
        self.cells = temp_cells

    def gen(self):
        for c in range(self.cell_count):
            temp = []
            for r in range(self.cell_count):
                cell = Cell(c*self.cell_size, r*self.cell_size, self.cell_size)
                cell.set_state(random.randint(0, 1))
                temp.append(cell)
            self.cells.append(temp)


class Player(Cell):
    def __init__(self, row, col, size):
        super().__init__(row, col, size)


class Game:
    def __init__(self):
        self.width = 800
        self.height = 800
        self.cell_count = 30
        self.cell_size = ((self.width / self.cell_count) + (self.height / self.cell_count)) / 2
        self.board = Mazectric(self.cell_count, self.cell_size, self.width, self.height)
        pygame.init()
        pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.is_debug = False

    def draw(self):
        self.board.draw()
        if self.is_debug:
            self.board.debug()
        pygame.display.flip()

    def process_inputs(self):
        self.board.process_inputs()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self.is_debug = not self.is_debug

    def update(self):
        self.board.update()

    def process_outputs(self):
        self.board.process_outputs()
        self.draw()

    def loop(self):
        while self.running:
            self.process_inputs()
            self.update()
            self.process_outputs()
            self.clock.tick(5)
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.loop()
