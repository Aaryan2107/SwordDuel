import pygame
import math  
import random  as random
from sys import exit

pygame.init()
pygame.mixer.init()
info = pygame.display.Info()
screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.NOFRAME)
screen_width = info.current_w
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        self.space_pressed = False
        super().__init__()
        self.health = 100
        self.max_health = 100  
        self.is_attacking = False  
        self.direction = True  # True for right, False for left
        
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
        
        
    def collide(self,Enemy):
        if self.hitbox.colliderect(Enemy.hitbox):
            if abs(Enemy.rect.centerx - self.rect.centerx) < 120:
                if Enemy.is_attacking:
                    self.health -=random.uniform(0.1,0.3)
                  
    # load images from a given path and number of images
    def images_loader(self,path,number):
        images = []
        for i in range(1,number+1):
            img = pygame.image.load(f'{path}_{i}.png').convert_alpha()
            images.append(img)
        return images
    
    # Handle player input for movement and actions`
    def player_input(self):
        key = pygame.key.get_pressed()
        mouse_Button = pygame.mouse.get_pressed()

        # Jump
        if key[pygame.K_SPACE] and self.space_pressed == False:
            self.gravity = -20
            self.space_pressed = True

        # Move Right
        if key[pygame.K_d] or key[pygame.K_LEFT]:
            if not self.direction:  # if facing left before
                self.direction = True
                self.Player_filp_animation()  # flip to face right
            self.rect.x += 5

        # Move Left
        elif key[pygame.K_a] or key[pygame.K_RIGHT]:
            if self.direction:  # if facing right before
                self.direction = False
                self.Player_filp_animation()  # flip to face left
            self.rect.x -= 5
        
        # Slide
        elif key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT]:
           if self.direction:  self.rect.x += 10
           else : self.rect.x -= 10
        else:
            pass

    # Scale images by a factor of certain amount 
    def scale_image(self,list):
        for i in range (len(list)):
            x = int(list[i].get_width() *5)
            y = int(list[i].get_height() *5)
            list[i] = pygame.transform.scale(list[i], (x, y))   
        return list 
    
    #` Apply gravity to the player for jumping and falling
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 800:	
            self.rect.bottom = 800
            self.gravity = 0         
            self.space_pressed = False

    # Flip player images horizontally
    def player_flip(self,list):
        for i in range(len(list)):
            list[i] = pygame.transform.flip(list[i], True, False)
        return list
    
    # Flip all player animations when changing direction
    def Player_filp_animation(self):
        self.Idle_List = self.player_flip(self.Idle_List)
        self.Run_List = self.player_flip(self.Run_List)
        self.Jump_List = self.player_flip(self.Jump_List)
        self.attack_list = self.player_flip(self.attack_list)
        self.slide_list = self.player_flip(self.slide_list)
        self.crouch_list = self.player_flip(self.crouch_list)
        self.Turn_list = self.player_flip(self.Turn_list)


    # Update player animation state based on actions
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
        elif keys[pygame.K_d] or keys[pygame.K_a] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]: 
            self.is_attacking = False 
            self.Run_index +=0.1
            if self.Run_index >= len(self.Run_List): self.Run_index =0
            self.image = self.Run_List[int(self.Run_index)]
        elif keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            self.is_attacking = False 
            self.slide_index +=0.2
            if self.slide_index >= len(self.slide_list): self.slide_index =0
            self.image = self.slide_list[int(self.slide_index)]
        elif keys[pygame.K_c]:
            self.is_attacking = False 
            self.crouch_index +=0.1
            if self.crouch_index >= len(self.crouch_list): self.crouch_index =0
            self.image = self.crouch_list[int(self.crouch_index)]
        else:
            self.is_attacking = False 
            self.Idle_index += 0.1
            if self.Idle_index >= len(self.Idle_List): self.Idle_index = 0
            self.image = self.Idle_List[int(self.Idle_index)]
        if self.rect.left < -235:
            self.rect.left = -235
        # Right boundary
        if self.rect.right > screen_width+250:
            self.rect.right = screen_width+250  
            
    def draw_health_bar(self,screen):
        Bar_Background = pygame.image.load('graphic/Player/HUD/bar_background.png').convert_alpha()
        Bar_Background = pygame.transform.scale(Bar_Background,(int(Bar_Background.get_width()*5),int(Bar_Background.get_height()*10)))
        Bar = pygame.image.load('graphic/Player/HUD/bar.png').convert_alpha()
        Bar = pygame.transform.scale(Bar,(int(Bar.get_width()*5),int(Bar.get_height()*5)))
        screen.blit(Bar_Background, (50, 10))
        bar_width = Bar.get_width()*0.9
        fill = (self.health / self.max_health) * bar_width
        fill_rect = pygame.Rect(30, 15, fill, Bar.get_height()*0.7)
        pygame.draw.rect(screen, (255, 0, 0), fill_rect)
        screen.blit(Bar,(10,10) )

  
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
    
    # Flip enemy images horizontally
    def flip_enemy(self,list):
            for i in range(len(list)):
                list[i] = pygame.transform.flip(list[i], True, False)
            return list
    def update(self,player):
        pass
