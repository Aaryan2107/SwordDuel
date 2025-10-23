import pygame
from sys import exit
pygame.init()

info = pygame.display.Info()
screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.NOFRAME)
clock = pygame.time.Clock()
class Player(pygame.sprite.Sprite):
    def __init__(self):
        self.space_pressed = False
        super().__init__()
        self.health = 100
        self.max_health = 100
        # Player Idle Position images
        self.Idle_List = self.images_loader("graphic/Player/Idle/Idle", 10)
        self.scale_image(self.Idle_List)
        self.Idle_index = 0
        self.image = self.Idle_List[self.Idle_index]
        self.rect = self.image.get_rect(midbottom = (120, 800))

        # Player run position images
        self.Run_List = self.images_loader("graphic/Player/Run/Run", 10)
        self.scale_image(self.Run_List)
        self.Run_index = 0  
        self.image = self.Run_List[self.Run_index]

        # player jump images
        self.Jump_List = self.images_loader("graphic/Player/Jump/Jump", 3)
        self.scale_image(self.Jump_List)
        self.Jump_index = 0
        self.gravity = 0
        self.image = self.Jump_List[self.Jump_index]
       
        # player Normal attack images
        self.attack_list = self.images_loader("graphic/Player/Player_Attack_1/n_attack", 4)
        self.attack_index = 0
        self.scale_image(self.attack_list)
        self.image = self.attack_list[self.attack_index]

        # player Slide images
        self.slide_list = self.images_loader("graphic/Player/Slide/Slide",4)
        self.scale_image(self.slide_list)
        self.slide_index = 0    
        self.image = self.slide_list[self.slide_index]

        # player Crouch images
        self.crouch_list = self.images_loader("graphic/Player/Crouch/Crouch",3)
        self.scale_image(self.crouch_list)  
        self.crouch_index = 0  
        self.image = self.crouch_list[self.crouch_index]

        # player TurnAround images
        self.Turn_list = self.images_loader("graphic/Player/TurnAround/TurnAround",3)
        self.scale_image(self.Turn_list)  
        self.Turn_index = 0 
     
    # Load images function : load images from a given path and number of images
    def images_loader(self,path,number):
        images = []
        for i in range(1,number+1):
            img = pygame.image.load(f'{path}_{i}.png').convert_alpha()
            images.append(img)
        return images
    def player_input(self):
        key = pygame.key.get_pressed()
        mouse_Button = pygame.mouse.get_pressed()
        if key[pygame.K_SPACE] and self.space_pressed == False:
            self.gravity = -20
            self.space_pressed = True
        if key[pygame.K_w]:
            self.rect.x += 5
        elif key[pygame.K_LSHIFT]:
            self.rect.x += 10
        elif key[pygame.K_s]:
            self.rect.x -= 10
    def scale_image(self,list):
        for i in range (len(list)):
            x = int(list[i].get_width() *5)
            y = int(list[i].get_height() *5)
            list[i] = pygame.transform.scale(list[i], (x, y))    
    
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 800:	
            self.rect.bottom = 800
            self.gravity = 0         
            self.space_pressed = False
  
    def player_animation_state(self):
        keys = pygame.key.get_pressed()
        mouse_Button = pygame.mouse.get_pressed()
        if mouse_Button[0]:
            self.attack_index += 0.2
            if self.attack_index >= len(self.attack_list): self.attack_index = 0
            self.image = self.attack_list[int(self.attack_index)]
        elif self.rect.bottom < 800:
            self.Jump_index += 0.1
            if self.Jump_index >= len(self.Jump_List): self.Jump_index = 0
            self.image = self.Jump_List[int(self.Jump_index)]
        elif pygame.key.get_pressed()[pygame.K_w]: 
            self.Run_index +=0.1
            if self.Run_index >= len(self.Run_List): self.Run_index =0
            self.image = self.Run_List[int(self.Run_index)]
        elif pygame.key.get_pressed()[pygame.K_LSHIFT]:
            self.slide_index +=0.2
            if self.slide_index >= len(self.slide_list): self.slide_index =0
            self.image = self.slide_list[int(self.slide_index)]
        elif pygame.key.get_pressed()[pygame.K_c]:
            self.crouch_index +=0.1
            if self.crouch_index >= len(self.crouch_list): self.crouch_index =0
            self.image = self.crouch_list[int(self.crouch_index)]
        elif pygame.key.get_pressed()[pygame.K_s]:
            self.Turn_index +=0.1
            if self.Turn_index >= len(self.Turn_list): self.Turn_index =0
            self.image = self.Turn_list[int(self.Turn_index)]
        else:
            self.Idle_index += 0.1
            if self.Idle_index >= len(self.Idle_List): self.Idle_index = 0
            self.image = self.Idle_List[int(self.Idle_index)]
    def draw_health_bar(self, surface):
        bar_width = 200
        bar_height = 20
        x, y = self.rect.centerx - 100, self.rect.top - 40
        fill = (self.health / self.max_health) * bar_width
        outline_rect = pygame.Rect(x, y, bar_width, bar_height)
        fill_rect = pygame.Rect(x, y, fill, bar_height)
        pygame.draw.rect(surface, (255, 0, 0), fill_rect)
        pygame.draw.rect(surface, (255, 255, 255), outline_rect, 2)

        
    
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.player_animation_state()


      
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

    def update(self,player):
        pass
