# A Gravity Journey
# Ver 3


import simplegui
import random
import math

WIDTH = 800
HEIGHT = 600
started = False
howto = False
high_score = False

background = simplegui.load_image("https://i.imgur.com/sdfuQ6n.jpg")
tile = simplegui.load_image("https://i.imgur.com/3OWpBdz.png")
#tile = simplegui.load_image("https://i.imgur.com/ruqTFnR.png")
fire_trap = simplegui.load_image("https://i.imgur.com/NW1z3Jr.png")
reverse_fire = simplegui.load_image("https://i.imgur.com/vHswhqV.png")
character = simplegui.load_image("https://i.imgur.com/McszdaC.png")
reverse_char = simplegui.load_image("https://i.imgur.com/LgPh9uF.png")
needle_trap = simplegui.load_image("https://i.imgur.com/qIO2WTx.png")
needle_trap_2 = simplegui.load_image("https://i.imgur.com/NvHVydF.png")
enemy_image = simplegui.load_image("https://i.imgur.com/sRswcw1.png")
coin_image = simplegui.load_image("http://i.imgur.com/tjrkrQ7.png")
instructions = simplegui.load_image("https://i.imgur.com/gTqFZwz.png")
back_button = simplegui.load_image("https://i.imgur.com/yX0qR9m.png")
hall_of_fame = simplegui.load_image("https://i.imgur.com/kHV9iIm.jpg")
door = simplegui.load_image("https://i.imgur.com/LTDnVZQ.png")

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

