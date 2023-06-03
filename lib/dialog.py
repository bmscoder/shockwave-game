import pygame as pg
from lib.button import Button


class Dialog:
    def __init__(self, screen, screenWidth, screenHeight, show_choosing_player_window):
        self.x = 175
        self.y = 200
        self.btn_width = 100
        self.btn_height = 50
        self.screen = screen
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.show_choosing_player_window = show_choosing_player_window

        self.activated = False
        self.buttons = []

        self.createButton()

    def createButton(self):
        self.font = pg.font.Font(None, 24)

        restartBtn = Button(self.screen, self.screenWidth // 2 - self.btn_width // 2, self.screenHeight - 200,
                            self.btn_width, self.btn_height, "Restart", self.font, self.show_choosing_player_window)

        self.buttons.append(restartBtn)

    def draw(self, text, x, y):
        if self.activated:
            self.font = pg.font.Font(None, 75)
            scoreText = self.font.render(f"{text}", True, (255, 0, 0))
            # textWidth, textHeight = scoreText.get_size()
            textX = x
            textY = y
            self.screen.blit(scoreText, (textX, textY))

            for btn in self.buttons:
                btn.draw()
        return self.buttons[0]
