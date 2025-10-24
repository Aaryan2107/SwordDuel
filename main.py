import pygame
import math  
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
        self.is_attacking = False  
        
        # Player Idle Position images
        self.Idle_List = self.images_loader("graphic/Player/Idle/Idle", 10)
        self.scale_image(self.Idle_List)
        self.Idle_index = 0
        self.image = self.Idle_List[self.Idle_index]
        self.rect = self.image.get_rect(midbottom = (120, 800))
        self.hitbox = self.rect.inflate(-60, -40)  

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
     
    # load images from a given path and number of images
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
            self.is_attacking = True  
            self.attack_index += 0.2
            if self.attack_index >= len(self.attack_list): 
                self.attack_index = 0
            self.image = self.attack_list[int(self.attack_index)]
        elif self.rect.bottom < 800:
            self.is_attacking = False 
            self.Jump_index += 0.1
            if self.Jump_index >= len(self.Jump_List): self.Jump_index = 0
            self.image = self.Jump_List[int(self.Jump_index)]
        elif pygame.key.get_pressed()[pygame.K_w]: 
            self.is_attacking = False 
            self.Run_index +=0.1
            if self.Run_index >= len(self.Run_List): self.Run_index =0
            self.image = self.Run_List[int(self.Run_index)]
        elif pygame.key.get_pressed()[pygame.K_LSHIFT]:
            self.is_attacking = False 
            self.slide_index +=0.2
            if self.slide_index >= len(self.slide_list): self.slide_index =0
            self.image = self.slide_list[int(self.slide_index)]
        elif pygame.key.get_pressed()[pygame.K_c]:
            self.is_attacking = False 
            self.crouch_index +=0.1
            if self.crouch_index >= len(self.crouch_list): self.crouch_index =0
            self.image = self.crouch_list[int(self.crouch_index)]
        elif pygame.key.get_pressed()[pygame.K_s]:
            self.is_attacking = False 
            self.Turn_index +=0.1
            if self.Turn_index >= len(self.Turn_list): self.Turn_index =0
            self.image = self.Turn_list[int(self.Turn_index)]
        else:
            self.is_attacking = False 
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
        self.hitbox.midbottom = self.rect.midbottom 

    def reset(self):
        self.health = self.max_health
        self.rect = self.image.get_rect(midbottom = (120, 800))
        self.gravity = 0         
        self.space_pressed = False
        self.is_attacking = False
     
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
            self.hitbox = self.rect.inflate(-60, -40) 

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
            if abs(player.rect.x - self.rect.x) < 240:  # close enough to attack
                self.rect.x = self.rect.x  # stop moving

        def attack_Cooldown(self):
            if self.is_attacking:
                current_time = pygame.time.get_ticks()
                if current_time - self.attack_time >= self.attack_cooldown:
                    self.is_attacking = False
                    
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
            self.hitbox.midbottom = self.rect.midbottom 

