# A Gravity Journey by Anh Tran
# Ver 8
# Pitch sheet: https://www.dropbox.com/s/9w9kt91q2poq7yd/gravity_pitch_sheet.pdf?dl=0

# CodeSkulptor link: http://www.codeskulptor.org/#user40_caqRkp02OL_4.py

import simplegui
import random
import math

WIDTH = 800
HEIGHT = 600
started = False
howto = False
high_score = False
pause = False
end_game = False
name_entered = False
ghost_check = True

# Images and sprite sheets 
background = simplegui.load_image("https://i.imgur.com/sdfuQ6n.jpg")
tile = simplegui.load_image("https://i.imgur.com/3OWpBdz.png")
fading_tile = simplegui.load_image("https://i.imgur.com/PVUDDTX.png")
fire_trap = simplegui.load_image("http://i.imgur.com/XYMZwba.png")
reverse_fire = simplegui.load_image("https://i.imgur.com/iBwpsgi.png")
character = simplegui.load_image("https://i.imgur.com/XaMlNCf.png")
reverse_char = simplegui.load_image("https://i.imgur.com/jIePbKn.png")
needle_trap = simplegui.load_image("https://i.imgur.com/qIO2WTx.png")
needle_trap_2 = simplegui.load_image("https://i.imgur.com/NvHVydF.png")
enemy_image = simplegui.load_image("https://i.imgur.com/sRswcw1.png")
coin_image = simplegui.load_image("http://i.imgur.com/tjrkrQ7.png")
instructions = simplegui.load_image("https://i.imgur.com/I2oE64i.png")
back_button = simplegui.load_image("https://i.imgur.com/yX0qR9m.png")
hall_of_fame = simplegui.load_image("https://i.imgur.com/kHV9iIm.jpg")
door = simplegui.load_image("https://i.imgur.com/LTDnVZQ.png")
ghost_image = simplegui.load_image("https://i.imgur.com/dv9AV9m.png")
explosion_image = simplegui.load_image("https://i.imgur.com/Ja5TmQw.png")

sound_track = simplegui.load_sound("https://www.dropbox.com/s/i5ylmjzpa1qermj/267396_setuniman_hurry-1l50.ogg?dl=1")
foot_step = simplegui.load_sound("https://www.dropbox.com/s/a7r90i20iotauhn/234263__fewes__footsteps-wood.ogg?dl=1")
gravity_change = simplegui.load_sound("https://www.dropbox.com/s/hlxiq7zifgyj5xu/204452__ludist__necro-winde.mp3?dl=1")
coin_sound = simplegui.load_sound("https://www.dropbox.com/s/xvmjhgv8tq9hdw2/140382__d-w__coins-01.ogg?dl=1")
door_opened = simplegui.load_sound("https://www.dropbox.com/s/0vrb1uxnoxxetfy/275184__lennyboy__dooropened.ogg?dl=1")
explosion_sound = simplegui.load_sound("https://www.dropbox.com/s/yeptor14ief3l27/123235__dj-chronos__explosion-2.ogg?dl=1")
dead_sound = simplegui.load_sound("https://www.dropbox.com/s/edny7imkd7d45n0/319998_manuts_death-5.ogg?dl=1")
click_sound = simplegui.load_sound("https://www.dropbox.com/s/1a6co2hom5mlozr/39562_the-bizniss_mouse-click.ogg?dl=1")
win_sound = simplegui.load_sound("https://www.dropbox.com/s/10z51efez439k05/177120_rdholder_2dogsound-tadaa1-3s-2013jan31-cc-b.ogg?dl=1")

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

