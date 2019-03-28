def spritecollide(player_x, player_y, block_list):
        block_hit_list = []
        for block_x,block_y in block_list:
                if player_y in range(block_y - ((40//2) + (80//2)), block_y + ((40//2) + (80//2))):
                        if (block_x - 20 <= player_x - 20 and player_x - 20 <= block_x + 20) or (block_x - 20 <= player_x + 20 and player_x - 20 <= block_x + 20):
                                block_hit_list.append([block_x,block_y])   
        return block_hit_list

            
