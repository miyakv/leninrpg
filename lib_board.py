import pygame


class Board:
    # создание поля
    def __init__(self, width, height, cell_size, left_m=10, top_m=10):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = left_m
        self.top = top_m
        self.cell_size = cell_size

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

