import arcade.key
from codetect import spritecollide, collision
from MapReader import reader

MAP = ['maps/map1.txt',
       'maps/map2.txt',
       'maps/map3.txt',
       'maps/map4.txt',
       'maps/map5.txt']
TOTAL_MAP = len(MAP)
GRAVITY = 1

class Player:
    JUMPING_VELOCITY = 15
    def __init__(self, world, x, y, stage, block_size):
        self.world = world
        self.stage = stage
        self.block_size = block_size
        self.width = block_size
        self.height = block_size * 2
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.life = 3
        self.kill = 0

        self.turn = 0 # 0-right 1-left
        self.jump_status = 0
        
    def jump(self):
        self.vy = Player.JUMPING_VELOCITY
        self.jump_status += 1

    def check_turn(self):
        if self.vx > 0:
            self.turn = 0
        elif self.vx < 0:
            self.turn = 1

    def hit_slime(self):
        slime_list = []
        for slime in self.world.slime:
            slime_list.append((slime.x,slime.y))
        slime_hit_list = spritecollide(self.x, self.y ,self.height, self.block_size, slime_list)
        if slime_hit_list != []:
            return True

    def hit_kingslime(self):
        for kingslime in self.world.kingslime:
            if collision(self.x, self.y, self.width, self.height, kingslime.x, kingslime.y, kingslime.width - 60, kingslime.height - 60):
                return True
        
    def hit_checkpoint(self):
        for checkpoint in self.world.checkpoint:
            if collision(self.x, self.y, 40, 80, checkpoint.x, checkpoint.y, 40, 80):
                self.world.spawnpoint = [checkpoint.map, checkpoint.x, checkpoint.y]
                checkpoint.delete()
            
    def dead(self):
        self.world.time = 1

    def move_out_of_block(self, block_hit_list):
        for block_x, block_y in block_hit_list:
            if self.y > block_y + self.block_size:
                if self.vy < 0:
                    if not (block_x + self.block_size == self.x or block_x - self.block_size == self.x):
                        self.y = block_y + (self.block_size * 3 / 2)
                        self.vy = 0
                        self.jump_status = 0
            elif self.y < block_y - self.block_size:
                if self.vy > 0:
                    self.y = block_y - (self.block_size * 3 / 2)
                    self.vy = 0
            elif self.x > block_x:
                if self.vx <= 0:
                    self.x = block_x + (self.block_size)
            elif self.x < block_x:
                if self.vx >= 0:
                    self.x = block_x - (self.block_size)

    def change_map(self):
        if self.world.currentmap != TOTAL_MAP - 1:
            if self.x > 800:
                self.world.currentmap += 1
                self.turn = 0
                if self.world.currentmap == TOTAL_MAP:
                    self.world.currentmap = 0
                self.world.change_map(MAP[self.world.currentmap])
                self.x = 0
        else:
            if self.x >= 780:
                self.x = 780

##        if self.world.currentmap == 0:
        if self.x <= 20:
            self.x = 20

##        else:
##            if self.x < 0:
##                self.world.currentmap -= 1
##                self.turn = 1
##                if self.world.currentmap == -1:
##                    self.world.currentmap = TOTAL_MAP - 1
##                self.world.change_map(MAP[self.world.currentmap])
##                self.x = 800

            

    def update(self, delta):
        self.x += self.vx
        self.y += self.vy
        if self.vy != -10:
            self.vy -= GRAVITY
        self.change_map()
        self.check_turn()
        self.hit_checkpoint()

        block_hit_list = spritecollide(self.x, self.y ,self.height, self.block_size, self.stage.block_list)
        self.move_out_of_block(block_hit_list)
        if self.hit_slime():
            self.life -= 1
            self.dead()
        if self.hit_kingslime():
            self.life -= 1
            self.dead()
        if self.y <= -100:
            self.life -= 1
            self.dead()
        
            



