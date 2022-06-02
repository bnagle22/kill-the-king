# killTheKing.py
# Pawn vs. King

# You control the pawn and you need to shoot the king with lasers to win.

import pygame, random
from random import randint
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
pygame.mixer.init()

WIDTH = 845
HEIGHT = 775

PAWNLIVES = 3
KINGLIVES = 10
NUMLASERS = 1000

BROWN = (128,74,36)
WHITE = (255,255,255)


#Construct screen and set caption
screen = pygame.display.set_mode((WIDTH,HEIGHT))    
pygame.display.set_caption("Benjamin Nagle")


#Create pawn sprite- this is the piece that the user controls
class Pawn(pygame.sprite.Sprite):
    
    #Initialize sprite and load image
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("newpawn.png")
        self.image = self.image.convert()

        aColor = self.image.get_at((0,22))
        self.image.set_colorkey(aColor)

        self.image = pygame.transform.scale(self.image, (60,80))
        self.rect = self.image.get_rect();
        self.rect.center = (392,680)
    def update(self):
        pass

    # These functions move the pawn 80 pixels up, down, left, or right,
    # but only on the first two rows of the chessboard
    def moveup(self):
        if (self.rect.top > screen.get_height()-150):
            self.rect.centery -= 80

    def movedown(self):
        if (self.rect.bottom < screen.get_height()-75):
            self.rect.bottom += 80

    def moveleft(self):
        if (self.rect.left > 200):
            self.rect.left -= 80

    def moveright(self):
        if (self.rect.right < screen.get_width()-150):
            self.rect.right += 80
            
    #Returns the center, which is used later for collisions and shooting lasers
    def get_pos(self):
        return self.rect.center

#Create king sprite- this piece moves randomly and shoots randomly
class King(pygame.sprite.Sprite):

    #Initialize sprite and load image
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("newking.png")
        self.image = self.image.convert()
        aColor = self.image.get_at((1,1))
        self.image.set_colorkey(aColor)
        self.image = pygame.transform.scale(self.image, (85,85))
        self.rect = self.image.get_rect();
        self.rect.center = (392,125)
        self.frame = 0

    #The update function causes the king to move twice every second, depending
    # on a random number.
    def update(self):
        self.frame +=1
        if self.frame >= 15:
            self.frame =0
            self.kmove()
            
    #The kmove function causes the king to move 80 pixels up, down, left, or
    # right, depending on a random number. He is more likely to move sideways.
    def kmove(self):
        direction = random.randint(1,8)

        if direction == 1:
            if self.rect.top > 120:
                self.rect.top -= 80
        if direction == 2:
            if self.rect.bottom < screen.get_height()-500:
                self.rect.bottom += 80
        if direction == 3 or direction == 4 or direction == 5:
            if self.rect.left >200:
                self.rect.left -= 80
        if direction == 6 or direction == 7 or direction == 8:
            if self.rect.right < screen.get_width()-150:
                self.rect.right += 80

    
    #Returns the center, which is used later for collisions and shooting lasers
    def get_pos(self):
        return self.rect.center
    
#Create laser sprite- this is fired by the pawn
class Laser(pygame.sprite.Sprite):

    #Initialize sprite and load image
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("laser.png")
        self.image = self.image.convert()
        self.image.set_colorkey(self.image.get_at((0,0)))
        self.image = pygame.transform.scale(self.image, (30,30))
        self.rect = self.image.get_rect()
        self.rect.center = (-100, -100)
        self.dy = 0
        self.shooting = False

    #The laser moves while it is being fired
    def update(self):
        if self.shooting:
            self.rect.centery -= self.dy
            
    #The laser resets after it is finished firing
    def reset(self):
        self.rect.center = (-100, -100)
        self.dy = 0
        self.shooting = False

    #The laser is fired from the pawn sprite
    def fire(self, pawn_pos):
        if not self.shooting:
            self.rect.center = pawn_pos
            self.rect.centery -= 5
            self.rect.centerx += 1
            self.dy = 10
            self.shooting = True

#Create laser sprite- this is fired by the king
class KingLaser(pygame.sprite.Sprite):

    #Initialize sprite and load image
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("laser.png")
        self.image = self.image.convert()
        self.image.set_colorkey(self.image.get_at((0,0)))
        self.image = pygame.transform.scale(self.image, (60,60))
        self.rect = self.image.get_rect()
        self.rect.center = (-100, -100)
        self.dy = 0
        self.shooting = False

    #The laser moves while it is being fired
    def update(self):
        if self.shooting:
            self.rect.centery -= self.dy

    #The laser resets after it is finished firing
    def reset(self):
        self.rect.center = (-100, -100)
        self.dy = 0
        self.shooting = False

    #The laser is fired from the king sprite
    def fire(self, king_pos):
        if not self.shooting:
            self.rect.center = king_pos
            self.rect.centery -= 5
            self.rect.centerx += 1
            self.dy = -25
            self.shooting = True
            
