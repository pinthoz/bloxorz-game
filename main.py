import pygame, sys, time, random
from pygame.locals import *
import levels
from queue import Queue
from copy import deepcopy


MAX_X = 9
MAX_Y = 14

class Board:
    def __init__(self, level):
        self.start = [level['start']['x'], level['start']['y'],\
            level['start']['x'], level['start']['y']]  #start position
        self.block = [level['start']['x'], level['start']['y'],\
            level['start']['x'], level['start']['y']]  #box position [x1, y1, x2, y2]
        self.block_choose = 0 #keep track of which of the two blocks is currently being moved
        self.block_direction()
        self.level_swatches = [] #list of swatches in the level
        self.moves = '' #string of moves
        self.falling = False #if the block is falling
        self.num_swatches_switch = 0 #number of swatches in the level
        for i in range(MAX_Y+1):
            self.level_swatches.append([False]*(MAX_X+1)) #initialize list of swatches
        board_level = level['geometry'] #board of the level
        for i in range(MAX_Y+1):
            for j in range(MAX_X+1):
                tile = board_level[i][j] #tile of the board
                if tile == 'k' or tile == 'q': # w, b : same as l and r, but initially on instead of off   #   l, r : if a switch is hit, these fields appear or disappear
                    self.level_swatches[i][j] = True #swatch in the position
                if tile == 'G':
                    self.end = [j, i, j, i] #end position j -> x, i -> y
             
                    
    def swatchSwitch(self, swatches, x, y):    #  k, q : if a switch is hit, these fields appear or disappear
        xDecoded = f'{x:02d}'
        yDecoded = f'{y:02d}'
        fields = swatches[xDecoded+yDecoded]
        onSwatches = False
        for field in fields:
            xf = field["position"]["x"]
            yf = field["position"]["y"]
            action = field["action"]
            if action == "onoff":
                self.level_swatches[yf][xf] = not self.level_swatches[yf][xf]
            elif action == "on":
                self.level_swatches[yf][xf] = True
            elif action == "off":
                self.level_swatches[yf][xf] = False
            elif action == "split1":
                self.block[0] = xf
                self.block[1] = yf
                self.standing = False
                self.twotlies = False
                self.vertical = None
            elif action == "split2":
                self.block[2] = xf
                self.block[3] = yf
                self.standing = False
                self.twotiles = False
                self.vertical = None
            
            if action != 'off':
                onSwatches = True
        
        if onSwatches:
            self.num_swatches_switch += 1
    
               
    def block_direction(self):
        if self.block[0] == self.block[2] and self.block[1] == self.block[3]: #block standing
            self.standing = True
            self.twotiles = True
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

        # Check if the block are in bridges
        if level[box1_y][box1_x] in ['l', 'r', 'k', 'q'] and not self.level_swatches[box1_y][box1_x]:
            return False
        if level[box2_y][box2_x] in ['l', 'r', 'k', 'q'] and not self.level_swatches[box2_y][box2_x]:
            return False

        # Check if the block are standing on a floor tile
        if self.standing and level[box1_y][box1_x] == 'f':
            return False

        return True
    
    def make_move(self, level, swatches, move):   #  returns True if the move is valid, False otherwise and if we have reached the end (valid, end)
        if move == 'U':
            if self.standing:   
                x = self.block[0]
                y = self.block[1]
                self.block = [x, y+2, x, y+1]      #if it is standing and we do up move, it will be laying vertical
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
                self.block = [x, y-1, x, y-2]
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
                self.block = [x+2, y, x+1, y]      #if it is standing and we do right move, it will be laying horizontal
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
                self.swatchSwitch(swatches, self.block[self.block_choose*2], self.block[self.block_choose*2+1])                 
        else:
            if self.standing:
                if level[self.block[1]][self.block[0]] == 's' or level[self.block[1]][self.block[0]] == 'h' or level[self.block[1]][self.block[0]] == 'v': #if the block is standing on a swatch
                    self.swatchSwitch(swatches, self.block[0], self.block[1])
                else:
                    if level[self.block[1]][self.block[0]] == 's': #if the block is standing on a swatch
                        self.swatchSwitch(swatches, self.block[0], self.block[1])
                    if level[self.block[3]][self.block[2]] == 's':  #if the block is standing on a swatch
                        self.swatchSwitch(swatches, self.block[2], self.block[3])
        
        if (self.standing) and (self.block == self.end): #if the block is standing on the end tile
            self.falling = True
            return (True, True)
        
        return (True, False) 

    def tile_available(self, level, x, y):
        if level[y][x] == ' ' or ((level[y][x] == 'l' or level[y][x] == 'r' or level[y][x] == 'k' or level[y][x] == 'q') and not self.level_swatches[y][x]):
            return False
        return True


    def getTuple(self):
        return (self.block[0], self.block[1], self.block[2], self.block[3], self.block_choose, tuple(tuple(i) for i in self.level_swatches))

    def __eq__(self, other):
        return self.getTuple() == other.getTuple()

    def __hash__(self):
        return hash(self.getTuple()) 
    

def swatchesDecode(swatches):
    vitalSwatchesNum = 0
    swatchesDict = dict()
    for swatch in swatches:
        x = swatch["position"]["x"]
        y = swatch["position"]["y"]
        xDecoded = f'{x:02d}'
        yDecoded = f'{y:02d}'
        swatchesDict[xDecoded+yDecoded] =swatch['fields']
        for field in swatch['fields']:
            if field['action'] != 'off':
                vitalSwatchesNum += 1
            break
    return swatchesDict, vitalSwatchesNum


