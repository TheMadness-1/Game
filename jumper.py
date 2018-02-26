import random
import pygame
import time


class Canvas():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 640))

    def redraw(self):
        self.screen.fill((0, 0, 0))


    def quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def screen_return(self):
        return self.screen

    def read_key(self):
        action_list = [0, 0, 0]
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            action_list[1] = 1
        if pressed[pygame.K_LEFT]:
            action_list[0] = 1
        if pressed[pygame.K_RIGHT]:
            action_list[2] = 1
        return action_list


class Pillar():
    def __init__(self, screen):
        self.screen = screen
        self.x1 = random.randint(20, 200)
        self.x2 = self.x1 + random.randint(250, 440)
        self.y1 = random.randint(10, 630)
        self.y2 = self.y1
        self.x1_board = self.x1 + 50
        self.x2_board = self.x2 + 50
        self.x_color = random.randint(0, 255)
        self.y_color = random.randint(0, 255)
        self.z_color = random.randint(0, 255)

    def draw_pillar(self):
        self.pillar = pygame.draw.line(self.screen, (self.x_color, self.y_color, self.z_color), (self.x1, self.y1), (self.x2, self.y2))
        self.y1 += 0.25
        self.y2 += 0.25
        if self.y1 > 640:
            self.y1, self.y2 = 0, 0
            self.x1 = random.randint(50, 300)
            self.x2 = self.x1 + random.randint(150, 300)

    def return_points(self):
        return (self.x1, self.y1, self.x2, self.y2)




class Bonuses():
    def __init__(self, screen):
        self.screen = screen
        self.start_position_x = random.randint(50, 560)
        self.start_position_y = 5
        self.size_length = 10
        self.size_width = 10
        self.bonus_position_list = 0

    def create_bonuses(self):
        self.bonus = pygame.draw.rect(self.screen, (0, 128, 255), pygame.Rect(self.start_position_x,
                                                                               self.start_position_y,
                                                                               self.size_length,
                                                                               self.size_width))

    def bonuses_moving(self):
        self.start_position_y += 1
        if (self.start_position_x > 0) and (self.start_position_x < 620):
            self.start_position_x += random.randint(-5, 5)
        elif self.start_position_x < 10:
            self.start_position_x += 10
        elif self.start_position_x > 620:
            self.start_position_x -= 10

    def return_bonuses_position(self):
        self.bonus_position_list = [self.start_position_x, self.start_position_y]
        return self.bonus_position_list


class Player():
    def __init__(self, screen):
        self.screen = screen
        self.x_move = 320
        self.y_move = 240
        self.length = 25
        self.width = 25
        self.impulse_up = 0
        self.impulse_g = 0
        self.position_k = True
        self.game_k = True
        self.game_score = 0

    def redraw(self):
        self.player = pygame.draw.rect(self.screen, (0, 128, 255), pygame.Rect(self.x_move,
                                                                               self.y_move,
                                                                               self.length,
                                                                               self.width))

    def _move_left(self):
        self.x_move -= 1.5

    def _move_right(self):
        self.x_move += 1.5

    def _move_jump(self):
        self.impulse_up = 300
        self.y_move -= self.impulse_up

    def _move_down(self):
        if self.position_k:
            self.y_move += self.impulse_g
            self.increase_impulse()
        else:
            self.impulse_g = 0

    def increase_impulse(self):
        if self.impulse_g < 2.5:
            self.impulse_g += 0.05
        else:
            self.impulse_g = 1.5

    def _reduce_impulse(self):
        if self.impulse_up > 0:
            self.impulse_up -= 1
        else:
            self.impulse_up = 0

    def _catch_bonus_check(self, bonus_position_list):
        self.bonus_position_list = bonus_position_list
        #print(bonus_position_list, self.x_move, self.length)
        if ((bonus_position_list[0] + 5 > self.x_move) and (bonus_position_list[0] < self.x_move + self.length)) and ((bonus_position_list[1] + 5 > self.y_move) and (bonus_position_list[1] < self.y_move + self.width)):
            print("bonus was catched")

    def request(self, action , bonus_position_list, points_pillar=[]):
        self._reduce_impulse()
        self._catch_bonus_check(bonus_position_list)
        self._across_check(points_pillar)
        self._move_down()
        self.action = action
        if self.action[0] == 1:
            self._move_left()
        if self.action[1] == 1 and self.impulse_up <= 0:
            self._move_jump()
        if self.action[2] == 1:
            self._move_right()
        # if self.action[0] == 1:
        #    self._move_left()


    def _across_check(self, points):
        self.bottom_x = self.x_move
        self.bottom_y = self.y_move + self.width
        self.position_k = True
        for pillar in points:
            if ((self.bottom_y > pillar[1]) and (-pillar[1] + self.bottom_y <= 4)) \
                    and ((self.bottom_x + self.width > pillar[0]) and (self.bottom_x < pillar[2])):
                self.position_k = False
                self.game_score += 1
                #print("check was")

    def return_game_score(self):
        return self.game_score

    def game_state(self):
        if self.y_move > 660:
            self.game_k = False
        return self.game_k




game_board = Canvas()
screen = game_board.screen_return()
player = Player(screen)
pillars_list = []
for i in range(10):
    pillars_list.append(Pillar(screen))
bonuses = Bonuses(screen)
go = True
k_time = random.randint(0, 10)
game_k = True

while game_k:
    game_k = player.game_state()
    game_board.redraw()
    #if k_time == 5:
    bonuses.create_bonuses()
    bonuses.bonuses_moving()
    points = []
    for pillar in pillars_list:
        pillar.draw_pillar()
        points.append(pillar.return_points())
    action = game_board.read_key()
    bonus_position_list = bonuses.return_bonuses_position()
    player.request(action, bonus_position_list, points_pillar=points)
    player.redraw()
    game_score = player.return_game_score()
    go = game_board.quit()
    if not game_k:
        print(10*"YOU LOSE!!!")
        print("YOUR FINAL SCORE IS", round(game_score/10))
    pygame.display.flip()
    time.sleep(0.01)