# Class for main character
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
        self.lives = 5
        self.points = 0
        self.dead = False
        self.dead_count = 0

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
        self.lives -= 1
        self.pos = [100, 460]
        camera.pos = [0, 0]
        camera.track = [100, 460]
        self.vel = [0, 0]
        self.check = 'Down'
        ghost.reset()
        foot_step.rewind()
        self.dead = False
        self.fly = False
        self.dead_count = 0
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
                    
    def update(self):
        global started, end_game
        if not self.dead:
            if self.lives < 1:
                self.level = 0
                self.reset()
                self.lives = 5
                stage1.reset()
                stage2.reset()
                end_game = True
                end.name = ""
                stage3.reset()
                stage4.reset()
                
            self.sound()
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
            camera.track[1] = self.pos[1] 
        
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
            else:
                grid = stage4.get_info()
    
            if self.pos[1] < 0 or self.pos[1] > 600:
                dead_sound.play()
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
                    elif grid[row + 1][column_check1] == 'T' and (row + 1) * 50 - self.pos[1] <= (self.draw_size[1] - 20)/2.0:
                        self.dead = True
                    elif grid[row + 1][column_check2] == 'T' and (row + 1) * 50 - self.pos[1] <= (self.draw_size[1] - 20)/2.0:
                        self.dead = True
                    elif grid[row + 1][column_check1] == 'N' and (row + 1) * 50 - self.pos[1] <= (self.draw_size[1] - 10)/2.0:
                        self.dead = True
                    elif grid[row + 1][column_check2] == 'N' and (row + 1) * 50 - self.pos[1] <= (self.draw_size[1] - 10)/2.0:
                        self.dead = True
                    else:
                        self.vel[1] += gravity_constant 
                    if column > 0:
                        if grid[row][column + 1] == 'W' and self.vel[0] > 0 and (column+1)*50 - camera.track[0] <= self.draw_size[0]/2.0:
                            self.vel[0] = 0
                        elif grid[row][column - 1] == 'W' and self.vel[0] < 0 and camera.track[0] - column * 50 <= self.draw_size[0]/2.0:
                            self.vel[0] = 0
                        elif grid[row][column + 1] == 'T' and self.vel[0] > 0 and (column+1)*50 - camera.track[0] <= (self.draw_size[0] - 10)/2.0:
                            self.dead = True
                        elif grid[row][column - 1] == 'T' and self.vel[0] < 0 and camera.track[0] - column * 50 <= (self.draw_size[0] - 10)/2.0:
                            self.dead = True
                        elif grid[row][column + 1] == 'N' and self.vel[0] > 0 and (column+1)*50 - camera.track[0] <= (self.draw_size[0] - 10)/2.0:
                            self.dead = True
                        elif grid[row][column - 1] == 'N' and self.vel[0] < 0 and camera.track[0] - column * 50 <= (self.draw_size[0] - 10)/2.0:
                            self.dead = True
                            
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
                    elif grid[row - 1][column_check1] == 'R' and self.pos[1] - row * 50 <= (self.draw_size[1] - 20)/2.0:
                        self.dead = True
                    elif grid[row - 1][column_check2] == 'R' and self.pos[1] - row * 50 <= (self.draw_size[1] - 20)/2.0:
                        self.dead = True                        
                    else:
                        self.vel[1] -= gravity_constant
                    if column > 0:
                        if grid[row][column + 1] == 'W' and self.vel[0] > 0 and (column+1)*50 - camera.track[0] <= self.draw_size[0]/2.0:
                            self.vel[0] = 0
                        elif grid[row][column - 1] == 'W' and self.vel[0] < 0 and camera.track[0] - column * 50 <= self.draw_size[0]/2.0:
                            self.vel[0] = 0
                        elif grid[row][column - 1] == 'R' and self.vel[0] < 0 and camera.track[0] - column * 50 <= (self.draw_size[0] - 10)/2.0:
                            self.dead = True
                        elif grid[row][column + 1] == 'R' and self.vel[0] > 0 and (column+1)*50 - camera.track[0] <= (self.draw_size[0] - 10)/2.0:
                            self.dead = True

        else:
            dead_sound.play()
            self.check = 'Down'
            self.fly = True
            self.dead_count = self.dead_count + 1
            if self.dead_count < 40:
                self.pos[1] -= 7/6.0
                self.pos[0] -= 5/6.0
            else:
                self.vel[1] += 2/6.0
                self.pos[1] += self.vel[1]
            if self.pos[1] > 600:
                self.reset()
                if self.level == 2:
                    stage3.soft_reset()
                elif self.level == 3:
                    stage4.soft_reset()
                            
    def reverse_gravity(self):
        if self.pos[1] > 40 and self.pos[1] < (600 - 40):
            if self.check == 'Down' and self.fly == False:
                self.vel[1] = 0
                self.check = 'Up'
            
            elif self.check == 'Up' and self.fly == False:
                self.vel[1] = 0
                self.check = 'Down'
    
    def move_right(self):
        self.vel[0] = 18.0/6.0
    
    def move_left(self):
        self.vel[0] = - 18.0 / 6.0
    
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
            gravity_change.play()
    
    def keyup_handler(self, key):
        if key == simplegui.KEY_MAP['left']:
            self.vel[0] = 0
            self.walk_left = False
            self.walk_track = 0
            
        elif key == simplegui.KEY_MAP['right']:
            self.vel[0] = 0
            self.walk_right = False
            self.walk_track = 0
            
    def sound(self):
        if self.fly:
            gravity_change.play()
            foot_step.rewind()
        else:
            gravity_change.rewind()
            if self.walk_left or self.walk_right:
                foot_step.play()
            else:
                foot_step.rewind()
                
    def collide(self, other_object):
        if dist(camera.track, other_object.get_position()) <= 45:
            self.dead = True
            return True
        else:
            return False

# Class for scroller
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
            