class Knight(Enemy):
        def __init__(self): 
            super().__init__()
            self.health = 100
            self.max_health = 100
            self.damage = 5      
            # Using the Ememy Parent class method to load images and scale them
            self.Idle_list = self.images_loader("graphic/Enemy/Knight/Idle/Idle",4)
            self.scale_image(self.Idle_list,5)
            self.Idle_index = 0
            self.image = self.Idle_list[self.Idle_index]
            self.rect = self.image.get_rect(midbottom = (1200, 800))

            # Knight Walk images 
            self.Walk_list = self.images_loader("graphic/Enemy/Knight/Walk/Walk",8)
            self.scale_image(self.Walk_list,5)
            self.Walk_index = 0
            self.image = self.Walk_list[self.Walk_index]

            # Knight Attack images
            self.Attack_list = self.images_loader("graphic/Enemy/Knight/Attack/Attack",7)
            self.scale_image(self.Attack_list,5)
            self.Attack_index = 0
            self.image = self.Attack_list[self.Attack_index]
            # Knight Cooldown
            self.is_attacking = False
            self.attack_cooldown = 1000  # milliseconds
            self.attack_time = 0
        def Enemy_AI(self, player):
            if abs(player.rect.x - self.rect.x) < 600 and abs(player.rect.x - self.rect.x) > 240:  # player is nearby
                if player.rect.x > self.rect.x :  # player is to the right
                    self.rect.x += 2  # move right
                if player.rect.x < self.rect.x :  # player is to the left
                    self.rect.x -= 2  # move left
                else:
                    self.rect.x += 2  # move right
            if abs(player.rect.x - self.rect.x) < 240:  # close enough to attack
                self.rect.x = self.rect.x  # stop moving

        def attack_Cooldown(self):
            if is_attacking:
                current_time = pygame.time.get_ticks()
                if current_time - self.attack_time >= self.attack_cooldown:
                    is_attacking = False
        def Animation_state(self,player):
            if abs(player.rect.x - self.rect.x) < 600 and abs(player.rect.x - self.rect.x) > 240:
                self.Walk_index += 0.1
                if self.Walk_index >= len(self.Walk_list): self.Walk_index = 0
                self.image = self.Walk_list[int(self.Walk_index)]
            elif abs(player.rect.x - self.rect.x) < 240:
                self.Attack_index += 0.1
                if self.Attack_index >= len(self.Attack_list): 
                    self.Attack_index = 0
                    
                self.image = self.Attack_list[int(self.Attack_index)]
            else:
                self.Idle_index += 0.1
                if self.Idle_index >= len(self.Idle_list): self.Idle_index = 0
                self.image = self.Idle_list[int(self.Idle_index)]
        def draw_health_bar(self, surface):
            bar_width = 150
            bar_height = 15
            x, y = self.rect.centerx - 75, self.rect.top - 25
            fill = (self.health / self.max_health) * bar_width
            outline_rect = pygame.Rect(x, y, bar_width, bar_height)
            fill_rect = pygame.Rect(x, y, fill, bar_height)
            pygame.draw.rect(surface, (255, 0, 0), fill_rect)
            pygame.draw.rect(surface, (255, 255, 255), outline_rect, 2)

        def take_damage(self, amount):
            self.health -= amount
                if self.health <= 0:
                    self.kill()

        def update(self,player):
            self.Enemy_AI(player)
            self.Animation_state(player)



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
        

Background_1 = pygame.image.load('graphic/Background/background.png')
scale_factor = 0.8
x = int(Background_1.get_width() * scale_factor)
y = int(Background_1.get_height() * scale_factor)
Background_1 = pygame.transform.scale(Background_1, (x, y))


player = pygame.sprite.GroupSingle()
player.add(Player())
# enemy = pygame.sprite.GroupSingle()
# enemy.add(Enemy())
Enemy_Group = pygame.sprite.Group()
Enemy_Group.add(Knight())
Game_Active = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Restart game when Game Over
        if not Game_Active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # Reset everything
                player.sprite.health = 100
                Enemy_Group.empty()
                Enemy_Group.add(Knight())
                Game_Active = True

    if Game_Active:
        screen.blit(Background_1, (0, 0))
        Enemy_Group.update(player.sprite)
        Enemy_Group.draw(screen)
        player.update()
        player.draw(screen)

        # --- Combat interaction ---
        for enemy in Enemy_Group:
            # Enemy attacking player if close enough
            if abs(enemy.rect.centerx - player.sprite.rect.centerx) < 120:
                player.sprite.health -= 0.3  # enemy deals damage

            # Player attacking enemy when left mouse clicked
            if pygame.mouse.get_pressed()[0]:
                if abs(enemy.rect.centerx - player.sprite.rect.centerx) < 200:
                    enemy.take_damage(0.8)
                    

            # Draw enemy health bar
            enemy.draw_health_bar(screen)

        # Draw player health bar
        player.sprite.draw_health_bar(screen)

        # --- Game Over trigger ---
        if player.sprite.health <= 0:
            Game_Active = False

    else:
        # GAME OVER SCREEN
        screen.fill((0, 0, 0))  

        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        restart_text = small_font.render("Press 'R' to Restart", True, (255, 255, 255))
        game_over_rect = game_over_text.get_rect(center=(info.current_w // 2, info.current_h // 2 - 100))
        restart_rect = restart_text.get_rect(center=(info.current_w // 2, info.current_h // 2 + 50))

        screen.blit(game_over_text, game_over_rect)
        screen.blit(restart_text, restart_rect)

    pygame.display.update()
    clock.tick(60)
