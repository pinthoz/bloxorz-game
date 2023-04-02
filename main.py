import pygame, sys, time, random
from pygame.locals import *
import levels
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
        self.num_swatches_switch = 0 #number of swatches in the level
        for i in range(MAX_Y+1):
            self.level_swatches.append([False]*(MAX_X+1)) #initialize list of swatches
        board_level = level['geometry'] #board of the level
        for i in range(MAX_Y+1):
            for j in range(MAX_X+1):
                tile = board_level[i][j] #tile of the board
                if tile == 'k' or tile == 'q': # w, b : same as l and r, but initially on instead of off   #   l, r : if a switch is hit, these fields appear or disappear
                    self.level_swatches[i][j] = True #swatch in the position
                if tile == 'e':
                    self.end = [j, i, j, i] #end position j -> x, i -> y
             
                    
    def swatchSwitch(self, swatches, x, y):
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
                    self.block[1] = self.block[3] # swap block1 and block2 
                    self.block[3] = self.block[1] # swap block1 and block2
                    self.standing = False
                    self.twotiles = True
                    self.vertical = True
            elif block1[1] == block2[1]:
                if block1[0] - block2[0] == 1:
                    self.standing = False
                    self.twotiles = True
                    self.vertical = False
                elif block1[0] - block2[0] == -1:
                    self.block[0] = self.block[2]
                    self.block[2] = self.block[0]
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
        if level[box1_y][box1_x] in ['l', 'r', 'k', 'q'] and not self.level_swatch[box1_y][box1_x]:
            return False
        if level[box2_y][box2_x] in ['l', 'r', 'k', 'q'] and not self.level_swatch[box2_y][box2_x]:
            return False

        # Check if the block are standing on a floor tile
        if self.standing and level[box1_y][box1_x] == 'f':
            return False

        return True
    
    def make_move(self, level, swatches, move):
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
        
        if self.standing and self.block == self.end: #if the block is standing on the end tile
            return (True, True)
        
        return (True, False) 

    def tile_available(self, level, x, y):
        if level[y][x] == ' ' or ((level[y][x] == 'l' or level[y][x] == 'r' or level[y][x] == 'k' or level[y][x] == 'q') and not self.level_swatches[y][x]):
            return False
        return True


    def __eq__(self, other):
        return (self.block[0], self.block[1], self.block[2], self.block[3], self.boxChoose, tuple(tuple(i) for i in self.level_swatches) == \
            other.block[0], other.block[1], other.block[2], other.block[3], other.boxChoose, tuple(tuple(i) for i in other.level_swatches))

    def __hash__(self):
        return hash(self.block[0], self.block[1], self.block[2], self.block[3], self.block_choose, \
            tuple(tuple(i) for i in self.level_swatches))  
    

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


def gameGenerate(levelNo):
    if levelNo > len(levels.levels):
        levelNo = 1
    elif levelNo < 1:
        levelNo = len(levels.levels)
    level = levels.levels[levelNo-1]
    gameObj = Board(level)
    map = level['geometry']
    enumMap = [list(enumerate(row)) for row in map]
    enumMap = list(enumerate(enumMap))
    swatches, vitalSwatchesNum = swatchesDecode(level['swatches'])
    return levelNo, gameObj, map, enumMap, swatches, vitalSwatchesNum



##################################################################################################
#pygame

pygame.init()
pygame.display.set_caption('Bloxorz')
screen = pygame.display.set_mode((840, 600),0,32)
display = pygame.Surface((400, 275), pygame.SRCALPHA, 32)
display = display.convert_alpha()
POKEFONT = pygame.font.Font("assets/PKMN RBYGSC.ttf", 25)


box_component = [pygame.image.load('assets/component_0'+str(x) + '.png').convert() if x < 10 else pygame.image.load('assets/component_'+ str(x) + '.png').convert() for x in range(14) ]

for component in box_component:
    component.set_colorkey((0, 0, 0))

