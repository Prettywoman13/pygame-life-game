import pygame
from copy import deepcopy


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]

        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.setplay = False

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, (255, 255, 255), (
                    x * self.cell_size + self.left,
                    y * self.cell_size + self.top,
                    self.cell_size,
                    self.cell_size), 1)
                if self.board[y][x] == 0:
                    pygame.draw.rect(screen, (40, 40, 40), (
                        x * self.cell_size + self.left + 1,
                        y * self.cell_size + self.top + 1,
                        self.cell_size - 2,
                        self.cell_size - 2))
                else:
                    pygame.draw.rect(screen, pygame.Color(0, 255, 0), (
                        x * self.cell_size + self.left + 1,
                        y * self.cell_size + self.top + 1,
                        self.cell_size - 2,
                        self.cell_size - 2))
        self.clock.tick(self.fps)

    def update_frame(self, tick):
        self.fps += tick
        if self.fps < 10:
            self.fps = 10
        if self.fps > 120:
            self.fps = 120
        print(self.fps)

    def change_play_state(self, flag):
        self.setplay = flag

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def get_cell(self, mouse_pos):
        x1 = (mouse_pos[0] - self.left) // self.cell_size
        y1 = (mouse_pos[1] - self.top) // self.cell_size
        if 0 <= x1 < self.width and 0 <= y1 < self.height:
            print(x1, y1)
            return (x1, y1)
        else:
            print(None)
        print(mouse_pos)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_state(self):
        return self.setplay

    def on_click(self, cell_coords):
        if self.setplay:
            return None
        if cell_coords != None:
            x, y = cell_coords[0], cell_coords[1]
            self.board[y][x] = 0 if self.board[y][x] == 1 else 1


class Life(Board):
    def __init__(self, width, height):
        super().__init__(width, height)

    def next_move(self):
        self.boardcopy = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                self.boardcopy[y][x] = self.step(y, x)
        self.board = deepcopy(self.boardcopy)

    def step(self, y, x):
        t = [self.board[y - 1][x - 1],
             self.board[y - 1][x],
             self.board[y - 1][(x + 1) % self.width],
             self.board[y][x - 1],
             self.board[y][(x + 1) % self.width],
             self.board[(y + 1) % self.height][x - 1],
             self.board[(y + 1) % self.height][x],
             self.board[(y + 1) % self.height][(x + 1) % self.width]
             ]
        if self.board[y][x] == 0 and sum(t) == 3:
            return 1
        elif self.board[y][x] == 1 and 2 <= sum(t) <= 3:
            return 1
        else:
            return 0


def main():
    pygame.init()
    size = 620, 620
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Game of life')

    board = Life(30, 30)
    board.set_view(10, 10, 20)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    board.get_click(event.pos)
                if event.button == 3:
                    board.change_play_state(not board.get_state())

                if event.button == 4:
                    board.update_frame(-5)
                if event.button == 5:
                    board.update_frame(5)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    board.change_play_state(not board.get_state())
        if board.setplay:
            board.next_move()

        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