class wizard(Enemy): # Inherits from Enemy class
    def __init__(self, projectile_group, player_sprite):
        super().__init__()
        self.projectile_group = projectile_group
        self.player = player_sprite 
        self.health = 100
        self.max_health = 100 
        
        # wizard Idle Position images
        self.Idle_List = self.images_loader("graphic/Enemies/Evil_Wizard/Idle/Idle", 10)
        self.scale_image(self.Idle_List, 3.4)
        self.Idle_index = 0
        self.image = self.Idle_List[int(self.Idle_index)]
        
        # wizard walk images
        self.walk_list = self.images_loader("graphic/Enemies/Evil_Wizard/walk/walk", 8)
        self.scale_image(self.walk_list, 3.4)
        self.walk_index = 0

         # wizard attack position images
        self.attack_list = self.images_loader("graphic/Enemies/Evil_Wizard/attack/attack", 13)
        self.attack_index = 0
        self.scale_image(self.attack_list, 3.4) 

        # Spawn logic: start off-screen right 
        self.is_entering = True
        self.destination_x = info.current_w - 300 
        self.rect = self.image.get_rect(midbottom = (info.current_w + 200, 945)) 
        
        self.attack_state = False
        self.attack_cooldown = 4000
        self.last_attack_time = pygame.time.get_ticks()
        self.hitbox = self.rect.inflate(-100, -50)
        
        
    def spawn_projectile(self):
        spawn_pos_x = self.rect.midleft[0]
        spawn_pos_y = self.rect.midleft[1] + 20 
        target_pos = self.player.rect.center
        new_proj = Projectile(spawn_pos_x, spawn_pos_y, target_pos[0], target_pos[1])
        self.projectile_group.add(new_proj)    
    
    def scale_image(self,list,factor):
        for i in range (len(list)):
            x = int(list[i].get_width() *factor)
            y = int(list[i].get_height() *factor)
            scaled_image = pygame.transform.scale(list[i], (x, y))
            flipped_image = pygame.transform.flip(scaled_image, True, False)
            list[i] = flipped_image  
            
    def update(self, player): 
        current_time = pygame.time.get_ticks()
        
        if self.is_entering:
            # Move left 
            self.rect.x -= 3
            self.walk_index += 0.1 
            if self.walk_index >= len(self.walk_list):
                self.walk_index = 0
            self.image = self.walk_list[int(self.walk_index)] 
            
            if self.rect.centerx <= self.destination_x:
                self.is_entering = False
                self.last_attack_time = current_time 
        
        elif self.attack_state:
            self.attack_index += 0.3 
            if self.attack_index >= len(self.attack_list):
                self.attack_state = False 
                self.attack_index = 0
                self.last_attack_time = current_time 
                self.spawn_projectile() 
            self.image = self.attack_list[int(self.attack_index)]
        else:
            self.Idle_index += 0.1
            if self.Idle_index >= len(self.Idle_List):
                self.Idle_index = 0
            self.image = self.Idle_List[int(self.Idle_index)] 
            if current_time - self.last_attack_time >= self.attack_cooldown:
                self.attack_state = True
                self.attack_index = 0
                
        self.hitbox.midbottom = self.rect.midbottom

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

class Projectile(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, target_x, target_y):
        super().__init__()
        # loading projectile images
        self.projectile_list = self.images_loader('graphic/Enemies/Evil_Wizard/projectiles/projectile',4)
        self.scale_image(self.projectile_list)
        self.projectile_index = 0
        self.image = self.projectile_list[self.projectile_index]
        self.rect = self.image.get_rect(center=(start_x, start_y))
        self.hitbox = self.rect.inflate(-20, -20)
        # base state and speed
        self.speed = 10
        self.deflected = False
        # using direction vector between player and wizard to calculate the shortest distace
        dx = target_x - start_x
        dy = target_y - start_y
        distance = math.hypot(dx, dy)
        if distance > 0:
            self.velocity_x = (dx / distance) * self.speed
            self.velocity_y = (dy / distance) * self.speed
        else:
            self.velocity_x = -self.speed 
            self.velocity_y = 0
            
    def deflect(self):
        if not self.deflected: 
            self.deflected = True
            self.velocity_x *= -1.5 
            self.velocity_y *= -1.5
            self.projectile_list = [pygame.transform.flip(img, True, False) for img in self.projectile_list]
            
    def animate(self):
        self.projectile_index += 0.2 
        if self.projectile_index >= len(self.projectile_list):
            self.projectile_index = 0
        self.image = self.projectile_list[int(self.projectile_index)]
        
    def update(self):
        self.animate()  
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        self.hitbox.center = self.rect.center
        if self.rect.bottom < 0 or self.rect.top > info.current_h or \
           self.rect.right < 0 or self.rect.left > info.current_w:
            self.kill()
            
    def images_loader(self,path,number):
        images = []
        for i in range(1,number+1):
            img = pygame.image.load(f'{path}_{i}.png').convert_alpha()
            images.append(img)
        return images            

    def scale_image(self,list):
        for i in range (len(list)):
            x = int(list[i].get_width() * 5)
            y = int(list[i].get_height() * 5)
            scaled_image = pygame.transform.scale(list[i], (x, y))
            flipped_image = pygame.transform.flip(scaled_image, True, False) 
            list[i] = flipped_image  

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
        self.Level(level) 
        
