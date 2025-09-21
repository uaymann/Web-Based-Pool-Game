# Pool Game Web Application

This project is a web-based 8-ball game, a full-stack application built with C, Python, SQL, JavaScript, HTML, and CSS. It integrates a custom physics library written in C (exposed to Python through SWIG) with a Python backend and a database for tracking player information and game states. The frontend provides an interactive interface where users can play a simulated pool game, while the backend handles game logic, data storage, and winner determination.

---

## Requirements
- Python 3.11 (and `python3.11-dev` headers if rebuilding the library)
- SWIG
- `clang` or `gcc`
- A web browser (Chrome, Firefox, etc.)

---

## Building the Project
To compile the shared libraries and SWIG bindings, run:

```bash
make
```
This generates:

- libphylib.so – shared C library
- _phylib.so + phylib.py – Python bindings
- phylib_wrap.c – SWIG wrapper code

If you need to clean everything:
```bash
make clean
```

---

## Running the Backend
Start the Python server (choose a port number, e.g. 8000):
```bash
LD_LIBRARY_PATH=.
python3 A4server.py 8000
```
You should see:
```yaml
Server listening in port: 8000
```

---

## How to play
1. Go to `http://localhost:8000/form.html` in your browser to open the start page where you put in player names.
2. Once you hit "Start Game" the game will begin and indicate whose turn is first.
3. Drag your mouse in the direction you want your cue ball to go; the length of the line you drag out will determine the ball's speed and acceleration.
4. Once a winner is determined, the game will end and the browser will show a pop-up that says which player won the game.

---

## Game Data and Database

This project uses **SQLite** (`phylib.db`) to store and manage game data.  
The database keeps track of:
- Players and their names (entered from `form.html`)
- Game state (ball positions, turns, and shots taken)
- Scores and fouls
- The final outcome (who won the game)

During gameplay:
1. When players enter their names in the start form, they are saved into the database.
2. Each shot taken is recorded with its result (balls pocketed, cue ball reset, etc.).
3. The database is queried after each shot to check if the game-ending conditions are met (e.g., sinking the 8-ball).
4. Once a winner is determined, the backend uses the stored data to identify the winning player and sends this result back to the frontend.

This ensures that the game state is persistent across turns and makes it easier to manage scoring logic and determine the winner correctly.

---

## Notes:

- the light coloured balls go to player 1 and darker coloured ones go to player 2, the black ball is the 8-ball
- if the cue ball is hit into a hole, you must click anywhere on the table once to get it back in its original position for the next player's turn
- there are some bugs in the current version of the game, dragging the cue ball line too far may cause glitches in the animation but the game will resume once the balls have come to a stop

