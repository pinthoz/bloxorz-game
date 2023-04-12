import pygame, sys, time
from pygame.locals import *
import levels
from queue import Queue
from copy import deepcopy
import math
from queue import PriorityQueue
from collections import deque


MAX_X = 9
MAX_Y = 14


class Board:
    def __init__(self, level, cost=0):
       
        self.start = [level['start']['x'], level['start']['y'],\
            level['start']['x'], level['start']['y']]  #start position
        self.block = [level['start']['x'], level['start']['y'],\
            level['start']['x'], level['start']['y']]  #box position [x1, y1, x2, y2]
        self.block_choose = 0 #keep track of which of the two blocks is currently being moved
        self.block_direction()
        self.level_buttons = [] #list of buttons in the level
        self.moves = '' #string of moves
        self.num_buttons_switch = 0 #number of buttons in the level
        for i in range(MAX_Y+1):
            self.level_buttons.append([False]*(MAX_X+1)) #initialize list of buttons
        board_level = level['geometry'] #board of the level
        for i in range(MAX_Y+1):
            for j in range(MAX_X+1):
                tile = board_level[i][j] #tile of the board
                if tile == 'k' or tile == 'q': # w, b : same as l and r, but initially on instead of off   #   l, r : if a switch is hit, these fields appear or disappear
                    self.level_buttons[i][j] = True #button in the position
                if tile == 'G':
                    self.end = [j, i, j, i] #end position j -> x, i -> y
             
                    
    def buttonSwitch(self, buttons, x, y):    #  k, q : if a switch is hit, these fields appear or disappear
        xDecoded = f'{x:02d}'
        yDecoded = f'{y:02d}'
        fields = buttons[xDecoded+yDecoded]
        onButtons = False
        for field in fields:
            xf = field["position"]["x"]
            yf = field["position"]["y"]
            action = field["action"]
            if action == "onoff":
                self.level_buttons[yf][xf] = not self.level_buttons[yf][xf]
            elif action == "on":
                self.level_buttons[yf][xf] = True
            elif action == "off":
                self.level_buttons[yf][xf] = False
            
            if action != 'off':
                onButtons = True
        
        if onButtons:
            self.num_buttons_switch += 1
    
               
    def block_direction(self): 
        if self.block[0] == self.block[2] and self.block[1] == self.block[3]: #block standing
            self.standing = True
            self.twotiles = True #block is laying vertical or horizontal
            self.vertical = None
        else:
            block1 = [self.block[0], self.block[1]] 
            block2 = [self.block[2], self.block[3]]
            if block1[0] == block2[0]:
                if block1[1] - block2[1] == 1:
                    self.standing =False
                    self.twotiles = True
                    self.vertical = True
                elif block1[1] - block2[1] == -1:
                    self.block[1] , self.block[3]  = self.block[3],  self.block[1]# swap block1 and block2 
                    self.standing = False
                    self.twotiles = True
                    self.vertical = True
            elif block1[1] == block2[1]:
                if block1[0] - block2[0] == 1:
                    self.standing = False
                    self.twotiles = True
                    self.vertical = False
                elif block1[0] - block2[0] == -1:
                    self.block[0], self.block[2]  == self.block[2], self.block[0]

                    self.standing = False
                    self.twotiles = True
                    self.vertical = False
            else:
                self.standing = False
                self.twotiles = False
                self.vertical = None
                
    def valid_move(self, level):
        box1_x, box1_y = self.block[0], self.block[1]
        box2_x, box2_y = self.block[2], self.block[3]

        # Check if the block is within the boundaries of the map
        if not (0 <= box1_x <= MAX_X and 0 <= box1_y <= MAX_Y and level[box1_y][box1_x] != ' '):
            return False
        if not (0 <= box2_x <= MAX_X and 0 <= box2_y <= MAX_Y and level[box2_y][box2_x] != ' '):
            return False

        # Check if the block is in bridges
        if level[box1_y][box1_x] in ['l', 'r', 'k', 'q'] and not self.level_buttons[box1_y][box1_x]:
            return False
        if level[box2_y][box2_x] in ['l', 'r', 'k', 'q'] and not self.level_buttons[box2_y][box2_x]:
            return False

        # Check if the block is standing on a floor tile
        if self.standing and level[box1_y][box1_x] == 'f':
            return False

        return True
    
    def make_move(self, level, buttons, move):   #  returns True if the move is valid, False otherwise and if we have reached the end (valid, end)
        if move == 'U':
            if self.standing:   
                x = self.block[0]
                y = self.block[1]
                self.block = [x, y+2, x, y+1]      #if it is standing and we do up move, it will be laying vertically
            else:
                if self.twotiles:          
                    x1 = self.block[0]
                    y1 = self.block[1]
                    x2 = self.block[2]
                    y2 = self.block[3]            
                    if self.vertical:
                        self.block = [x1, y1+1, x1, y1+1]    #if it is laying vertical and we do up move, it will be standing
                    else:
                        self.block = [x1, y1+1, x2, y2+1]  #if it is laying horizontal and we do up move, it will be laying horizontal

        elif move == 'D':
            if self.standing:
                x = self.block[0]
                y = self.block[1]
                self.block = [x, y-1, x, y-2]    #if it is standing and we do up move, it will be laying horizontally
            else:
                if self.twotiles:
                    x1 = self.block[0]
                    y1 = self.block[1]
                    x2 = self.block[2]
                    y2 = self.block[3]
                    if self.vertical:
                        self.block = [x2, y2-1, x2, y2-1]
                    else:
                        self.block = [x1, y1-1, x2, y2-1]

                    
        elif move == 'R':
            if self.standing:
                x = self.block[0]
                y = self.block[1]
                self.block = [x-1, y, x-2, y]      #if it is standing and we do right move, it will be laying horizontal
            else:
                if self.twotiles:
                    x1 = self.block[0]
                    y1 = self.block[1]
                    x2 = self.block[2]
                    y2 = self.block[3]
                    if self.vertical:
                        self.block = [x1-1, y1, x2-1, y2]  #if it is laying vertical and we do right move, it will be laying vertical
                    else:
                        self.block = [x2-1, y2, x2-1, y2]  #if it is laying horizontal and we do right move, it will be standing

                    
        elif move == 'L':
            if self.standing:
                x = self.block[0]
                y = self.block[1]
                self.block = [x+2, y, x+1, y]      #if it is standing and we do left move, it will be laying horizontal
            else:
                if self.twotiles:
                    x1 = self.block[0]
                    y1 = self.block[1]
                    x2 = self.block[2]
                    y2 = self.block[3] 
                    if self.vertical:
                        self.block = [x1+1, y1, x2+1, y2]  #if it is laying vertical and we do right move, it will be laying vertical
                    else:
                        self.block = [x1+1, y1, x1+1, y1]
        

        self.moves += move
        self.block_direction()
        
        if not self.valid_move(level):
            return (False,False)
        
        if not self.twotiles:
            if  level[self.block[self.block_choose*2+1]][self.block[self.block_choose*2]] == 's':
                self.buttonSwitch(buttons, self.block[self.block_choose*2], self.block[self.block_choose*2+1])                 
        else:
            if self.standing:
                if level[self.block[1]][self.block[0]] == 's' or level[self.block[1]][self.block[0]] == 'h' or level[self.block[1]][self.block[0]] == 'v': #if the block is standing on a button
                    self.buttonSwitch(buttons, self.block[0], self.block[1])
                else:
                    if level[self.block[1]][self.block[0]] == 's': #if the block is standing on a button
                        self.buttonSwitch(buttons, self.block[0], self.block[1])
                    if level[self.block[3]][self.block[2]] == 's':  #if the block is standing on a button
                        self.buttonSwitch(buttons, self.block[2], self.block[3])
        
        if (self.standing) and (self.block == self.end): #if the block is standing on the end tile
            self.falling = True
            return (True, True)
        
        return (True, False) 

    def tile_available(self, level, x, y):
        if level[y][x] == ' ' or ((level[y][x] == 'l' or level[y][x] == 'r' or level[y][x] == 'k' or level[y][x] == 'q') and not self.level_buttons[y][x]):
            return False
        return True


    def getTuple(self):
        return (self.block[0], self.block[1], self.block[2], self.block[3], self.block_choose, tuple(tuple(i) for i in self.level_buttons))

    def __eq__(self, other):
        return self.getTuple() == other.getTuple()

    def __hash__(self):
        return hash(self.getTuple()) 
 
 
