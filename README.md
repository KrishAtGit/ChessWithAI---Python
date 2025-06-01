# CHESS GAME IN PYTHON, WITH AI
## Overview
This is a complete chess game developed in Python utilizing Pygame and the Stockfish chess engine. Compete against an AI opponent with customizable difficulty settings, all while experiencing smooth animations and sound effects.

## Features
- Complete implementation of chess rules and piece movements
- AI powered opponent using StockFish
- Different levels of AI, 0 - 20
- Piece animations
- Visual highlighting of valid moves
- Game restart functionality
- Pawn promotion to queen

## PAWN PROMOTION
- ![Screenshot 2025-06-01 211244](https://github.com/user-attachments/assets/570c1e34-aa49-45af-8056-e56baad0ac76)
  
- ![Screenshot 2025-06-01 211255](https://github.com/user-attachments/assets/038c1ad0-5953-4bce-8ec4-d97b5a96b837)

- ![Screenshot 2025-06-01 211305](https://github.com/user-attachments/assets/854e1d87-3019-4f0a-ae03-a02620e8ed09)

## Requirements
- Python 3.7+
- Pygame
- python-chess
- Stockfish chess engine

## Installation
1. ### Clone Repository
    ```git clone https://github.com/KrishAtGit/ChessWithAI---Python.git``` and 
    ```cd ChessWithAI---Python```

2.  ### Install dependencies
    ```pip install pygame python-chess```

3. ### Install StockFish
    Link: https://stockfishchess.org/download/

4. ### Change the path of StockFish in code
    ```self.engine = chess.engine.SimpleEngine.popen_uci("path\to\stockfish.exe")```
5. ### Run the code
    ```python chess_game.py```