# Class for stage, where everything happens            
class Stage:
    def __init__(self, level_matrix, coin_group = set(), goal_group = set(), enemy_group = set()):
        self.level_info = level_matrix
        self.coin_count = 0
        self.needle_count = 0
        self.flame_count = 0
        self.enemy_group = enemy_group
        self.goal_group = goal_group
        self.coin_group = coin_group
        self.block_group = set()
        self.moving_group = set()
        for i in range(12):
            for j in range(len(self.level_info[1])):
                if self.level_info[i][j] == 'F':
                    block = Blocks([25 + 50 * j, 25 + 50 * i], fading_tile)
                    self.block_group.add(block)
                elif self.level_info[i][j] == 'C':
                    new_coin = Coin([25 + 50 * j, 25 + 50 * i], coin_image, [16, 16], [32, 32])
                    self.coin_group.add(new_coin)
                elif self.level_info[i][j] == 'B':
                    blink_block = Blocks([25 + 50 * j, 25 + 50 * i], tile, 'Blink')
                    self.block_group.add(blink_block)
                elif self.level_info[i][j] == 'M':
                    moving_block = Blocks([25 + 50 * j, 25 + 50 * i], tile, 'Moving', 'Right')
                    self.moving_group.add(moving_block)
                elif self.level_info[i][j] == 'H':
                    horizontal_enemy = Enemy([25 + 50 * j, 10 + 50 * i], enemy_image, [32, 32], [64, 64], 'horizontal')
                    self.enemy_group.add(horizontal_enemy)
                elif self.level_info[i][j] == 'V':
                    vertical_enemy = Enemy([25 + 50 * j, 10 + 50 * i], enemy_image, [32, 32], [64, 64], 'vertical')
                    self.enemy_group.add(vertical_enemy)
                elif self.level_info[i][j] == 'L':
                    moving_block = Blocks([25 + 50 * j, 25 + 50 * i], tile, 'Moving', 'Left')
                    self.moving_group.add(moving_block)
                    
    def reset(self):
        self.block_group = set()
        self.coin_group = set()
        self.moving_group = set()
        for i in range(12):
            for j in range(len(self.level_info[1])):
                if self.level_info[i][j] == 'F':
                    block = Blocks([25 + 50 * j, 25 + 50 * i], fading_tile)
                    self.block_group.add(block)
                elif self.level_info[i][j] == 'C':
                    new_coin = Coin([25 + 50 * j, 25 + 50 * i], coin_image, [16, 16], [32, 32])
                    self.coin_group.add(new_coin)
                elif self.level_info[i][j] == 'B':
                    blink_block = Blocks([25 + 50 * j, 25 + 50 * i], tile, 'Blink')
                    self.block_group.add(blink_block)
                elif self.level_info[i][j] == 'M':
                    moving_block = Blocks([25 + 50 * j, 25 + 50 * i], tile, 'Moving', 'Right')
                    self.moving_group.add(moving_block)
                elif self.level_info[i][j] == 'L':
                    moving_block = Blocks([25 + 50 * j, 25 + 50 * i], tile, 'Moving', 'Left')
                    self.moving_group.add(moving_block)
                    
    def soft_reset(self):
        self.moving_group = set()
        for i in range(12):
            for j in range(len(self.level_info[1])):
                if self.level_info[i][j] == 'M':
                    moving_block = Blocks([25 + 50 * j, 25 + 50 * i], tile, 'Moving', 'Right')
                    self.moving_group.add(moving_block)
                elif self.level_info[i][j] == 'L':
                    moving_block = Blocks([25 + 50 * j, 25 + 50 * i], tile, 'Moving', 'Left')
                    self.moving_group.add(moving_block)
        
    def draw(self, canvas):
        canvas.draw_image(background, [800, 600], [1600, 1200], [WIDTH/2, HEIGHT/2], [WIDTH, HEIGHT])
        for enemy in self.enemy_group:
            if enemy.track[0] > camera.pos[0] and enemy.track[0] < camera.pos[0] + 900:
                enemy.draw(canvas)
                char.collide(enemy)   
        for goal in self.goal_group:
            goal.draw(canvas)    
        for coin in self.coin_group:
            if coin.track[0] > camera.pos[0] and coin.track[0] < camera.pos[0] + 900:
                coin.draw(canvas)
                if coin.collide():
                    self.coin_group.discard(coin)
                    coin_sound.rewind()
                    coin_sound.play()
                    char.coins += 1
        for blockidx in self.block_group:
            if blockidx.track[0] > camera.pos[0] and blockidx.track[0] < camera.pos[0] + 900:
                blockidx.draw(canvas)
                if blockidx.collide() and blockidx.block_type == 'Fading':
                    self.block_group.discard(blockidx)            
        for moving_block in self.moving_group:
            moving_block.draw(canvas)
            moving_block.collide()
           
        self.coin_count = (self.coin_count + 1) % (8 * 10)
        self.needle_count = (self.needle_count + 1) % (2 * 8)
        self.flame_count = (self.flame_count + 1) % (7 * 13)
        
        for i in range(12):
            for j in range(camera.left_bound, camera.right_bound +2):
                if self.level_info[i][j] == 'W':
                    canvas.draw_image(tile, [125, 125], [250, 250], [camera.draw_pos[0]+ 50 * (j-camera.left_bound), 25 + 50 * i], [50, 50])                
                elif self.level_info[i][j] == 'T':
                    canvas.draw_image(fire_trap, [256/2 + (self.flame_count/7) * 256, 256/2], [256, 256], [camera.draw_pos[0]+ 50 * (j-camera.left_bound), 25 + 50 * i], [50, 50])
                elif self.level_info[i][j] == 'R':
                    canvas.draw_image(reverse_fire, [256/2 + (self.flame_count/7) * 256, 256/2], [256, 256], [camera.draw_pos[0]+ 50 * (j-camera.left_bound), 25 + 50 * i], [50, 50])
                elif self.level_info[i][j] == 'N':
                    if self.needle_count < 8:
                        canvas.draw_image(needle_trap, [369/2.0, 369/2.0], [369, 369], [camera.draw_pos[0]+ 50 * (j-camera.left_bound), 25 + 50 * i], [50, 50])
                    else:
                        canvas.draw_image(needle_trap_2, [369/2.0, 369/2.0], [369, 369], [camera.draw_pos[0]+ 50 * (j-camera.left_bound), 25 + 50 * i], [50, 50])             

        canvas.draw_text('x '+str(char.coins), [50, 50], 40, 'Red', 'sans-serif')
        canvas.draw_image(coin_image, [16, 16], [32, 32], [25, 40], [70, 70])
        canvas.draw_text('x '+str(char.lives), [700, 50], 40, 'Red', 'sans-serif')
        canvas.draw_image(character, [32 + 64 * 2, 32 + 64 * 14], [64, 64], [675, 35], [80, 80]) 
   
    def get_info(self):
        return self.level_info
    