class Character:
    def __init__(self, pos, health, image, reverse_image, center, size, inventory = set(),  gravity_check = 'Down'):
        self.original = [pos[0], pos[1]]
        self.pos = [pos[0], pos[1]]
        self.health = health
        self.image = image
        self.reverse_image = reverse_image
        self.image_center = center
        self.image_size = size
        self.check = gravity_check
        self.vel = [0, 0]
        self.level = 0
        self.draw_size = [50, 80]
        self.size = [80, 80]
        self.walk_left = False
        self.walk_right = False
        self.fly = False
        self.fly_track = 0
        self.walk_track = 0
        self.coins = 0
        
    def get_draw_size(self):
        return self.draw_size
        
    def get_level(self):
        return self.level
    
    def draw(self,canvas):
        if self.check == 'Down':
            if self.fly == True and self.walk_right == True:
                self.walk_track = (self.walk_track + 1) % (7 * 2)
                canvas.draw_image(self.image, [32 + (int)(self.walk_track/2) * 64, 3 * 64 + 32], self.image_size,
                                  self.pos, self.size)
            elif self.fly == True and self.walk_left == True:
                self.walk_track = (self.walk_track + 1) % (7 * 2)
                canvas.draw_image(self.image, [32 + (int)(self.walk_track/2) * 64, 64 + 32], self.image_size,
                                  self.pos, self.size)
            elif self.fly == True:
                self.fly_track = (self.fly_track + 1) % 7 
                canvas.draw_image(self.image, [32 + (int)(self.fly_track) * 64, 2 * 64 + 32], self.image_size,
                                  self.pos, self.size)
            elif self.walk_right == True:
                self.walk_track = (self.walk_track + 1) % 45
                canvas.draw_image(self.image, [32 + (int)(self.walk_track/5) * 64, 11 * 64 + 32], self.image_size,
                                  self.pos, self.size)
            elif self.walk_left == True:
                self.walk_track = (self.walk_track + 1) % 45
                canvas.draw_image(self.image, [32 + (int)(self.walk_track/5) * 64, 9 * 64 + 32], self.image_size,
                                  self.pos, self.size)
            else:
                canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, 
                          self.size)
        elif self.check == 'Up':
            if self.fly == True and self.walk_right == True:
                self.walk_track = (self.walk_track + 1) % (7 * 2)
                canvas.draw_image(self.reverse_image, [32 + (int)(self.walk_track/2) * 64, 17 * 64 + 32], self.image_size,
                                  self.pos, self.size)
            elif self.fly == True and self.walk_left == True:
                self.walk_track = (self.walk_track + 1) % (7 * 2)
                canvas.draw_image(self.reverse_image, [32 + (int)(self.walk_track/2) * 64, 19 * 64 + 32], self.image_size,
                                  self.pos, self.size)
            elif self.fly == True:
                self.fly_track = (self.fly_track + 1) % 7 
                canvas.draw_image(self.reverse_image, [32 + (int)(self.fly_track) * 64, 18 * 64 + 32], self.image_size,
                                  self.pos, self.size)
            elif self.walk_right == True:
                self.walk_track = (self.walk_track + 1) % 45
                canvas.draw_image(self.reverse_image, [32 + (int)(self.walk_track/5) * 64, 9 * 64 + 32], self.image_size,
                                  self.pos, self.size)
            elif self.walk_left == True:
                self.walk_track = (self.walk_track + 1) % 45
                canvas.draw_image(self.reverse_image, [32 + (int)(self.walk_track/5) * 64, 11 * 64 + 32], self.image_size,
                                  self.pos, self.size)
            else:
                canvas.draw_image(self.reverse_image, self.image_center, self.image_size, self.pos, 
                              self.size)
        
    def reset(self):
        self.pos = [100, 460]
        camera.pos = [0, 0]
        camera.track = [100, 460]
        self.vel = [0, 0]
        self.check = 'Down'
        # self.coins = 0 
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
                    
    def update(self):
        #self.collide(enemy)
        #self.collide(enemy2)
        #self.collide(enemy3)
        self.pos[1] = self.pos[1] + self.vel[1]
        if self.pos[0] > 200 and self.pos[0] < 550:
            self.pos[0] = self.pos[0] + self.vel[0]
                
        elif self.pos[0] <= 550 and self.vel[0] > 0:
            self.pos[0] = self.pos[0] + self.vel[0]
                
        elif self.pos[0] >= 550 and self.vel[0] < 0:
            self.pos[0] = self.pos[0] + self.vel[0]
                
        elif self.pos[0] <= 550 and self.vel[0] < 0:
            camera.pos[0] = camera.pos[0] + self.vel[0]
                
        elif self.pos[0] >= 550 and self.vel[0] > 0:
            camera.pos[0] = camera.pos[0] + self.vel[0]
                
        camera.track[0] = camera.track[0] + self.vel[0]
        camera.track[1] = camera.track[1] + self.vel[1]
        gravity_constant = 2.0 / 6.0
        column = (int)(camera.track[0] / 50.0)
        row = (int)(self.pos[1] / 50.0)
        row_check1 = (int)( (self.pos[1] + self.draw_size[1] / 2 - 5) / 50.0 )
        row_check2 = (int)( (self.pos[1] - self.draw_size[1] / 2 + 5) / 50.0 )
        column_check1 = (int)( (camera.track[0] + self.draw_size[0]/2 - 10) / 50.0 )
        column_check2 = (int)( (camera.track[0] - self.draw_size[0]/2 + 10) / 50.0 )
        
        if self.level == 0:
            grid = stage1.get_info()
        elif self.level == 1:
            grid = stage2.get_info()
        elif self.level == 2:
             grid = stage3.get_info()
        
        #if self.pos[0] < 0:
        #    if self.level == 0:
        #        self.level = 0
        #        self.reset()
        #    else:
        #        self.level -= 1
        #        self.reset()
        #elif self.pos[0] > 750:
        #    self.reset()
        #    self.level += 1
        
        if self.pos[1] < 0 or self.pos[1] > 600:
            self.reset()
        
        if row > 0 and row < 11 and column > -1 and column_check2 > -1:
            if self.check == 'Down':
                if grid[row + 1][column_check1] == 'W' and (row + 1) * 50 - self.pos[1] <= self.draw_size[1]/2.0:
                    self.vel[1] = 0
                    self.pos[1] = (row+1) * 50 - self.draw_size[1]/2.0
                    self.fly = False
                    self.fly_track = 0
                elif grid[row + 1][column_check2] == 'W' and (row + 1) * 50 - self.pos[1] <= self.draw_size[1]/2.0:
                    self.vel[1] = 0
                    self.pos[1] = (row+1) * 50 - self.draw_size[1]/2.0
                    self.fly = False
                    self.fly_track = 0
                elif grid[row + 1][column_check1] == 'T' and (row + 1) * 50 - self.pos[1] <= self.draw_size[1]/2.0:
                    self.reset()
                elif grid[row + 1][column_check2] == 'T' and (row + 1) * 50 - self.pos[1] <= self.draw_size[1]/2.0:
                    self.reset()
                elif grid[row + 1][column_check1] == 'N' and (row + 1) * 50 - self.pos[1] <= self.draw_size[1]/2.0:
                    self.reset()
                elif grid[row + 1][column_check2] == 'N' and (row + 1) * 50 - self.pos[1] <= self.draw_size[1]/2.0:
                    self.reset()
                else:
                    self.vel[1] += gravity_constant
                if column > 0:
                    if grid[row][column + 1] == 'W' and self.vel[0] > 0 and (column+1)*50 - camera.track[0] <= self.draw_size[0]/2.0:
                        self.vel[0] = 0
                    elif grid[row][column - 1] == 'W' and self.vel[0] < 0 and camera.track[0] - column * 50 <= self.draw_size[0]/2.0:
                        self.vel[0] = 0
                    elif grid[row][column + 1] == 'T' and self.vel[0] > 0 and (column+1)*50 - camera.track[0] <= self.draw_size[0]/2.0:
                        self.reset()
                    elif grid[row][column - 1] == 'T' and self.vel[0] < 0 and camera.track[0] - column * 50 <= self.draw_size[0]/2.0:
                        self.reset()
                    elif grid[row][column + 1] == 'N' and self.vel[0] > 0 and (column+1)*50 - camera.track[0] <= self.draw_size[0]/2.0:
                        self.reset()
                    elif grid[row][column - 1] == 'N' and self.vel[0] < 0 and camera.track[0] - column * 50 <= self.draw_size[0]/2.0:
                        self.reset()
            elif self.check == 'Up':
                if grid[row- 1][column_check1] == 'W' and self.pos[1] - row * 50 <= self.draw_size[1]/2.0:
                    self.vel[1] = 0
                    self.pos[1] = row * 50 + self.draw_size[1]/2.0
                    self.fly = False
                    self.fly_track = 0
                elif grid[row - 1][column_check2] == 'W' and self.pos[1] - row * 50 <= self.draw_size[1]/2.0:
                    self.vel[1] = 0
                    self.pos[1] = row * 50 + self.draw_size[1]/2.0
                    self.fly = False
                    self.fly_track = 0
                elif grid[row - 1][column_check1] == 'R' and self.pos[1] - row * 50 <= self.draw_size[1]/2.0:
                    self.reset()
                elif grid[row - 1][column_check2] == 'R' and self.pos[1] - row * 50 <= self.draw_size[1]/2.0:
                    self.reset()
                    
                else:
                    self.vel[1] -= gravity_constant
                if column > 0:
                    if grid[row][column + 1] == 'W' and self.vel[0] > 0 and (column+1)*50 - camera.track[0] <= self.draw_size[0]/2.0:
                        self.vel[0] = 0
                    elif grid[row][column - 1] == 'W' and self.vel[0] < 0 and camera.track[0] - column * 50 <= self.draw_size[0]/2.0:
                        self.vel[0] = 0
                    elif grid[row][column - 1] == 'R' and self.vel[0] < 0 and camera.track[0] - column * 50 <= self.draw_size[0]/2.0:
                        self.reset()
                    elif grid[row][column + 1] == 'R' and self.vel[0] > 0 and (column+1)*50 - camera.track[0] <= self.draw_size[0]/2.0:
                        self.reset()
                        
       
    def reverse_gravity(self):
        if self.check == 'Down':
            self.vel[1] = 0
            self.check = 'Up'
        elif self.check == 'Up':
            self.vel[1] = 0
            self.check = 'Down'
    
    def move_right(self):
        self.vel[0] = 15.0/6.0
    
    def move_left(self):
        self.vel[0] = - 15.0 / 6.0
    
    def keydown_handler(self, key):
        if key == simplegui.KEY_MAP['left']:
            self.move_left()
            self.walk_left = True
        elif key == simplegui.KEY_MAP['right']:
            self.move_right()
            self.walk_right = True
        if key == simplegui.KEY_MAP['space']:
            self.reverse_gravity()
            self.fly = True
    
    def keyup_handler(self, key):
        if key == simplegui.KEY_MAP['left']:
            self.vel[0] = 0
            self.walk_left = False
            self.walk_track = 0
        elif key == simplegui.KEY_MAP['right']:
            self.vel[0] = 0
            self.walk_right = False
            self.walk_track = 0
            
    def collide(self, other_object):
        
        if dist(camera.track, other_object.get_position()) <= 60:
            # print camera.track, other_object.get_position()
            self.reset()
            return True
        else:
            return False
                              
