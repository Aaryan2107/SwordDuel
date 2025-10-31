if player.rect.x > self.rect.x and not self.Direction: # Player is right, Boss is Left
            self.Direction = True # Change state to Right
            self.Boss_flip_Animation()
        elif player.rect.x < self.rect.x and self.Direction: # Player is left, Boss is Right
            self.Direction = False # Change state to Left
            self.Boss_flip_Animation()
