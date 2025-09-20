import pyxel

WINDOW_WIDTH = 160
WINDOW_HEIGHT = 120
PADDLE_WIDTH = 2
PADDLE_HEIGHT = 20
BALL_SIZE = 4
PADDLE_SPEED = 2
BALL_SPEED_X = 2
BALL_SPEED_Y = 2

class Pong:
    def __init__(self):
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.reset()
        pyxel.run(self.update, self.draw)

    def reset(self):
        self.paddle_y = WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2
        self.ai_paddle_y = WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2
        self.ball_x = WINDOW_WIDTH // 2 - BALL_SIZE // 2
        self.ball_y = WINDOW_HEIGHT // 2 - BALL_SIZE // 2
        self.ball_vx = BALL_SPEED_X
        self.ball_vy = BALL_SPEED_Y
        self.score = 0
        self.ai_score = 0

    def update(self):
        # プレイヤーパドル操作
        if pyxel.btn(pyxel.KEY_UP):
            self.paddle_y = max(self.paddle_y - PADDLE_SPEED, 0)
        if pyxel.btn(pyxel.KEY_DOWN):
            self.paddle_y = min(self.paddle_y + PADDLE_SPEED, WINDOW_HEIGHT - PADDLE_HEIGHT)

        # AIパドル操作
        if self.ball_y < self.ai_paddle_y:
            self.ai_paddle_y = max(self.ai_paddle_y - PADDLE_SPEED, 0)
        elif self.ball_y > self.ai_paddle_y + PADDLE_HEIGHT:
            self.ai_paddle_y = min(self.ai_paddle_y + PADDLE_SPEED, WINDOW_HEIGHT - PADDLE_HEIGHT)

        # ボール移動
        self.ball_x += self.ball_vx
        self.ball_y += self.ball_vy

        # 上下壁反射
        if self.ball_y <= 0 or self.ball_y + BALL_SIZE >= WINDOW_HEIGHT:
            self.ball_vy *= -1

        # プレイヤーパドル衝突
        if (self.ball_x <= PADDLE_WIDTH and
            self.paddle_y < self.ball_y + BALL_SIZE and
            self.ball_y < self.paddle_y + PADDLE_HEIGHT):
            self.ball_vx *= -1
            self.ball_x = PADDLE_WIDTH

        # AIパドル衝突
        if (self.ball_x + BALL_SIZE >= WINDOW_WIDTH - PADDLE_WIDTH and
            self.ai_paddle_y < self.ball_y + BALL_SIZE and
            self.ball_y < self.ai_paddle_y + PADDLE_HEIGHT):
            self.ball_vx *= -1
            self.ball_x = WINDOW_WIDTH - PADDLE_WIDTH - BALL_SIZE

        # スコア判定
        if self.ball_x < 0:
            self.ai_score += 1
            self.reset_ball()
        elif self.ball_x > WINDOW_WIDTH:
            self.score += 1
            self.reset_ball()

    def reset_ball(self):
        self.ball_x = WINDOW_WIDTH // 2 - BALL_SIZE // 2
        self.ball_y = WINDOW_HEIGHT // 2 - BALL_SIZE // 2
        self.ball_vx *= -1
        self.ball_vy = BALL_SPEED_Y if self.ball_vy > 0 else -BALL_SPEED_Y

    def draw(self):
        pyxel.cls(0)
        # プレイヤーパドル
        pyxel.rect(0, self.paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT, 7)
        # AIパドル
        pyxel.rect(WINDOW_WIDTH - PADDLE_WIDTH, self.ai_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT, 7)
        # ボール
        pyxel.rect(self.ball_x, self.ball_y, BALL_SIZE, BALL_SIZE, 8)
        # スコア表示
        pyxel.text(60, 5, f"YOU: {self.score}  AI: {self.ai_score}", 7)

if __name__ == "__main__":
    Pong()