class PauseMenu:
    def __init__(self, screen):
    

        # Button rectangles
        self.resume_rect = pygame.Rect(screen.get_width() // 2 - 120, screen.get_height() // 2 - 40, 240, 70)
        self.exit_rect = pygame.Rect(screen.get_width() // 2 - 120, screen.get_height() // 2 + 50, 240, 70)

    def draw(self):
        # Semi-transparent dark overlay
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        # Popup box
        popup_rect = pygame.Rect(self.screen.get_width() // 2 - 250, self.screen.get_height() // 2 - 200, 500, 350)
        pygame.draw.rect(self.screen, (30, 30, 30), popup_rect, border_radius=20)
        pygame.draw.rect(self.screen, (255, 255, 255), popup_rect, 3, border_radius=20)

        # Title text
        title = self.font_big.render("Paused", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 120))
        self.screen.blit(title, title_rect)

        # Resume button
        pygame.draw.rect(self.screen, (90, 180, 90), self.resume_rect, border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255), self.resume_rect, 3, border_radius=10)
        resume_text = self.font_small.render("Resume", True, (255, 255, 255))
        self.screen.blit(resume_text, resume_text.get_rect(center=self.resume_rect.center))


        # Exit button
        pygame.draw.rect(self.screen, (180, 60, 60), self.exit_rect, border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255), self.exit_rect, 3, border_radius=10)
        exit_text = self.font_small.render("Exit", True, (255, 255, 255))
        self.screen.blit(exit_text, exit_text.get_rect(center=self.exit_rect.center))

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if self.resume_rect.collidepoint(mouse_pos):
                self.is_paused = False  # Resume game
            elif self.exit_rect.collidepoint(mouse_pos):
                pygame.quit()
                exit()
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

            # Knight Hit images
            self.Hit_list = self.images_loader("graphic/Enemy/Knight/Hit/Hit",4)
            self.scale_image(self.Hit_list,5)       
            self.Hit_index = 0
            self.image = self.Hit_list[self.Hit_index]
            # Knight Cooldown
            self.is_attacking = False
            self.just_attacked = False
            self.attack_cooldown = 1000 # milliseconds
            self.attack_time = 0
            # Knight Direction
            self.Direction = True  # True for left, False for right
            
        def Enemy_AI(self, player):
            if abs(player.rect.x - self.rect.x) < 600 and abs(player.rect.x - self.rect.x) > 240:  # player is nearby
                if player.rect.x > self.rect.x :  # player is to the right
                    self.rect.x += 2  # move right
                if player.rect.x < self.rect.x :  # player is to the left
                    self.rect.x -= 2  # move left
            if abs(player.rect.x - self.rect.x) < 240:  # close enough to attack
                self.rect.x = self.rect.x  # stop moving
                self.attack_Cooldown()
                    
            if player.rect.x > self.rect.x and abs(player.rect.x - self.rect.x) >1 : # crossing  enemy
                if self.Direction :
                    self.Direction = False
                    self.Enemy_flip_animation(player)
            else : # player is on the left side
                if not self.Direction:
                    self.Direction = True
                    self.Enemy_flip_animation(player)
                
        # Flip all enemy animations when changing direction
        def Enemy_flip_animation(self,player):
                self.Idle_list = self.flip_enemy(self.Idle_list)
                self.Walk_list = self.flip_enemy(self.Walk_list)
                self.Attack_list = self.flip_enemy(self.Attack_list)
        def attack_Cooldown(self):
            current_time = pygame.time.get_ticks()
            if current_time - self.attack_time >= self.attack_cooldown:
                self.is_attacking = True
                self.attack_time = current_time
                    
        def Animation_state(self,player):
            if abs(player.rect.x - self.rect.x) < 600 and abs(player.rect.x - self.rect.x) > 240:
                self.Walk_index += 0.1
                if self.Walk_index >= len(self.Walk_list): self.Walk_index = 0
                self.image = self.Walk_list[int(self.Walk_index)]
            elif abs(player.rect.x - self.rect.x) < 240:
                if self.is_attacking:
                    self.Attack_index += 0.1
                    if self.Attack_index >= len(self.Attack_list): 
                        self.Attack_index = 0
                        self.is_attacking = False
                        self.just_attacked = True
                    self.image = self.Attack_list[int(self.Attack_index)]
            else:
                self.Idle_index += 0.1
                if self.Idle_index >= len(self.Idle_list): 
                    self.Idle_index = 0
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
            self.just_attacked = False
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

