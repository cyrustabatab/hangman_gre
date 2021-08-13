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
        
        self.words = pd.read_csv(words,index_col=0).index

        self.word_text = self.font.render("WORD:",True,BLACK)
        self.guess_text = self.font.render("GUESS:",True,BLACK)
        self.font.set_underline(True)
        self.letters_guessed_text = self.font.render("LETTERS GUESSED",True,BLACK)
        self.letter_used_start = None
        self.font.set_underline(False)
        self.letter_already_used_text = self.font.render("LETTER ALREADY GUESSED",True,RED)
        
        
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
        self.lives = 6
        self.guess = ''
        self.user_guess_text =self.font.render(self.guess,True,BLACK)
        self.letters_used = []
        self.letters_used_text = None



    
    
    

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

        
        if self.letters_used_text:
            screen.blit(self.letters_used_text,(left_x,y + 100))

        if self.letter_used_start:
            screen.blit(self.letter_already_used_text,(left_x,y + 350))




    
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
        


        





    def _play(self):

        
        self._setup()
        

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
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




