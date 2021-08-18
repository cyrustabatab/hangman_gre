import pygame
import time
pygame.init()
import sys
import pandas as pd
import random
import math


SCREEN_WIDTH =1200 
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

pygame.display.set_caption("HANGMAN")
clock = pygame.time.Clock()
WHITE = (255,) * 3
BLACK = (0,) * 3
RED = (255,0,0)
GREEN = (0,255,0)


class Button(pygame.sprite.Sprite):


    def __init__(self,text,x,y,button_color,text_color,font,button_width=None,button_height=None,centered_x=False):
        super().__init__()

        text = font.render(text,True,text_color)
        
        if button_width is None:
            button_width = text.get_width()
        if button_height is None:
            button_height = text.get_height()

        if centered_x:
            x = SCREEN_WIDTH//2 - button_width//2


        self.image = pygame.Surface((button_width,button_height))
        self.image.fill(button_color)

        self.image.blit(text,(self.image.get_width()//2 - text.get_width()//2,self.image.get_height()//2 - text.get_height()//2))


        self.rect = self.image.get_rect(topleft=(x,y))


    def clicked_on(self,point):
        return self.rect.collidepoint(point)








class Menu:


    def __init__(self):

        self._start()


    def _start(self):



        while True:


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            
            screen.fill(WHITE)
            pygame.display.update()




class Game:


    line_thickness = 4 
    font = pygame.font.SysFont("calibri",40,bold=True)
    def __init__(self,words="words.csv"):
        
        self.definitions = pd.read_csv(words,index_col=0)
        self.words = self.definitions.index

        self.word_text = self.font.render("WORD:",True,BLACK)
        self.guess_text = self.font.render("GUESS:",True,BLACK)
        self.font.set_underline(True)
        self.letters_guessed_text = self.font.render("LETTERS GUESSED",True,BLACK)
        self.letter_used_start = None
        self.font.set_underline(False)
        self.letter_already_used_text = self.font.render("LETTER ALREADY GUESSED",True,RED)
        self.you_win_text = self.font.render("YOU GUESSED IT!",True,GREEN)
        self.hint_button = pygame.sprite.GroupSingle(Button("HINT",None,250,BLACK,WHITE,self.font,centered_x=True))
        self.score_text = self.font.render("0",True,BLACK)
        
        
        self._play()
    

    def _choose_word(self):


        return random.choice(self.words)
    

    def _draw_hangman(self):


        pygame.draw.line(screen,BLACK,(20,SCREEN_HEIGHT),(20,20),self.line_thickness)
        pygame.draw.line(screen,BLACK,(20,20),(220,20),self.line_thickness)
        pygame.draw.line(screen,BLACK,(120,20),(120,70),self.line_thickness)
        
        radius = 50
        if self.lives >= 1:
            pygame.draw.circle(screen,BLACK,(120,70 + radius),radius,self.line_thickness)
            pygame.draw.circle(screen,BLACK,(100,70 + radius -10),self.line_thickness)
            pygame.draw.circle(screen,BLACK,(140,70 + radius -10),self.line_thickness)

            pygame.draw.circle(screen,BLACK,(120,75 + radius + 20),20,1)
        

        if self.lives >=  2:
            pygame.draw.line(screen,BLACK,(120,170),(120,370),self.line_thickness)

        if self.lives >= 3:
            pygame.draw.line(screen,BLACK,(120,220),(180,270),self.line_thickness)


        if self.lives >= 4:
            pygame.draw.line(screen,BLACK,(120,220),(60,270),self.line_thickness)


        if self.lives >= 5:
            pygame.draw.line(screen,BLACK,(120,370),(60,420),self.line_thickness)

        if self.lives == 6:
            pygame.draw.line(screen,BLACK,(120,370),(180,420),self.line_thickness)
    
    def _setup(self):

        self.word = self._choose_word()
        self.guesses = [None] * len(self.word)
        self.definition_text = self.font.render(self.definitions.loc[self.word,'definition'],True,BLACK)
        self.show_definition = False
        self.lives = 6
        self.guess = ''
        self.game_over = False
        self.user_guess_text =self.font.render(self.guess,True,BLACK)
        self.letters_used = []
        self.letters_used_text = None
        self.score = 0



    
    
    

    def _draw_guesses(self):


        
        left_x = 400
        y = 100
        screen.blit(self.word_text,(left_x - self.word_text.get_width() - 5,y - self.word_text.get_height()))
        gap = 20
        length = 25
        for i,guess in enumerate(self.guesses):
            pygame.draw.line(screen,BLACK,(left_x + gap +  i * (length + gap),y),(left_x + gap + i * (length + gap) + length,y),self.line_thickness)
            if guess:
                screen.blit(guess,(left_x + gap + i * (length + gap) + length//2 -  guess.get_width()//2,y - guess.get_height()))



        screen.blit(self.guess_text,(left_x - self.guess_text.get_width() - 5,y + 250))
        screen.blit(self.user_guess_text,(left_x + 20,y + 250))
        screen.blit(self.letters_guessed_text,(left_x,y + 50))
        
        if not self.game_over and self.lives <= 3:
            self.hint_button.draw(screen)
        
        if self.show_definition:
            screen.blit(self.definition_text,(SCREEN_WIDTH//2 - self.definition_text.get_width()//2,y + 350))

        
        if self.letters_used_text:
            screen.blit(self.letters_used_text,(left_x,y + 100))

        if self.letter_used_start:
            screen.blit(self.letter_already_used_text,(SCREEN_WIDTH//2 - self.letter_already_used_text.get_width()//2,y + 350))
        elif self.game_over:
            screen.blit(self.game_over_text,(SCREEN_WIDTH//2 - self.game_over_text.get_width()//2,y + 350))

        screen.blit(self.score_text,(SCREEN_WIDTH - self.score_text.get_width(),2))


    
    def _check_guess(self):
        
        if self.letter_used_start:
            self.letter_used_start = None
        
        if self.guess in self.letters_used:
            self.letter_used_start = time.time()
            return
        found = False
        for i,c in enumerate(self.word):
            if c == self.guess:
                self.guesses[i] = self.font.render(c,True,BLACK)
                found = True
        


        self.letters_used.append(self.guess)
        self.letters_used_text = self.font.render(','.join(self.letters_used),True,BLACK)
        

        if not found:
            self.lives -= 1
            if self.lives == 0:
                self._show_missed_guesses()
                self.game_over_start_time = time.time()
                self.game_over_text = self.font.render(f"Sorry! The word was {self.word}",True,RED)
                self.game_over = True
                self.show_definition = False
        elif None not in self.guesses:
                self.game_over_start_time = time.time()
                self.game_over_text = self.you_win_text
                self.score += 1
                self.score_text = self.font.render(f"{self.score}",True,BLACK)
                self.game_over = True
                self.show_definition = False
        
                


        
    def _show_missed_guesses(self):



        for i,c in enumerate(self.guesses):
            if c is None:
                self.guesses[i] = self.font.render(self.word[i],True,RED)

        





    def _play(self):

        
        self._setup()
        

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if not self.game_over:
                        if not self.guess and pygame.K_a <= event.key <= pygame.K_z:
                            self.guess += chr(event.key)
                            self.user_guess_text = self.font.render(self.guess,True,BLACK)
                        elif event.key == pygame.K_BACKSPACE:
                            self.guess = ''
                            self.user_guess_text = self.font.render(self.guess,True,BLACK)
                        elif self.guess and event.key == pygame.K_RETURN:
                            self._check_guess()
                            self.guess= ''
                            self.user_guess_text = self.font.render(self.guess,True,BLACK)
                    elif event.key == pygame.K_RETURN:
                        self._setup()




            

            if not self.game_over and self.lives <= 3:
                point = pygame.mouse.get_pos()

                if self.hint_button.sprite.clicked_on(point):
                    self.show_definition = True
                else:
                    self.show_definition = False
        

            if self.letter_used_start:
                current_time = time.time()
                if current_time - self.letter_used_start >= 2:
                    self.letter_used_start = None









        
            screen.fill(WHITE)
            self._draw_hangman()
            self._draw_guesses()
            

            pygame.display.update()









if __name__ == "__main__":



    Game()




