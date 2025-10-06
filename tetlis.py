import pyxel
import random

# Constants
SCREEN_WIDTH = 120
SCREEN_HEIGHT = 220
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
BLOCK_SIZE = 10
FALL_SPEED = 15 # Frames per fall step

SCORE_MAP = {1: 100, 2: 300, 3: 500, 4: 800}

TETROMINOES = {
    'I': {'shape': [[1, 1, 1, 1]], 'color': 8},
    'O': {'shape': [[1, 1], [1, 1]], 'color': 9},
    'T': {'shape': [[0, 1, 0], [1, 1, 1]], 'color': 10},
    'L': {'shape': [[0, 0, 1], [1, 1, 1]], 'color': 11},
    'J': {'shape': [[1, 0, 0], [1, 1, 1]], 'color': 12},
    'S': {'shape': [[0, 1, 1], [1, 1, 0]], 'color': 13},
    'Z': {'shape': [[1, 1, 0], [0, 1, 1]], 'color': 14},
}

def rotate_shape(shape):
    """
    Rotates a shape matrix 90 degrees clockwise.
    """
    return [list(row) for row in zip(*shape[::-1])]

class Tetris:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Tetris")
        self.reset()
        pyxel.run(self.update, self.draw)

    def reset(self):
        """
        Resets the game state.
        """
        self.board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.game_over = False
        self.fall_timer = 0
        self.score = 0
        self.spawn_piece()

    def spawn_piece(self):
        """
        Spawns a new random tetromino at the top of the board.
        """
        piece_type = random.choice(list(TETROMINOES.keys()))
        self.current_piece = {
            'shape': [row[:] for row in TETROMINOES[piece_type]['shape']],
            'color': TETROMINOES[piece_type]['color']
        }
        self.piece_x = BOARD_WIDTH // 2 - len(self.current_piece['shape'][0]) // 2
        self.piece_y = 0
        if self.check_collision(self.current_piece['shape'], self.piece_x, self.piece_y):
            self.game_over = True

    def check_collision(self, shape, x, y):
        """
        Check if the piece at the given position collides with the board or walls.
        """
        for r, row in enumerate(shape):
            for c, cell in enumerate(row):
                if cell:
                    board_x = x + c
                    board_y = y + r
                    if not (0 <= board_x < BOARD_WIDTH and 0 <= board_y < BOARD_HEIGHT):
                        return True # Wall collision
                    if self.board[board_y][board_x] != 0:
                        return True # Collision with another piece
        return False

    def lock_piece(self):
        """
        Locks the current piece onto the board and checks for cleared lines.
        """
        shape = self.current_piece['shape']
        for r, row in enumerate(shape):
            for c, cell in enumerate(row):
                if cell:
                    self.board[self.piece_y + r][self.piece_x + c] = self.current_piece['color']
        
        self.check_and_clear_lines()
        self.spawn_piece()

    def check_and_clear_lines(self):
        """
        Checks for and clears any completed lines, updating the score.
        """
        lines_cleared = 0
        y = BOARD_HEIGHT - 1
        while y >= 0:
            if all(self.board[y]): # Check if the row is full
                del self.board[y]
                self.board.insert(0, [0 for _ in range(BOARD_WIDTH)])
                lines_cleared += 1
            else:
                y -= 1
        
        if lines_cleared > 0:
            self.score += SCORE_MAP.get(lines_cleared, 0)

    def update(self):
        """
        Update the game state for each frame.
        """
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if self.game_over:
            if pyxel.btnp(pyxel.KEY_R):
                self.reset()
            return

        # --- Player Movement ---
        if pyxel.btnp(pyxel.KEY_LEFT):
            if not self.check_collision(self.current_piece['shape'], self.piece_x - 1, self.piece_y):
                self.piece_x -= 1
        if pyxel.btnp(pyxel.KEY_RIGHT):
            if not self.check_collision(self.current_piece['shape'], self.piece_x + 1, self.piece_y):
                self.piece_x += 1
        
        # --- Rotation ---
        if pyxel.btnp(pyxel.KEY_UP):
            rotated_shape = rotate_shape(self.current_piece['shape'])
            if not self.check_collision(rotated_shape, self.piece_x, self.piece_y):
                self.current_piece['shape'] = rotated_shape

        # --- Soft Drop ---
        if pyxel.btn(pyxel.KEY_DOWN):
            if not self.check_collision(self.current_piece['shape'], self.piece_x, self.piece_y + 1):
                self.piece_y += 1
                self.score += 1 # Bonus point for soft drop
                self.fall_timer = 0

        # --- Gravity ---
        self.fall_timer += 1
        if self.fall_timer >= FALL_SPEED:
            self.fall_timer = 0
            if not self.check_collision(self.current_piece['shape'], self.piece_x, self.piece_y + 1):
                self.piece_y += 1
            else:
                self.lock_piece()

    def draw(self):
        """
        Draw the game screen.
        """
        pyxel.cls(0) # Clear screen with black

        # Draw the board (locked pieces)
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                color = self.board[y][x]
                if color > 0:
                    pyxel.rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE, color)

        # Draw the current falling piece
        if self.current_piece and not self.game_over:
            shape = self.current_piece['shape']
            color = self.current_piece['color']
            for y, row in enumerate(shape):
                for x, cell in enumerate(row):
                    if cell:
                        pyxel.rect((self.piece_x + x) * BLOCK_SIZE, (self.piece_y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE, color)

        # Draw Score
        pyxel.text(5, 5, f"SCORE: {self.score}", 7)

        # Draw game over message
        if self.game_over:
            pyxel.text(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2, "GAME OVER", 7)
            pyxel.text(SCREEN_WIDTH // 2 - 30, SCREEN_HEIGHT // 2 + 10, "(R) to Restart", 7)


if __name__ == "__main__":
    Tetris()