#Create label class with text string, pixel location, font type, font size,
# and text color
class Label(pygame.sprite.Sprite):
    
    def __init__(self, textStr, topleft, fontName, fontSize, textColor):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(fontName, fontSize)
        self.text = textStr
        self.topleft = topleft
        self.textColor = textColor

    #Udpate function renders text on the label
    def update(self):
        self.image = self.font.render(self.text, 1, self.textColor)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.topleft

#Create lives class to display lives remaining for the pawn and king
class Lives(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.kLives = KINGLIVES
        self.pLives = PAWNLIVES
        self.score = 0
        fontName = "swash.ttf"
        self.font = pygame.font.Font(fontName, 40)

    def update(self):
        self.text = ("King Lives: " + str(self.kLives) + "   Pawn Lives: " + str(self.pLives))
        self.image = self.font.render(self.text, 1, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.topleft = (20,8)

#Create title screen which displays instructions and plays music.
def titleScreen(background):
    
    #Plays beginning of Tenacious D rock song on a loop
    pygame.mixer.music.load("bee.wav")
    pygame.mixer.music.play()

    #Assign true type font
    fontName = "swash.ttf"

    #Construct labels with instructions for the game
    titleMsg = Label("Kill The King", (200,70), fontName, 60, (255,255,255))
    instr1   = Label("It's the end of an intense game of chess.",
                        (30,200), fontName, 30, (255,255,255))
    instr2   = Label("Somehow, the only pieces left are a pawn and a king.",
                        (30,240), fontName, 30, (255,255,255))
    instr3   = Label("You control the pawn and your goal is to kill the king.",
                        (30,280), fontName, 30, (255,255,255))
    instr4   = Label("Use the arrow keys to move and press space to shoot lasers.",
                         (30,360), fontName, 30, (255,255,255))
    instr5   = Label("The king is also shooting lasers at you, so be careful.",
                         (30, 400), fontName, 30, (255,255,255))
    startMsg = Label("Click to start", (205, 480), fontName, 30, (255,255,255))

    #Add labels to a group
    labelGroup = pygame.sprite.Group(titleMsg, startMsg,
                                     instr1, instr2, instr3, instr4, instr5)
    #Blit background to screen once
    screen.blit(background, (0,0))

    clock = pygame.time.Clock()
    keepGoing = True
    
    #Create loop that allows user to click and move to the game
    while keepGoing:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                keepGoing = False     
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    keepGoing = False

        #Update the display            
        labelGroup.clear(screen, background)
        labelGroup.update()
        labelGroup.draw(screen)

        pygame.display.flip()

#Create end screen that is displayed when the user wins
def endScreen1(background):

    fontName = "swash.ttf"
    
    titleMsg = Label("You killed the king!", (180,30), fontName, 60, (0,0,0))
    instr1   = Label("Thanks for playing",
                        (30,430), fontName, 30, (0,0,0))
    instr2   = Label("Coded by Benjamin Nagle",
                        (30,470), fontName, 30, (0,0,0))
    instr3   = Label("Music:",
                        (30,530), fontName, 30, (0,0,0))
    instr4   = Label("Tenacious D- Beelzeboss (The Final Showdown)",
                         (30,570), fontName, 30, (0,0,0))
    instr5   = Label("Joseph Haydn- Quartet No. 67 in F major, Op. 77, No. 2",
                         (30, 610), fontName, 30, (0,0,0))
    startMsg = Label("Press the spacebar to play again", (205, 670), fontName, 30, (0,0,0))

    labelGroup = pygame.sprite.Group(titleMsg, startMsg,
                                     instr1, instr2, instr3, instr4, instr5)

    #Load image of pawn and king
    endImage = EndImage()
    allsprites = pygame.sprite.Group(endImage)
    background.fill(WHITE)
    screen.blit(background, (0,0))
    
    clock = pygame.time.Clock()
    keepGoing = True
    choice = False
   
    #Allows user to quit
    while keepGoing:
        clock.tick(30)

        for event in pygame.event.get():   
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    keepGoing = False
                    choice = True
                elif event.key == pygame.K_q:
                    keepGoing = False
                    
        labelGroup.clear(screen, background)
        labelGroup.update()
        labelGroup.draw(screen)

        allsprites.clear(screen, background)
        allsprites.update()
        allsprites.draw(screen)

        pygame.display.flip()
    return choice

#Create end screen that is displayed when the user loses
def endScreen2(background):

    fontName = "kanit.ttf"
    
    titleMsg = Label(" Sorry,", (200,80), fontName, 120, (0,0,250))
    instr1   = Label("     you lose",
                        (30,200), fontName, 120, (0,0,250))
    instr2   = Label("     Press the spacebar",
                         (30, 400), fontName, 65, (0,0,250))
    startMsg = Label("to play again", (205, 480), fontName, 65, (0,0,250))

    labelGroup = pygame.sprite.Group(titleMsg, startMsg,
                                     instr1, instr2)
    
    screen.blit(background, (0,0))

    clock = pygame.time.Clock()
    keepGoing = True
    choice = False
    
    #Allows user to quit
    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():   
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    keepGoing = False
                    choice = True
                elif event.key == pygame.K_q:
                    keepGoing = False
                
        labelGroup.clear(screen, background)
        labelGroup.update()
        labelGroup.draw(screen)

        pygame.display.flip()
    return choice
    
#Class is used to load the image of pawn and king on end screen 1
class EndImage(pygame.sprite.Sprite):

    #Initialize and load image
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("pwn+kng.png")
        self.image = self.image.convert()
        aColor = self.image.get_at((0,22))
        self.image.set_colorkey(aColor)
        self.image = pygame.transform.scale(self.image, (440,280))
        self.rect = self.image.get_rect();
        self.rect.center = (480,260)
    def update(self):
        pass

#Plays the game
def game(background):

    #Plays Haydn string quartet during the game
    pygame.mixer.music.load("menuet.wav")
    pygame.mixer.music.play()

    #Loads board background image
    background = pygame.image.load("Board.png").convert()
    screen.blit(background, (0,0))

    #Construct game entities
    pawn = Pawn()
    king = King()
    laser = Laser()
    kLaser = KingLaser()
    lives = Lives()

    #Add sprites to a group
    allsprites = pygame.sprite.Group(pawn, king, laser, kLaser, lives)

    keepGoing=True
    shooting = False
    kshooting = False
    win = False
    
    lasers = NUMLASERS
    kLives = KINGLIVES
    pLives = PAWNLIVES

    clock = pygame.time.Clock()
    background_image = pygame.image.load("Board.png").convert()

    #Event loop allows user to move the pawn and shoot lasers
    while(keepGoing):

        for event in pygame.event.get():
            clock.tick(30)

            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    keepGoing = False
                elif event.key == pygame.K_UP:
                    pawn.moveup()
                elif event.key == pygame.K_DOWN:
                    pawn.movedown()
                elif event.key == pygame.K_LEFT:
                    pawn.moveleft()
                elif event.key == pygame.K_RIGHT:
                    pawn.moveright()
                elif event.key == pygame.K_SPACE:
                    if shooting == False:
                        laser.fire(pawn.get_pos())
                        pLasersound = pygame.mixer.Sound("pLasersound.wav")
                        pLasersound.play()
                        shooting = True

        #The king fires lasers randomly
        number = random.randint(1,80)
        if number == 1:
            if kshooting == False:
                kLaser.fire(king.get_pos())
                kLasersound = pygame.mixer.Sound("kLasersound.wav")
                kLasersound.play()
                kshooting = True
        
        #Check for collisions
        if pygame.sprite.collide_rect(laser, king):
            lives.kLives -= 1
            laser.reset()
            kHit = pygame.mixer.Sound("kHit.wav")
            kHit.play()
        if lives.kLives <= 0:
            keepGoing = False
            win = True

        if pygame.sprite.collide_rect(kLaser, pawn):
            lives.pLives -= 1
            kLaser.reset()
            pHit = pygame.mixer.Sound("pHit.wav")
            pHit.play()
            kshooting = False

        #Check to see if the user loses    
        if lives.pLives <= 0:
            keepGoing = False

        #Resets laser once it moves off the screen     
        if laser.rect.top <= 0:
            shooting = False
            lasers -=1
            laser.reset()
        if kLaser.rect.top >= screen.get_height():
            kshooting = False
            lasers -=1
            kLaser.reset()

        #Update the display
        screen.blit(background_image, [0, 0])
        allsprites.clear(screen, background)
        allsprites.update()
        allsprites.draw(screen)

        pygame.display.flip()
        
    #Determine which end screen to display
    if win:
        return endScreen1(background)
    else:
        return endScreen2(background)
          
#The main function loads the background, runs the title screen, and the game
def main():
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(BROWN)
    screen.blit(background, (0,0))

    clock = pygame.time.Clock()
    
    titleScreen(background)
    
    repeat = True
    while repeat:
        repeat = game(background)

#Call the main function and allow user to quit
main()
pygame.quit()
exit()



    
