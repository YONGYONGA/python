# Tic Tac Toe

import random
import pygame

WINDOW_WIDTH = 420
WINDOW_HEIGHT = 500

BLACK = (0, 0, 0)
WHITE=(255,255,255)
BLUE = (0, 0, 255)
pygame.init()
pygame.display.set_caption("TTT")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont('FixedSys', 33, True, False)
font1 = pygame.font.SysFont('FixedSys', 180, True, False)
font2 = pygame.font.SysFont('FixedSys', 44, True, False)
###project _minimax

def evaluate(theBoard) :
   
    # Checking victory. win+10 lose -10 else 0
    if(isWinner(theBoard,playerLetter)):
        return 10
    elif(isWinner(theBoard,computerLetter)):
        return -10
    return 0
 
# This is the minimax function. It considers all
# the possible ways the game can go and returns
# the value of the board
def minimax(board, depth, isMax) :
    score = evaluate(board)
    if (score == 10) :
        return score
    if (score == -10) :
        return score
    if (isBoardFull(board) == True) :
        return 0
        #아직 max값 못찾음, 현재 정보에서 재귀적으로 호출 ㄱ. 대신 다음은 min을 찾아야 하니 isMAx=False
    if (isMax) :    
        best = -1000
        for i in range(1,10):
            if(board[i]==' '):
                board[i]=playerLetter
                best=max(best,minimax(board,depth+1,not isMax))
                board[i]=' '
        return best 
    else :
        best = 1000 
        for i in range(1,10):
            if(board[i]==' '):
                board[i]=computerLetter
                best=min(best,minimax(board,depth+1,not isMax))
                board[i]=' '
        return best
 
# This will return the best possible move for the player
def findBestMove(board,MM) :
    bestVal = -1000
    bestMove = (-1, -1)
    ##MM=1인건 player turn. 즉 최대값이 필요
    ##MM=-1인건 computer turn 즉 최소값이 필요.
    # Traverse all cells, evaluate minimax function for
    # all empty cells. And return the cell with optimal
    # value.
    if(MM==1):
        bestVal = -1000
        for i in range(1,10):
            if board[i]==' ':
                board[i]=playerLetter
                moveVal=minimax(board,0,False)
                board[i]=' '
                if(moveVal>bestVal):
                    bestMove=i
                    bestVal=moveVal 
        print("The value of the best Move is :", bestVal)
        print("at : ",bestMove)
        print()
    elif(MM==-1):
        bestVal=1000
        for i in range(1,10):
            if board[i]==' ':
                board[i]=computerLetter
                moveVal=minimax(board,0,True)
                board[i]=' '
                if(moveVal<bestVal):
                    bestMove=i
                    bestVal=moveVal 
        print("The value of the best (com)Move is :", bestVal)
        print("at : ",bestMove)
        print()        
    return bestMove





def drawBoard(board):
    # This function prints out the board that it was passed.

    # "board" is a list of 10 strings representing the board (ignore index 0)
    print(board[7] + '|' + board[8] + '|' + board[9])
    print('-+-+-')
    print(board[4] + '|' + board[5] + '|' + board[6])
    print('-+-+-')
    print(board[1] + '|' + board[2] + '|' + board[3])

def inputPlayerLetter():
    # Lets the player type which letter they want to be.
    # Returns a list with the player's letter as the first item, and the computer's letter as the second.
    letter = ''
    while not (letter == 'X' or letter == 'O'):
        print('Do you want to be X or O?')
        letter = input().upper()

    # the first element in the list is the player's letter, the second is the computer's letter.
    if letter == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']

def whoGoesFirst():
    # Randomly choose the player who goes first.
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'

def makeMove(board, letter, move):
    board[move] = letter

def isWinner(bo, le):
    # Given a board and a player's letter, this function returns True if that player has won.
    # We use bo instead of board and le instead of letter so we don't have to type as much.
    return ((bo[7] == le and bo[8] == le and bo[9] == le) or # across the top
    (bo[4] == le and bo[5] == le and bo[6] == le) or # across the middle
    (bo[1] == le and bo[2] == le and bo[3] == le) or # across the bottom
    (bo[7] == le and bo[4] == le and bo[1] == le) or # down the left side
    (bo[8] == le and bo[5] == le and bo[2] == le) or # down the middle
    (bo[9] == le and bo[6] == le and bo[3] == le) or # down the right side
    (bo[7] == le and bo[5] == le and bo[3] == le) or # diagonal
    (bo[9] == le and bo[5] == le and bo[1] == le)) # diagonal