class Boss(Enemy):
    def __init__(self):
        super().__init__()
        # Boss specific initialization can go here
        self.health = 300  # Or any starting health
        self.max_health = 300
        # Boss Idle images
        self.Idle_list = self.images_loader("graphic/Enemies/Boss/Idle/Idle",14)
        self.scale_image(self.Idle_list,1.35)
        self.Idle_index = 0
        self.image = self.Idle_list[self.Idle_index]

        # Boss Walk images
        self.Walk_list = self.images_loader("graphic/Enemies/Boss/Walk/Walk",15)
        self.scale_image(self.Walk_list,1.35)
        self.Walk_index = 0
        self.flip_enemy(self.Walk_list)

        # Boss Attack_1 images
        self.Attack_1_list = self.images_loader("graphic/Enemies/Boss/Attack_1/Attack",11)
        self.scale_image(self.Attack_1_list,1.35)
        self.Attack_1_index = 0

        # Boss Attack_2 images
        self.Attack_2_list = self.images_loader("graphic/Enemies/Boss/Attack_2/Attack",14)
        self.scale_image(self.Attack_2_list,1.35)
        self.Attack_2_index = 0

        # Boss Attack_3 images
        self.Attack_3_list = self.images_loader("graphic/Enemies/Boss/Attack_3/Attack",10)
        self.scale_image(self.Attack_3_list,1.35)
        self.Attack_3_index = 0
        
        self.ground_y = 900  # whatever your ground level is
        self.rect = self.image.get_rect(midbottom=(1500, self.ground_y))
        self.hitbox = self.rect.inflate(-100, -50)

        # Direction, timing, and attack control
        self.Direction = True
        self.attack_time = 0
        self.attack_cooldown = 2000  # ms
        self.is_attacking = False
        self.just_attacked = False

        # Flip all Boss animations when changing direction
    def Boss_flip_Animation(self):
        self.Idle_list = self.flip_enemy(self.Idle_list)
        self.Walk_list = self.flip_enemy(self.Walk_list)
        self.Attack_1_list = self.flip_enemy(self.Attack_1_list)
        self.Attack_2_list = self.flip_enemy(self.Attack_2_list)
        self.Attack_3_list = self.flip_enemy(self.Attack_3_list)

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

    def Enemy_AI(self, player):
    # Distance between player and boss
        distance = abs(player.rect.x - self.rect.x)
         
        # Boss moves toward player if within 800px but farther than 300px
        if 800 > distance > 300:
            if player.rect.x > self.rect.x:
                self.rect.x += 2  # Move right
            else:
                self.rect.x -= 2  # Move left

        # When player is close enough, boss stops and prepares to attack
        if distance <= 300:
            self.rect.x = self.rect.x  # Stop movement
            self.attack_Cooldown()

        # Flip direction when player crosses over
        if player.rect.x > self.rect.x and not self.Direction: # Player is right, Boss is Left
            self.Direction = True # Change state to Right
            self.Boss_flip_Animation()
        elif player.rect.x < self.rect.x and self.Direction: # Player is left, Boss is Right
            self.Direction = False # Change state to Left
            self.Boss_flip_Animation()


    def attack_Cooldown(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.attack_time >= self.attack_cooldown:
            self.is_attacking = True
            self.attack_time = current_time


    def Animation_state(self, player):
        distance = abs(player.rect.x - self.rect.x)
        bottom = self.rect.bottom
        # Walking animation when approaching player
        if 800 > distance > 300:
            self.Walk_index += 0.1
            if self.Walk_index >= len(self.Walk_list):
                self.Walk_index = 0
            self.image = self.Walk_list[int(self.Walk_index)]
            self.rect = self.image.get_rect(midbottom=(self.rect.centerx, self.ground_y))
        # Attack animation when close
        elif distance <= 300:
            if self.is_attacking:
                # Randomly choose one of 3 attack animations for variety
                if not hasattr(self, "current_attack"):
                    self.current_attack = random.choice([1, 2, 3])

                if self.current_attack == 1:
                    anim_list = self.Attack_1_list
                    self.Attack_1_index += 0.15
                    if self.Attack_1_index >= len(anim_list):
                        self.Attack_1_index = 0
                        self.is_attacking = False
                        self.just_attacked = True
                        del self.current_attack
                    self.image = anim_list[int(self.Attack_1_index)]
                    self.rect = self.image.get_rect(midbottom=(self.rect.centerx, self.ground_y + 200))

                elif self.current_attack == 2:
                    anim_list = self.Attack_2_list
                    self.Attack_2_index += 0.15
                    if self.Attack_2_index >= len(anim_list):
                        self.Attack_2_index = 0
                        self.is_attacking = False
                        self.just_attacked = True
                        del self.current_attack
                    self.image = anim_list[int(self.Attack_2_index)]
                    self.rect = self.image.get_rect(midbottom=(self.rect.centerx, self.ground_y + 200))

                elif self.current_attack == 3:
                    anim_list = self.Attack_3_list
                    self.Attack_3_index += 0.15
                    if self.Attack_3_index >= len(anim_list):
                        self.Attack_3_index = 0
                        self.is_attacking = False
                        self.just_attacked = True
                        del self.current_attack
                    self.image = anim_list[int(self.Attack_3_index)]
                    self.rect = self.image.get_rect(midbottom=(self.rect.centerx, self.ground_y + 200))

        # Idle animation when player is far
        else:
            self.Idle_index += 0.1
            if self.Idle_index >= len(self.Idle_list):
                self.Idle_index = 0
            self.image = self.Idle_list[int(self.Idle_index)]
            self.rect = self.image.get_rect(midbottom=(self.rect.centerx, self.ground_y))


    def update(self,player):
        self.just_attacked = False
        self.Enemy_AI(player)
        self.Animation_state(player)
        self.hitbox.midbottom = self.rect.midbottom

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
class Level:
    def __init__(self, screen, player, projectile_group):
        self.screen = screen
        self.player = player
        self.projectile_group = projectile_group
        self.current_level = 1
        self.enemy_group = pygame.sprite.Group()
        self.transitioning = False

        # Backgrounds for each level
        self.backgrounds = [
            "graphic/Background/background.png",
            "graphic/Background/background2.png",
            "graphic/Background/background3.png"
        ]

        # Optional background music per level
        self.music = [
            "audio/level1.mp3",
            "audio/level2.mp3",
            "audio/level3.mp3"
        ]

        self.load_level(self.current_level)

    def load_level(self, level_num):
        """Load a specific level: background, enemies, and music."""
        self.enemy_group.empty()
        self.projectile_group.empty()

        # Background
        idx = min(level_num - 1, len(self.backgrounds) - 1)
        bg_path = self.backgrounds[idx]
        self.bg_image = pygame.image.load(bg_path).convert()
        self.bg_image = pygame.transform.scale(
            self.bg_image,
            (int(self.bg_image.get_width() * 0.8), int(self.bg_image.get_height() * 0.8))
        )

        # Spawn enemies
        if level_num == 1:
            self.enemy_group.add(Knight())
        elif level_num == 2:
            self.enemy_group.add(wizard(self.projectile_group, self.player.sprite))
        elif level_num == 3:
            boss = Knight()
            boss.health = 200
            boss.rect.centerx += 200
            self.enemy_group.add(boss)


    def update(self):
        """Draw and update the current level."""
        self.screen.blit(self.bg_image, (0, 0))

        # Enemies and projectiles
        self.enemy_group.update(self.player.sprite)
        self.enemy_group.draw(self.screen)
        self.projectile_group.update()
        self.projectile_group.draw(self.screen)

        # Draw enemy health bars
        for enemy in self.enemy_group:
            enemy.draw_health_bar(self.screen)

        # Check if all enemies defeated
        if not self.enemy_group and not self.transitioning:
            self.transitioning = True
            pygame.time.set_timer(pygame.USEREVENT + 1, 1500)  # 1.5 s delay

    def handle_transition(self, event):
        """Move to next level when timer event fires."""
        if event.type == pygame.USEREVENT + 1 and self.transitioning:
            pygame.time.set_timer(pygame.USEREVENT + 1, 0)
            self.current_level += 1
            self.transitioning = False
            self.load_level(self.current_level)
# Background_1 = pygame.image.load('graphic/Background/background.png')
# scale_factor = 0.8
# x = int(Background_1.get_width() * scale_factor)
# y = int(Background_1.get_height() * scale_factor)
# Background_1 = pygame.transform.scale(Background_1, (x, y))

player = pygame.sprite.GroupSingle()
player.add(Player())
Enemy_Group = pygame.sprite.Group()
Enemy_Group.add(Knight())
projectile_group = pygame.sprite.Group() 
game_stage = 'knight' 
pause_menu = PauseMenu(screen)
Game_Active = True
font = pygame.font.Font(None , 150) 
small_font = pygame.font.Font(None,60)
win_text = font.render("YOU WIN", True, (0, 255, 0)) 

# Boss_enemy = pygame.sprite.GroupSingle()
# Boss_enemy.add(Boss())
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
                pause_menu.draw()
                Game_Active = True
                

    if Game_Active:
        if pause_menu.is_paused:
            pause_menu.draw()
        else:
                screen.blit(Background_1, (0, 0))

                if not Enemy_Group and game_stage == 'knight':
                    game_stage = 'wizard'
                    Enemy_Group.add(wizard(projectile_group, player.sprite))

                elif not Enemy_Group and game_stage == 'wizard':
                    game_stage = 'boss'
                    Enemy_Group.add(Boss())

                Enemy_Group.update(player.sprite)
                projectile_group.update()
                player.update()
                
                Enemy_Group.draw(screen)
                projectile_group.draw(screen)
                player.draw(screen)
                
                player_sprite = player.sprite

        for enemy in Enemy_Group:
            if isinstance(enemy, Knight):
                if enemy.just_attacked and player_sprite.hitbox.colliderect(enemy.hitbox):
                    player_sprite.health -= 15 
                if player_sprite.is_attacking and abs(enemy.rect.centerx - player_sprite.rect.centerx) < 200:
                    enemy.take_damage(0.8)         
            elif isinstance(enemy, wizard):
                if player_sprite.is_attacking and player_sprite.hitbox.colliderect(enemy.hitbox):
                    enemy.take_damage(0.8) 

            elif isinstance(enemy, Boss):
                    if enemy.just_attacked and player_sprite.hitbox.colliderect(enemy.hitbox):
                        player_sprite.health -= 25 
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
        elif not Enemy_Group and game_stage == 'boss': 
                Game_Active = False
        
        
    else:
        screen.fill((0, 0, 0))  
        if player.sprite.health <= 0:
            game_over_text = font.render("GAME OVER", True, (255, 0, 0))
            game_over_rect = game_over_text.get_rect(center=(info.current_w // 2, info.current_h // 2 - 100))
            knight_win=pygame.mixer.Sound('audio/knight_win.mp3')
            screen.blit(game_over_text, game_over_rect)
        else:
            win_rect = win_text.get_rect(center=(info.current_w // 2, info.current_h // 2 - 100))
            screen.blit(win_text, win_rect)
        restart_text = small_font.render("Press 'R' to Restart", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(info.current_w // 2, info.current_h // 2 + 50))
        player_win=pygame.mixer.Sound('audio/player_win.mp3')
        screen.blit(restart_text, restart_rect)
        
        if player.sprite.health <= 0:
            player.sprite.reset()
        
    pygame.display.update()
    clock.tick(60)