class HeuristicBoard: # for Greedy Search
    def __init__(self, board: Board, heuristic: int):
        self.board = board
        self.heuristic = heuristic

    def __lt__(self, other):
        if isinstance(other, HeuristicBoard):
            return self.heuristic < other.heuristic
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, HeuristicBoard):
            return self.board == other.board and self.heuristic == other.heuristic
        return NotImplemented

class AStarBoard: # for A* Search
    def __init__(self, board: Board, heuristic: int, cost: int):
        self.board = board
        self.heuristic = heuristic
        self.cost = cost

    def __lt__(self, other):
        if isinstance(other, AStarBoard):
            return self.heuristic + self.cost < other.heuristic + other.cost
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, AStarBoard):
            return self.board == other.board and self.heuristic == other.heuristic and self.cost == other.cost
        return NotImplemented    

def buttonsDecode(buttons): #activate buttons
    vitalButtonsNum = 0
    buttonsDict = dict()
    for button in buttons:
        x = button["position"]["x"]
        y = button["position"]["y"]
        xDecoded = f'{x:02d}'
        yDecoded = f'{y:02d}'
        buttonsDict[xDecoded+yDecoded] =button['fields']
        for field in button['fields']:
            if field['action'] != 'off':
                vitalButtonsNum += 1
            break
    return buttonsDict, vitalButtonsNum