def gameGenerate(levelN):
    if levelN > len(levels.levels):
       levelN = 1
    if levelN < 1:
        levelN = len(levels.levels)
    level = levels.levels[levelN-1]
    gameObj = Board(level)
    map = level['geometry']
    enumMap = [list(enumerate(row)) for row in map]
    enumMap = list(enumerate(enumMap))
    swatches, vitalSwatchesNum = swatchesDecode(level['swatches'])
    return levelN, gameObj, map, enumMap, swatches, vitalSwatchesNum

##########################################################################################################################################################################
#Algorithms

def bfs(level, swatches, state: Board):
    q = Queue()
    q.put(state)
    visited = {}
    while q.qsize() > 0:  
        state = q.get()
        if state in visited:
            continue
        for move in ['U', 'D', 'L', 'R']:
            new_state = deepcopy(state)
            isProper, isWin = new_state.make_move(level, swatches, move)
            if isWin:
                return new_state.moves
            if isProper:
                moves_done = visited.get(new_state)  
                if not (moves_done and moves_done < len(new_state.moves)):
                    q.put(new_state)
        
        if not state.twotiles:
            new_state = deepcopy(state)
            isProper, isWin = new_state.make_move(map,swatches,'S')
            lenMoves = visited.get(new_state)
            if not (lenMoves and lenMoves < len(new_state.moves)):
                q.put(new_state)
        
        visited[state] = len(state.moves)

##########################################################################################################################################################################
#MENU

def show_message(screen,text,x,y, color=(0,0,0)):
    rendered_text = FONT.render(text, True, color)
    text_rect = rendered_text.get_rect()
    text_rect.center = (x, y)
    screen.blit(rendered_text, text_rect)


def menu(screen, menu_background):
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

##########################################################################################################################################################################################
#PYGAME

pygame.init()
pygame.display.set_caption('Space Block - Roll the Block')
screen = pygame.display.set_mode((840, 600),0,32)
display = pygame.Surface((400, 275), pygame.SRCALPHA, 32)
display = display.convert_alpha()
FONT = pygame.font.Font("images/PKMN RBYGSC.ttf", 25)  # adress of the font and size
FONT_low = pygame.font.Font("images/PKMN RBYGSC.ttf", 15) # adress of the font and size


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
level1, gameObj, level, enumlevel, swatches, vitalSwatchesNum = gameGenerate(level1)
tempGameObj = gameObj
runAlgor = False
level_number = 0

currentPop = []
currentGene = ''
runVisual = False


while level_number != len(levels.levels):
    # display.fill((0,0,0))
    display = pygame.Surface((400, 275), pygame.SRCALPHA, 32)
    display = display.convert_alpha()
    isProper = True
    isWin = False
    #For change direction in level: for x, row in enumerate(level):
    if runAlgor:
        if m < len(solution):
            isProper, isWin = gameObj.make_move(level, swatches, solution[m])
            m += 1
            time.sleep(0.2)
        else:
            level1, gameObj, level, enumlevel, swatches, vitalSwatchesNum = gameGenerate(level1)
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
                    isProper, isWin = gameObj.make_move(level, swatches, 'R')
                elif event.key == K_LEFT:
                    isProper, isWin = gameObj.make_move(level, swatches, 'L')
                elif event.key == K_UP: 
                    isProper, isWin = gameObj.make_move(level, swatches, 'U')
                elif event.key == K_DOWN:
                    isProper, isWin = gameObj.make_move(level, swatches, 'D')
                elif event.key == K_a:
                    level1, gameObj, level, enumlevel, swatches, vitalSwatchesNum = gameGenerate(level1)
                    runAlgor = True
                    m = len(gameObj.moves)
                    t = time.time()
                    solution = bfs(level, swatches,gameObj)
                    print('Time: ', time.time() - t)
                    print('Moves: ', len(solution))
                # for box in gameObj.block:
                #     if box[0] > levels.MAX_X or box[0] < 0 or box[1] > levels.MAX_Y or box[1] < 0 or level[box[1]][box[0]] == ' ':
                #         gameObj.block = [(levels.levels[level]['start']['x'],levels.levels[level]['start']['y'])]
                if not isProper:
                    level1, gameObj, level, enumlevel, swatches, vitalSwatchesNum = gameGenerate(level1)

    for y, row in reversed(enumlevel):
        for x, tile in reversed(row): 
            if tile == 'X':
                display.blit(tile_img, (144 - x * 16 + y * 16, 220 - x * 8 - y * 8))
                #For change direction in level: display.blit(grass_img, (x * 10 + y * 10, 100 + x * 5 - y * 5))
            elif (tile == 'l' or tile == 'r' or tile == 'k' or tile == 'q'):
                if gameObj.level_swatches[y][x]:
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
    
    bfs_text = FONT_low.render('Press A to use BFS', True, (255, 255, 255))
    bfs_rect = bfs_text.get_rect()
    bfs_rect.bottomright = (screen.get_width() - 10, screen.get_height() - 10)
    screen.blit(bfs_text, bfs_rect)
    
    text = FONT.render('Level ' + f'{level1:02d}', True, (0, 0, 0))
    rect = text.get_rect()
    rect.right = (screen.get_width() - 10)
    screen.blit(text, rect)

    pygame.display.update()
    
    if isWin:
        show_message(screen, "Congratulations", screen.get_width() // 2, screen.get_height() // 2 - 50)
        show_message(screen, "Level " + f'{level1:02d}' + " Completed", screen.get_width() // 2, screen.get_height() // 2)
        show_message(screen, "Steps: " + f'{len(gameObj.moves)}', screen.get_width() // 2, screen.get_height() // 2 +50)
        pygame.display.update()
        time.sleep(3)                        
        level1 += 1
        level_number += 1
        level1, gameObj, level, enumlevel, swatches, vitalSwatchesNum = gameGenerate(level1)

    