# Class for monsters
class Enemy:
    def __init__(self, track, image, center, size, move_type, gravity_check = 'Down'):
        self.track = track
        self.image = image
        self.image_size = size
        self.image_center = center
        self.check = gravity_check 
        self.size = [60, 80]
        self.draw_size = [80, 80]
        self.draw_pos = [0, 0]
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
                                  self.draw_pos, self.draw_size)
            elif self.fly == True and self.walk_left == True:
                self.walk_track = (self.walk_track + 1) % (7 * 2)
                canvas.draw_image(self.reverse_image, [32 + (int)(self.walk_track/2) * 64, 19 * 64 + 32], self.image_size,
                                  self.draw_pos, self.draw_size)
            elif self.fly == True:
                self.fly_track = (self.fly_track + 1) % 7 
                canvas.draw_image(self.reverse_image, [32 + (int)(self.fly_track) * 64, 18 * 64 + 32], self.image_size,
                                  self.draw_pos, self.draw_size)
            elif self.walk_right == True:
                self.walk_track = (self.walk_track + 1) % 45
                canvas.draw_image(self.reverse_image, [32 + (int)(self.walk_track/5) * 64, 9 * 64 + 32], self.image_size,
                                  self.draw_pos, self.draw_size)
            elif self.walk_left == True:
                self.walk_track = (self.walk_track + 1) % 45
                canvas.draw_image(self.reverse_image, [32 + (int)(self.walk_track/5) * 64, 11 * 64 + 32], self.image_size,
                                  self.draw_pos, self.draw_size)
            else:
                canvas.draw_image(self.reverse_image, self.image_center, self.image_size, self.draw_pos, 
                              self.draw_size)
            
    
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

# Menu with options: How to play, High score, and Start game    
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
                             ' N N  N  N N N  NNN  N          ',
                             ' NNN N N N N N   N  N N         ',
                             ' N N  N   N N    N   N          ',
                             '                                ',
                             '                                ',
                             '               WCWCWCWWCCWCW    ',
                             '               WWWCWCWCWCWWW    ',
                             '               WCWCWCWWWCWCW    ',
                             '                                ',
                             '                                ',
                             '                                ']
        self.coin_count = 0
        self.needle_count = 0
        self.enemy_count = 0
        self.char_count = 0 
        self.start_button_horizontal = [4 * 25, 27 * 25]
        self.start_button_vertical = [2 * 25, 11 * 25]
        self.howto_button_horizontal = [1 * 25, 23 * 25]
        self.howto_button_vertical = [13 * 25, 16 * 25]
        self.high_button_horizontal = [15 * 25, 28 * 25]
        self.high_button_vertical = [18 * 25, 21 * 25]
        
    def draw(self, canvas): 
        self.coin_count = (self.coin_count + 1) % (8 * 10)
        self.needle_count = (self.needle_count + 1) % (2 * 9)
        self.enemy_count = (self.enemy_count + 1) % (10 * 6)
        self.char_count = (self.char_count + 1) % (10 * 9)
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
        canvas.draw_image(ghost_image, [32 + (self.enemy_count / 10) * 64, 32 + 15 * 64], [64, 64], [10 * 25, 9 * 25], [50, 50])
        canvas.draw_image(character, [32 + (self.char_count / 10) * 64, 32 + 10 * 64], [64, 64], [15 * 25, 25], [50, 50])
        
    def click(self, pos):
        global started, howto, high_score
        if started == False and howto == False and high_score == False:
            if pos[0] > self.start_button_horizontal[0] and pos[0] < self.start_button_horizontal[1]:
                if pos[1] > self.start_button_vertical[0] and pos[1] < self.start_button_vertical[1]:
                    click_sound.play()
                    started = True
                    char.level = 0
                    char.coins = 0            
            if pos[0] > self.howto_button_horizontal[0] and pos[0] < self.howto_button_horizontal[1]:
                if pos[1] > self.howto_button_vertical[0] and pos[1] < self.howto_button_vertical[1]:
                    click_sound.play()
                    howto = True                    
            if pos[0] > self.high_button_horizontal[0] and pos[0] < self.high_button_horizontal[1]:
                if pos[1] > self.high_button_vertical[0] and pos[1] < self.high_button_vertical[1]:
                    click_sound.play()
                    high_score = True
                                       
# How to play
class Instructions:
    def __init__(self):
        self.button_horizontal = [600, 600 + 113]
        self.button_vertical = [50, 50 + 83]
        self.button_pos = [(self.button_horizontal[0] + self.button_horizontal[1]) / 2.0,
                           (self.button_vertical[0] + self.button_vertical[1]) / 2.0]
        self.button_width = self.button_horizontal[1] - self.button_horizontal[0]
        self.button_height = self.button_vertical[1] - self.button_vertical[0]
        
    def draw(self, canvas):
        canvas.draw_image(instructions, [1067/2.0, 300], [1067, 600], [WIDTH/2, HEIGHT/2], [WIDTH, HEIGHT])
        canvas.draw_image(back_button, [113/2.0, 83/2.0], [113, 83], self.button_pos, 
                          [self.button_width, self.button_height])
        
    def click(self, pos):
        global howto
        if pos[0] > self.button_horizontal[0] and pos[0] < self.button_horizontal[1]:
            if pos[1] > self.button_vertical[0] and pos[1] < self.button_vertical[1]:
                howto = False                