def gameGenerate(levelN): #generate level
    if levelN > len(levels.levels):
       levelN = 1
    if levelN < 1:
        levelN = len(levels.levels)
    level = levels.levels[levelN-1]
    gameObj = Board(level)
    map = level['geometry']
    enumMap = [list(enumerate(row)) for row in map]
    enumMap = list(enumerate(enumMap))
    buttons, vitalButtonsNum = buttonsDecode(level['buttons'])
    return levelN, gameObj, map, enumMap, buttons, vitalButtonsNum

##########################################################################################################################################################################
#Algorithms

def bfs(level, buttons, state: Board):
    global max_nodes

    queue = Queue()
    queue.put(state)
    visited = {}
    max_nodes = 0
    while queue.qsize() > 0:        
        state = queue.get()
        if state in visited:
            continue

        visited[state] = len(state.moves)
        max_nodes += 1

        for move in ['U', 'D', 'L', 'R']:
            new_state = deepcopy(state)
            isProper, isWin = new_state.make_move(level, buttons, move)
            if isWin:
                return new_state.moves
            if isProper:
                moves_done = visited.get(new_state)  
                if not (moves_done and moves_done < len(new_state.moves)):
                    queue.put(new_state)


def dfs(level, buttons, state: Board):   
    global max_nodes

    stack = deque()
    stack.append(state)
    visited = {}
    max_nodes = 0

    while len(stack) > 0:
        state = stack.pop()  # gets last element in queue == first element in stack

        if state not in visited:
            visited[state] = len(state.moves)
            max_nodes += 1

            for move in ['U', 'D', 'L', 'R']:
                new_state = deepcopy(state)
                isProper, isWin = new_state.make_move(level, buttons, move)
                if isWin:
                    return new_state.moves
                if isProper:
                    moves_done = visited.get(new_state)  
                    if not (moves_done and moves_done < len(new_state.moves)):
                        stack.append(new_state)

    return None
########################################################################

'''def dls(level, buttons, state: Board, depth_limit):
    
    global max_nodes
    
    stack = [state]
    
    while stack:
        if len(stack) > max_nodes:
            max_nodes = len(stack)
        
        state = stack.pop()
        
        for move in ['U', 'D', 'L', 'R']:
            new_state = deepcopy(state)
            isProper, isWin = new_state.make_move(level, buttons, move)
            if isWin:
                return new_state.moves
            if isProper and len(new_state.moves) <= depth_limit:
                stack.append(new_state)
                
    return None

def idfs(level, buttons, state: Board):
    depth_limit = 0
    while True:
        result = dls(level, buttons, state, depth_limit)
        if result is not None:
            return result
        depth_limit += 1'''
########################################################################

def dls(level, buttons, state: Board, depth_limit, visited):
    global max_nodes
    
    if state in visited or depth_limit == 0:
        return None

    visited[state] = True
    max_nodes += 1
    for move in ['U', 'D', 'L', 'R']:
        new_state = deepcopy(state)
        isProper, isWin = new_state.make_move(level, buttons, move)

        if isWin:
            return new_state.moves

        if isProper:
            result = dls(level, buttons, new_state, depth_limit - 1, visited)
            if result is not None:
                return result

    visited.pop(state)
    return None


def idfs(level, buttons, state: Board):
    global max_nodes
    depth_limit = 0
    while True:
        visited = {}
        max_nodes = 0
        result = dls(level, buttons, state, depth_limit, visited)
        if result is not None:
            return result
        depth_limit += 1

