import pygame
from Enemy import Enemy

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