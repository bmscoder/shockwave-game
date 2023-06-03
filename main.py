import pygame as pg
import pymunk as pm
from lib.button import Button
from lib.player import Player
from lib.wall import Wall
from lib.bombs import Bombs
from lib.dialog import Dialog
import pymunk.pygame_util
from datetime import datetime
import sys

SOUNDS = {}


class Game:
    def __init__(self):
        self.screenWidth = 600
        self.screenHeight = 600
        self.fps = 60
        self.caption = "Shockwave game"
        self.screen = pg.display.set_mode((self.screenWidth, self.screenHeight))
        pg.display.set_caption(self.caption)
        self.space = pm.Space()
        self.space.gravity = 0, 0
        self.bgimage = pg.image.load("assets/photos/bg.png")
        self.wimage = pg.image.load("assets/photos/welcome.jpg")
        self.clock = pg.time.Clock()
        self.btn_width = 100
        self.btn_height = 50
        pg.mixer.init()
        bgmusic = pg.mixer.Sound('assets/audios/bgmusic.mp3')
        bgmusic.play(-1)
        self.show_start_window()

    def show_start_window(self):
        pg.init()
        self.font = pg.font.Font(None, 24)
        self.screen.blit(self.wimage, (0, 0))
        start_btn = Button(self.screen, 250, 500,
                           self.btn_width, self.btn_height, "Boshlash", self.font, self.show_choosing_player_window)
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                start_btn.handle_event(event)
            pg.display.update()
            self.clock.tick(self.fps)

    def show_choosing_player_window(self):
        pg.init()
        self.screen.blit(self.wimage, (0, 0))
        btns = [
            Button(self.screen, self.screenWidth // 2 - self.btn_width // 2, self.screenHeight - 100, self.btn_width,
                   self.btn_height, "3 o'yinchi", self.font, lambda: self.start_game(3)),
            Button(self.screen, self.screenWidth // 2 - self.btn_width // 2 - 200, self.screenHeight - 100,
                   self.btn_width, self.btn_height, "2 o'yinchi", self.font, lambda: self.start_game(2)),
            Button(self.screen, self.screenWidth // 2 - self.btn_width // 2 + 200, self.screenHeight - 100,
                   self.btn_width, self.btn_height, "4 o'yinchi", self.font, lambda: self.start_game(4))
        ]

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                for btn in btns:
                    btn.handle_event(event)

            self.clock.tick(self.fps)
            pg.display.update()

    def start_game(self, playersCount):
        pg.init()
        pymunk.pygame_util.positive_y_is_up = False
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.playerWidth = 80
        self.playerHeight = 50

        dist = 50
        if playersCount == 2:
            players_list = [
                Player(self.screen, self.space, (dist, dist), "assets/photos/blue.png",
                       (self.playerWidth, self.playerHeight), -135, (pg.K_w, pg.K_s, pg.K_a, pg.K_d), "BLUE"),
                Player(self.screen, self.space, (self.screenWidth - 50, self.screenHeight - 50),
                       "assets/photos/red.png", (self.playerWidth, self.playerHeight), 45,
                       (pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT), "RED"),
            ]
        elif playersCount == 3:
            players_list = [
                Player(self.screen, self.space, (dist, dist), "assets/photos/blue.png",
                       (self.playerWidth, self.playerHeight), -135, (pg.K_w, pg.K_s, pg.K_a, pg.K_d), "BLUE"),
                Player(self.screen, self.space, (dist, self.screenHeight - 50), "assets/photos/green.png",
                       (self.playerWidth, self.playerHeight), -45, (pg.K_u, pg.K_j, pg.K_h, pg.K_k), "GREEN"),
                Player(self.screen, self.space, (self.screenWidth - 50, self.screenHeight - 50),
                       "assets/photos/red.png", (self.playerWidth, self.playerHeight), 45,
                       (pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT), "RED"),
            ]
        elif playersCount == 4:
            players_list = [
                Player(self.screen, self.space, (dist, dist), "assets/photos/blue.png",
                       (self.playerWidth, self.playerHeight), -135, (pg.K_w, pg.K_s, pg.K_a, pg.K_d), "BLUE"),
                Player(self.screen, self.space, (self.screenWidth - 50, dist), "assets/photos/yellow.png",
                       (self.playerWidth, self.playerHeight), 135, (pg.K_KP8, pg.K_KP5, pg.K_KP4, pg.K_KP6), "YELLOW"),
                Player(self.screen, self.space, (dist, self.screenHeight - 50), "assets/photos/green.png",
                       (self.playerWidth, self.playerHeight), -45, (pg.K_u, pg.K_j, pg.K_h, pg.K_k), "GREEN"),
                Player(self.screen, self.space, (self.screenWidth - 50, self.screenHeight - 50),
                       "assets/photos/red.png", (self.playerWidth, self.playerHeight), 45,
                       (pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT), "RED"),
            ]

        wallWidth = 10
        walls = [
            Wall(self.screen, self.space, (-wallWidth, -wallWidth), (wallWidth, self.screenHeight + 2 * wallWidth)),
            Wall(self.screen, self.space, (0, -wallWidth), (self.screenWidth, wallWidth)),
            Wall(self.screen, self.space, (self.screenWidth, -wallWidth),
                 (wallWidth, self.screenHeight + 2 * wallWidth)),
            Wall(self.screen, self.space, (0, self.screenHeight), (self.screenWidth, wallWidth))
        ]

        self.bomb_duration = 3
        self.bomb_duration_coef = 0.1
        self.duration = 2
        self.is_bombs_placed = False
        time_start = datetime.now()

        bombs = Bombs(self.screen)

        SOUNDS['warning'] = pg.mixer.Sound('assets/audios/warning.ogg')
        SOUNDS['bomb'] = pg.mixer.Sound('assets/audios/bomb.mp3')

        dialog = Dialog(self.screen, self.screenWidth, self.screenHeight, self.show_choosing_player_window)
        while True:
            self.screen.blit(self.bgimage, (0, 0))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            pressed_keys = pg.key.get_pressed()
            for player in players_list:
                player.process(pressed_keys)

            time_end = datetime.now()
            delta_time = time_end - time_start

            if delta_time.seconds >= self.duration and not self.is_bombs_placed:
                bombs.put_bombs(True)
                self.is_bombs_placed = True
                time_start = datetime.now()
                SOUNDS['warning'].play()
            elif delta_time.seconds < self.bomb_duration and self.is_bombs_placed:
                bombs.put_bombs()
                for player in players_list:
                    player.forward_dist = 8
            elif delta_time.seconds >= self.bomb_duration:
                safe_cells_coords = bombs.get_safe_cells_coords(SOUNDS)
                new_player_list = []
                for i, player in enumerate(players_list):
                    if self.check_death(safe_cells_coords, player.body.position):
                        self.space.remove(player.body, player.shape)
                    else:
                        new_player_list.append(player)
                players_list = new_player_list.copy()

                self.bomb_duration -= self.bomb_duration_coef
                self.is_bombs_placed = False
                for player in players_list:
                    player.forward_dist = 4
                time_start = datetime.now()

            for player in players_list:
                player.draw()

            if len(players_list) == 1:
                dialog.activated = True
                if player.color == "BLUE":
                    x = 75
                elif player.color == "YELLOW":
                    x = 30
                elif player.color == "GREEN":
                    x = 50
                elif player.color == "RED":
                    x = 90
                btn = dialog.draw(f"{player.color} PLAYER WIN", x, 280)
                for i, player in enumerate(players_list):
                    self.space.remove(player.body, player.shape)
                while True:
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            pg.quit()
                            sys.exit()
                        btn.handle_event(event)

                    self.clock.tick(self.fps)
                    pg.display.update()

            elif len(players_list) == 0:
                dialog.activated = True
                btn = dialog.draw("TIE", 250, 270)
                for i, player in enumerate(players_list):
                    self.space.remove(player.body, player.shape)
                while True:
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            pg.quit()
                            sys.exit()
                        btn.handle_event(event)

                    self.clock.tick(self.fps)
                    pg.display.update()

            self.space.step(0.1)
            self.clock.tick(self.fps)
            pg.display.update()

    def check_death(self, coords, pos):
        alive = False
        for coord in coords:
            if coord[0] <= pos[0] <= coord[2] and coord[1] <= pos[1] <= coord[3]:
                alive = True
                break
        return not alive


if __name__ == "__main__":
    new_game = Game()