# High score                
class Hall_of_fame:
    def __init__(self):
        self.splash_screen= ['                                ',
                             '                                ',
                             ' W W WWW W   W    WWW WWW       ',
                             ' W W W W W   W    W W W         ',
                             ' WWW WWW W   W    W W WWW       ',
                             ' W W W W W   W    W W W         ',
                             ' W W W W WWW WWW  WWW W         ',
                             '                                ',
                             '           WWW WWW W   W WWW    ',
                             '           W   W W WW WW W      ',
                             '           WWW WWW W W W WW     ',
                             '           W   W W W   W W      ',
                             '           W   W W W   W WWW    ',
                             '                                ',
                             '                                ',
                             '                                ',
                             '                                ',
                             '                                ',
                             '                                ',
                             '                                ',
                             '                                ',
                             '                                ',
                             '                                ',
                             '                                ']
        self.names = {}
        self.scores = []
        self.button_horizontal = [650, 650 + 113]
        self.button_vertical = [25, 25 + 83]
        self.button_pos = [(self.button_horizontal[0] + self.button_horizontal[1]) / 2.0,
                           (self.button_vertical[0] + self.button_vertical[1]) / 2.0]
        self.button_width = self.button_horizontal[1] - self.button_horizontal[0]
        self.button_height = self.button_vertical[1] - self.button_vertical[0]
        self.count = 1
        
    def draw(self, canvas):
        canvas.draw_image(background, [800, 600], [1600, 1200], [WIDTH/2, HEIGHT/2], [WIDTH, HEIGHT])
        canvas.draw_image(back_button, [113/2.0, 83/2.0], [113, 83], self.button_pos, 
                          [self.button_width, self.button_height])
        for i in range(24):
            for j in range(31):
                if self.splash_screen[i][j] == 'W':
                    canvas.draw_image(tile, [125, 125], [250, 250], [12.5 + 25 * j, 12.5 + 25 * i], [25, 25])            
        self.count = 0
        self.scores.sort(reverse = True)
        for score in self.scores:
            self.count += 1
            canvas.draw_text(str(self.count) + '. ' + self.names[score], 
                             [4 * 25, (14 + self.count) * 25], 20, 'Black', 'sans-serif') 
            canvas.draw_text(str(score), [20 * 25, (14 + self.count) * 25], 20, 
                             'Black', 'sans-serif')   
    def click(self, pos):
        global high_score
        if pos[0] > self.button_horizontal[0] and pos[0] < self.button_horizontal[1]:
            if pos[1] > self.button_vertical[0] and pos[1] < self.button_vertical[1]:
                high_score = False
                click_sound.play()

# The goal of each stage
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
        global pause
        self.update()
        if self.collide():
            win_sound.play()
            door_opened.play()
            self.count = (self.count + 1) % (3 * 10)
            canvas.draw_image(self.image, [32 + 4 * 64, 32 + (int)(self.count/10) * 64], self.image_size, 
                              self.draw_pos, self.draw_size)
            char.coins += 1
            coin_sound.rewind()
            coin_sound.play()
            if self.count == 2 * 10 + 2:
                if char.level < 3:
                    char.level += 1
                    char.reset()
                    char.lives += 1
                    pause = False
                else:
                    end_game = True
                    end.name = ""
                self.count = 0    
        else:
            canvas.draw_image(self.image, [32 + 4 * 64, 32], self.image_size, 
                              self.draw_pos, self.draw_size)
# Obtainable objects            
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

# Class for fading blocks, moving blocks, blinking blocks
class Blocks:
    def __init__(self, track, image, block_type = 'Fading', move_type = 'Left'):
        self.track = track
        self.image = image
        self.image_size = [250, 250]
        self.draw_pos = [0, 0]
        self.fade_count = 0
        self.draw_size = [50, 50]
        self.horizontal = [self.track[0] - 25, self.track[0] + 25]
        self.vertical = [self.track[1] - 25, self.track[1] + 25]
        self.char_size = [50, 80]
        self.block_type = block_type
        self.move_counter = 0
        self.vel = [0, 0]
        self.move_type = move_type
        
    def move_left(self):
        self.vel[0] = - 14/ 6.0
    
    def move_right(self):
        self.vel[0] = 14/ 6.0
        
    def update(self):
        self.draw_pos[1] = self.track[1]
        self.draw_pos[0] = self.track[0] - camera.pos[0]
        if self.block_type == 'Moving':
            self.move_counter = (self.move_counter + 1) % 940
            if self.move_counter < 470:
                if self.move_type == 'Left':
                    self.move_left()
                else:
                    self.move_right()
            else:
                if self.move_type == 'Left':
                    self.move_right()
                else:
                    self.move_left()        
            self.track[0] += self.vel[0]
            self.horizontal = [self.track[0] - 25, self.track[0] + 25]
            self.vertical = [self.track[1] - 25, self.track[1] + 25]
        
    def collide(self):
        left_check = camera.track[0] - self.char_size[0]/2.0 
        right_check = camera.track[0] + self.char_size[0]/2.0
        up_check = camera.track[1] - self.char_size[1]/2.0
        down_check = camera.track[1] + self.char_size[1]/2.0
        if char.check == 'Down':
            if left_check > self.horizontal[0] - self.char_size[0] + 5 and right_check < self.horizontal[1] + self.char_size[0] - 5:
                if down_check >= self.vertical[0] and up_check < self.vertical[0]:
                    char.vel[1] = 0
                    char.pos[1] = self.vertical[0] - self.char_size[1]/2.0
                    char.fly = False
                    char.fly_track = 0
                    return True
            if self.block_type != 'Moving':    
                if (up_check < self.vertical[1] and down_check > self.vertical[1]) or (down_check > self.vertical[0] and up_check < self.vertical[0]):
                    if char.vel[0] < 0 and left_check <= self.horizontal[1] and right_check >= self.horizontal[1]:
                        char.vel[0] = 0
                    elif char.vel[0] > 0 and right_check >= self.horizontal[0] and left_check <= self.horizontal[0]:
                        char.vel[0] = 0
                    
        elif char.check == 'Up':
            if left_check > self.horizontal[0] - self.char_size[0] + 5 and right_check < self.horizontal[1] + self.char_size[0] - 5:
                if up_check <= self.vertical[1] and down_check > self.vertical[1]:
                    char.vel[1] = 0
                    char.pos[1] = self.vertical[1] + self.char_size[1] / 2.0
                    char.fly = False
                    char.fly_track = 0
                    return True    
            if self.block_type != 'Moving':    
                if (up_check < self.vertical[1] and down_check > self.vertical[1]) or (down_check > self.vertical[0] and up_check < self.vertical[0]):
                    if char.vel[0] < 0 and left_check <= self.horizontal[1] and right_check >= self.horizontal[1]:
                        char.vel[0] = 0
                    elif char.vel[0] > 0 and right_check >= self.horizontal[0] and left_check <= self.horizontal[0]:
                        char.vel[0] = 0
                
    def draw(self, canvas):
        self.update()
        if self.block_type == 'Blink':
            if dist(self.track, camera.track) <= 120:
                canvas.draw_image(self.image, [125, 125], self.image_size, 
                          self.draw_pos, self.draw_size)
        else:
            canvas.draw_image(self.image, [125, 125], self.image_size, 
                              self.draw_pos, self.draw_size)

