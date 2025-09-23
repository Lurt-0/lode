# Lode

A two player game made in Python for a university programming course.

## Documentation

### Starting

Before startting the game you need to make sure you have python 3 installed and you also need to install pygame module. You can install python here: `https://www.python.org/downloads/` and than you can install pygame by typing `python3 -m pip install -U pygame --user` into the terminal. You can start the game by typing `python main.py` in project directory or by opening and starting the `main.py` file in your chosen IDE.

#### Menu

You can sellect either 1 Player, where you play against AI or 2 Players, where you play ageinst somebody on the same device. You can also select Guit to leave the game.

#### Game

Game has two parts "selection" and "shooting" in selection both players place their boats and while shooting you try to sink all of opponents boats. If you miss the other player plays (AI plays automatically). For more info press TAB while in game.

### Technical description

The game has two ways of placing boats, in first option you can place boats yourself by clicking two ending tiles of a boat. During this process the game dynamicly checks, that your boat placment is valid, and if it is the game dysplays, where the boat will be. In second option the game randomly sellects tile, direction and boat lenght and it tryes to place a boat if it can, until all boats are placed. If you choose game for one player, than you will play against AI. Until the AI hits a boat it shoots random valid tiles. When it hits a boat it shoots random neihgbouring tiles and when it hits a second tile and than it continues in that direction, or the opossite, until the whole boat is sunk. After every shot the game checks, if the current player has sunk all the boats, and if he did it loads the ending screen, whitch is modified start screen.
