import arcade.key
from codetect import spritecollide
class Player:
    JUMPING_VELOCITY = 15
    GRAVITY = 1
    def __init__(self, world, x, y, stage, block_size):
        self.world = world
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
            if self.y > block_y:
                if self.vy < 0:
                    self.y = block_y + (self.block_size * 3 / 2)
                    self.jump_status = 0
            elif self.y < block_y:
                if self.vy > 0:
                    self.y = block_y - (self.block_size * 3 / 2)
                    self.vy = 0
            elif self.x > block_x:
                if self.vx < 0:
                    self.x = block_x + (self.block_size * 3 / 2)
            elif self.x < block_x:
                if self.vx > 0:
                    self.x = block_x - (self.block_size * 3 / 2)

    def update(self, delta):
        self.x += self.vx
        self.y += self.vy
        
        if self.vy != -10:
            self.vy -= Player.GRAVITY

        block_hit_list = spritecollide(self.x, self.y, self.stage.block_list)
        self.move_player_out_of_block(block_hit_list)


class World:
    def __init__(self, width, height, block_size):
        self.width = width
        self.height = height
        self.block_size = block_size
        
        self.stage = Stage(self)
        self.player = Player(self, 30, 80, self.stage, self.block_size)

        
    def update(self, delta):
        self.player.update(delta)

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.W:
            if self.player.jump_status != 2:
                self.player.jump()
        if key == arcade.key.A:
            self.player.vx -= 5
        if key == arcade.key.D:
            self.player.vx += 5

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
                    '...............####.',
                    '....................',
                    '....................',
                    '..#######...........',
                    '..............####..',
                    '....................',
                    '....................',
                    '......###...........',
                    '....................',
                    '##..................' ]
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

    



