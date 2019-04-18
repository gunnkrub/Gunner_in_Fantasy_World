import arcade.key
from codetect import spritecollide
class Player:
    JUMPING_VELOCITY = 15
    GRAVITY = 1
    def __init__(self, world, x, y, stage, block_size):
        self.world = world
        self.width = block_size
        self.height = block_size * 2
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.jump_status = 0
        """
        jump_status = 0 Can double jump
        jump_status = 1 Jumped 1 time
        jump_status = 2 Jumped 2 times
        """

        self.stage = stage

        self.block_size = block_size
        
    def jump(self):
        self.vy = Player.JUMPING_VELOCITY
        self.jump_status += 1

    def move_player_out_of_block(self, block_hit_list):
   
        for block_x, block_y in block_hit_list:
            if self.y > block_y + self.block_size: # on block
                if self.vy < 0: # falling
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

    def update(self, delta):
        self.x += self.vx
        self.y += self.vy
        
        if self.vy != -10:
            self.vy -= Player.GRAVITY

        block_hit_list = spritecollide(self.x, self.y ,self.height, self.block_size, self.stage.block_list)
        if len(block_hit_list) == 3:
            del block_hit_list[2]
            
        self.move_player_out_of_block(block_hit_list)


class Bullet:
    def __init__(self, world):
        self.world = world
        self.player = self.world.player
        self.x = self.player.x + (self.player.block_size / 2)
        self.y = self.player.y - 2
        self.vx = 5
        self.bullet_width = 6
        self.bullet_height = 3

    def bullet_hit_block(self):
        for block_x, block_y in self.world.stage.block_list:
            if block_x - (self.world.block_size / 2) <= self.x + (self.bullet_width / 2) <= block_x + (self.world.block_size / 2):
                if block_y - (self.world.block_size / 2) <= self.y + (self.bullet_height / 2) <= block_y + (self.world.block_size / 2) or block_y - (self.world.block_size / 2) <= self.y + (self.bullet_height / 2) <= block_y + (self.world.block_size / 2):
                   return True                
        return False

    def bullet_hit_slime(self):
        for slime in self.world.slime:
            if slime.x - (self.world.block_size / 2) <= self.x + (self.bullet_width / 2) <= slime.x + (self.world.block_size / 2):
                if slime.y - (self.world.block_size / 2) <= self.y + (self.bullet_height / 2) <= slime.y + (self.world.block_size / 2) or slime.y - (self.world.block_size / 2) <= self.y + (self.bullet_height / 2) <= slime.y + (self.world.block_size / 2):
                   self.world.slime.remove(slime)
                   return True
        return False
    
    def delete(self):
        self.world.bullet.remove(self)
        
    def update(self, delta):
        self.x += self.vx
        if self.x > self.world.width + (self.bullet_width / 2):
            self.delete()
        if self.bullet_hit_block():
            self.delete()
        if self.bullet_hit_slime():
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

    def move_slime_out_of_block(self, block_hit_list):
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
    def get_position(self):
        return self.x, self.y


    def update(self, delta):
        self.x += self.vx
        self.y += self.vy
        self.vy -= self.player.GRAVITY
        
        block_hit_list = spritecollide(self.x, self.y ,self.height, self.block_size, self.stage.block_list)
        self.move_slime_out_of_block(block_hit_list)

        





class World:
    def __init__(self, width, height, block_size):
        self.width = width
        self.height = height
        self.block_size = block_size

        self.stage = Stage(self)
        self.player = Player(self, 30, 80, self.stage, self.block_size)

        self.bullet = [] # bullet()
        self.slime = [] # slime()
        self.slime_list = [] # position of slime

        self.write_slime_list()

    def get_bullet_position(self):
        bullet_list = []
        for Bullet in self.bullet:
            bullet_list.append(self.Bullet.get_position())
        return bullet_list
            

##    def write_slime_list(self):
##        for Slime in self.slime:
##            for slime_x, slime_y in self.Slime.get_position():
##                print((slime_x,slime_y))
##                self.slime_list.append((slime_x, slime_y))

    
    def write_slime_list(self):    
        for row in range(self.stage.height):
            for column in range(self.stage.width):
                if self.stage.has_slime(row, column):
                    self.slime_list.append(self.stage.get_sprite_position(row, column))
        for slime_x, slime_y in self.slime_list:
            self.slime.append(Slime(self, slime_x, slime_y, self.stage, self.player, self.block_size))
        
    def update(self, delta):
        self.player.update(delta)
        for bullet in self.bullet:
            bullet.update(delta)
        for slime in self.slime:
            slime.update(delta)



    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.W:
            if self.player.jump_status != 2:
                self.player.jump()
        if key == arcade.key.A:
            self.player.vx -= 5
        if key == arcade.key.D:
            self.player.vx += 5
        if key == arcade.key.SPACE:
            self.bullet.append(Bullet(self))

    def on_key_release(self, key, modifiers):
        if key == arcade.key.A or key == arcade.key.D:
            self.player.vx = 0


class Stage:
    def __init__(self,world):
        self.world = world
        self.map = ['....................',
                    '....................',
                    '....................',
                    '....................',
                    '....................',
                    '....................',
                    '.................##.',
                    '....................',
                    '....................',
                    '....................',
                    '.......#............',
                    '......##...#.#......',
                    '.....###...#.#......',
                    '...0####...#.#...0.#',
                    '####################' ]
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.block_list = []
        self.write_block_list()

    def get_sprite_position(self, row, column):
        """ find x,y from column,row
        row = 0-19 column = 0-14     """
        x = ((column + 1) * self.world.block_size) - self.world.block_size//2
        y = (self.world.height - ((row + 1) * self.world.block_size)) + self.world.block_size//2
        return x,y
    
    def write_block_list(self):    
        for row in range(self.height):
            for column in range(self.width):
                if self.has_block(row, column):
                    self.block_list.append(self.get_sprite_position(row, column))


    def has_block(self, row, column):
        return self.map[row][column] == '#'
    def has_blank(self, row, column):
        return self.map[row][column] == '.'
    def has_slime(self, row, column):
        return self.map[row][column] == '0'

    



