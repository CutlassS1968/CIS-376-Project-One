import pygame


class Board:
    def __init__(self, col_count, row_count, cell_size, width, height):
        self.col_count = col_count
        self.row_count = row_count
        self.cell_size = cell_size
        self.width = width
        self.height = height
        self.cells = []
        self.gen()

    def gen(self):
        for c in range(self.col_count):
            temp = []
            for r in range(self.row_count):
                cell = Cell(c, r, self.cell_size)
                temp.append(cell)
            self.cells.append(temp)

    # Draw each cell to the surface
    def draw(self):
        screen = pygame.display.get_surface()
        line_width = 5
        for c in range(self.col_count):
            for r in range(self.row_count):
                cell = self.cells[c][r]
                pygame.draw.rect(screen, cell.get_color(), cell.get_rect())
        for i in range(self.col_count + 1):
            p1 = i * self.cell_size, 0
            p2 = i * self.cell_size, self.height
            pygame.draw.line(screen, (15, 15, 15), p1, p2, line_width)
        for i in range(self.row_count + 1):
            p1 = 0, i * self.cell_size
            p2 = self.width, i * self.cell_size
            pygame.draw.line(screen, (15, 15, 15), p1, p2, line_width)

    def check_open_cell(self, row, col):
        pass


class Cell:
    def __init__(self, row, col, size):
        self.row = row
        self.col = col
        self.size = size
        self.rect = pygame.Rect(row, col, row*size, col*size)
        self.color = (255, 255, 255)

    def get_rect(self):
        return self.rect

    def get_color(self):
        return self.color


class Mazectric(Board):
    def __init__(self, col_count, row_count, cell_size, width, height):
        super().__init__(col_count, row_count, cell_size, width, height)

    def generate_board(self):
        pass

    def update(self):
        pass


class Player:
    def __init__(self, row, col):
        self.row = row
        self.col = col


class Game:
    def __init__(self):
        self.width = 600
        self.height = 600
        self.col_count = 10
        self.row_count = 10
        self.cell_size = ((self.width / self.col_count) + (self.height / self.row_count)) / 2
        print(self.cell_size)
        self.board = Board(self.col_count, self.row_count, self.cell_size, self.width, self.height)
        pygame.init()
        pygame.display.set_mode((self.width, self.height))
        self.running = True

    def draw(self):
        self.board.draw()
        pygame.display.flip()

    def process_inputs(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        self.draw()

    def process_outputs(self):
        pass

    def loop(self):
        while self.running:
            self.process_inputs()
            self.update()
            self.process_outputs()
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.loop()