class Bullet:
    def __init__(self, world):
        self.world = world
        self.player = self.world.player
        self.bullet_width = 6
        self.bullet_height = 3
        self.vx = self.get_direction()
            
    def get_direction(self):
        if self.player.turn == 0:
            self.x = self.player.x + (self.player.block_size / 2)
            self.y = self.player.y - 2
            self.vx = 7
        if self.player.turn == 1:
            self.x = self.player.x - (self.player.block_size / 2)
            self.y = self.player.y - 2
            self.vx = -7
        return self.vx

    def hit_block(self):
        for block_x, block_y in self.world.stage.block_list:
            if block_x - (self.world.block_size / 2) <= self.x + (self.bullet_width / 2) <= block_x + (self.world.block_size / 2):
                if block_y - (self.world.block_size / 2) <= self.y + (self.bullet_height / 2) <= block_y + (self.world.block_size / 2) or block_y - (self.world.block_size / 2) <= self.y - (self.bullet_height / 2) <= block_y + (self.world.block_size / 2):
                   return True                
        return False

    def hit_slime(self):
        for slime in self.world.slime:
            if slime.x - (self.world.block_size / 2) <= self.x + (self.bullet_width / 2) <= slime.x + (self.world.block_size / 2):
                if slime.y - (self.world.block_size / 2) <= self.y + (self.bullet_height / 2) <= slime.y + (self.world.block_size / 2) or slime.y - (self.world.block_size / 2) <= self.y + (self.bullet_height / 2) <= slime.y + (self.world.block_size / 2):
                   slime.health -= 10
                   if slime.health == 0:
                       self.player.kill += 1
                       self.world.slime.remove(slime)
                   return True
        return False

    def hit_kingslime(self):
        for kingslime in self.world.kingslime:
            if collision(self.x ,self.y, self.bullet_width, self.bullet_height, kingslime.x, kingslime.y, kingslime.width, kingslime.height):
                kingslime.health -= 10
                if kingslime.health == 0:
                    self.player.kill += 50
                    self.world.kingslime.remove(kingslime)
                    self.world.time = 2
                return True
            
    def delete(self):
        self.world.bullet.remove(self)
        
    def update(self, delta):
        self.x += self.vx
        if self.x > self.world.width + 10 or self.x < - 10:
            self.delete()
        if self.hit_block():
            self.delete()
        if self.hit_slime():
            self.delete()
        if self.hit_kingslime():
            self.delete()
            

        
class Slime:
    def __init__(self, world, x, y, stage, player, block_size):
        self.world = world
        self.stage = stage
        self.player = player
        self.block_size = block_size
        self.height = self.block_size
        self.x = x
        self.y = y
        self.vx = -1.5
        self.vy = 0
        self.health = 20
        self.MAX_HEALTH = 20

    def move_out_of_block(self, block_hit_list):
        for block_x, block_y in block_hit_list:
            if self.y > block_y:
                if self.vy < 0:
                    self.y = block_y + (self.block_size)
                    self.vy = 0
            elif self.y < block_y:
                if self.vy > 0:
                    self.y = block_y - (self.block_size)
                    self.vy = 0
            elif self.x > block_x:
                if self.vx < 0:
                    self.x = block_x + (self.block_size)
                    self.vx = -self.vx
            elif self.x < block_x:
                if self.vx > 0:
                    self.x = block_x - (self.block_size)
                    self.vx = -self.vx

    def update(self, delta):
        self.x += self.vx
        self.y += self.vy
        self.vy -= GRAVITY
        
        block_hit_list = spritecollide(self.x, self.y ,self.height, self.block_size, self.stage.block_list)
        self.move_out_of_block(block_hit_list)

    def delete(self):
        self.world.slime.remove(self)


