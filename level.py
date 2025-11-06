import pygame
from Boss import Boss
from wizard import wizard
from Knight import Knight

class Level:
    def __init__(self, screen, player, projectile_group):
        self.screen = screen
        self.player = player
        self.projectile_group = projectile_group
        self.current_level = 1
        self.enemy_group = pygame.sprite.Group()
        self.transitioning = False
        self.win_triggered = False # Flag to signal the game is won
        self.font = pygame.font.Font(None, 80) # Font for transition text


    # Backgrounds for each level
        self.backgrounds = [
            "graphic/Background/background.png", 
            "graphic/Background/background1.png", 
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
        self.player.sprite.reset() 
        self.enemy_group.empty()
        self.projectile_group.empty()

        # Background
        # Use user-specified backgrounds
        if level_num == 1:
            bg_path = self.backgrounds[0]
        elif level_num == 2:
            bg_path = self.backgrounds[1]
        elif level_num == 3:
            bg_path = self.backgrounds[2]
        else:
            bg_path = self.backgrounds[0] # Default

        self.bg_image = pygame.image.load(bg_path).convert()
        self.bg_image = pygame.transform.scale(self.bg_image,
                                               (int(self.bg_image.get_width() * 0.8),
                                                 int(self.bg_image.get_height() * 0.8)))

        # Spawn enemies
        if level_num == 1:
            self.enemy_group.add(Knight())
        elif level_num == 2:
            self.enemy_group.add(wizard(self.projectile_group, self.player.sprite))
        elif level_num == 3:
            boss = Boss()
            boss.health = 200 
            boss.rect.centerx += 200
            self.enemy_group.add(boss)

    def update_logic(self):
        if self.transitioning or self.win_triggered:
            return

        # Enemies and projectiles
        self.enemy_group.update(self.player.sprite)
        self.projectile_group.update()

        # Check if all enemies defeated
        if not self.enemy_group and not self.transitioning:
            self.transitioning = True
            # 2 second delay 
            pygame.time.set_timer(pygame.USEREVENT + 1, 2000) 

    def draw(self):
        # draw black screen
        if self.transitioning:
            self.screen.fill((0, 0, 0))
            cleared_text = self.font.render("Level Cleared", True, (255, 255, 255))
            text_rect = cleared_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            self.screen.blit(cleared_text, text_rect)
            return # Don't draw anything else
        
        self.screen.blit(self.bg_image, (0, 0))
        self.enemy_group.draw(self.screen)
        self.projectile_group.draw(self.screen)

        # Draw enemy health bars
        for enemy in self.enemy_group:
            enemy.draw_health_bar(self.screen)

    def handle_transition(self, event):
        """Move to next level when timer event fires."""
        if event.type == pygame.USEREVENT + 1 and self.transitioning:
            pygame.time.set_timer(pygame.USEREVENT + 1, 0) # Clear the timer
            self.current_level += 1
            self.transitioning = False
            if self.current_level==1:
                Knight_entery = pygame.mixer.Sound('audio/knight_entery.mp3')
                Knight_entery.play(0)
            elif self.current_level==2:
                wizard_entery = pygame.mixer.Sound('audio/witch_entery.mp3')
                wizard_entery.play(0)
            elif self.current_level==3:
                Boss_entery = pygame.mixer.Sound('audio/boss_entery.mp3')
                Boss_entery.play(0)

            if self.current_level > 3: # Boss was level 3
                self.win_triggered = True # Signal the win
            else:
                self.load_level(self.current_level)
