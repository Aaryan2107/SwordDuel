import pygame
import Settings as info
import Settings as screen_width
import Settings as screen_height
import math
from Enemy import Enemy
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
        self.destination_x = info.screen_width - 300 
        self.rect = self.image.get_rect(midbottom = (info.screen_width + 200, 945)) 
        
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
        if self.rect.bottom < 0 or self.rect.top > info.screen_height or \
           self.rect.right < 0 or self.rect.left > info.screen_width:
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