background = pygame.image.load('assets/background.png').convert()
tile_img = pygame.image.load('assets/obj_04.png').convert()
bridge_img = pygame.image.load('assets/bridge_0.png').convert()
roundBtn_img = pygame.image.load('assets/button_0.png').convert()
xBtn_img = pygame.image.load('assets/button_2.png').convert()
snow_img = pygame.image.load('assets/snow_0.png').convert()
splitBtn_img = pygame.image.load('assets/button_4.png').convert()

background.set_colorkey((0, 0, 0))
background = pygame.transform.scale(background, (840, 600))
tile_img.set_colorkey((0, 0, 0))
bridge_img.set_colorkey((0, 0, 0))
roundBtn_img.set_colorkey((0, 0, 0))
xBtn_img.set_colorkey((0, 0, 0))
snow_img.set_colorkey((0, 0, 0))
splitBtn_img.set_colorkey((0, 0, 0))

#gameObj.block = [(0,2),(0,0)]
# gameObj.block = [(0,2),(0,1)]
# gameObj.block = [(0,1),(0,2)]
# gameObj.block = [(0,1),(1,1)]
# gameObj.block = [(1,1),(0,1)]
# gameObj.block = [(1,1),(2,1)]
# gameObj.block = [(0,0)]

level1 = 1
level1, gameObj, level1, enumlevel, swatches, vitalSwatchesNum = gameGenerate(level1)
tempGameObj = gameObj
runAlgor = False


currentPop = []
currentGene = ''
runVisual = False

while True:
    # display.fill((0,0,0))
    display = pygame.Surface((400, 275), pygame.SRCALPHA, 32)
    display = display.convert_alpha()
    isProper = True
    isWin = False
    #For change direction in level: for x, row in enumerate(level):
    if runAlgor:
        if i < len(solution):
            isProper, isWin = gameObj.make_move(level, swatches, solution[i])
            i += 1
            time.sleep(0.3)
        else:
            level1 += 1
            level1, gameObj, level, enumlevel, swatches, vitalSwatchesNum = gameGenerate(level1)
            runAlgor = False
    for y, row in reversed(enumlevel):
        for x, tile in reversed(row): 
            if tile == 'b':
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
                display.blit(snow_img, (144 - x * 16 + y * 16, 220 - x * 8 - y * 8))
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
                            
                elif gameObj.block[gameObj.boxChoose*2] == x and gameObj.block[gameObj.boxChoose*2+1] == y:
                    display.blit(box_component[7], (144 - x * 16 + y * 16, 220 - x * 8 - y * 8 - 8))
                    display.blit(box_component[5], (144 - x * 16 + y * 16, 220 - x * 8 - y * 8 - 16))
                else:
                    display.blit(box_component[13], (144 - x * 16 + y * 16, 220 - x * 8 - y * 8 - 8))
                    display.blit(box_component[12], (144 - x * 16 + y * 16, 220 - x * 8 - y * 8 - 16))
    if not runAlgor and not runVisual:
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
                    isProper, isWin = gameObj.make_move(level1, swatches, 'R')
                elif event.key == K_LEFT:
                    isProper, isWin = gameObj.make_move(level1, swatches, 'L')
                elif event.key == K_UP: 
                    isProper, isWin = gameObj.make_move(level1, swatches, 'U')
                elif event.key == K_DOWN:
                    isProper, isWin = gameObj.make_move(level1, swatches, 'D')
                elif event.key == K_SPACE:
                    if not gameObj.isConsecutiveblock:
                        isProper, isWin = gameObj.make_move(level1, swatches, 'S')
                # for box in gameObj.block:
                #     if box[0] > levels.MAX_X or box[0] < 0 or box[1] > levels.MAX_Y or box[1] < 0 or level[box[1]][box[0]] == ' ':
                #         gameObj.block = [(levels.levels[level]['start']['x'],levels.levels[level]['start']['y'])]
                if not isProper:
                    level1, gameObj, level, enumlevel, swatches, vitalSwatchesNum = gameGenerate(level1)
                elif isWin:
                    level1 += 1
                    level1, gameObj, level, enumlevel, swatches, vitalSwatchesNum = gameGenerate(level1)

    
    screen.blit(background, (0,0))
    screen.blit(pygame.transform.scale(display, (400*1.8, 275*1.8)), (60, 120))

    # screen.blit(display, (0, 100))
    pygame.display.update()