def getBoardCopy(board):
    # Make a copy of the board list and return it.
    boardCopy = []
    for i in board:
        boardCopy.append(i)
    return boardCopy

def isSpaceFree(board, move):
    # Return true if the passed move is free on the passed board.
    return board[move] == ' '

def getPlayerMove(board):
    # Let the player type in their move.
    move = ' '
    while move not in '1 2 3 4 5 6 7 8 9'.split() or not isSpaceFree(board, int(move)):
        print('What is your next move? (1-9)')
        move = input()
    return int(move)

def chooseRandomMoveFromList(board, movesList):
    # Returns a valid move from the passed list on the passed board.
    # Returns None if there is no valid move.
    possibleMoves = []
    for i in movesList:
        if isSpaceFree(board, i):
            possibleMoves.append(i)

    if len(possibleMoves) != 0:
        return random.choice(possibleMoves)
    else:
        return None

def getComputerMove(board, computerLetter):
    # Given a board and the computer's letter, determine where to move and return that move.
    if computerLetter == 'X':
        playerLetter = 'O'
    else:
        playerLetter = 'X'

    # Here is our algorithm for our Tic Tac Toe AI:
    # First, check if we can win in the next move
    for i in range(1, 10):
        boardCopy = getBoardCopy(board)
        if isSpaceFree(boardCopy, i):
            makeMove(boardCopy, computerLetter, i)
            if isWinner(boardCopy, computerLetter):
                return i

    # Check if the player could win on his next move, and block them.
    for i in range(1, 10):
        boardCopy = getBoardCopy(board)
        if isSpaceFree(boardCopy, i):
            makeMove(boardCopy, playerLetter, i)
            if isWinner(boardCopy, playerLetter):
                return i

    # Try to take one of the corners, if they are free.
    move = chooseRandomMoveFromList(board, [1, 3, 7, 9])
    if move != None:
        return move

    # Try to take the center, if it is free.
    if isSpaceFree(board, 5):
        return 5

    # Move on one of the sides.
    return chooseRandomMoveFromList(board, [2, 4, 6, 8])

def isBoardFull(board):
    # Return True if every space on the board has been taken. Otherwise return False.
    for i in range(1, 10):
        if isSpaceFree(board, i):
            return False
    return True
def check_mouse(x,y,board):
    if(x<=0 or x==140 or x==280 or x>=420):
        return False
    elif(y<=0 or y==140 or y==280 or y>=420):
        return False
    arr_y=int(x/140)
    arr_x=int(y/140)
    index=int(abs(arr_x-2)*3+arr_y+1)
    return isSpaceFree(board,index)
def new_get(x,y):
    arr_y=int(x/140)
    arr_x=int(y/140)
    index=int(abs(arr_x-2)*3+arr_y+1)
    return index
def clear_screen(location):
    xe=(abs(int((location-1)/3)-2))
    ye=(location-1)%3    
    ys=int(ye)*140
    xs=int(xe)*140
    pygame.draw.rect(screen,WHITE,(ys+2,xs+2,135,135))
    pygame.display.flip()    
