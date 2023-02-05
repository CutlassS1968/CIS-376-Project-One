import pygame
import random


ON = 1
OFF = 0


class Cell:
    """Cell class is used for creating individual entries in a board object

    Attributes:
        row: the row the cell is in
        col: the column the cell is in
        size: the size of the cell
        rect: the drawable object that represents the cell
        color: the color of the cell
    """
    def __init__(self, row, col, size):
        """Inits Cell with row, column, rect, color, and cell size"""
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
    """Tile is a type of cell that is used in the Mazectric and GameOfLife boards

    Attributes:
        row: the row the Tile is in
        col: the column the Tile is in
        size: the size of the Tile
        color: the color of the Tile
        state: Current state of the tile (either ON or OFF)
    """

    def __init__(self, row, col, size):
        """Inits Tile with row, column, starting state, color, and cell size"""
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
    """Player is a type of cell that can be moved around a board

    Attributes:
        row: the row the Player is in
        col: the column the Player is in
        size: the size of the Player
        color: the color of the cell
    """

    def __init__(self, row, col, size):
        """Inits Player with row, column, color, and cell size"""
        super().__init__(row, col, size)
        self.color = (255, 0, 0)

    def get_row(self):
        return self.row

    def set_row(self, row):
        """Updates the row and rect location"""
        self.row = row
        self.rect.x = self.row * self.size

    def get_col(self):
        return self.col

    def set_col(self, col):
        """Updates the col and rect location"""
        self.col = col
        self.rect.y = self.col * self.size

    def get_size(self):
        return self.size


class Board:
    """Represents the current game state

    Attributes:
        tile_count: total number of rows/columns
        tile_size: size of each tile
        width: width of the board
        height: height of the board
    """

    def __init__(self, tile_count, tile_size, width, height):
        """Inits Board with tile_count, tile_size, width, and height"""
        self.tile_count = tile_count
        self.tile_size = tile_size
        self.width = width
        self.height = height
        self.tiles = []
        self.gen()

    def process_inputs(self):
        """Processes all user inputs"""
        pass

    def update(self):
        """Processes next board state"""
        pass

    def process_outputs(self):
        """Outputs current board state"""
        pass

    def get_neighbor_counts(self):
        """Returns list of each tile's neighbor count"""
        counts = []
        # Utilize python's index wrapping in lists to find each cell's neighbor count
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
        """Inits the board's tiles"""
        self.tiles.clear()
        for c in range(self.tile_count):
            temp = []
            for r in range(self.tile_count):
                tile = Tile(c * self.tile_size, r * self.tile_size, self.tile_size)
                tile.set_state(random.randint(0, 1))
                temp.append(tile)
            self.tiles.append(temp)

    def draw(self):
        """Draws the current board state to the display"""
        screen = pygame.display.get_surface()
        line_width = 1
        # Draw the tiles
        for c in range(self.tile_count):
            for r in range(self.tile_count):
                tile = self.tiles[c][r]
                pygame.draw.rect(screen, tile.get_color(), tile.get_rect())
        # Draw horizontal dividing lines
        for i in range(self.tile_count + 1):
            p1 = i * self.tile_size, 0
            p2 = i * self.tile_size, self.height
            pygame.draw.line(screen, (15, 15, 15), p1, p2, line_width)
        # Draw vertical dividing lines
        for i in range(self.tile_count + 1):
            p1 = 0, i * self.tile_size
            p2 = self.width, i * self.tile_size
            pygame.draw.line(screen, (15, 15, 15), p1, p2, line_width)

    def debug(self):
        """Draws a debug overlay with each tile's neighbor count"""
        counts = self.get_neighbor_counts()
        screen = pygame.display.get_surface()
        font = pygame.font.SysFont('Helvetica.ttf', 32)
        for c in range(self.tile_count):
            for r in range(self.tile_count):
                count = counts[c][r]
                pos = c * self.tile_size, r * self.tile_size
                text = font.render(str(count), True, (127, 127, 127))
                screen.blit(text, pos)

    def flip_tile_at_loc(self, pos):
        """Toggles a tile's state at the given position"""
        for i in range(self.tile_count):
            for j in range(self.tile_count):
                rect = self.tiles[i][j].get_rect()
                if rect.collidepoint(pos):
                    self.tiles[i][j].set_state(int(not bool(self.tiles[i][j].get_state())))