class Camera:
    def __init__(self):
        self.pos = [0, 0]
        self.draw_pos = [0, 0]
        self.track = [150, 460]
        self.draw_size = char.get_draw_size()
        self.left_bound = 0
        self.right_bound = 15
        
    def update(self):
        self.draw_pos[0] = 25 - self.pos[0] % 50
        self.left_bound = (int)(self.pos[0] // 50)
        self.right_bound = (int)(self.left_bound + 15)
            
class Stage:
    def __init__(self, level_matrix, coin_group = set(), goal_group = set(), enemy_group = set()):
        self.level_info = level_matrix
        self.coin_count = 0
        self.needle_count = 0
        self.enemy_group = enemy_group
        self.goal_group = goal_group
        self.coin_group = coin_group
        
    def draw(self, canvas):
        #print char.coins
        
        canvas.draw_image(background, [800, 600], [1600, 1200], [WIDTH/2, HEIGHT/2], [WIDTH, HEIGHT])
        
        
        for enemy in self.enemy_group:
            enemy.draw(canvas)
            char.collide(enemy)
            
        for goal in self.goal_group:
            goal.draw(canvas)
            
        for coin in self.coin_group:
            coin.draw(canvas)
            if coin.collide():
                self.coin_group.discard(coin)
                char.coins += 1
            
        self.coin_count = (self.coin_count + 1) % (8 * 10)
        self.needle_count = (self.needle_count + 1) % (2 * 8)
        for i in range(12):
            for j in range(camera.left_bound, camera.right_bound +2):
                if self.level_info[i][j] == 'W':
                    canvas.draw_image(tile, [125, 125], [250, 250], [camera.draw_pos[0]+ 50 * (j-camera.left_bound), 25 + 50 * i], [50, 50])                
                elif self.level_info[i][j] == 'T':
                    canvas.draw_image(fire_trap, [32, 32], [64, 64], [camera.draw_pos[0]+ 50 * (j-camera.left_bound), 25 + 50 * i], [50, 50])
                elif self.level_info[i][j] == 'R':
                    canvas.draw_image(reverse_fire, [32, 32], [64, 64], [camera.draw_pos[0]+ 50 * (j-camera.left_bound), 25 + 50 * i], [50, 50])
                elif self.level_info[i][j] == 'N':
                    if self.needle_count < 8:
                        canvas.draw_image(needle_trap, [369/2.0, 369/2.0], [369, 369], [camera.draw_pos[0]+ 50 * (j-camera.left_bound), 25 + 50 * i], [50, 50])
                    else:
                        canvas.draw_image(needle_trap_2, [369/2.0, 369/2.0], [369, 369], [camera.draw_pos[0]+ 50 * (j-camera.left_bound), 25 + 50 * i], [50, 50])
                elif self.level_info[i][j] == 'C':
                    canvas.draw_image(coin_image, [16, 16 + (self.coin_count / 10) * 32], [32, 32], [camera.draw_pos[0]+ 50 * (j-camera.left_bound), 25 + 50 * i], [40, 40])
                    

        canvas.draw_text('x '+str(char.coins), [50, 50], 40, 'Red')
        canvas.draw_image(coin_image, [16, 16], [32, 32], [25, 40], [70, 70])
        
    def get_info(self):
        return self.level_info
    
    def get_matrix_info(self):
        return self.matrix_info

class Enemy:
    def __init__(self, track, image, center, size, height, move_type, gravity_check = 'Down'):
        self.track = track
        self.image = image
        self.image_size = size
        self.image_center = center
        self.check = gravity_check 
        self.size = [60, 80]
        self.draw_size = [80, 80]
        self.draw_pos = [0, height]
        self.vel = [0, 0]
        self.counter = 0
        self.move_type = move_type
        self.walk_right = False
        self.walk_left = False
        self.fly = False
        self.walk_track = 0
        self.fly_track = 0
        
    def draw(self, canvas):
        self.update()
        if self.check == 'Down':
            if self.fly == True and self.walk_right == True:
                self.walk_track = (self.walk_track + 2) % (7 * 2)
                canvas.draw_image(self.image, [32 + (int)(self.walk_track/2) * 64, 3 * 64 + 32], self.image_size,
                                  self.draw_pos, self.draw_size)
            elif self.fly == True and self.walk_left == True:
                self.walk_track = (self.walk_track + 1) % (7 * 2)
                canvas.draw_image(self.image, [32 + (int)(self.walk_track/2) * 64, 64 + 32], self.image_size,
                                  self.draw_pos, self.draw_size)
            elif self.fly == True:
                self.fly_track = (self.fly_track + 1) % 7 
                canvas.draw_image(self.image, [32 + (int)(self.fly_track) * 64, 2 * 64 + 32], self.image_size,
                                  self.draw_pos, self.draw_size)
            elif self.walk_right == True:
                self.walk_track = (self.walk_track + 1) % 45
                canvas.draw_image(self.image, [32 + (int)(self.walk_track/5) * 64, 11 * 64 + 32], self.image_size,
                                  self.draw_pos, self.draw_size)
            elif self.walk_left == True:
                self.walk_track = (self.walk_track + 1) % 45
                canvas.draw_image(self.image, [32 + (int)(self.walk_track/5) * 64, 9 * 64 + 32], self.image_size,
                                  self.draw_pos, self.draw_size)
            else:
                canvas.draw_image(self.image, self.image_center, self.image_size, self.draw_pos, 
                                    self.draw_size)
        elif self.check == 'Up':
            if self.fly == True and self.walk_right == True:
                self.walk_track = (self.walk_track + 1) % (7 * 2)
                canvas.draw_image(self.reverse_image, [32 + (int)(self.walk_track/2) * 64, 17 * 64 + 32], self.image_size,
                                  self.pos, self.size)
            elif self.fly == True and self.walk_left == True:
                self.walk_track = (self.walk_track + 1) % (7 * 2)
                canvas.draw_image(self.reverse_image, [32 + (int)(self.walk_track/2) * 64, 19 * 64 + 32], self.image_size,
                                  self.pos, self.size)
            elif self.fly == True:
                self.fly_track = (self.fly_track + 1) % 7 
                canvas.draw_image(self.reverse_image, [32 + (int)(self.fly_track) * 64, 18 * 64 + 32], self.image_size,
                                  self.pos, self.size)
            elif self.walk_right == True:
                self.walk_track = (self.walk_track + 1) % 45
                canvas.draw_image(self.reverse_image, [32 + (int)(self.walk_track/5) * 64, 9 * 64 + 32], self.image_size,
                                  self.pos, self.size)
            elif self.walk_left == True:
                self.walk_track = (self.walk_track + 1) % 45
                canvas.draw_image(self.reverse_image, [32 + (int)(self.walk_track/5) * 64, 11 * 64 + 32], self.image_size,
                                  self.pos, self.size)
            else:
                canvas.draw_image(self.reverse_image, self.image_center, self.image_size, self.pos, 
                              self.size)
            
    
    def move_left(self):
        self.vel[0] = - 6 / 6.0
        self.walk_left = True
        
    def move_right(self):
        self.vel[0] = 6 / 6.0
        self.walk_right = True
        
    def stop(self):
        self.vel = [0, 0]
        self.walk_right = False
        self.walk_left = False
        self.fly = False
    
    def fly_up(self):
        self.vel[1] = - 6/6.0
        self.fly = True
        
    def fly_down(self):
        self.vel[1] = 6/6.0
        self.fly = True
        
    def update(self):
        self.counter = (self.counter + 1) % 360
        if self.move_type == 'horizontal':
            if self.counter < 180:
                self.stop()
                self.move_right()
            else:
                self.stop()
                self.move_left()
        elif self.move_type == 'vertical':
            if self.counter < 180:
                self.stop()
                self.fly_up()
            else:
                self.stop()
                self.fly_down()
        self.track[0] = self.track[0] + self.vel[0]
        self.track[1] = self.track[1] + self.vel[1]
        self.draw_pos[0] = self.track[0] - camera.pos[0] 
        self.draw_pos[1] = self.track[1]
     
    def get_position(self):
        return self.track
    
class Menu:
    def __init__(self):
        self.splash_screen= ['                                ',
                             '                                ',
                             '    WWWWWWWWWWWWWWWWWWWWWWW     ',
                             '    W                     W     ',
                             '    W WWW WWW WWW WWW WWW W     ',
                             '    W W    W  W W W W  W  W     ',
                             '    W WWW  W  WWW WW   W  W     ',
                             '    W   W  W  W W W W  W  W     ',
                             '    W WWW  W  W W W W  W  W     ',
                             '    W                     W     ',
                             '    WWWWWWWWWWWWWWWWWWWWWWW     ',
                             '                                ',
                             '                                ',
                             ' N N NNN N N N  NNN NNN         ',
                             ' NNN N N N N N   N  N N         ',
                             ' N N NNN  N N    N  NNN         ',
                             '                                ',
                             '                                ',
                             '               C C C CC  C C    ',
                             '               CCC C C C CCC    ',
                             '               C C C CCC C C    ',
                             '                                ',
                             '                                ',
                             '                                ']
        self.coin_count = 0
        self.needle_count = 0
        
        self.start_button_horizontal = [4 * 25, 27 * 25]
        self.start_button_vertical = [2 * 25, 11 * 25]
        
        self.howto_button_horizontal = [1 * 25, 23 * 25]
        self.howto_button_vertical = [13 * 25, 16 * 25]
        
        self.high_button_horizontal = [15 * 25, 28 * 25]
        self.high_button_vertical = [18 * 25, 21 * 25]
        
    def draw(self, canvas):
        self.coin_count = (self.coin_count + 1) % (8 * 10)
        self.needle_count = (self.needle_count + 1) % (2 * 9)
        canvas.draw_image(background, [800, 600], [1600, 1200], [WIDTH/2, HEIGHT/2], [WIDTH, HEIGHT])
        for i in range(24):
            for j in range(31):
                if self.splash_screen[i][j] == 'W':
                    canvas.draw_image(tile, [125, 125], [250, 250], [12.5 + 25 * j, 12.5 + 25 * i], [25, 25])
                elif self.splash_screen[i][j] == 'N':
                    if self.needle_count < 9:
                        canvas.draw_image(needle_trap, [369/2.0, 369/2.0], [369, 369], [12.5 + 25 * j, 12.5 + 25 * i], [25, 25])
                    else:
                        canvas.draw_image(needle_trap_2, [369/2.0, 369/2.0], [369, 369], [12.5 + 25 * j, 12.5 + 25 * i], [25, 25])
                elif self.splash_screen[i][j] == 'C':
                    canvas.draw_image(coin_image, [16, 16 + (self.coin_count / 10) * 32], [32, 32], [12.5 + 25 * j, 12.5 + 25 * i], [38, 38])

    def click(self, pos):
        global started, howto, high_score
        if started == False and howto == False and high_score == False:
            if pos[0] > self.start_button_horizontal[0] and pos[0] < self.start_button_horizontal[1]:
                if pos[1] > self.start_button_vertical[0] and pos[1] < self.start_button_vertical[1]:
                    started = True
            
            if pos[0] > self.howto_button_horizontal[0] and pos[0] < self.howto_button_horizontal[1]:
                if pos[1] > self.howto_button_vertical[0] and pos[1] < self.howto_button_vertical[1]:
                    howto = True
                    
            if pos[0] > self.high_button_horizontal[0] and pos[0] < self.high_button_horizontal[1]:
                if pos[1] > self.high_button_vertical[0] and pos[1] < self.high_button_vertical[1]:
                    high_score = True
                                       
            
class Instructions:
    def __init__(self):

        self.button_horizontal = [600, 600 + 113]
        self.button_vertical = [50, 50 + 83]
        self.button_pos = [(self.button_horizontal[0] + self.button_horizontal[1]) / 2.0,
                           (self.button_vertical[0] + self.button_vertical[1]) / 2.0]
        self.button_width = self.button_horizontal[1] - self.button_horizontal[0]
        self.button_height = self.button_vertical[1] - self.button_vertical[0]
        
    def draw(self, canvas):
        canvas.draw_image(instructions, [2133/2.0, 600], [2133, 1200], [WIDTH/2, HEIGHT/2], [WIDTH, HEIGHT])
        canvas.draw_image(back_button, [113/2.0, 83/2.0], [113, 83], self.button_pos, 
                          [self.button_width, self.button_height])
        
    def click(self, pos):
        global howto
        if pos[0] > self.button_horizontal[0] and pos[0] < self.button_horizontal[1]:
            if pos[1] > self.button_vertical[0] and pos[1] < self.button_vertical[1]:
                howto = False
                
                
class Hall_of_fame:
    def __init__(self):

        self.button_horizontal = [650, 650 + 113]
        self.button_vertical = [25, 25 + 83]
        self.button_pos = [(self.button_horizontal[0] + self.button_horizontal[1]) / 2.0,
                           (self.button_vertical[0] + self.button_vertical[1]) / 2.0]
        self.button_width = self.button_horizontal[1] - self.button_horizontal[0]
        self.button_height = self.button_vertical[1] - self.button_vertical[0]
        
    def draw(self, canvas):
        canvas.draw_image(hall_of_fame, [2133/2.0, 600], [2133, 1200], [WIDTH/2, HEIGHT/2], [WIDTH, HEIGHT])
        canvas.draw_image(back_button, [113/2.0, 83/2.0], [113, 83], self.button_pos, 
                          [self.button_width, self.button_height])
        
    def click(self, pos):
        global high_score
        if pos[0] > self.button_horizontal[0] and pos[0] < self.button_horizontal[1]:
            if pos[1] > self.button_vertical[0] and pos[1] < self.button_vertical[1]:
                high_score = False
                

class Door:
    def __init__(self, track, image, center, size):
        self.track = track
        self.image = image
        self.image_size = size
        self.image_center = center
        self.draw_pos = [0, 0]
        self.count = 0
        self.draw_size = [80, 80]
        
    def update(self):
        self.draw_pos[1] = self.track[1]
        self.draw_pos[0] = self.track[0] - camera.pos[0]
        
    def collide(self):
        if dist(self.track, camera.track) <= 50:
            return True
        return False
        
    def draw(self, canvas):
        self.update()
        if self.collide():
            self.count = (self.count + 1) % (3 * 10)
            canvas.draw_image(self.image, [32 + 4 * 64, 32 + (int)(self.count/10) * 64], self.image_size, 
                              self.draw_pos, self.draw_size)
            if self.count == 2 * 10 + 2:
                char.reset()
                char.coins = 0
                char.level += 1
                self.count = 0
                
        else:
            canvas.draw_image(self.image, [32 + 4 * 64, 32], self.image_size, 
                              self.draw_pos, self.draw_size)
            
class Coin:
    def __init__(self, track, image, center, size):
        self.track = track
        self.image = image
        self.image_size = size
        self.image_center = center
        self.draw_pos = [0, 0]
        self.count = 0
        self.draw_size = [50, 50]
        
    def collide(self):
        if dist(self.track, camera.track) <= 35:
            return True
        return False
    
    def update(self):
        self.draw_pos[1] = self.track[1]
        self.draw_pos[0] = self.track[0] - camera.pos[0]
        
    def draw(self, canvas):
        self.update()
        self.count = (self.count + 1) % (8 * 10)
        canvas.draw_image(self.image, [16, 16 + (int)(self.count / 10) * 32], self.image_size, 
                          self.draw_pos, self.draw_size)
    
level1_matrix = ['WWWWWWWWWWW WWWWW  WWWWWWWWWWWWWWWWWWWWWWWWWW  WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
                 'WWWWWWWWWWW WWWWW  WWWWWWWWWWWWWWWWWWWWWWWWWW  WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
                 'W    W W               W W       RRR                          W WWWWWWWWWWWWWWWWWWWWWW',
                 'W                      WWW                                    W W            WWWWWWWWW',
                 'W                                                                            WWWWWWWWW',
                 'W                                                                            WWWWWWWWW',
                 'W                                                                            WWWWWWWWW',
                 'W                                                                            WWWWWWWWW',
                 'W         WW                          W W                                    WWWWWWWWW',
                 'W         WW      TTT        NNN      WWW                                    WWWWWWWWW',
                 'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW  WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
                 'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW  WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW']

level2_matrix = ['WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW                     WWWWWWWWWWWWWWWWWWW     WWW  WWW  WWWW  WWWW     WWWWWWWWWWWWWWWWW',
                 'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW                     WWWWWWW  WWWWWWW                                WWWWWWWWWWWWWWWWW',
                 'WWWWWWWWWWWWWWWW                   WW  WW  WW  WW W                                                               WWWWW',
                 'W             WW                                                          WWWWWWWWWWWWWWWWWWWWWWWWW               WWWWW',
                 'W             WW                                                           RRRRR  RRRRRRRRRR RRRRRR    WWW        WWWWW',
                 'W                        WWW                                WWW                                                   WWWWW',
                 'W                                                           W W                                                   WWWWW',
                 'W        WWW                                                W W                                                   WWWWW',
                 'W                                   WW  WWW   W   WWW                      NNNNNNNNNNNNNNNNNNNNNNNN               WWWWW',
                 'W       NNNNNN                                                             WWWWWWWWWWWWWWWWWWWWWWWW   TTTT        WWWWW',
                 'WWWWWWWWWWWWWWWWWWWTTTTWWWWWWWWWW                    WWWWWW   WWWWWWWWW                               WWWW        WWWWW',
                 'WWWWWWWW     WWWWWWWWWWWWWWW         W   W  W   W   W  WWWW     WWWWWWW                               WWWWWWWWWWWWWWWWW']



char = Character([150, 460], 100, character, reverse_char, [32, 32 + 64 * 6], [64, 64])
enemy = Enemy([1100, 460], enemy_image, [32, 32], [64, 64], 460, 'horizontal')
enemy2 = Enemy([400, 400], enemy_image, [32, 32], [64, 64], 400, 'vertical')
enemy3 = Enemy([1700, 400], enemy_image, [32, 32], [64, 64], 400, 'vertical')
enemy_group = set([enemy, enemy2, enemy3])

enemy4 = Enemy([25 + 24 * 50, 460], enemy_image, [32, 32], [64, 64], 460, 'horizontal')
enemy5 = Enemy([25 + 42 * 50, 300], enemy_image, [32, 32], [64, 64], 300, 'vertical')
enemy_group2 = set([enemy2, enemy3, enemy4, enemy5])

coin_group = set()
for i in range(4):
    coin = Coin([25 + (13 + i) * 50, 25 + 6 * 50], coin_image, [16, 16], [32, 32])
    coin_group.add(coin)  
    
for i in range(3):
    coin = Coin([25 + (39 + i) * 50, 25 + 6 * 50], coin_image, [16, 16], [32, 32])
    coin_group.add(coin)
    
for i in range(5):
    coin = Coin([25 + (63 + i) * 50, 25 + 9 * 50], coin_image, [16, 16], [32, 32])
    coin_group.add(coin)
    
coin_group2 = coin_group.copy()
for i in range(10):
    coin = Coin([25 + (77 + i) * 50, 25 + 6 * 50], coin_image, [15, 16], [32, 32])
    coin_group2.add(coin)

camera = Camera()
menu = Menu()
instruct = Instructions()
hall = Hall_of_fame()

goal = Door([71 * 50 + 25, 460], door, [32, 32], [64, 64])
goal_group = set([goal])
stage1 = Stage(level1_matrix, coin_group, goal_group, enemy_group)
stage2 = Stage(level2_matrix, coin_group2, set(), enemy_group2)

def keyup_handler(key):
    char.keyup_handler(key)
    
def keydown_handler(key):
    char.keydown_handler(key)   
    
def mouse_click(pos):
    menu.click(pos)
    if started == False and howto == True:
        instruct.click(pos)
    elif started == False and high_score == True:
        hall.click(pos)
    
def draw_handler(canvas):
    global stage1
    # print started, howto
    if started == False:
        if howto == False and high_score == False:
            menu.draw(canvas)
        elif howto == True:
            instruct.draw(canvas)
        else:
            hall.draw(canvas)
        
    else:
        camera.update()
        if char.get_level() == 0:
            stage1.draw(canvas)
            
        elif char.get_level() == 1:
            stage2.draw(canvas)
            
        else:
            stage3.draw(canvas)

        #goal.draw(canvas)
        #enemy.draw(canvas)
        #enemy2.draw(canvas)
        #enemy3.draw(canvas)
        char.update()
        char.draw(canvas)
    
    
frame = simplegui.create_frame("Gravity", WIDTH, HEIGHT)
frame.set_draw_handler(draw_handler)
frame.set_keyup_handler(keyup_handler)
frame.set_keydown_handler(keydown_handler)
frame.set_mouseclick_handler(mouse_click)
frame.start()