Background_1 = pygame.image.load('graphic/Background/background.png')
scale_factor = 0.8
x = int(Background_1.get_width() * scale_factor)
y = int(Background_1.get_height() * scale_factor)
Background_1 = pygame.transform.scale(Background_1, (x, y))

player = pygame.sprite.GroupSingle()
player.add(Player())
Enemy_Group = pygame.sprite.Group()
Enemy_Group.add(Knight())
projectile_group = pygame.sprite.Group() 
game_stage = 'knight' 

Game_Active = True
font = pygame.font.Font(None , 150) 
small_font = pygame.font.Font(None,60)
win_text = font.render("YOU WIN", True, (0, 255, 0)) 

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if not Game_Active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                player.sprite.reset() 
                Enemy_Group.empty()
                projectile_group.empty() 
                Enemy_Group.add(Knight()) 
                game_stage = 'knight'
                Game_Active = True

    if Game_Active:
        screen.blit(Background_1, (0, 0))

        if not Enemy_Group and game_stage == 'knight':
            game_stage = 'wizard'
            Enemy_Group.add(wizard(projectile_group, player.sprite))
        
        Enemy_Group.update(player.sprite)
        projectile_group.update()
        player.update()
        
        Enemy_Group.draw(screen)
        projectile_group.draw(screen)
        player.draw(screen)
        
        player_sprite = player.sprite

        for enemy in Enemy_Group:
            if isinstance(enemy, Knight):
                if abs(enemy.rect.centerx - player_sprite.rect.centerx) < 120:
                    player_sprite.health -= 0.3  
                if player_sprite.is_attacking and abs(enemy.rect.centerx - player_sprite.rect.centerx) < 200:
                    enemy.take_damage(0.8)         
            elif isinstance(enemy, wizard):
                if player_sprite.is_attacking and player_sprite.hitbox.colliderect(enemy.hitbox):
                    enemy.take_damage(0.8) 

            enemy.draw_health_bar(screen)

        for proj in projectile_group:
            if player_sprite.is_attacking and not proj.deflected:
                if player_sprite.rect.colliderect(proj.hitbox): 
                    proj.deflect()
            elif not proj.deflected:
                if player_sprite.hitbox.colliderect(proj.hitbox):
                    player_sprite.health -= 10 
                    proj.kill()

        for enemy in Enemy_Group:
            if isinstance(enemy, wizard): 
                for proj in projectile_group:
                    if enemy.hitbox.colliderect(proj.hitbox) and proj.deflected:
                        enemy.take_damage(25) 
                        proj.kill() 

        player.sprite.draw_health_bar(screen)

        if player.sprite.health <= 0:
            Game_Active = False
        elif not Enemy_Group and game_stage == 'wizard': 
            Game_Active = False

    else:
        screen.fill((0, 0, 0))  
        if player.sprite.health <= 0:
            game_over_text = font.render("GAME OVER", True, (255, 0, 0))
            game_over_rect = game_over_text.get_rect(center=(info.current_w // 2, info.current_h // 2 - 100))
            screen.blit(game_over_text, game_over_rect)
        else:
            win_rect = win_text.get_rect(center=(info.current_w // 2, info.current_h // 2 - 100))
            screen.blit(win_text, win_rect)
        restart_text = small_font.render("Press 'R' to Restart", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(info.current_w // 2, info.current_h // 2 + 50))
        screen.blit(restart_text, restart_rect)
        
        if player.sprite.health <= 0:
            player.sprite.reset()
            
    pygame.display.update()
    clock.tick(60)
