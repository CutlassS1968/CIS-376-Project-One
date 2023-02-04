import pygame

import engine


WIDTH = 800
HEIGHT = 800
CELL_COUNT = 20
FRAME_RATE = 30
CURRENT_BOARD = "Mazectric"

BOARDS = {"Mazectric": engine.Mazectric,
          "GameOfLife": engine.GameOfLife}


class Game:
    """Main class that handles/organizes the board and the main loop

    Attributes:
        width: width of the window
        height: height of the window
        cell_count: total number of cells in each column/row
        frame_rate: maximum number of frames do be drawn each second
        board_name: type of board the game will be running
    """

    def __init__(self, width, height, cell_count, frame_rate, board_name):
        """Inits current game with width, height, cell_count, frame_rate, and board_name"""
        self.width = width
        self.height = height
        self.cell_count = cell_count
        self.frame_rate = frame_rate
        self.cell_size = ((self.width / self.cell_count) + (self.height / self.cell_count)) / 2
        self.board = BOARDS[board_name](self.cell_count, self.cell_size, self.width, self.height)
        pygame.init()
        pygame.display.set_mode((self.width, self.height))
        # Used for frame limiting the window
        self.clock = pygame.time.Clock()
        # Used in exiting game loop
        self.running = True
        # Allows user to display a debug overlay
        self.is_debug = False
        # Determines whether player has won
        self.win_condition = False

    def draw(self):
        """Draws any overlays"""
        # Draw board's debug if player turned on debug
        if self.is_debug:
            self.board.debug()
        # If player has won, then display win message
        if self.win_condition:
            screen = pygame.display.get_surface()
            font = pygame.font.SysFont('Helvetica.ttf', 128)
            text = font.render("You Win!", True, (255, 63, 63))
            screen.blit(text, (self.width / 4, self.height / 4))
        pygame.display.flip()

    def process_inputs(self):
        """Processes user inputs"""
        # Don't process board input if player has won
        if not self.win_condition:
            self.running = self.board.process_inputs()
        # Check for debug key and exit condition
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    self.is_debug = not self.is_debug

    def update(self):
        """Processes the board and checks win condition"""
        self.win_condition = self.board.update()

    def process_outputs(self):
        """Processes all outputs"""
        self.board.process_outputs()
        self.draw()

    def loop(self):
        """Main game loop"""
        while self.running:
            self.process_inputs()
            self.update()
            self.process_outputs()
            self.clock.tick(self.frame_rate)
        pygame.quit()


if __name__ == "__main__":
    game = Game(WIDTH, HEIGHT, CELL_COUNT, FRAME_RATE, CURRENT_BOARD)
    game.loop()