print('Welcome to Tic Tac Toe!')
initial=0
screen.fill(WHITE)
letter=''
gameend=False
gamerealend=False
mouse_x=-5
mouse=y=-5
turn=''
mouse_c=False
theBoard = [' '] * 10
playerLetter=''
computerLetter=''
M=0
bee=-1
while True:
    if(gamerealend):
        break
    if(initial!=0 and gameend==False and turn=='player' and M==0):
        M=1
        bee=findBestMove(theBoard,M)
        #print(bee)
        xe=(abs(int((bee-1)/3)-2))
        ye=(bee-1)%3
        #print((xx,yy))
        text = font1.render(playerLetter, True, (255,192,203))
        screen.blit(text, [int(ye)*140,int(xe)*140])                       
        pygame.display.flip()        
    if(initial==0):
        text = font.render('Do you want to be X or O?', True, BLACK)
        screen.blit(text, [0, 210])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gamerealend=True
            break    
        elif event.type==pygame.KEYDOWN:
            if(initial==0 and gameend==False):
                if(event.key==pygame.K_x):
                    playerLetter='X'
                    computerLetter='O'
                    initial=1
                    screen.fill(WHITE)
                elif(event.key==pygame.K_o):
                    playerLetter='O'
                    computerLetter='X'   
                    initial=1
                    screen.fill(WHITE)
            elif(gameend==True):##게임의 종료
                if(event.key==pygame.K_y): ##재시작을 원함, 변수, 화면초기화
                    theBoard = [' '] * 10
                    playerLetter=''
                    computerLetter=''
                    screen.fill(WHITE)
                    initial=0                
                    gameend=False
                    M=0
                else:
                    gamerealend=True
        elif event.type==pygame.MOUSEBUTTONDOWN:
            if(initial!=0 and gameend==False and turn=='player'):
                pos = pygame.mouse.get_pos()
                mouse_x = pos[0]
                mouse_y = pos[1]
                if(check_mouse(mouse_x,mouse_y,theBoard)):
                    M=-1
                    if(bee!=-1):
                        #추천했던 위치 안보이게 초기화
                        clear_screen(bee)
                        bee=-1
                    mouse_c=True

    pygame.display.flip()
    if(initial==1):


        pygame.draw.line(screen, BLACK, [140, 0], [140, 420], 2)
        pygame.draw.line(screen, BLACK, [280, 0], [280, 420], 2)
        pygame.draw.line(screen, BLACK, [0, 140], [420, 140], 2)
        pygame.draw.line(screen, BLACK, [0, 280], [420, 280], 2)
        pygame.draw.line(screen, BLACK, [0, 420], [420, 420], 2)
        theBoard = [' '] * 10
        #playerLetter, computerLetter = inputPlayerLetter()
        turn = whoGoesFirst()
        k=''
        if(turn=='computer'):
            k=computerLetter
        else:
            k=playerLetter
        text = font.render('The ' + turn + '({})  first.'.format(k), True, BLACK)
        #print(turn+" is first")
        screen.blit(text, [0, 450])
        gameend = False
        initial+=1
    elif(initial==2):

        if(gameend==False):
            if turn == 'player' and mouse_c==True:
                # Player's turn.
                #drawBoard(theBoard)
                move = new_get(mouse_x,mouse_y)
                makeMove(theBoard, playerLetter, move)
                #print("plyater: "+ str(move))
                xx=(abs(int((move-1)/3)-2))
                yy=(move-1)%3
                #print((xx,yy))
                text = font1.render(playerLetter, True, (50,0,50))
                screen.blit(text, [int(yy)*140,int(xx)*140])   
                    
                if isWinner(theBoard, playerLetter):
                    text = font2.render('You win!', True, BLUE)
                    screen.blit(text, [0,210])  
                    gameend = True
                else:
                    if isBoardFull(theBoard):
                        text = font2.render('The game is a tie!', True, BLUE)
                        screen.blit(text, [0,210])
                        gameend = True  
                    else:
                        turn = 'computer'
                mouse_c=False

            elif(turn=='computer'):
                # Computer's turn.
                M=-1
                move=findBestMove(theBoard,M)
                #move = getComputerMove(theBoard, computerLetter)
                #print("computer:",move)
                xx=(abs(int((move-1)/3)-2))
                yy=(move-1)%3
                #print((xx,yy))
                text = font1.render(computerLetter, True, (100,100,0))
                ##위치수정
                screen.blit(text, [int(yy)*140,int(xx)*140])                  
                makeMove(theBoard, computerLetter, move)

                if isWinner(theBoard, computerLetter):
                    #drawBoard(theBoard)
                    text = font2.render('You lose!', True, BLUE)
                    screen.blit(text, [0,210])                      
                    gameend = True
                else:
                    if isBoardFull(theBoard):
                        text = font2.render('The game is a tie!', True, BLUE)
                        screen.blit(text, [0,210])
                        gameend = True  
                    else:
                        turn = 'player'
                M=0
        pygame.display.flip()
    if(gameend==True):
        text = font2.render('again?(yes or no)', True, BLUE)
        screen.blit(text, [0,300])     

pygame.quit()   
