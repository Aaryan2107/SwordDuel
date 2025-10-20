import pygame
from sys import exit
pygame.init()
screen = pygame.display.set_mode((1920,1080))
clock = pygame.time.Clock()
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Player Idle Position images
        idle_1 =pygame.image.load('graphic/Player/Idle/_Idle_r1.png')
        idle_2 =pygame.image.load('graphic/Player/Idle/_Idle_r2.png')
        idle_3 =pygame.image.load('graphic/Player/Idle/_Idle_r3.png')
        idle_4 =pygame.image.load('graphic/Player/Idle/_Idle_r4.png')
        idle_5 =pygame.image.load('graphic/Player/Idle/_Idle_r5.png')
        idle_6 =pygame.image.load('graphic/Player/Idle/_Idle_r6.png')
        idle_7 =pygame.image.load('graphic/Player/Idle/_Idle_r7.png')
        idle_8 =pygame.image.load('graphic/Player/Idle/_Idle_r8.png')
        idle_9 =pygame.image.load('graphic/Player/Idle/_Idle_r9.png')
        idle_10 =pygame.image.load('graphic/Player/Idle/_Idle_r10.png')
        self.Idle_List = [idle_1,idle_2,idle_3,idle_4,idle_5,idle_6,idle_7,idle_8,idle_9,idle_10]
        self.Idle_index = 0
        self.image = self.Idle_List[self.Idle_index]
        self.rect = self.image.get_rect()
        # player Normal attack images
        attack_1 = pygame.image.load('graphic/Player/Player_Attack_1/n_attack_1.png').convert_alpha()
        attack_2 = pygame.image.load('graphic/Player/Player_Attack_1/n_attack_2.png').convert_alpha()
        attack_3 = pygame.image.load('graphic/Player/Player_Attack_1/n_attack_3.png').convert_alpha()
        attack_4 = pygame.image.load('graphic/Player/Player_Attack_1/n_attack_4.png').convert_alpha()
        self.attack_list = [attack_1,attack_2,attack_3,attack_4]
        self.attack_index = 0
        def player_input(self):
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:   
                self.image = self.attack_list[self.attack_index]
                self.rect = self.image.get_rect(midbottom = (80,300))
            else:
                self.image = self.Idle_List[self.Idle_index]
                self.rect = self.image.get_rect(midbottom = (80,300))
    def player_animation_state(self):
        if 
        self.attack_index += 0.3
        if self.attack_index > len(self.attack_list): self.attack_index = 0
        self.image = self.attack_list[self.attack_index]

    def update(self):
       

attack_sprite = pygame.sprite.Group()
attack_sprite.add(Player())
class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        Background_1 = pygame.image.load('graphic/Background/background.png')
        Background_2 = pygame.image.load('graphic/Background/background1.png')
        Background_3 = pygame.image.load('graphic/Background/background2.png')
        Background_4 = pygame.image.load('graphic/Background/background3.png')
        self.background_list = [Background_1,Background_2,Background_3,Background_4]
        self.Background__index =0 
        def Level(self,level):
            if level == 0:
                screen.blit(self.background_list[self.Background__index])
            elif level == 1 :
                screen.blit(self.background_list[self.Background__index+1])
            else: pass 
        
        
        def update(self,level):
            Level(level)
        




# player = pygame.sprite.GroupSingle()
# player.add(Player())
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.key == :
                Player.animate()
    attack_sprite.draw(screen)
    attack_sprite.update()

    pygame.display.update()
    clock.tick(60)
       