def Manhattan(state:Board):  
    #heuristic function based on the sum of Manhattan distance from current position to goal position
    x1_currentposition = state.block[0]
    y1_currentposition =state.block[1]
    x2_currentposition = state.block[2]
    y2_currentposition =state.block[3]
    x1_goalposition = state.end[0]
    y1_goalposition= state.end[1]
    x2_goalposition =state.end[2]
    y2_goalposition= state.end[3]
   
    distanceM1 = abs(x1_currentposition - x1_goalposition) + abs(y1_currentposition - y1_goalposition)
    distanceM2 = abs(x2_currentposition - x2_goalposition) + abs(y2_currentposition - y2_goalposition)
    distanceM = max(distanceM1, distanceM2)  
    if state.standing:
        distanceM += 1
    return distanceM    

def Euclidean(state:Board):  
    # heuristic function based on euclidean distances from current position to goal position
    x1_currentposition = state.block[0]
    y1_currentposition =state.block[1]
    x2_currentposition = state.block[2]
    y2_currentposition =state.block[3]
    x1_goalposition = state.end[0]
    y1_goalposition= state.end[1]
    x2_goalposition = state.end[2]
    y2_goalposition= state.end[3]

    distanceE1 = math.sqrt((x1_currentposition-x1_goalposition)**2 + (y1_currentposition-y1_goalposition)**2)
    distanceE2 = math.sqrt((x2_currentposition-x2_goalposition)**2 + (y2_currentposition-y2_goalposition)**2)
    distanceE = max(distanceE1,distanceE2)  
    if state.standing:
        distanceE += 1
    return distanceE


def Chebyshev(state: Board):   # heuristic function based on Chebyshev distance - according to article Tahani Q. Alhassan et al. / Procedia Computer Science 163 (2019) 391–399
    # h(n)=max(|x-xg|,|y - yg|) where x is the row number of current positions of block, \
    # xg is the row number of goal position, y and yg are the same but in terms of columns 
    #the block has 2 bricks and represented by two x,y coordinates, the heuristic value for the both \
    # bricks h(n)1 and h(n)2 are calculated, then the maximum one is considered as the overall heuristic.
   
    x1_currentposition = state.block[0]
    y1_currentposition =state.block[1]
    x2_currentposition = state.block[2]
    y2_currentposition =state.block[3]
    x1_goalposition = state.end[0]
    y1_goalposition= state.end[1]
    x2_goalposition = state.end[2]
    y2_goalposition= state.end[3]

    distanceC1 = max(abs(x1_currentposition-x1_goalposition), abs(y1_currentposition-y1_goalposition))
    distanceC2 = max(abs(x2_currentposition-x2_goalposition), abs(y2_currentposition-y2_goalposition))
    distanceC= max(distanceC1,distanceC2)
    if state.standing == True:
        distanceC += 1  
    return distanceC
    

def greedy(level, buttons, state: Board, heuristic):
    global max_nodes

    q = PriorityQueue()
    q.put(HeuristicBoard(state, heuristic(state)))
    visited = set()
    max_nodes = 0

    while not q.empty():
        heuristic_board = q.get()
        state = heuristic_board.board

        if state in visited:
            continue

        visited.add(state)
        max_nodes += 1

        for move in ['U', 'D', 'L', 'R']:
            new_state = deepcopy(state)
            isProper, isWin = new_state.make_move(level, buttons, move)
            if isWin:
                return new_state.moves
            if isProper:
                q.put(HeuristicBoard(new_state, heuristic(new_state)))

    return None



def a_star(level, buttons, state: Board, heuristic):
    global max_nodes

    q = PriorityQueue()
    q.put(AStarBoard(state, heuristic(state), 0))
    visited = set()
    max_nodes = 0

    while not q.empty():
        astar_board = q.get()
        state = astar_board.board
        cost = astar_board.cost

        if state in visited:
            continue

        visited.add(state)
        max_nodes += 1

        for move in ['U', 'D', 'L', 'R']:
            new_state = deepcopy(state)
            isProper, isWin = new_state.make_move(level, buttons, move)
            if isWin:
                return new_state.moves
            if isProper:
                q.put(AStarBoard(new_state, heuristic(new_state), cost + 1))

    return None

##########################################################################################################################################################################
#MENU

def show_message(screen,text,x,y, color=(0,0,0)): #function to show text on the screen
    rendered_text = FONT.render(text, True, color)
    text_rect = rendered_text.get_rect()
    text_rect.center = (x, y)
    screen.blit(rendered_text, text_rect)


