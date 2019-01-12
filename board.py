import pygame


pygame.init()
size = 500, 500
screen = pygame.display.set_mode(size)


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, pygame.Color(255, 255, 255),
                                 (
                                     x * self.cell_size + self.left,
                                     y * self.cell_size + self.top,
                                     self.cell_size,
                                     self.cell_size
                                 ), 1)
                if self.board[y][x] == 1:
                    pygame.draw.rect(screen, pygame.Color(255, 255, 255),
                                 (
                                     x * self.cell_size + self.left,
                                     y * self.cell_size + self.top,
                                     self.cell_size,
                                     self.cell_size
                                 ))

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or \
            cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def on_click(self, cell):
        if not cell:
            return None
        self.board[cell[1]][cell[0]] = 1 - self.board[cell[1]][cell[0]]

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)


board = Board(8, 8)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)
    screen.fill((0, 0, 0))
    board.render()
    pygame.display.flip()
pygame.quit()

