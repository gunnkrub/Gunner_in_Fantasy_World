def spritecollide(x, y, height, block_size, block_list):
        block_hit_list = []
        for block_x,block_y in block_list:
                if y in range(block_y - ((block_size//2) + (height//2)), block_y + ((block_size//2) + (height//2))):
                    if     ((block_x - (block_size // 2) < x - (block_size // 2) and x - (block_size // 2) < block_x + (block_size // 2))
                         or (block_x - (block_size // 2) < x + (block_size // 2) and x - (block_size // 2) < block_x + (block_size // 2))):
                        block_hit_list.append([block_x,block_y])   
        return block_hit_list