# Chasing ghost    
class Ghost:
    def __init__(self, track, image, explosion_image):
        self.track = track 
        self.image = image
        self.image_size = [64, 64]
        self.draw_size = [80, 80]
        self.draw_pos = [0, 0]
        self.degree = 0
        self.count = 0
        self.boom = False
        self.expimg = explosion_image
        
    def reset(self):
        self.track = [0, 0]
        self.count = 0
        
    def update(self):
        self.degree = math.atan2((camera.track[0] - self.track[0]), (camera.track[1] - self.track[1]))
        self.track[0] += (2 + 0.1 * char.level) * math.sin(self.degree)
        self.track[1] += (2 + 0.1 * char.level) * math.cos(self.degree)
        self.draw_pos[1] = self.track[1]
        self.draw_pos[0] = self.track[0] - camera.pos[0]
        
    def collide(self):
        if not self.boom:
            if dist(self.track, camera.track) <= 45:
                return True
            return False
        else:
            if dist(self.track, camera.track) <= 105:
                return True
            return False
    
    def draw(self, canvas):
        self.update()
        self.count = (self.count + 1) % (8 * 7 + 48 * 2 + 8 * 7)
        if self.count < 8 * 7:
            self.boom = False
            if math.sin(self.degree) >= 0:
                canvas.draw_image(self.image, [32 + 64 * (self.count / 8), 32 + 3 * 64], self.image_size, 
                            self.draw_pos, self.draw_size)
            else:
                canvas.draw_image(self.image, [32 + 64 * (self.count/8), 32 + 1 * 64], self.image_size,
                              self.draw_pos, self.draw_size)
                
        elif self.count < 2 * 8 * 7:
            self.boom = False
            explosion_sound.rewind()
            explosion_sound.play()
            canvas.draw_image(self.image, [32 + 64 * ((self.count - 8 * 7)/8), 32 + 2 * 64], self.image_size,
                              self.draw_pos, self.draw_size)
            
        else:
            if self.count > 2 * 8 * 7 + 15 * 2 and self.count < 2 * 8 * 7 + (48 - 10) * 2:
                self.boom = True    
            canvas.draw_image(self.expimg, [256/2 + 256 * ((self.count - 2 * 8 * 7)/2), 256/2], [256, 256],
                              self.draw_pos, [320, 320])
            
class Pause:
    def __init__(self):
        self.splash_screen= ['                                ',
                             'WWW WWW W  W WWW W W  W W W WWW ',
                             'W   W W WW W  W  W WW W W W W   ',
                             'W   W W W WW  W  W W WW W W WW  ',
                             'W   W W W  W  W  W W  W W W W   ',
                             'WWW WWW W  W  W  W W  W WWW WWW ',
                             '                                ',
                             '               WWW              ',
                             '                 W              ',
                             '                WW              ',
                             '                W               ',
                             '                                ',
                             '                W               ',
                             '       WWWWWW       WWWWWW      ',
                             '       W    W       W    W      ',
                             '       W    W       W    W      ',
                             '       W    W       W    W      ',
                             '       W    W       W    W      ',
                             '       WWWWWW       WWWWWW      ',
                             '                                ',
                             '     C C CC  CC     TT T TTT    ',
                             '      C  C   C      T TT T T    ',
                             '      C  CC CC      T  T TTT    ',
                             '                                ']
        self.coin_count = 0
        self.flame_count = 0
        self.yes_horizontal = [7 * 25, (7 + 6) * 25]
        self.yes_vertical = [13 * 25, 19 * 25]
        self.no_horizontal = [20 * 25, 26 * 25]
        self.no_vertical = [13 * 25, 19 * 25]
        
    def draw(self, canvas): 
        self.coin_count = (self.coin_count + 1) % (8 * 10)
        self.flame_count = (self.flame_count + 1) % (7 * 13)
        canvas.draw_image(background, [800, 600], [1600, 1200], [WIDTH/2, HEIGHT/2], [WIDTH, HEIGHT])
        for i in range(24):
            for j in range(31):
                if self.splash_screen[i][j] == 'W':
                    canvas.draw_image(tile, [125, 125], [250, 250], [12.5 + 25 * j, 12.5 + 25 * i], [25, 25])
                elif self.splash_screen[i][j] == 'T':
                    canvas.draw_image(fire_trap, [256/2 + (self.flame_count/7) * 256, 256/2], [256, 256], [12.5 + 25 * j, 12.5 + 25 * i], [25, 25])
                elif self.splash_screen[i][j] == 'C':
                    canvas.draw_image(coin_image, [16, 16 + (self.coin_count / 10) * 32], [32, 32], [12.5 + 25 * j, 12.5 + 25 * i], [38, 38])            
        canvas.draw_image(character, [32 + 2 * 64, 32 + 20 * 64], [64, 64], [10 * 25, 16 * 25], [80, 80])
        canvas.draw_image(character, [32 + 5 * 64, 32 + 20 * 64], [64, 64], [23 * 25, 16 * 25], [80, 80])
                    
    def click(self, pos):
        global started, pause
        if pos[0] > self.yes_horizontal[0] and pos[0] < self.yes_horizontal[1]:
            if pos[1] > self.yes_vertical[0] and pos[1] < self.yes_vertical[1]:
                click_sound.play()
                pause = False        
        elif pos[0] > self.no_horizontal[0] and pos[0] < self.no_horizontal[1]:
            if pos[1] > self.no_vertical[0] and pos[1] < self.no_vertical[1]:
                click_sound.play()
                pause = False
                started = False
                char.reset()
                char.lives = 5
                
