import pygame
import random


ON = 1
OFF = 0


class Cell:
    def __init__(self, row, col, size):
        self.row = row
        self.col = col
        self.size = size
        self.rect = pygame.Rect(row, col, size, size)
        self.color = (0, 0, 0)

    def get_rect(self):
        return self.rect

    def get_color(self):
        return self.color

    def set_color(self, color):
        self.color = color


class Tile(Cell):
    def __init__(self, row, col, size):
        super().__init__(row, col, size)
        self.color = (0, 0, 0)
        self.state = OFF

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state
        self.update_color()

    def update_color(self):
        if self.state == ON:
            self.color = (255, 255, 255)
        elif self.state == OFF:
            self.color = (0, 0, 0)


class Player(Cell):
    def __init__(self, row, col, size):
        super().__init__(row, col, size)
        self.color = (255, 0, 0)


class Board:
    def __init__(self, tile_count, tile_size, width, height):
        self.tile_count = tile_count
        self.tile_size = tile_size
        self.width = width
        self.height = height
        self.tiles = []
        self.gen()

    def process_inputs(self):
        pass

    def update(self):
        pass

    def process_outputs(self):
        pass

    def get_neighbor_counts(self):
        counts = []
        adj_table = [(-1, -1), (0, -1), (1, -1), (-1,  0), (1,  0), (-1,  1), (0,  1), (1,  1)]
        for i in range(self.tile_count):
            t = []
            for j in range(self.tile_count):
                c = 0
                for x, y in adj_table:
                    ix = (i + x) % self.tile_count
                    jy = (j + y) % self.tile_count
                    c += self.tiles[ix][jy].get_state()
                t.append(c)
            counts.append(t)
        return counts

    def gen(self):
        self.tiles.clear()
        for c in range(self.tile_count):
            temp = []
            for r in range(self.tile_count):
                tile = Tile(c * self.tile_size, r * self.tile_size, self.tile_size)
                tile.set_state(random.randint(0, 1))
                temp.append(tile)
            self.tiles.append(temp)

    # Draw each cell to the surface
    def draw(self):
        screen = pygame.display.get_surface()
        line_width = 1
        for c in range(self.tile_count):
            for r in range(self.tile_count):
                tile = self.tiles[c][r]
                pygame.draw.rect(screen, tile.get_color(), tile.get_rect())
        for i in range(self.tile_count + 1):
            p1 = i * self.tile_size, 0
            p2 = i * self.tile_size, self.height
            pygame.draw.line(screen, (15, 15, 15), p1, p2, line_width)
        for i in range(self.tile_count + 1):
            p1 = 0, i * self.tile_size
            p2 = self.width, i * self.tile_size
            pygame.draw.line(screen, (15, 15, 15), p1, p2, line_width)

    def debug(self):
        counts = self.get_neighbor_counts()
        screen = pygame.display.get_surface()
        font = pygame.font.SysFont('Helvetica.ttf', 32)
        for c in range(self.tile_count):
            for r in range(self.tile_count):
                count = counts[c][r]
                pos = c * self.tile_size, r * self.tile_size
                text = font.render(str(count), True, (127, 127, 127))
                screen.blit(text, pos)


class Mazectric(Board):
    def __init__(self, cell_count, cell_size, width, height):
        super().__init__(cell_count, cell_size, width, height)
        self.player = Player(0, 0, cell_size)

    def update(self):
        temp_tiles = self.tiles.copy()
        counts = self.get_neighbor_counts()
        for i in range(self.tile_count):
            for j in range(self.tile_count):
                tile = self.tiles[i][j].get_state()
                c = counts[i][j]
                if tile == OFF and c == 3:
                    temp_tiles[i][j].set_state(ON)
                if c < 1 or c > 4:
                    temp_tiles[i][j].set_state(OFF)
        self.tiles.clear()
        self.tiles = temp_tiles

    def process_inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.gen()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    for i in range(self.tile_count):
                        for j in range(self.tile_count):
                            rect = self.tiles[i][j].get_rect()
                            if rect.collidepoint(mouse_pos):
                                self.tiles[i][j].set_state(OFF)


class GameOfLife(Board):
    def __init__(self, cell_count, cell_size, width, height):
        super().__init__(cell_count, cell_size, width, height)

    def update(self):
        temp_tiles = self.tiles.copy()
        counts = self.get_neighbor_counts()
        for i in range(self.tile_count):
            for j in range(self.tile_count):
                tile = self.tiles[i][j].get_state()
                c = counts[i][j]
                if (tile == ON and c < 2) or (tile == ON and c > 3):
                    temp_tiles[i][j].set_state(OFF)
                if tile == OFF and c == 3:
                    temp_tiles[i][j].set_state(ON)
        self.tiles.clear()
        self.tiles = temp_tiles

    def process_inputs(self):
        # mouse_pos = pygame.mouse.get_pos()
        # for i in range(self.cell_count):
        #     for j in range(self.cell_count):
        #         rect = self.cells[i][j].get_rect()
        #         if rect.collidepoint(mouse_pos):
        #             self.cells[i][j].set_color((255, 0, 0))
        pass

