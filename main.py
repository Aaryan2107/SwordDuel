import pygame
import math  
import random  as random

from Settings import PauseMenu,MainMenu,SettingsMenu,keybinds,info
from Enemy import Enemy
from player import Player
from Knight import Knight
from level import Level
from Boss import Boss
from wizard import wizard

from sys import exit


screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.NOFRAME)

clock = pygame.time.Clock()



Background_1 = pygame.image.load('graphic/Background/background.png')
scale_factor = 0.8
x = int(Background_1.get_width() * scale_factor)
y = int(Background_1.get_height() * scale_factor)
Background_1 = pygame.transform.scale(Background_1, (x, y))

player = pygame.sprite.GroupSingle()
player.add(Player())
projectile_group = pygame.sprite.Group() 
level_manager = Level(screen, player, projectile_group)

# Menus
pause_menu = PauseMenu(screen)
main_menu = MainMenu(screen)

# keybinds



settings_menu = SettingsMenu(screen, keybinds)

# Game states
Game_Active = False
main_menu_active = True
settings_menu_active = False # NEW state

# Fonts and text
font = pygame.font.Font(None , 150) 
small_font = pygame.font.Font(None,60)
win_text = font.render("YOU WIN", True, (0, 255, 0)) 

# restart game logic
def reset_game():
    player.sprite.reset() 
    projectile_group.empty() 

    # Reset the level manager
    level_manager.current_level = 1
    level_manager.load_level(1) # This will load level 1 and reset player
    level_manager.transitioning = False
    level_manager.win_triggered = False
    
    pause_menu.is_paused = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if main_menu_active:
            # Handle input for the main menu
            action = main_menu.handle_input(event)
            if action == 'start':
                main_menu_active = False
                Game_Active = True
                reset_game()
            elif action == 'options':
                main_menu_active = False
                settings_menu_active = True
                
            elif action == 'quit':
                pygame.quit()
                exit()
            elif action == 'quit':
                pygame.quit()
                exit()

        elif settings_menu_active:
            action = settings_menu.handle_input(event)
            if action == 'main_menu':
                settings_menu_active = False
                main_menu_active = True

        elif Game_Active:
            if not pause_menu.is_paused:
                # Handle level transition event
                level_manager.handle_transition(event)
            # Handle input during the game for pause
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause_menu.is_paused = not pause_menu.is_paused 

            if pause_menu.is_paused:
                # Handle input for the pause menu
                action = pause_menu.handle_input(event)
                if action == 'main_menu':
                    Game_Active = False
                    main_menu_active = True

        elif not Game_Active and not main_menu_active:
            # Handle input on the "Game Over" or "You Win" screen
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    Game_Active = True
                    reset_game()
                elif event.key == pygame.K_m:
                    main_menu_active = True

    if main_menu_active:
        # Draw the main menu
        main_menu.draw(Background_1)

    elif settings_menu_active:
        # Draw the main menu as a background, then the settings menu on top
        main_menu.draw(Background_1)
        settings_menu.draw()

    elif Game_Active:
        if pause_menu.is_paused:
            # Draw the game in the background, then the menu on top
            level_manager.draw()
            player.draw(screen)
            player.sprite.Draw_Flasks(screen)
            player.sprite.draw_health_bar(screen)
            player.sprite.draw_health_bar(screen)
            # Draw pause menu last
            pause_menu.draw()
        else:
            level_manager.update_logic()
            
            # Update player logic only if not transitioning
            if not level_manager.transitioning:
                player.update()

            # Draw everything
            level_manager.draw()

            # Draw player and health bar only if not transitioning
            if not level_manager.transitioning:
                player.draw(screen)
                player.sprite.Draw_Flasks(screen)
                player.sprite.draw_health_bar(screen)

                # collision and damage logic
                player_sprite = player.sprite

                # using level_manager.enemy_group
                for enemy in level_manager.enemy_group:
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

                # using level_manager.projectile_group
                for proj in level_manager.projectile_group:
                    # Only check for collisions if the projectile hasn't been deflected
                    if not proj.deflected:
                        # 1. Check for Deflection
                        if player_sprite.is_attacking and player_sprite.rect.colliderect(proj.hitbox):
                            proj.deflect()
                            # 2. Check for Damage (if it wasn't deflected)
                        elif player_sprite.hitbox.colliderect(proj.hitbox):
                            player_sprite.health -= 10 
                            proj.kill()

                for enemy in level_manager.enemy_group:
                    if isinstance(enemy, wizard): 
                        for proj in level_manager.projectile_group:
                            if enemy.hitbox.colliderect(proj.hitbox) and proj.deflected:
                                enemy.take_damage(25) 
                                proj.kill() 

            # checking win or lose
            if player.sprite.health <= 0:
                Game_Active = False
            elif level_manager.win_triggered: 
                Game_Active = False
            
    else: 
        # Draw the "Game Over" or "You Win" screen
        screen.fill((0, 0, 0)) 
        
        if player.sprite.health <= 0:
            # Player lost
            game_over_text = font.render("GAME OVER", True, (255, 0, 0))
            game_over_rect = game_over_text.get_rect(center=(info.current_w // 2, info.current_h // 2 - 100))
            screen.blit(game_over_text, game_over_rect)
        else:
            # Player won
            win_rect = win_text.get_rect(center=(info.current_w // 2, info.current_h // 2 - 100))
            screen.blit(win_text, win_rect)
        
        # Draw restart and menu options
        restart_text = small_font.render("Press 'R' to Restart", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(info.current_w // 2, info.current_h // 2 + 50))
        screen.blit(restart_text, restart_rect)
        
        menu_text = small_font.render("Press 'M' for Menu", True, (255, 255, 255))
        menu_rect = menu_text.get_rect(center=(info.current_w // 2, info.current_h // 2 + 110))
        screen.blit(menu_text, menu_rect)
        
    pygame.display.update()
    clock.tick(60)
