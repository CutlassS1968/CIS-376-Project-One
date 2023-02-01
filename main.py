import pygame

import engine


ON = 1
OFF = 0


class Game:
    def __init__(self):
        self.width = 800
        self.height = 800
        self.cell_count = 80
        self.cell_size = ((self.width / self.cell_count) + (self.height / self.cell_count)) / 2
        self.board = engine.GameOfLife(self.cell_count, self.cell_size, self.width, self.height)
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
            self.clock.tick(30)
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.loop()
