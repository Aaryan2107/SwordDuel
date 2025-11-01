import pygame
pygame.init()
pygame.mixer.init()
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h
keybinds = {
    'jump': pygame.K_SPACE,
    'move_left': pygame.K_a,
    'move_right': pygame.K_d,
    'slide': pygame.K_LSHIFT,
    'crouch': pygame.K_c,
    'heal': pygame.K_1
}
class PauseMenu:
    def __init__(self, screen):
        self.screen = screen
        self.is_paused = False 
        self.font_big = pygame.font.Font(None, 80)
        self.font_small = pygame.font.Font(None, 50)
    

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
                self.is_paused = False 
                return None
            elif self.exit_rect.collidepoint(mouse_pos):
                self.is_paused = False # Ensure we are not paused when returning
                return 'main_menu'   # Signal to return to the main menu
        return None

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.font_title = pygame.font.Font(None, 120)
        self.font_button = pygame.font.Font(None, 70)
        
        # Title
        self.title_text = self.font_title.render("SWORDDUEL", True, (200, 200, 200))
        self.title_rect = self.title_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 250)) # Adjusted Y

        # Button rectangles
        button_width = 300
        button_height = 80
        button_y_start = self.screen_height // 2 - 100 # Adjusted start Y
        
        # MODIFIED:
        self.start_rect = pygame.Rect(self.screen_width // 2 - button_width // 2, button_y_start, button_width, button_height)
        self.options_rect = pygame.Rect(self.screen_width // 2 - button_width // 2, button_y_start + 100, button_width, button_height)
        self.exit_rect = pygame.Rect(self.screen_width // 2 - button_width // 2, button_y_start + 200, button_width, button_height)

        # Button text
        self.start_text = self.font_button.render("Start Game", True, (255, 255, 255))
        self.options_text = self.font_button.render("Options", True, (255, 255, 255)) # NEW
        self.exit_text = self.font_button.render("Exit Game", True, (255, 255, 255))

    def draw(self, background_image):
        # Draw background and overlay
        self.screen.blit(background_image, (0, 0))
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        # Draw title
        self.screen.blit(self.title_text, self.title_rect)

        # Draw Start button
        pygame.draw.rect(self.screen, (90, 180, 90), self.start_rect, border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255), self.start_rect, 3, border_radius=10)
        self.screen.blit(self.start_text, self.start_text.get_rect(center=self.start_rect.center))

        # Draw Options button (NEW)
        pygame.draw.rect(self.screen, (60, 100, 180), self.options_rect, border_radius=10) # Blue color
        pygame.draw.rect(self.screen, (255, 255, 255), self.options_rect, 3, border_radius=10)
        self.screen.blit(self.options_text, self.options_text.get_rect(center=self.options_rect.center))

        # Draw Exit button
        pygame.draw.rect(self.screen, (180, 60, 60), self.exit_rect, border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255), self.exit_rect, 3, border_radius=10)
        self.screen.blit(self.exit_text, self.exit_text.get_rect(center=self.exit_rect.center))

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if self.start_rect.collidepoint(mouse_pos):
                return 'start'  # Signal to start the game
            
            elif self.options_rect.collidepoint(mouse_pos):
                return 'options' # Signal to open settings
                
            elif self.exit_rect.collidepoint(mouse_pos):
                return 'quit'  # Signal to quit the application
        return None

class SettingsMenu:
    def __init__(self, screen, keybinds):
        self.screen = screen
        self.keybinds = keybinds  # Store a reference to the global keybinds
        self.font_title = pygame.font.Font(None, 100)
        self.font_button = pygame.font.Font(None, 60)
        self.font_info = pygame.font.Font(None, 40)
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        # State for waiting for a new key
        self.waiting_for_key = None

        # Create rectangles for each action
        self.action_rects = {}
        button_width = 500
        button_height = 60
        start_y = self.screen_height // 2 - 200
        
        # List of actions to display
        self.actions = ['jump', 'move_left', 'move_right', 'slide', 'crouch', 'heal']

        for i, action in enumerate(self.actions):
            y_pos = start_y + i * (button_height + 20)
            rect = pygame.Rect(self.screen_width // 2 - button_width // 2, y_pos, button_width, button_height)
            self.action_rects[action] = rect

        # Back button
        self.back_rect = pygame.Rect(self.screen_width // 2 - 150, self.screen_height // 2 + 250, 300, 70)
        self.back_text = self.font_button.render("Back", True, (255, 255, 255))

    def draw(self):
        # Draw a dark overlay 
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        # Title
        title_text = self.font_title.render("Controls", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 100))
        self.screen.blit(title_text, title_rect)

        # Draw each action button
        for action, rect in self.action_rects.items():
            action_display = action.replace('_', ' ').title() # 'move_left' -> 'Move Left'
            
            # Get the name of the currently bound key
            key_code = self.keybinds[action]
            key_name = pygame.key.name(key_code).upper()

            # Format the text
            if self.waiting_for_key == action:
                text_str = f"{action_display}: ...PRESS A KEY..."
                pygame.draw.rect(self.screen, (220, 180, 50), rect, border_radius=10) # yellow
            else:
                text_str = f"{action_display}: {key_name}"
                pygame.draw.rect(self.screen, (80, 80, 100), rect, border_radius=10) # blue/grey
            
            pygame.draw.rect(self.screen, (255, 255, 255), rect, 3, border_radius=10)
            
            text_surf = self.font_button.render(text_str, True, (255, 255, 255))
            self.screen.blit(text_surf, text_surf.get_rect(center=rect.center))

        # Draw Back button
        pygame.draw.rect(self.screen, (180, 60, 60), self.back_rect, border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255), self.back_rect, 3, border_radius=10)
        self.screen.blit(self.back_text, self.back_text.get_rect(center=self.back_rect.center))

    def handle_input(self, event):
        # If we are waiting for a key, the next keydown event is our new bind
        if self.waiting_for_key:
            if event.type == pygame.KEYDOWN:
                # Rebind the key in the dictionary
                self.keybinds[self.waiting_for_key] = event.key
                self.waiting_for_key = None # Stop waiting
            return None # Ignore other events like mouse clicks while waiting

        # If not waiting, check for mouse clicks on buttons
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if self.back_rect.collidepoint(mouse_pos):
                return 'main_menu'
            
            # Check if any action rect was clicked
            for action, rect in self.action_rects.items():
                if rect.collidepoint(mouse_pos):
                    self.waiting_for_key = action # Start waiting
                    return None
        
        return None