def menu(screen, menu_background): #function to show the menu
    menu_font = pygame.font.Font("images/PKMN RBYGSC.ttf", 30)
    menu_options = ["Start Game", "Rules", "Exit"] 
    menu_active = True
    selected_option = 0

    def show_rules():
        rules_active = True
        while rules_active:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        rules_active = False
                        
            screen.blit(menu_background, (0, 0))
            show_message(screen, "Rules:", screen.get_width() // 2, 200, (255, 255, 255))
            show_message(screen, "1. Move the block to the goal.", screen.get_width() // 2, 250, (255, 255, 255))
            show_message(screen, "2. Press arrow keys to move.", screen.get_width() // 2, 300, (255, 255, 255))
            show_message(screen, "3. Do not fall off the edges.", screen.get_width() // 2, 350, (255, 255, 255))
            show_message(screen, "Press ESC", screen.get_width() // 2, 450, (255, 255, 255))
            show_message(screen, "to return to the menu", screen.get_width() // 2, 480, (255, 255, 255))

            pygame.display.update()

    while menu_active:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == K_RETURN:
                    if selected_option == 0:
                        pygame.display.update()
                        return
                    elif selected_option == 1:  
                        show_rules()
                    elif selected_option == 2:
                        pygame.quit()
                        sys.exit()

        screen.blit(menu_background, (0, 0))

        for i, option in enumerate(menu_options):
            color = (0, 0, 0) if i == selected_option else (128, 128, 128)
            rendered_option = menu_font.render(option, True, color)
            option_rect = rendered_option.get_rect()
            option_rect.center = (screen.get_width() // 2, screen.get_height() // 2 - 50 + 50 * i)
            screen.blit(rendered_option, option_rect)

        pygame.display.update()
        
def show_menu_heuristic():  #function to show the menu with the heuristic options
    global screen
    background_image = pygame.image.load("images/background.png")
    font = pygame.font.Font("images/PKMN RBYGSC.ttf", 25)
    font_low = pygame.font.Font("images/PKMN RBYGSC.ttf", 18)
    text = font.render("Select the heuristic: ", True, (255, 255, 255))
    text1 = font_low.render("Press 1 to use Manhattan distance", True, (255, 255, 255))
    text2 = font_low.render("Press 2 to use Euclidean distance", True, (255, 255, 255))
    text3 = font_low.render("Press 3 to use Chebyshev distance", True, (255, 255, 255))

    while True:
        screen.blit(background_image, (0, 0))
        screen.blit(text, (100, 200))
        screen.blit(text1, (100, 250))
        screen.blit(text2, (100, 280))
        screen.blit(text3, (100, 310))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return Manhattan
                elif event.key == pygame.K_2:
                    return Euclidean
                elif event.key == pygame.K_3:
                    return Chebyshev
                

        pygame.display.flip()

##########################################################################################################################################################################################
#PYGAME

pygame.init() #initialize pygame
pygame.display.set_caption('Space Block - Roll the Block')
screen = pygame.display.set_mode((840, 600),0,32)
display = pygame.Surface((400, 275), pygame.SRCALPHA, 32)
display = display.convert_alpha()
FONT = pygame.font.Font("images/PKMN RBYGSC.ttf", 25)  # address of the font and size
FONT_low = pygame.font.Font("images/PKMN RBYGSC.ttf", 15) # address of the font and size


menu_background = pygame.image.load('images/background_menu.png').convert()
menu_background = pygame.transform.scale(menu_background, (840, 600))
menu(screen, menu_background)

box_component = [pygame.image.load('images/component_0'+str(x) + '.png').convert() if x < 10 else pygame.image.load('images/component_'+ str(x) + '.png').convert() for x in range(14) ]

for component in box_component:
    component.set_colorkey((0, 0, 0))

background = pygame.image.load('images/background.png').convert()
tile_img = pygame.image.load('images/obj_04.png').convert()
bridge_img = pygame.image.load('images/bridge_0.png').convert()
roundBtn_img = pygame.image.load('images/button_0.png').convert()
xBtn_img = pygame.image.load('images/button_2.png').convert()
tile_restrict_img = pygame.image.load('images/tilerestrict.png').convert()
splitBtn_img = pygame.image.load('images/button_4.png').convert()

background.set_colorkey((0, 0, 0))
background = pygame.transform.scale(background, (840, 600))
tile_img.set_colorkey((0, 0, 0))
bridge_img.set_colorkey((0, 0, 0))
roundBtn_img.set_colorkey((0, 0, 0))
xBtn_img.set_colorkey((0, 0, 0))
tile_restrict_img.set_colorkey((0, 0, 0))
splitBtn_img.set_colorkey((0, 0, 0))


level1 = 1
level1, gameObj, level, enumlevel, buttons, vitalButtonsNum = gameGenerate(level1)
tempGameObj = gameObj
runAlgor = False
level_number = 0

currentPop = []
currentGene = ''
runVisual = False
heuristic = None

max_nodes = 0
points = 0 

##############
#best solution
sol = {
    1 : 7,
    2 : 24,
    3 : 19,
    4 : 28,
    5 : 23,
    6 : 50
}

############## 

while level_number != len(levels.levels): #main loop
    # display.fill((0,0,0))
    display = pygame.Surface((400, 275), pygame.SRCALPHA, 32)
    display = display.convert_alpha()
    isProper = True
    isWin = False
    #For change direction in level: for x, row in enumerate(level):
    if runAlgor:
        if m < len(solution):
            isProper, isWin = gameObj.make_move(level, buttons, solution[m])
            m += 1
            time.sleep(0.2)
        else:
            level1, gameObj, level, enumlevel, buttons, vitalButtonsNum = gameGenerate(level1)
            runAlgor = False

    if not runAlgor:
        for event in pygame.event.get():
            # event = pygame.event.get().pop()
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_RIGHT:
                    isProper, isWin = gameObj.make_move(level, buttons, 'R')
                elif event.key == K_LEFT:
                    isProper, isWin = gameObj.make_move(level, buttons, 'L')
                elif event.key == K_UP: 
                    isProper, isWin = gameObj.make_move(level, buttons, 'U')
                elif event.key == K_DOWN:
                    isProper, isWin = gameObj.make_move(level, buttons, 'D')
                elif event.key == K_b:
                    level1, gameObj, level, enumlevel, buttons, vitalButtonsNum = gameGenerate(level1)
                    runAlgor = True
                    m = len(gameObj.moves)
                    t = time.time()
                    solution = bfs(level, buttons,gameObj)
                    print('----------------------------------------------')
                    print('BFS')
                    print('Level: ', level1)
                    print('Time: ', time.time() - t)
                    print('Moves: ', len(solution))
                    print('Moves done: ', solution)
                    print('Max nodes saved: ', max_nodes)
                elif event.key == K_d:
                    level1, gameObj, level, enumlevel, buttons, vitalButtonsNum = gameGenerate(level1)
                    runAlgor = True
                    m = len(gameObj.moves)
                    t = time.time()
                    solution = dfs(level, buttons,gameObj)
                    print('----------------------------------------------')
                    print('DFS')
                    print('Level: ', level1)
                    print('Time: ', time.time() - t)
                    print('Moves: ', len(solution))
                    print('Moves done: ', solution)
                    print('Max nodes saved: ', max_nodes)
                elif event.key == K_i:
                    level1, gameObj, level, enumlevel, buttons, vitalButtonsNum = gameGenerate(level1)
                    runAlgor = True
                    m = len(gameObj.moves)
                    t = time.time()
                    solution = idfs(level, buttons,gameObj)
                    print('----------------------------------------------')
                    print('IDFS')
                    print('Level: ', level1)
                    print('Time: ', time.time() - t)
                    print('Moves: ', len(solution))
                    print('Moves done: ', solution)
                    print('Max nodes saved: ', max_nodes)
                elif event.key == K_g:
                    level1, gameObj, level, enumlevel, buttons, vitalButtonsNum = gameGenerate(level1)
                    h = show_menu_heuristic()
                    runAlgor = True
                    m = len(gameObj.moves)
                    t = time.time()
                    solution = greedy(level, buttons,gameObj, h)
                    print('----------------------------------------------')
                    print('Greedy with '+ h.__name__+' distance')
                    print('Level: ', level1)
                    print('Time: ', time.time() - t)
                    print('Moves: ', len(solution))
                    print('Moves done: ', solution)
                    print('Max nodes saved: ', max_nodes)
                elif event.key == K_a:
                    level1, gameObj, level, enumlevel, buttons, vitalButtonsNum = gameGenerate(level1)
                    h = show_menu_heuristic()
                    runAlgor = True
                    m = len(gameObj.moves)
                    t = time.time()
                    solution = a_star(level, buttons, gameObj, h)
                    print('----------------------------------------------')
                    print('A Star with '+ h.__name__ + ' distance')
                    print('Level: ', level1)
                    print('Time: ', time.time() - t)
                    print('Moves: ', len(solution))
                    print('Moves done: ', solution)
                    print('Max nodes saved: ', max_nodes)    
                      
                if not isProper:
                    level1, gameObj, level, enumlevel, buttons, vitalButtonsNum = gameGenerate(level1)
                
    
    for y, row in reversed(enumlevel):
        for x, tile in reversed(row): 
            if tile == 'X':
                display.blit(tile_img, (144 - x * 16 + y * 16, 220 - x * 8 - y * 8))
                #For change direction in level: display.blit(grass_img, (x * 10 + y * 10, 100 + x * 5 - y * 5))
            elif (tile == 'l' or tile == 'r' or tile == 'k' or tile == 'q'):
                if gameObj.level_buttons[y][x]:
                    display.blit(bridge_img, (144 - x * 16 + y * 16, 220 - x * 8 - y * 8))
            elif tile == 's':
                display.blit(tile_img, (144 - x * 16 + y * 16, 220 - x * 8 - y * 8))
                display.blit(roundBtn_img, (144 - x * 16 + y * 16, 220 - x * 8 - y * 8))
            elif tile == 'h':
                display.blit(tile_img, (144 - x * 16 + y * 16, 220 - x * 8 - y * 8))
                display.blit(xBtn_img, (144 - x * 16 + y * 16, 220 - x * 8 - y * 8))
            elif tile == 'f':
                display.blit(tile_restrict_img, (144 - x * 16 + y * 16, 220 - x * 8 - y * 8))
            elif tile == 'v':
                display.blit(tile_img, (144 - x * 16 + y * 16, 220 - x * 8 - y * 8))
                display.blit(splitBtn_img, (144 - x * 16 + y * 16, 220 - x * 8 - y * 8))
            
            if (x == gameObj.block[0] and y == gameObj.block[1]) or (x == gameObj.block[2] and y == gameObj.block[3]):
                if gameObj.standing:
                    display.blit(box_component[7], (144 - x * 16 + y * 16, 220 - x * 8 - y * 8 - 8))
                    display.blit(box_component[6], (144 - x * 16 + y * 16, 220 - x * 8 - y * 8 - 16))
                    display.blit(box_component[6], (144 - x * 16 + y * 16, 220 - x * 8 - y * 8 - 24))
                    display.blit(box_component[6], (144 - x * 16 + y * 16, 220 - x * 8 - y * 8 - 32))
                    display.blit(box_component[5], (144 - x * 16 + y * 16, 220 - x * 8 - y * 8 - 40))
                            
                elif gameObj.twotiles:
                    if gameObj.vertical:
                        if gameObj.block[0] == x and gameObj.block[1] == y:
                            display.blit(box_component[4], (144 - x * 16 + y * 16, 220 - x * 8 - y * 8 - 8))
                            display.blit(box_component[3], (144 - x * 16 + y * 16, 220 - x * 8 - y * 8 - 16))
                        else:
                            display.blit(box_component[2], (144 - x * 16 + y * 16, 220 - x * 8 - y * 8 - 8))
                            display.blit(box_component[1], (144 - x * 16 + y * 16, 220 - x * 8 - y * 8 - 16))
                    else:
                        if gameObj.block[0] == x and gameObj.block[1] == y:
                            display.blit(box_component[11], (144 - x * 16 + y * 16, 220 - x * 8 - y * 8 - 8))
                            display.blit(box_component[10], (144 - x * 16 + y * 16, 220 - x * 8 - y * 8 - 16))
                            
                        else:
                            display.blit(box_component[9], (144 - x * 16 + y * 16, 220 - x * 8 - y * 8 - 8))
                            display.blit(box_component[8], (144 - x * 16 + y * 16, 220 - x * 8 - y * 8 - 16))
                            
                elif gameObj.block[gameObj.block_choose*2] == x and gameObj.block[gameObj.block_choose*2+1] == y:
                    display.blit(box_component[7], (144 - x * 16 + y * 16, 220 - x * 8 - y * 8 - 8))
                    display.blit(box_component[5], (144 - x * 16 + y * 16, 220 - x * 8 - y * 8 - 16))
                else:
                    display.blit(box_component[13], (144 - x * 16 + y * 16, 220 - x * 8 - y * 8 - 8))
                    display.blit(box_component[12], (144 - x * 16 + y * 16, 220 - x * 8 - y * 8 - 16))

    screen.blit(background, (0,0))
    screen.blit(pygame.transform.scale(display, (400*1.8, 275*1.8)), (60, 120))
    
    moves = FONT.render('Moves: ' + f'{len(gameObj.moves)}', True, (0, 0, 0))
    rect_moves = moves.get_rect()
    rect_moves.left = (screen.get_width() - 400)
    screen.blit(moves, rect_moves)
    
    pts = FONT.render('Points: ' + f'{points}', True, (0, 0, 0))
    rect_pts = pts.get_rect()
    rect_pts.left = (screen.get_width() - 600)
    screen.blit(pts, rect_pts)
    
    bfs_text = FONT_low.render('Press B to use BFS', True, (255, 255, 255))
    bfs_rect = bfs_text.get_rect()
    bfs_rect.bottomright = (screen.get_width() - 10, screen.get_height() - 90)
    screen.blit(bfs_text, bfs_rect)
    
    dfs_text = FONT_low.render('Press D to use DFS', True, (255, 255, 255))
    dfs_rect = dfs_text.get_rect()
    dfs_rect.bottomright = (screen.get_width() - 10, screen.get_height() - 70)
    screen.blit(dfs_text, dfs_rect)
    
    idfs_text = FONT_low.render('Press I to use IDFS', True, (255, 255, 255))
    idfs_rect = idfs_text.get_rect()
    idfs_rect.bottomright = (screen.get_width() - 10, screen.get_height() - 50)
    screen.blit(idfs_text, idfs_rect)
    
    greedy_text = FONT_low.render('Press G to use Greedy', True, (255, 255, 255))
    greedy_rect = greedy_text.get_rect()
    greedy_rect.bottomright = (screen.get_width() - 10, screen.get_height() - 30)
    screen.blit(greedy_text, greedy_rect)

    astar_text = FONT_low.render('Press A to use A star', True, (255, 255, 255))
    astar_rect = astar_text.get_rect()
    astar_rect.bottomright = (screen.get_width() - 10, screen.get_height() - 10)
    screen.blit(astar_text, astar_rect)
    
    text = FONT.render('Level ' + f'{level1:02d}', True, (0, 0, 0))
    rect = text.get_rect()
    rect.right = (screen.get_width() - 10)
    screen.blit(text, rect)
    
    max_nodes = 0

    pygame.display.update()
    
    if isWin:
        show_message(screen, "Level " + f'{level1:02d}' + " Completed", screen.get_width() // 2, screen.get_height() // 2 -50)
        show_message(screen, "Steps: " + f'{len(gameObj.moves)}', screen.get_width() // 2, screen.get_height() // 2 -20)
        bs = sol[level1]
        if len(gameObj.moves) == bs and runAlgor ==False:
            show_message(screen, "Great Work. You found the best solution. ", screen.get_width() // 2, screen.get_height() // 2 +10)
            show_message(screen, "You received 3 points", screen.get_width() // 2, screen.get_height() // 2 +40)
            points += 3
            show_message(screen, "Your points: " + f'{points}', screen.get_width() // 2, screen.get_height() // 2 +70)
        elif len(gameObj.moves) <= bs +5 and runAlgor ==False:
            show_message(screen, "Nice Work. The best solution is "+ f'{bs}', screen.get_width() // 2, screen.get_height() // 2 +10)
            show_message(screen, "You received 2 points", screen.get_width() // 2, screen.get_height() // 2 +40)
            points += 2
            show_message(screen, "Your points: " + f'{points}', screen.get_width() // 2, screen.get_height() // 2 +70)
        elif len(gameObj.moves) > bs +5 and runAlgor ==False:
            show_message(screen, "The best solution is "+ f'{bs}', screen.get_width() // 2, screen.get_height() // 2 +10)
            show_message(screen, "You received 1 point", screen.get_width() // 2, screen.get_height() // 2 +40)
            points += 1
            show_message(screen, "Your points: " + f'{points}', screen.get_width() // 2, screen.get_height() // 2 +70)
        else:
            show_message(screen, "Your points: " + f'{points}', screen.get_width() // 2, screen.get_height() // 2 +40)
        pygame.display.update()
        time.sleep(4)                        
        level1 += 1
        level_number += 1
        level1, gameObj, level, enumlevel, buttons, vitalButtonsNum = gameGenerate(level1)


    