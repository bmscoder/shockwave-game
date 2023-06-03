import pygame as pg
from random import randint, shuffle


class Bombs:
    def __init__(self, screen):
        self.screen = screen
        self.cellWidth = 70

    def put_bombs(self, is_new=False):
        if is_new:
            bombs = self.generate_bombs()
        else:
            bombs = self.old_bombs

        for i in range(36):
            if bombs[i] == 0:
                x = i // 6
                y = i % 6
                tnt = pg.transform.scale(pg.image.load("assets/photos/tnt.png").convert(),
                                         (self.cellWidth, self.cellWidth))
                self.screen.blit(tnt, (y * 100 + 15, x * 100 + 15))
        self.old_bombs = bombs

    def get_safe_cells_coords(self, SOUNDS):
        SOUNDS['bomb'].play()
        bombs = self.old_bombs
        coords = []
        for i in range(36):
            if bombs[i] == 1:
                x = i // 6
                y = i % 6
                x1 = y * 100 + 15
                y1 = x * 100 + 15
                coords.append((x1, y1, x1 + self.cellWidth, y1 + self.cellWidth))
        return coords

    def generate_bombs(self):
        safe_cells_count = randint(3, 6)
        bombs = [0] * (36 - safe_cells_count) + [1] * safe_cells_count
        shuffle(bombs)
        return bombs
