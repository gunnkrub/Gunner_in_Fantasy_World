import arcade.key
class Player:
    GRAVITY = 1
    JUMPING_VELOCITY = 10

    def __init__(self, world, x, y, stage, block_size):
        self.world = world
        self.x = x
        self.y = y
        self.vy = 0

        self.stage = stage

        self.block_size = block_size

    def update(self, delta):
        self.y += self.vy
        self.vy -= Player.GRAVITY

    def jump(self):
        self.vy = Player.JUMPING_VELOCITY

    def get_row(self):
        return (self.y - (self.block_size//2)) // self.block_size

    def get_column(self):
        return self.x // self.block_size
        
    def get_row_and_column(self):
        x = get_column()
        y = get_row()
        return x,y

    def check_block(self):
        return [get_column(),get_row()] in self.stage.stage_cr




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
            self.player.jump()
        if key == arcade.key.A:
            self.player.x -= 10
        if key == arcade.key.D:
            self.player.x += 10

class Stage:
    def __init__(self,world):
        self.map = ['....................',
                    '....................',
                    '....................',
                    '....................',
                    '................#...',
                    '....................',
                    '........#...........',
                    '....................',
                    '....................',
                    '....................',
                    '...........#........',
                    '....................',
                    '....................',
                    '.........#..........',
                    '####################' ]
        self.height = len(self.map)
        self.width = len(self.map[0])

    def has_block(self, row, column):
        return self.map[row][column] == '#'
    def has_blank(self, row, column):
        return self.map[row][column] == '.'
        
            

