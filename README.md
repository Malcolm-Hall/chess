# ♕♘ Chess
The standard variant of chess written in Python, using the [Pyglet library][1] for a clean and responsive GUI.

![Chess starting position][4]

## Features
* Legal move checking
* Load any position from a valid [FEN][2]
* Pawn promotion to Queen, Rook, Bishop, or Knight
* [En passant][3]
* Undo moves
* More to come

## Requirements
Python 3.9 or later
Required python libraries can be installed via ``pip3``
```sh
pip3 install -r requirements.txt
```

## Usage
To start playing chess run ``main.py`` in the chess package directory
```sh
python3 chess/main.py
```
To load a position from [FEN notation][2] enter a valid FEN when prompted, otherwise leave blank for a new game of chess.

## Controls
* Left click: select and move chess pieces
* Right click: undo the last move

## License
Distributed under the GNU GPLv3 license. See ``LICENSE`` for more information.

[1]: http://pyglet.org/
[2]: https://en.wikipedia.org/wiki/Forsyth-Edwards_Notation
[3]: https://en.wikipedia.org/wiki/En_passant
[4]: resources/chess_starting_position.png