class Mazectric(Board):
    """Form of the Board class which follows the Mazectric rule set

    Attributes:
        tile_count: total number of rows/columns
        tile_size: size of each tile
        width: width of the board
        height: height of the board
    """

    def __init__(self, tile_count, tile_size, width, height):
        """Inits the Board with tile_count, tile_size, width, height, player, and key_commands"""
        super().__init__(tile_count, tile_size, width, height)
        self.player = Player(0, 0, tile_size)
        self.key_commands = {pygame.K_w: self.player_move_up,
                             pygame.K_s: self.player_move_down,
                             pygame.K_a: self.player_move_left,
                             pygame.K_d: self.player_move_right,
                             pygame.K_r: self.gen}

    def update(self):
        """Processes next board state"""
        self.update_tiles()
        self.update_player()
        return self.check_win_condition()

    def check_win_condition(self):
        """Returns true if win condition is met"""
        if self.player.get_row() == self.tile_count - 1 and self.player.get_col() == self.tile_count - 1:
            return True
        return False

    def update_tiles(self):
        """Processes the tile's next state given Mazectric rule set"""
        # Update board state
        temp_tiles = self.tiles.copy()
        counts = self.get_neighbor_counts()
        for i in range(self.tile_count):
            for j in range(self.tile_count):
                tile = self.tiles[i][j].get_state()
                c = counts[i][j]
                # sets the state of the tile and the tile's color given the Mazetric rule set
                if tile == OFF and c == 3:
                    temp_tiles[i][j].set_state(ON)
                if c < 1 or c > 4:
                    temp_tiles[i][j].set_state(OFF)
        self.tiles.clear()
        self.tiles = temp_tiles

    # TODO: unfinished method
    def update_player(self):
        """Moves the player to an empty tile if current tile is ON"""
        p_r, p_c = self.player.get_col(), self.player.get_row()
        if self.tiles[p_c][p_r].get_state() == ON:
            adj_table = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

    def process_inputs(self):
        """Processes user inputs"""
        for event in pygame.event.get():
            # Need to handle exit condition incase we are in here when we try to quit
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_f:
                    pass
                else:
                    func = self.key_commands.get(event.key)
                    if func is not None:
                        func()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.flip_tile_at_loc(pygame.mouse.get_pos())
        return True

    def process_outputs(self):
        self.draw()

    def draw(self):
        """Draws the current board state, player, and any overlays"""
        super().draw()
        self.draw_player()
        self.draw_overlay()

    def draw_player(self):
        """Draws the player"""
        screen = pygame.display.get_surface()
        size = self.player.get_size()
        row = self.player.get_row()
        col = self.player.get_col()
        c_center = (row * size) + (size / 2), (col * size) + (size / 2)
        c_radius = size / 2
        pygame.draw.circle(screen, self.player.get_color(), c_center, c_radius)

    def draw_overlay(self):
        """Draws all overlays"""
        screen = pygame.display.get_surface()
        font = pygame.font.SysFont('Helvetica.ttf', 30)
        screen.blit(font.render('Press \'Left Click\' to toggle a tile', True, (255, 0, 0)), (10, self.height - 80))
        screen.blit(font.render('Press \'R\' to reset', True, (255, 0, 0)), (10, self.height - 55))
        screen.blit(font.render('Press \'W A S D\' to move', True, (255, 0, 0)), (10, self.height - 30))

    def player_move_left(self):
        """Moves the player left if cell is empty"""
        c = self.player.get_col()
        r = self.player.get_row()
        if self.tiles[(r - 1) % self.tile_count][c].get_state() == OFF:
            self.player.set_row((self.player.get_row() - 1) % self.tile_count)

    def player_move_right(self):
        """Moves the player right if cell is empty"""
        c = self.player.get_col()
        r = self.player.get_row()
        if self.tiles[(r + 1) % self.tile_count][c].get_state() == OFF:
            self.player.set_row((self.player.get_row() + 1) % self.tile_count)

    def player_move_up(self):
        """Moves the player up if cell is empty"""
        c = self.player.get_col()
        r = self.player.get_row()
        if self.tiles[r][(c - 1) % self.tile_count].get_state() == OFF:
            self.player.set_col((self.player.get_col() - 1) % self.tile_count)

    def player_move_down(self):
        """Moves the player down if cell is empty"""
        c = self.player.get_col()
        r = self.player.get_row()
        if self.tiles[r][(c + 1) % self.tile_count].get_state() == OFF:
            self.player.set_col((self.player.get_col() + 1) % self.tile_count)


class GameOfLife(Board):
    """Form of the Board class which follows Conway's Game of Life rule set

        Attributes:
            tile_count: total number of rows/columns
            tile_size: size of each tile
            width: width of the board
            height: height of the board
    """

    def __init__(self, tile_count, tile_size, width, height):
        """Inits board with tile_count, tile_size, width, and height"""
        super().__init__(tile_count, tile_size, width, height)

    def update(self):
        """Processes next board state"""
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
        return False

    def process_inputs(self):
        """Processes user inputs"""
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.flip_tile_at_loc(pygame.mouse.get_pos())
        return True

    def process_outputs(self):
        self.draw()
