import pygame
import random as random
from Enemy import Enemy

class Boss(Enemy):
    def __init__(self):
        super().__init__()
        self.health = 300 
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
        
        self.ground_y = 900  
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
        if 1000 > distance > 300:
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