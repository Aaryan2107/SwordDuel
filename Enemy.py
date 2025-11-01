import pygame
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
    def scale_image(self,list,factor):
        for i in range (len(list)):
            x = int(list[i].get_width() *factor)
            y = int(list[i].get_height() *factor)
            list[i] = pygame.transform.scale(list[i], (x, y))    
    
    def images_loader(self,path,number):
        images = []
        for i in range(1,number+1):
            img = pygame.image.load(f'{path}_{i}.png').convert_alpha()
            images.append(img)
        return images
    
    # Flip enemy images horizontally
    def flip_enemy(self,list):
            for i in range(len(list)):
                list[i] = pygame.transform.flip(list[i], True, False)
            return list
    def update(self,player):
        pass
