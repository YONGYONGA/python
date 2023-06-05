import random
import pygame
import os
pygame.init()
fps = pygame.time.Clock()
screenWidth = 900
screenHeight = 900
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
current_path = os.path.dirname(__file__)
assets_path = os.path.join(current_path, 't')
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('hang')
HANGMAN_PICS = [pygame.image.load(os.path.join(assets_path, '1.png')),
pygame.image.load(os.path.join(assets_path, '2.png')),
pygame.image.load(os.path.join(assets_path, '3.png')),
pygame.image.load(os.path.join(assets_path, '4.png')),
pygame.image.load(os.path.join(assets_path, '5.png')),
pygame.image.load(os.path.join(assets_path, '6.png')),
pygame.image.load(os.path.join(assets_path, '7.png'))]
words = 'ant baboon badger bat bear beaver camel cat clam cobra cougar coyote crow deer dog donkey duck eagle ferret fox frog goat goose hawk lion lizard llama mole monkey moose mouse mule newt otter owl panda parrot pigeon python rabbit ram rat raven rhino salmon seal shark sheep skunk sloth snake spider stork swan tiger toad trout turkey turtle weasel whale wolf wombat zebra'.split()
font = pygame.font.SysFont('FixedSys', 40, True, False)
def getRandomWord(wordList):
    # This function returns a random string from the passed list of strings.
    wordIndex = random.randint(0, len(wordList) - 1)
    return wordList[wordIndex]

def displayBoard(missedLetters, correctLetters, secretWord):
    #print(HANGMAN_PICS[len(missedLetters)])
    global for_sound
    screen.blit(HANGMAN_PICS[len(missedLetters)], [10, 10])
    if(len(missedLetters)!=for_sound):
        sound.play()
        for_sound+=1
    #print()
    miss='Missed letters: '

    #print('Missed letters:', end=' ')
    for letter in missedLetters:
        miss+=letter+" "
     #   print(letter, end=' ')
    #print()


    text = font.render(miss, True, BLACK)
    screen.blit(text, [50, 400])

    blanks = '_' * len(secretWord)
    blan=""
    for i in range(len(secretWord)): # replace blanks with correctly guessed letters
        if secretWord[i] in correctLetters:
            blanks = blanks[:i] + secretWord[i] + blanks[i+1:]

    for letter in blanks: # show the secret word with spaces in between each letter
       # print(letter, end=' ')
        blan+=letter+" "
    text = font.render(blan, True, BLACK)
    screen.blit(text, [50, 450])
    pygame.display.flip()
    #print()

def getGuess(alreadyGuessed):
    # Returns the letter the player entered. This function makes sure the player entered a single letter and not something else.
    """while True:
     #   print('Guess a letter.')
        guess = input()
        guess = guess.lower()
        if len(guess) != 1:
      #      print('Please enter a single letter.')
        elif guess in alreadyGuessed:
       #     print('You have already guessed that letter. Choose again.')
        elif guess not in 'abcdefghijklmnopqrstuvwxyz':
        #    print('Please enter a LETTER.')
        else:
            return guess"""

def playAgain():
    # This function returns True if the player wants to play again; otherwise, it returns False.
    #print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')

pygame.mixer.music.load(os.path.join(assets_path, 'bgm.wav'))
pygame.mixer.music.play(-1) 
sound = pygame.mixer.Sound(os.path.join(assets_path, 'sound.wav'))
crab=pygame.mixer.Sound(os.path.join(assets_path, 'crap.wav'))
uu=pygame.mixer.Sound(os.path.join(assets_path, 'uuu.wav'))
#print('H A N G M A N')
missedLetters = ''
correctLetters = ''
secretWord = getRandomWord(words)
gameIsDone = False
yes=""
message=""
message2=""
guess=""
gamerealDone=False
foundAllLetters=False
screen.fill(WHITE)
for_sound=0
one=0
while True:
    if(gamerealDone):
        break

    displayBoard(missedLetters, correctLetters, secretWord)
    guess=""
    yes=""
    message=""
    message2=""
    # Let the player enter a letter.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gamerealDone=True
            break
        elif event.type == pygame.KEYDOWN:
            screen.fill(WHITE)
            if event.key >= 97 and event.key<=122:
                if(gameIsDone ==False):
                    yes=chr(event.key)

                    #print("감지는함")
                    if(yes in (missedLetters + correctLetters)):
                        message="({}) is already guessed that letter.".format(yes)
                        message2="Choose again."
                        guess=""
                        yes=""
                    else:
                        message=""
                        yes=yes.lower()
                        guess=yes
                else:
                    #print("끝나긴함")
                    if(event.key ==pygame.K_y):
                        screen.fill(WHITE)
                        missedLetters = ''
                        correctLetters = ''
                        gameIsDone = False
                        for_sound=0
                        one=0
                        secretWord = getRandomWord(words)      
                        pygame.display.flip()
                    else:
                        gamerealDone =True      
            else:
                yes=""
                message="Please enter a LETTER."
                guess=""
    text = font.render("Guess a letter : "+message+yes, True, BLACK)
    screen.blit(text, [50, 500])
    text = font.render(message2, True, BLACK)
    screen.blit(text, [50, 550])
    pygame.display.flip()
    if(guess!="" or len(missedLetters) == len(HANGMAN_PICS) - 1 or foundAllLetters==True):
        if (guess!="") and (guess in secretWord) :
            correctLetters = correctLetters + guess
            #ppprint(correctLetters)
            #ppprint(secretWord)
            # Check if the player has won.
            foundAllLetters = True
            for i in range(len(secretWord)):
                if secretWord[i] not in correctLetters:
                    foundAllLetters = False
                #    print("??")
                    break
                else:
                    foundAllLetters = True  
            if foundAllLetters:
                text = font.render('Yes! The secret word is', True, BLACK)
                screen.blit(text, [50, 550])      
                text = font.render('"'+secretWord + '"! You have won!', True, BLACK)
                screen.blit(text, [50, 600])              
                gameIsDone = True
                crab.play()
            pygame.display.flip()
        else:
            missedLetters = missedLetters + guess

            # Check if player has guessed too many times and lost.
            if len(missedLetters) == len(HANGMAN_PICS) - 1:
                displayBoard(missedLetters, correctLetters, secretWord)
                t='You have run out of guesses!'
                text = font.render(t, True, BLACK)
                screen.blit(text, [50, 550])
                t='After ' + str(len(missedLetters)) + ' missed guesses and ' + str(len(correctLetters))  
                text = font.render(t, True, BLACK)
                screen.blit(text, [50, 600])     
                t='correct guesses, the word was "' + secretWord +'"'
                text = font.render(t, True, BLACK)
                screen.blit(text, [100, 650])  
                if one==0:
                    uu.play()
                    one+=1
                gameIsDone = True
            pygame.display.flip()

        # Ask the player if they want to play again (but only if the game is done).
        if gameIsDone:
            text = font.render("Do you want to play again? (yes or no)", True, BLACK)
            screen.blit(text, [50, 800])  
    pygame.display.flip()
    fps.tick(200)
pygame.quit()