class Endgame:
    def __init__(self):
        self.name = ""
        self.splash_screen= ['                                ',
                             '  WWWW  WWW W   W WWW           ',
                             '  W     W W WW WW W             ',
                             '  W  WW WWW W W W WW            ',
                             '  W   W W W W   W W             ',
                             '  WWWWW W W W   W WWW           ',
                             '                                ',
                             '          WWW W WW WWW WWW  W   ',
                             '          W W W W  W   W W  W   ',
                             '          W W W W  WW  WW   W   ',
                             '          W W W W  W   W W      ',
                             '          WWW  W   WWW W W  W   ',
                             '                                ',
                             '                                ',
                             '                                ',
                             '                                ',
                             '                                ',
                             '                                ',
                             '                                ',
                             '                                ',
                             '                                ',
                             '                                ',
                             '                                ',
                             '                                ']        
    def draw(self, canvas):
        canvas.draw_image(background, [800, 600], [1600, 1200], [WIDTH/2, HEIGHT/2], [WIDTH, HEIGHT])
        for i in range(24):
            for j in range(31):
                if self.splash_screen[i][j] == 'W':
                    canvas.draw_image(tile, [125, 125], [250, 250], [12.5 + 25 * j, 12.5 + 25 * i], [25, 25])
                    
        if not name_entered:
            canvas.draw_text('Enter your name: ', [8 * 25, 16 * 25], 25, 'Black', 'sans-serif')
            canvas.draw_text(self.name, [16 * 25, 16 * 25], 25, 'Black', 'sans-serif')
            canvas.draw_text('Press "Enter" when you are done', [10 * 25, 19 * 25], 20, 'Black', 'sans-serif')
        else:
            canvas.draw_text('Click anywhere to get out!', [10 * 25, 16 * 25], 20, 'Black', 'sans-serif')
        
    def key_handler(self, key):
        global name_entered
        if not name_entered:
            if key > 47 and key < 91:
                self.name += chr(key)
            elif key == 13:
                name_entered = True
                hall.names[char.coins] = self.name
                hall.scores.append(char.coins)
    
    def click(self, pos):
        global started, end_game, name_entered
        if pos[0] > 0 and pos[0] < 800 and pos[1] > 0 and pos[1] < 600:
            click_sound.play()
            started = False
            end_game = False
            name_entered = False

class Loop_track:
    def __init__(self, sound):
        self.sound = sound

    def update(self):
        self.sound.play()      
        
# Stage 1
level1_matrix = ['WWWWWWWWWWW WWWWW  WWWWWWWWWWWWWWWWWWWWWWWWWW  WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
                 'WWWWWWWWWWW WWWWW  WWWCCCCCWWWWWWWWWWWWWWWWWW  WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
                 'W    W W     WWW     WCCCCCW     RRR           CCCC           WCWWWWWWWWWWWWWWWWWWWWWW',
                 'W                     WFWWF                                   WCW            WWWWWWWWW',
                 'W                                                                            WWWWWWWWW',
                 'W                                                                            WWWWWWWWW',
                 'W              CCCC                                                          WWWWWWWWW',
                 'W                                V     CCC       V                           WWWWWWWWW',
                 'W       V WWW                         WCW                                    WWWWWWWWW',
                 'W         WWW     TT  H      NNN      WWW                 CCCCC H            WWWWWWWWW',
                 'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW  WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
                 'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW  WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW']

# Stage 2
level2_matrix = ['WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW                     WWWWWWWWWWWWWWWWWWW       F    F    F   W     WWWW FFF  FFFF  WWWW    WWWWWWWWWWWWWWWWW',
                 'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW                     WWWWWWW  WWWWWWW    WW  WC  WWC WWC  WWC                CC           WWWWWWWWWWWWWWWWW',
                 'WWWWWWWWWWWWWWWW                   WW  WW  WW  WW W                       CC      C       CC       CCCCC                               WWWWW',
                 'W             WW                                                                               WWWWWWFFWWWWWWWWWFWWWWWWW               WWWWW',
                 'W             WW         CCC                                                    CCC              RRRR  RR  RR   R  RRR      WWW        WWWWW',
                 'W                        FFF                                WWW             WW  FFF  FF WW FF                                          WWWWW',
                 'W                                        CCCC               WCW    V                 CC CC             CCCC    CCCC                    WWWWW',
                 'W        WWW                                                WCW                                    CCCC    CCCC    CCCC                WWWWW',
                 'W       V                        V  WWFFWWW VFWF VWWW                                                                      CCCC        WWWWW',
                 'W       NNNNNN          HCC                                      CC                       CCC   NN   NN  NNN  N  NN   NN   TTTT        WWWWW',
                 'WWWWWWWWWWWWWWWWWWWTTTTWWWWWWWWWW                    WWWWWW      CC     WW   WW  CCW   W  FFF   WWWWWWWWWWWWWWWWWWWWWWWW   WWWW        WWWWW',
                 'WWWWWWWW     WWWWWWWWWWWWWWW         W   W  W   W   W  WWWW    WWWWFFWW          FFW    W                                  WWWWWWWWWWWWWWWWW']

