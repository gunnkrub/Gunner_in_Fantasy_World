import arcade
from models import World, Stage

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 40
PLAYER_SIZE_X = 40
PLAYER_SIZE_Y = 80

BG = ["images/background1.png",
      "images/background2.png",
      "images/background3.jpg",
      "images/background4.png"]

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
        self.sprite = arcade.Sprite('images/Bullet.png',scale = 1.5)
        
    def draw(self, bullet_list):
        for bullet in bullet_list:
            self.sprite.set_position(bullet.x,bullet.y)
            self.sprite.draw()


class SlimeSprite():
    def __init__(self):
        self.sprite_right = arcade.Sprite('images/Slime_right.png')
        self.sprite_left = arcade.Sprite('images/Slime_left.png')
        self.health_bar = arcade.Sprite('images/Health_bar.png')
        self.gray_health_bar = arcade.Sprite('images/Gray_Health_bar.png')

    def draw(self, slime_list):
        for slime in slime_list:
            self.sprite_left.set_position(slime.x, slime.y)
            self.sprite_right.set_position(slime.x, slime.y)
            self.gray_health_bar.set_position(slime.x , slime.y + 35)
            self.gray_health_bar.draw()

            percent_health = int(((slime.health / slime.MAX_HEALTH) * 100 // 10))
            for i in range(percent_health):
                self.health_bar.set_position(slime.x - 13.5 + (i*3), slime.y + 35)
                self.health_bar.draw()

            if slime.vx >= 0:
                self.sprite_right.draw()
            else:
                self.sprite_left.draw()
            

class KingslimeSprite():
     def __init__(self):
        self.sprite_right = arcade.Sprite('images/Slime_right.png', scale = 4)
        self.sprite_left = arcade.Sprite('images/Slime_left.png', scale = 4)
        self.health_bar = arcade.Sprite('images/Boss_Health_bar.png')
        self.gray_health_bar = arcade.Sprite('images/Boss_Gray_Health_bar.png')

     def draw(self, kingslime_list):
        for kingslime in kingslime_list:
            self.sprite_right.set_position(kingslime.x, kingslime.y)
            self.sprite_left.set_position(kingslime.x, kingslime.y)
            self.gray_health_bar.set_position(400 , 550)
            self.gray_health_bar.draw()
            
            percent_health = int(((kingslime.health / kingslime.MAX_HEALTH) * 100 // 10))
            for i in range(percent_health):
                self.health_bar.set_position(400 - 135 + (i*30), 550)
                self.health_bar.draw()

            if kingslime.vx >= 0:
                self.sprite_right.draw()
            else:
                self.sprite_left.draw()

            
            

class CheckpointSprite():
    def __init__(self):
        self.sprite = arcade.Sprite('images/Checkpoint.png')

    def draw(self, checkpoint_list):
        for checkpoint in checkpoint_list:
            self.sprite.set_position(checkpoint.x, checkpoint.y)
            self.sprite.draw()

        
            
class GunnerWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)

 
        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT, BLOCK_SIZE)

        self.world.player.turn = 0
        self.player_right_sprite = ModelSprite('images/Gunner_right.png', model=self.world.player)
        self.player_left_sprite = ModelSprite('images/Gunner_left.png', model=self.world.player)
        self.bullet_sprite = BulletSprite()
        self.slime_sprite = SlimeSprite()
        self.kingslime_sprite = KingslimeSprite()
        self.checkpoint_sprite = CheckpointSprite()
        
##        if self.world.currentmap == 0:
##            self.background = arcade.Sprite("images/background1.jpg")
##        if self.world.currentmap == 1:
##            self.background = arcade.Sprite("images/background2.png")
##        if self.world.currentmap == 2:
##            self.background = arcade.Sprite("images/background3.jpg")
##        if self.world.currentmap == 3:
##            self.background = arcade.Sprite("images/background4.png")
##            
        self.stage_drawer = StageDrawer(self.world.stage)

    def update(self, delta):
        self.world.update(delta)
    
    def on_draw(self):
        arcade.start_render()
        self.background = arcade.Sprite("images/forest.png")
##        self.background = arcade.Sprite(BG[self.world.currentmap])
        self.background.set_position(400,300)
        self.background.draw()
        if self.world.player.turn == 0:
            self.player_right_sprite.draw()
        if self.world.player.turn == 1:
            self.player_left_sprite.draw()
        
        self.slime_sprite.draw(self.world.slime)
        self.kingslime_sprite.draw(self.world.kingslime)
        self.bullet_sprite.draw(self.world.bullet)
        self.checkpoint_sprite.draw(self.world.checkpoint)
        
        self.stage_drawer.draw()

        if self.world.time == 1:
            if self.world.player.life > 0:
                arcade.draw_text(f"PRESS 'R' TO RESPAWN", 50, 300, arcade.color.WHITE, 60)
            if self.world.player.life == 0:
                arcade.draw_text(f"PRESS 'R' TO RESTART", 50, 300, arcade.color.WHITE, 60)
            
        arcade.draw_text(f"LIFE: {self.world.player.life}", 25, 550, arcade.color.RED, 30)
        arcade.draw_text(f"SCORE: {self.world.player.kill}", 600, 550, arcade.color.WHITE, 30)

        if self.world.time == 2:
            arcade.draw_text("YOU WON!", 75, 300, arcade.color.GOLD, 120)




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
        # find x,y from column,rowself.health_bar.draw()
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
