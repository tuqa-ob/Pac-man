*This activity has been created as part of the 42 curriculum by sal-omar, tobaidat.*

# Pac-Man

## Description

**Pac-Man** is a clone of the classic arcade game, written in Python 3.13 with the `pygame` library. It was developed by two students over roughly three months.

**Goal:** the player moves through a maze and must eat every pac-gum and super pac-gum on the level. Once the level is cleared, the game moves on to the next level with a new maze. Clearing all the levels wins the game.

**Main features**

- Multiple levels, each with its own maze (generated with the provided `mazegenerator` package).
- The player starts with a configurable number of lives and loses one each time a ghost catches them.
- Eating a **pac-gum** gives points; eating a **super pac-gum** gives more points and lets the player eat ghosts for a short time, earning extra points per ghost.
- Four ghosts: three move randomly, and the **red ghost chases the player using BFS**.
- A time limit per level (`level_max_time`).
- Name entry after every win or loss, and a **Top 10 highscores** screen.
- Main menu, instructions screen, pause menu, and game over / victory screens.
- Everything is driven by a JSON configuration file.

## Instructions

### 1. Download and Run the Packaged Game

The game is available as a free Linux build on itch.io.

1. Visit the [Pac-Man itch.io page](https://tobaidat.itch.io/pac-man).
2. Download `PacMan-Linux.zip`.
3. Extract the ZIP file.
4. Make sure the extracted directory contains both the `PacMan/` folder and the `config.json` file.
5. Open a terminal in the extracted directory and run:

```bash
./PacMan/PacMan ./config.json
```

No separate Python or Pygame installation is required.

**Platform:** Linux 64-bit (x86_64).

### 2. Run from Source Code

To run the game from the source code, make sure Python 3 and the required dependencies are installed.

Install the dependencies:

```bash
make
```

You can launch the game using either of the following commands from the project root directory:

**Option A: Using Makefile**

```bash
make run
```

**Option B: Using Python directly**

```bash
python3 pac-man.py config.json
```

### Controls

| Key | Action |
| --- | --- |
| Arrow keys / `W` `A` `S` `D` | Move Pac-Man |
| `C` | Toggle cheat mode |

### Cheat Mode (for evaluation)

Press `C` to activate or deactivate cheat mode.

| Key | Effect |
| --- | --- |
| `I` | Toggle invincibility |
| `F` | Freeze or unfreeze ghosts |
| `B` | Toggle speed boost |
| `E` | Gain an extra life |
| `L` | Skip the current level |

## Configuration

The game is launched with a JSON file (`config.json` by default). The file must provide the following keys:

| Key | Description | Example / default |
| --- | --- | --- |
| `highscore_filename` | File where the highscores are stored | `highscores.json` |
| `level` | Array of levels, in play order; each level has its own `width` and `height` | 10 levels, from 10x10 up to 30x35 |
| `lives` | Starting number of lives | `3` |
| `pacgum` | Number of pac-gums | `42` |
| `points_per_pacgum` | Points for eating a pac-gum | `10` |
| `points_per_super_pacgum` | Points for eating a super pac-gum | `50` |
| `points_per_ghost` | Points for eating a ghost | `200` |
| `seed` | Seed used for maze generation (reproducible mazes) | `42` |
| `level_max_time` | Maximum time per level, in seconds | `90` |

Default `config.json`:

```json
#Game Configuration File

{
  "highscore_filename": "highscores.json",
  "lives": 3,
  "points_per_pacgum": 10,
  "points_per_super_pacgum": 50,
  "points_per_ghost": 200,
  "seed": 42,
  "level_max_time": 90,
  "pacgum": 42,
  "level": [
    {"width": 10, "height": 10},
    {"width": 15, "height": 10},
    {"width": 20, "height": 10},
    {"width": 20, "height": 15},
    {"width": 20, "height": 20},
    {"width": 25, "height": 20},
    {"width": 25, "height": 25},
    {"width": 30, "height": 25},
    {"width": 30, "height": 30},
    {"width": 30, "height": 35}
  ]
}
```

The first line is a comment (`#Game Configuration File`); comment lines starting with `#` are ignored when the file is read. The mazes get progressively bigger, so the game gets harder level after level, and the player wins after clearing the last one .

When `level_max_time` runs out, the game ends with a **Game Over**, and the player is asked to enter their name for the highscores.

**Robust parsing rules**

- The file is standard JSON, plus comments: every line starting with `#` is ignored. Comments starting with `//` are also supported. (Only the configuration file supports comments; the highscores file does not.)
- If a key is **missing** or its value is **invalid** (wrong type, out of range), the value is clamped to a safe default, a clear message is logged, and the game continues.
- **Unknown keys** are ignored.
- The game never crashes with a traceback because of the configuration file: if the file cannot be read or parsed, the defaults are used and an error message is logged.

**Built-in default values** (defined in `pm_game/config.py` and used whenever a value is missing or invalid):

| Key | Default |
| --- | --- |
| `highscore_filename` | `highscores.json` |
| `lives` | `3` |
| `pacgum` | `42` |
| `points_per_pacgum` | `10` |
| `points_per_super_pacgum` | `50` |
| `points_per_ghost` | `200` |
| `seed` | `42` |
| `level_max_time` | `90` |
| `level` | 10 levels: 10x10, 15x10, 20x10, 20x15, 25x15, 25x20, 30x20, 30x25, 35x25, 40x30 |


**Allowed ranges**

- All numeric values (`lives`, `pacgum`, the points, `seed`) must be `0` or greater.
- `level_max_time` must be strictly greater than `0`.
- The minimum maze size is `5x5`. There is no upper limit on the maze size.

Any value outside these ranges is replaced by its default value.

## Highscore

The game has a **persistent highscore system**: scores survive between runs. Highscores are stored in a JSON file named `highscores.json` (the name comes from `highscore_filename` in the config).

- After every **win or loss**, the player enters their name.
- The name and final score are saved.
- Only the **10 best scores** are kept and displayed in the Highscores screen, sorted from highest to lowest.

**Why this design?** JSON is human-readable, easy to load and save with Python's standard library, needs no extra dependency, and is the same format as the configuration file. Saving after both wins and losses means every run counts and the table always reflects the best results. Keeping only the top 10 keeps the file small and the screen readable.

If `highscores.json` does not exist, the game creates it by itself. Until a score is saved, the Highscores screen shows *No scores yet*.

**File structure:** a JSON list of entries, each with a player `name` and a `score`, sorted from highest to lowest:

```json
[
  {
    "name": "tuqa",
    "score": 760
  },
  {
    "name": "sal-omar",
    "score": 620
  }
]
```

If the file is corrupted (for example, an empty file or invalid JSON), it is ignored and the game starts recording scores from scratch.

## Maze Generation

Mazes are generated with the **A-Maze-ing** package provided by the subject. It was delivered as a compressed archive; we extracted it and placed the resulting `mazegenerator/` folder at the root of the repository, and we import it in our code as `mazegenerator`.

- Each level has its own width and height, taken from the configuration.
- The `seed` from the configuration makes the generation reproducible.
- The `MazeGenerator` class is called with `perfect=False`, so the maze contains loops (several paths between two cells), which suits a Pac-Man game better than a perfect maze with a single path.
- The generator receives the width and height of the level and returns the maze as a grid of rows and columns. Each cell is encoded as a number from **0 to 15**, where each bit represents a wall: **north = 1, east = 2, south = 4, west = 8**.
- The game never talks to `mazegenerator` directly. The `MazeAdapter` class in `pm_game/adapter.py` calls the generator and converts its output into the structure used by the game. This keeps the generation separate from the game logic, so either side can change without breaking the other.

**Placing the game elements on the maze**

- **Pac-gums** are distributed randomly.
- **Super pac-gums** are placed in the corners of the maze.
- **Pac-Man** starts at the center of the maze.
- **Ghosts** start in the corners.

## Implementation

- **Game loop:** the game reads input, updates the player, ghosts and level state, then renders each frame with `pygame`.
- **Player:** moves with arrow keys or WASD, collects gums, and loses a life on contact with a ghost (unless a super pac-gum is active).
- **Ghosts:** four ghosts. Three move randomly; the red ghost computes a path to the player with **BFS** and follows it.
- **Collisions and scoring:** collisions between the player and ghosts, and between the player and gums, are handled in the game/level logic. Scores come from the configuration.
- **Timer:** each level has a time limit (`level_max_time`). When it reaches zero, the game is over.
- **Pause:** a pause button is shown on screen and is clicked with the mouse. The pause menu offers resuming or exiting the game.
- **Levels:** when all gums are eaten the next level is loaded with a new maze; finishing the last level wins the game.
- **Assets:** images and the `BebasNeue-Regular.ttf` font are stored in `assets/`.

> TODO: add how long the super pac-gum effect lasts, the speed of entities, and what happens to eaten ghosts.

## General Software Architecture

```
.
├── pac-man.py          # Entry point: loads the config and starts the game
├── config.json         # Game configuration
├── highscores.json     # Saved highscores
├── Makefile            # Installation and run targets
├── requirements.txt    # Python dependencies
├── assets/             # Images and font
├── mazegenerator/      # A-Maze-ing package (provided)
└── pm_game/            # Game package
    ├── adapter.py      # Converts mazegenerator output to the game's maze format
    ├── config.py       # Loads and validates the configuration file
    ├── direction.py    # Direction definitions
    ├── game.py         # Main game class and game loop
    ├── ghost.py        # Ghost behavior (random movement, BFS chase for the red ghost)
    ├── highscore.py    # Reading, updating and saving the Top 10
    ├── input.py        # Keyboard input handling
    ├── level.py        # Level state: maze, gums, win condition, timer
    ├── menu.py         # Main, pause and other menus
    ├── player.py       # Pac-Man movement, lives and score
    └── render.py       # Drawing everything on screen
```

> TODO: verify each description above against your real code and add the relationships between classes (for example, `Game` uses `Level`, `Player`, `Ghost`, `Menu`, `Render` and `HighScore`).

## Project Management

We collaborated through GitHub. The work was split as follows, in order:

1. **tobaidat** wrote the configuration module (`config.py`), handled all possible configuration errors, and prepared the `config.json` file.
2. **sal-omar** wrote `level.py`.
3. **tobaidat** wrote `game.py` and integrated the level into it, then wrote `player.py`.
4. **sal-omar** wrote `ghost.py`.
5. **tobaidat** wrote a first version of `render.py`. At this point the game worked, but in a basic form: no designs, options, or extra features.
6. **sal-omar** then built most of the front end: the backgrounds and images, and the screens (menu, win, game over, highscores, instructions) and buttons. She made them work together and made the screens react to mouse clicks.
7. **tobaidat** finally reviewed the whole code, found the mistakes and missing requirements we had overlooked, and fixed them.

Project management directory: [Project Management](./PROJECT_MANAGEMENT.md)

## Resources

**References**

- [pygame documentation](https://www.pygame.org/docs/)
- [Python documentation](https://docs.python.org/3/)
- [Breadth-first search (Wikipedia)](https://en.wikipedia.org/wiki/Breadth-first_search)
- [Pac-Man (Wikipedia)](https://en.wikipedia.org/wiki/Pac-Man)
- [Manhattan distance tutorial (DataCamp)](https://www.datacamp.com/tutorial/manhattan-distance): to understand the distance between a ghost and the player.
- [freepacman.org](https://freepacman.org): to get to know the original game and understand how it is played.

**Use of AI**

AI tools were used as follows:

- **Claude:** to understand the subject's tasks, to list all the requirements, and to make sure no case was forgotten. It was also used to help write this README.
- **ChatGPT:** to understand the algorithms, and how all the parts of the game work together inside the game loop.
- **Gemini:** to generate the images and backgrounds used in the game (found in `assets/`).
