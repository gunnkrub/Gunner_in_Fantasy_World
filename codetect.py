##def check_player_on_block(player_x, player_y, block_list):
##        for block_x,block_y in block_list:
##            if player_y == block_y + (40//2) + (80//2):
##                if (block_x - 20 <= player_x - 20 and player_x - 20 <= block_x + 20) or (block_x - 20 <= player_x + 20 and player_x - 20 <= block_x + 20):
##                    return True
##        return False
##
##
##

def player_in_block(player_x, player_y, block_list):
        for block_x,block_y in block_list:
                if player_y in range(block_y - ((40//2) + (80//2)), block_y + ((40//2) + (80//2))):
                        if (block_x - 20 <= player_x - 20 and player_x - 20 <= block_x + 20) or (block_x - 20 <= player_x + 20 and player_x - 20 <= block_x + 20):
                                return True
        return False




def player_in_block_list(player_x, player_y, block_list):
        dummy = []
        for block_x,block_y in block_list:
                if player_y in range(block_y - ((40//2) + (80//2)), block_y + ((40//2) + (80//2))):
                        if (block_x - 20 <= player_x - 20 and player_x - 20 <= block_x + 20) or (block_x - 20 <= player_x + 20 and player_x - 20 <= block_x + 20):
                                dummy.append([block_x,block_y])   
        return dummy


def move_player_on_block(player_x, player_y, block_list, player_vy):
        for block_x,block_y in block_list:
                if ((block_x - 20 <= player_x - 20 <= block_x + 20) or (block_x - 20 <= player_x + 20 <= block_x + 20)) and block_y - 20 <= player_y - 40 <= block_y + 20:
                        player_y = block_y + 60
                        return player_y,0
        return player_y, player_vy


##def move_on_block(player_x, player_y, player_vx, player_vy, block_list):
##        for block_x,block_y in block_list:
##                if player_vx >= 0:
##                        player_x = block_x - 40
##                else:
##                        player_x = block_x + 40
##                
                        
