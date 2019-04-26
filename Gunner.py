import arcade
from models import World, Stage

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 40
PLAYER_SIZE_X = 40
PLAYER_SIZE_Y = 80


class ModelSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)
 
        super().__init__(*args, **kwargs)
 
    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)

    def draw(self):
        self.sync_with_model()
        super().draw()

        
class BulletSprite:
    def __init__(self):
        self.sprite = arcade.Sprite('images/Bullet.png')
        
    def draw(self,bullet_list):
        for bullet in bullet_list:
            self.sprite.set_position(bullet.x,bullet.y)
            self.sprite.draw()


class SlimeSprite():
    def __init__(self):
        self.sprite = arcade.Sprite('images/Slime.png')

    def draw(self, slime_list):
        for slime in slime_list:
            self.sprite.set_position(slime.x, slime.y)
            self.sprite.draw()
        
            
class GunnerWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
 
        arcade.set_background_color(arcade.color.WHITE)
 
        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT, BLOCK_SIZE)

        self.world.player.turn = 0
        self.player_right_sprite = ModelSprite('images/Gunner_right.png', model=self.world.player)
        self.player_left_sprite = ModelSprite('images/Gunner_left.png', model=self.world.player)
        self.bullet_sprite = BulletSprite()
        self.slime_sprite = SlimeSprite()

        self.stage_drawer = StageDrawer(self.world.stage)

    def update(self, delta):
        self.world.update(delta)
    
    def on_draw(self):
        arcade.start_render()
##        arcade.draw_text(f'KILL {self.world.player.x}', 400, 300, arcade.color.YELLOW, 60)

        if self.world.player.turn == 0:
            self.player_right_sprite.draw()
        if self.world.player.turn == 1:
            self.player_left_sprite.draw()
        
        self.slime_sprite.draw(self.world.slime)
        self.bullet_sprite.draw(self.world.bullet)

        self.stage_drawer.draw()

    def on_key_press(self, key, key_modifiers):
        self.world.on_key_press(key, key_modifiers)

    def on_key_release(self, key, key_modifiers):
        self.world.on_key_release(key, key_modifiers)
 

class StageDrawer():
    def __init__(self, stage):
        self.stage = stage
        self.width = self.stage.width
        self.height = self.stage.height

        self.block_sprite = arcade.Sprite('images/Block.png')
        
    def get_sprite_position(self, row, column):
        # find x,y from column,row
        # row = 0-19 column = 0-14
        x = ((column + 1) * BLOCK_SIZE) - BLOCK_SIZE//2
        y = (SCREEN_HEIGHT - ((row + 1) * BLOCK_SIZE)) + BLOCK_SIZE//2
        return x,y
    
    def draw_sprite(self, sprite, row, column):
        x,y = self.get_sprite_position(row, column)
        sprite.set_position(x,y)
        sprite.draw()
        
    def draw(self):
        # row = 0-19 column = 0-14
        for row in range(self.height):
            for column in range(self.width):
                if self.stage.has_block(row, column):
                    self.draw_sprite(self.block_sprite, row, column)

                    
def main():
    window = GunnerWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()

if __name__ == '__main__':
    main()
