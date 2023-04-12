# Space Block - Roll the Block 

## Introduction

This is an implementation of the Space Block - Roll the Block solitaire game, which is a personal version of the Bloxorz game originally released on Miniclip in the year 2007.

Space Block – Roll the Block is a logic and spatial math solitaire puzzle game in which a 3D rectangular block slides along a board (platform) until it reaches a final destination.
The game implemented consists of a board built of 1x1 tiles that arrange in a specific shape and size, and of a 3D rectangular block composed of 2 tiles, sizing all together 1x1x2. 
The 3D block needs to roll/slide along the board until it reaches a certain destination - the goal destination, preferably in a few moves as possible. Along the path the block cannot fall off the edges of the platform it is put onto or get stressed (in a position that can make it fall off easily), which implies that the ends of the block must be always within the board bounderies. 

The game implemented has 6 levels, each with a distinct board configuration and distinct difficulty levels, containing traps that can make the player to fail the level. Some levels have buttons that trigger bridges. Each button is triggered when the block stands on it vertically. The bridges allow new paths that are needed to reach the goal tile and win the level.

The 3D block can be in three positions: 

	* standing vertically: in this position the block takes up one tile;
	* lying horizontally: in this position the block takes up two tiles;
	* lying vertically: in this position the block takes up two tiles;

The block can move from its previous position into four directions (right, left, up, down) by using the arrow keys.

When the block reaches the destination tile it must be in a standing position. 

The program allows a human player to solve the levels. It also has five different search methods that allow the computer to solve each level alone. It implements 3 uninformed search methods (breadth-first search, depth-first search and iterative deepening) and 2 heuristic search methods (greedy search and A* Algorithm), the later with three different heuristic functions each (Manhattan distance, Euclidean distance and Chebyshev distance). The application has a text or graphical use interface that shows the evolution of the game (level number of movements and score). The application also allows the player to interact in each level: it allows the player to select a search method for the computer to solve the level, and in the case of informed search methods, the player may also select the heuristic function to use.


## Coding language

Python 3.10.11


## How to compile, run and use the program

### Python packages required

pygame 2.3.0 


### Installation

```
$ pip3 install -r requirements.txt
```

### How to Run the Game

Run the file:
```
$ python3 main.py
```

### How to play

Press UP and DOWN arrow keys to navigate through the Menu
Press ENTER Key to start playing:
* Arrow Keys: to move the 3D block
	* When playing look at the board as if in a vertical position.
	* This means that:
		* UP key moves the block to the right
		* DOWN key moves the block to the left
		* LEFT key moves the block up
		* RIGHT key moves the block down
* Triggerring the buttons round and cross buttons will trigger the formation of "bridges" for the block to move
	* round button, can be hit by any part of the block
	* X button can be switched from off to on only if the block hits the switch vertically	
* Press ESC to quit the game