class Kingslime:
    def __init__(self, world, x, y, block_size):
        self.DELAY = 125
        self.world = world
        self.player = self.world.player
        self.stage = self.world.stage
        self.block_size = block_size
        self.width = 160
        self.height = 160
        self.x = x
        self.y = y
        self.vx = 1.5
        self.vy = 0
        self.health = 500
        self.MAX_HEALTH = 500
        self.timer = 0

    def move_out_of_block(self, block_hit_list):
        if self.x - (self.width // 2) <= 0:
            self.x = (self.width // 2)
            
        if self.x + (self.width // 2) >= 800:
            self.x = 800 - (self.width // 2)
            
        for block_x, block_y in block_hit_list:
            if self.y > block_y:
                if self.vy < 0:
                    self.y = block_y + (self.block_size // 2) + (self.height // 2)
                    self.vy = 0
                    if self.player.x >= self.x:
                        self.vx = 1.5
                    else:
                        self.vx = -1.5

    def jump(self):
        JUMPING_VELOCITY = 30
        self.vy = JUMPING_VELOCITY
        self.vx = 5
        if self.player.x < self.x:
            self.vx = -5
        else:
            self.vx = 5
        

    def update(self, delta):
        if self.timer != self.DELAY:
            self.timer += 1
        else:
            self.timer = 0
            self.jump()
     
        if self.vx == 1.5 or self.vx == -1.5:
            if self.player.x < self.x:
                self.vx = -1.5
            else:
                self.vx = 1.5
            self.x += self.vx
        else:
            self.x += self.vx
                
        self.y += self.vy
        self.vy -= GRAVITY
        
        block_hit_list = spritecollide(self.x, self.y ,self.height, self.block_size, self.stage.block_list)
        self.move_out_of_block(block_hit_list)

    def dead(self):
        if self.health == 0:
            return True

    def delete(self):
        self.world.kingslime.remove(self)


class Checkpoint:
    def __init__(self, world, Map, x, y):
        self.world = world
        self.map = Map
        self.block_size = 40
        self.height = 2 * self.block_size
        self.width = self.block_size
        self.x = x
        self.y = y
        
    def update(self, delta):
        pass

    def delete(self):
        self.world.checkpoint.remove(self)


class World:
    def __init__(self, width, height, block_size):
        self.width = width
        self.height = height
        self.block_size = block_size
        self.slime_spawn_location = []
        self.bullet = []
        self.slime = []
        self.kingslime = []
        self.checkpoint = []
        self.spawnpoint = [0, 30, 80]
        self.pressing = []
        self.time = 0
        self.currentmap = 0

        self.stage = Stage(self)
        self.player = Player(self, 30, 80, self.stage, self.block_size)
        self.write_slime()
        
       
    def write_slime(self):    
        for row in range(self.stage.height): # write slime_location
            for column in range(self.stage.width):
                if self.stage.has_slime(row, column):
                    self.slime_spawn_location.append(self.stage.get_sprite_position(row, column))
                    
        for slime_x, slime_y in self.slime_spawn_location: # write slime
            self.slime.append(Slime(self, slime_x, slime_y, self.stage, self.player, self.block_size))

    def write_checkpoint(self, currentmap, x, y):
        if self.currentmap == currentmap:
            if currentmap > self.spawnpoint[0]:
                self.checkpoint.append(Checkpoint(self, currentmap, x, y))


                                   
    def change_map(self, Map):
        self.slime_spawn_location = []
        self.slime = []
        self.bullet = []
        self.stage.delete()

        self.player.vy = 0

        self.stage.map = reader(Map)
        self.stage.write_block_list()
        self.write_slime()
        self.checkpoint = []
        self.kingslime = []
        self.write_checkpoint(1, 500, 80)
        self.write_checkpoint(3, 620, 280)
        if self.currentmap == 4: 
            self.kingslime.append(Kingslime(self,700, 120, self.block_size))

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.W:
            if self.player.jump_status != 2:
                self.player.jump()

        if key == arcade.key.O:
            self.currentmap = 4
            self.change_map(MAP[4])
                
        if key == arcade.key.A:
            self.pressing.append('A')
            self.player.vx = -5

        if key == arcade.key.D:
            self.pressing.append('D')
            self.player.vx = 5
        
        if self.time == 0:
            if key == arcade.key.SPACE:
                self.bullet.append(Bullet(self))
                
        if self.time == 1:
            if self.player.life != 0:
                if key == arcade.key.R:
                    self.time = 0
                    self.currentmap = self.spawnpoint[0]
                    self.change_map(MAP[self.currentmap])
                    self.player.x = self.spawnpoint[1]
                    self.player.y = self.spawnpoint[2]
                    self.player.turn = 0
            else:
                if key == arcade.key.R:
                    self.time = 0
                    self.spawnpoint = [0, 30, 80]
                    self.currentmap = self.spawnpoint[0]
                    self.change_map(MAP[self.currentmap])
                    self.player.x = self.spawnpoint[1]
                    self.player.y = self.spawnpoint[2]
                    self.player.turn = 0
                    self.player.life = 3
                    self.player.kill = 0
                
    def on_key_release(self, key, modifiers):
        if len(self.pressing) == 1:
            if key == arcade.key.A:
                self.pressing.remove('A')
                self.player.vx = 0
            if key == arcade.key.D:
                self.pressing.remove('D')
                self.player.vx = 0
    
        if len(self.pressing) == 2:
            if key == arcade.key.A or key == arcade.key.D:
                if key == arcade.key.A:
                    if self.pressing[0] == 'A':
                        self.player.vx = 5
                    if self.pressing[0] == 'D':
                        self.player.vx = 0
                    self.pressing.remove('A')

                if key == arcade.key.D:
                    if self.pressing[0] == 'D':
                        self.player.vx = -5
                    if self.pressing[0] == 'A':
                        self.player.vx = 0
                    self.pressing.remove('D')

    def update(self, delta):
        if self.time == 1:
            return
        self.player.update(delta)
        for bullet in self.bullet:
            bullet.update(delta)
        for slime in self.slime:
            slime.update(delta)
        for kingslime in self.kingslime:
            kingslime.update(delta)
        for checkpoint in self.checkpoint:
            checkpoint.update(delta)
        
            
            

class Stage:
    def __init__(self,world):
        self.world = world
        Map = MAP[self.world.currentmap]
        self.map = reader(Map)
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.block_list = []
        self.write_block_list()

    def get_sprite_position(self, row, column):
        """ find x,y from column,row
        row = 0-19 column = 0-14     "self.currentmap"""
        x = ((column + 1) * self.world.block_size) - self.world.block_size//2
        y = (self.world.height - ((row + 1) * self.world.block_size)) + self.world.block_size//2
        return x,y
    
    def write_block_list(self):    
        for row in range(self.height):
            for column in range(self.width):
                if self.has_block(row, column):
                    self.block_list.append(self.get_sprite_position(row, column))

    def delete(self):
        self.block_list = []

    def has_block(self, row, column):
        return self.map[row][column] == '#'
    def has_blank(self, row, column):
        return self.map[row][column] == '.'
    def has_slime(self, row, column):
        return self.map[row][column] == '0'

    

    