# Stage 3
level3_matrix = ['WWWWWWWWWWWFFFWWWWWWWW                                                           WWWWFFMM                                WWWW',
                 'WWWWWCCCCCCCCCCCCCCWWW                      LLL                  FFFFBBBB         CCCCC                                  WWWW',
                 'W   WCCCCCCCCCCCCCCW      CCCCC CCCC CCCCC                                                                CC             WWWW',
                 'W    WFWWFFWWWWWWWF       V    V    V     V                                                               CC             WWWW',
                 'W                                                                                                         CC             WWWW',
                 'W                                                                                                                        WWWW',
                 'W                                                                    B                W                                  WWWW',
                 'W                                                                    B                W                                  WWWW',
                 'W                        CCCC CCCC CCCC CCCC  MMMM                                    W                                  WWWW',
                 'W                       VWWWWVWWWWVWFFWVWWWWFF                                          LLL                 WWWWWWWWWWWWWWWWW',
                 'WWWWWWWWWWWWWWWWWWWWWWW                                                                                                  WWWW',
                 'W                                                                                                                        WWWW']
                 
# Stage 4
level4_matrix = ['WW                    WWWWWWFFFFF                         WWWWWWWWWWWWWWWWWWWWWWWWWWWW                        B                WWWWWW',
                 'WW                       CCCCCC                           WWWWWWWWW WWWWW WWWWW WWWW                                  LLL      WWWWWW',
                 'WWMMMM                                                    WWWWWWWWW WWWWW WWWWW WWWW FFFFFFFFFFFFFFFF   FFFF  B                WWWWWW',
                 'WW                       CCCC                             WWW      VCCCCCVCCCCCVCCCCV                         B                WWWWWW',
                 'WW                         CCCC                           WWW                                                 B                WWWWWW',
                 '                                                          WWW      V     V     V    V                                          WWWWWW',
                 '                                                  LLLLLLL                                                                      WWWWWW',
                 '                                                                                                              B                WWWWWW',
                 '                                                                                                              B           BB   WWWWWW',
                 '                      BBBBBBBBBBBB                                   NN    NN    N       FFFFFFFFFFFFFF FFFFFFF                WWWWWW',
                 'WWWWTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT                          LLL                                         WWWWWW',
                 'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW            WW    WW    W                                             WWWWWW']
    
# Initialize character
char = Character([150, 460], 100, character, reverse_char, [32, 32 + 64 * 6], [64, 64])

# Goal for the first stage
goal = Door([71 * 50 + 25, 460], door, [32, 32], [64, 64])
goal_group = set([goal])
# Goal for the second stage
goal2 = Door([133 * 50 + 25, 510], door, [32, 32], [64, 64])
goal_group2 = set([goal2])
# Goal for third stage
goal3 = Door([118 * 50, 410], door, [32, 32], [64, 64])
goal_group3 = set([goal3])
# Goal for the last stage
goal4 = Door([126 * 50, 360], door, [32, 32], [64, 64])
goal_group4 = set([goal4])

camera = Camera()
menu = Menu()
instruct = Instructions()
hall = Hall_of_fame()
pause_menu = Pause()
end = Endgame()
ghost = Ghost([0, 0], ghost_image, explosion_image)
track = Loop_track(sound_track)

# Initialize the stages
stage1 = Stage(level1_matrix, set(), goal_group, set())
stage2 = Stage(level2_matrix, set(), goal_group2, set())
stage3 = Stage(level3_matrix, set(), goal_group3, set())
stage4 = Stage(level4_matrix, set(), goal_group4, set())

def keyup_handler(key):
    char.keyup_handler(key)
    
def keydown_handler(key):
    if not end_game:
        char.keydown_handler(key)   
    else:
        end.key_handler(key)
    
def mouse_click(pos):
    if not started and not howto and not high_score:
        menu.click(pos)
    elif not started and howto:
        instruct.click(pos)
    elif not started and high_score:
        hall.click(pos)
    else:
        if pause:
            pause_menu.click(pos)
        elif end_game:
            end.click(pos)
            
def button_handler():
    global started, pause
    if started == True and pause == False:
        pause = True
        
def level_button():
    global pause
    char.level = (char.level + 1) % 4
    char.reset()
    char.coins = 0
    char.lives += 1
    pause = False
    stage1.reset()
    stage2.reset()
    stage3.reset()
    stage4.reset()
    
def ghost_turn():
    global ghost_check
    if ghost_check:
        ghost_check = False
    else:
        ghost_check = True
    
def draw_handler(canvas):
    global stage1, stage2
    track.update()
    if not started:
        if howto == False and high_score == False:
            menu.draw(canvas)
        elif howto == True:
            instruct.draw(canvas)
        else:
            hall.draw(canvas)
        
    else:
        if pause:
            pause_menu.draw(canvas)
        elif end_game:
            end.draw(canvas)
        else:
            camera.update()
            if char.get_level() == 0:
                stage1.draw(canvas)
            elif char.get_level() == 1:
                stage2.draw(canvas)
            elif char.get_level() == 2:
                stage3.draw(canvas)
            else:
                stage4.draw(canvas)
            char.update()
            if not char.dead:
                char.draw(canvas)
            else:
                if char.dead_count % 2 == 0:
                    char.draw(canvas)
            if ghost_check:
                ghost.draw(canvas)
                if ghost.collide():
                    char.dead = True
    
frame = simplegui.create_frame("Gravity", WIDTH, HEIGHT)
frame.set_draw_handler(draw_handler)
frame.set_keyup_handler(keyup_handler)
frame.set_keydown_handler(keydown_handler)
frame.set_mouseclick_handler(mouse_click)
button = frame.add_button('PAUSE', button_handler)
button2 = frame.add_button('Next Level', level_button)
button3 = frame.add_button('Ghost on/off', ghost_turn)
frame.start()
