def spritecollide(x, y, height, block_size, block_list):
        block_hit_list = []
        for block_x,block_y in block_list:
                if (block_y - ((block_size//2) + (height//2)) < y < block_y + ((block_size//2) + (height//2))):
                    if     ((block_x - (block_size // 2) < x - (block_size // 2) and x - (block_size // 2) < block_x + (block_size // 2))
                         or (block_x - (block_size // 2) < x + (block_size // 2) and x - (block_size // 2) < block_x + (block_size // 2))):
                        block_hit_list.append([block_x,block_y])   
        return block_hit_list

def collision(x, y, width, height, x2, y2, width2, height2):
        if x2 - (width2 // 2) <= x + width <= x2 + (width2 // 2) or x2 - (width2 // 2) <= x - width <= x2 + (width2 // 2):
                if y2 - (height2 // 2) <= y + height <= y2 + (height2 // 2) or y2 - (height2 // 2) <= y - width <= y2 + (y2 // 2):
                        return True











def checkpointcollision(x, y, flag_x, flag_y):
        height = 80
        width = 40
        flag_height = 80
        flag_width = 40

        if flag_x - (flag_width // 2) <= x + width <= flag_x + (flag_width // 2) or flag_x - (flag_width // 2) <= x - width <= flag_x + (flag_width // 2):
                if flag_y - (flag_height // 2) <= y + height <= flag_y + (flag_height // 2) or flag_y - (flag_height // 2) <= y - width <= flag_y + (flag_height // 2):
                        return True
        
