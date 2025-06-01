import pygame
import sys
import chess.engine
import tkinter.messagebox
import time  
import os

#NEW FEATURES ADDED:
#1. Sound effects for moves, captures, check, and checkmate.
#2. AI opponent using Stockfish engine.
#3. Pawn promotion with a message box.
#4. Animation for piece movement.
#5. Different levels of AI skill using Stockfish's skill level configuration.
#6. Restart using R key.
#7. Highlighting valid moves for the selected piece.


#initializing the game
pygame.init()

#defining constants for the game
WIDTH, HEIGHT = 600, 600 #board size
ROWS, COLS = 8, 8 #number of rows and columns
TILE_SIZE = WIDTH // COLS #1 tile of the board is the result of total width / number of cols
WHITE = (252, 252, 252) #this is the white tile color
BLACK = (115, 14, 6) #this is the black tile color, although it is not black, i labelled it as black as its easier to understand
HIGHLIGHT = (68, 202, 88) #color to highlight legal moves of the selected piece
FPS = 60 #frames per second, this is the speed of the game


#initialising mixer for sound effects
pygame.mixer.init()

#loading the images
IMAGES = {} #empty dict of images 
#list of the names of the chess pieces, which will be used to load the images
pieces = ['r','n','b','q','k','p','R','N','B','Q','K','P']

#function to load the images of the pieces
def load_images():
    #a dictionary to assign the images as r, n, etc. so its easier to place them on the board using a for loop
    #ASSIGNING LOWERCASE TO BLACK, AND UPPERCASE TO WHITE
    piece_to_filename = {
        'r': 'brown-castle.png',
        'n': 'brown-elephant.png',
        'b': 'bishop-brown.png',
        'q': 'brown-queen.png',
        'k': 'brown-king.png',
        'p': 'brown-pawn.png',
        'R': 'white-castle.png',
        'N': 'white-elephant.png',
        'B': 'white-bishop.png',
        'Q': 'white-queen.png',
        'K': 'white-king.png',
        'P': 'white-pawn.png',
    }
    
    #iterating over the items in the dictionary and placing them on the board
    for piece, filename in piece_to_filename.items():
        image = pygame.image.load(f"images/{filename}")
        IMAGES[piece] = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))

#function to load sounds for sound effects
def load_sound():
    #empty dictionary to store the sounds
    sounds = {}
    #folder where the sound files are stored
    folder = 'sounds'

    #list of sound files to be loaded, with their respective keys
    files = {
        'move' : 'move.mp3',
        'capture' : 'capture.mp3',
        'check' : 'check.mp3',
        'checkmate' : 'check.mp3',
        'restart' : 'restart.mp3',
    }

    #iterating through the files dictionary to load the sound files
    for key, value in files.items():
        try: 
            #loading the sound file and scaling it to the tile size
            sounds[key] = pygame.mixer.Sound(os.path.join(folder, value))
        except:
            #if the sound file is not found, print an error message
            print(f"Error loading sound: {value}!")
    #returning the sounds dictionary containing all the loaded sound effects
    return sounds


#making a class for the game
class ChessInPython:
    
    #CONSTRUCTOR OF THE CLASS
    def __init__(self):

        #initialising the display screen
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        #setting the title of the window
        pygame.display.set_caption("Manual Python Chess")

        #intialising clock
        self.clock = pygame.time.Clock()

        #intialising the chess board
        self.board = self.create_board()

        #by default, no pieces are selected
        self.selected = None

        #an array to store all the valid moves
        self.valid_moves = []

        #first white will play, according to the rule of chess
        self.turn = 'w'

        #setting running to true, indicating that the game is running
        self.running = True

        #initialising stockfish engine as AI (adding the path to the stockfish executable)
        self.engine = chess.engine.SimpleEngine.popen_uci(r"C:\Users\Krish Jangra\Downloads\stockfish-windows-x86-64-avx2 (1)\stockfish\stockfish-windows-x86-64-avx2.exe")
        self.skill_level = 10 #setting the skill level, it can be from 0 to 20 with 20 being the highest/most skilled
        #applying the skill level to the engine after defining it
        self.engine.configure({"Skill Level": self.skill_level})

        #storing AI move data, initially as none
        self.ai_move_data = None  

        #setting the game to not show stats screen by default
        self.show_stats_screen = False  
        #setting the win probability for both players, initially as 50% for both
        self.win_probability = {"white": 50, "black": 50}  

        #loading the sound effects
        self.sounds = load_sound()  

    #assigning the position as 'r', 'R', etc. to place the pieces accordingly
    #returning a 2D array of the whole board
    def create_board(self):
        return [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p'] * 8,
            [''] * 8,
            [''] * 8,
            [''] * 8,
            [''] * 8,
            ['P'] * 8,
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]

    #function to draw the chess board
    def draw_board(self):

        #2 for loops for rows and cols
        #for loop for rows
        for row in range(ROWS):
            #for loops for columns
            for col in range(COLS):
                #if the sum of the rows and cols is even, then the tile should be white
                if (row+col) % 2 == 0:
                    color = WHITE
                else:
                    #if odd, its black
                    color = BLACK

                #drawing the tile using the rectangle function from pygame
                pygame.draw.rect(self.screen, color, (col*TILE_SIZE, row*TILE_SIZE, TILE_SIZE, TILE_SIZE))

                #checking if the current tile (row, col) is one of the valid moves for the selected piece
                if (row, col) in self.valid_moves:
                    #creating a new image of the tile, with the same dimensions
                    s = pygame.Surface((TILE_SIZE, TILE_SIZE))
                    #setting transparency of the image, it will overlap the original tile
                    s.set_alpha(100)
                    #highlights the image to the color defined at the start of the code
                    s.fill(HIGHLIGHT)
                    #drawing the translucent image of green tile which marks the valid moves of the pieces
                    self.screen.blit(s, (col*TILE_SIZE, row*TILE_SIZE))

    #placing the images on the board
    def placing_pieces(self):
        #looping through the board, (rows and cols)
        for row in range(ROWS):
            for col in range(COLS):
                #assigning the piece on the board at the row,col position
                piece = self.board[row][col]
                #checking if the piece is present on the board (piece is a string that goes like 'r', 'R', etc.)
                if piece:
                    #calculates where the image should be placed, and places it on its respective position
                    self.screen.blit(IMAGES[piece], (col*TILE_SIZE, row*TILE_SIZE))

    #i set the pieces for white as uppercase letters in the create_board() function
    # for black its lowercase
    # this function checks if the piece is lowercase or uppercase  
    def get_piece_color(self, piece):
        #if the piece is R, Q, etc. (uppercase), then it is white
        if piece.isupper(): return 'w'
        #if lowercase, its black
        elif piece.islower(): return 'b'
        #otherwise, none
        return None

    #function to animate the move of the piece
    def animate_move(self, start_pos, end_pos, piece):
        #setting the frames per square for the animation
        #the more frames per square, the slower the animation will be
        frames_per_square = 2 
        #calculating the difference in rows 
        diff_row = end_pos[0] - start_pos[0]
        #calculating the difference in columns
        diff_col = end_pos[1] - start_pos[1]

        #calculating the total number of frames for the animation
        frame_count = (abs(diff_row) + abs(diff_col)) * frames_per_square

        #calculating the starting and ending positions of the piece
        start_x = start_pos[1] * TILE_SIZE
        start_y = start_pos[0] * TILE_SIZE
        end_x = end_pos[1] * TILE_SIZE
        end_y = end_pos[0] * TILE_SIZE

        #making a copy of the board to avoid modifying the original board during animation
        temp_board = [row.copy() for row in self.board]
        
        #storing the piece and temporarily remove it from the board for animation
        saved_piece = self.board[start_pos[0]][start_pos[1]]
        self.board[start_pos[0]][start_pos[1]] = ''

        #animating the piece moving from start to end position
        #iterating through the frames
        for frame in range(frame_count + 1):
            #x is the fraction of the current frame over the total number of frames
            x = frame / frame_count

            #calculating the current position of the piece based on the fraction x
            current_x = int(start_x + (end_x - start_x) * x)
            current_y = int(start_y + (end_y - start_y) * x)

            #drawing the board and pieces
            self.draw_board()
            #placing the pieces on the board
            self.placing_pieces()  
            #drawing the moving piece
            #we will use the saved piece to draw the piece at the current position
            self.screen.blit(IMAGES[piece], (current_x, current_y))  
            #updating the display
            pygame.display.flip()
            #ticking the clock to control the frame rate
            self.clock.tick(FPS)
    
        #restoring the piece to the board at the original position
        #this will ensure the actual move is made by make_move()
        self.board[start_pos[0]][start_pos[1]] = saved_piece

    
    #this function checks the moves in the horizontal/vertical direction, i.e, straight in any horizontal/vertcal direction
    #along with the initial row and col, it also takes the directions of the piece
    #WE WILL USE THIS FUNCTION FOR ROOK, BISHOP, QUEEN MOVES
    def get_linear_moves(self, row, col, directions):
        moves_made = [] #moves_made array

        #x and y are the offsets for the directions
        #iterating through the directions, which are passed as a list of tuples -> (x, y)
        for x, y in directions:
            #r and c are the new row and new col respectively, which are calculated by adding x and y to old row and col respectively
            r, c = row + x, col + y

            #while the new row and new col are within the bounds of the board
            while 0 <= r < 8 and 0 <= c < 8:
                #checking the target piece at the new row and new col
                target = self.board[r][c]
                #if the target piece is empty, we can move the piece to that position
                if target == '':
                    moves_made.append((r, c)) #adding the move to the moves_made array

                #if the target piece is of opposite color, we can capture it and move the piece to that position
                elif self.get_piece_color(target) != self.turn:
                    #adding the move to the moves_made array
                    moves_made.append((r, c))
                    break
                #any other case, if the target piece is of the same color, we cannot move there
                else:
                    break

                #updating the row and col to the new position
                r += x
                c += y
        #returning the array of moves made
        return moves_made

    #function for pawn moves
    def get_pawn_moves(self, row, col, piece):
        if piece.isupper():
            #the piece is uppercase, meaning its white
            #white pieces are placed at the bottom of the board, so the direction would be negative as its going up 
            #the rows are labelled from 0 to 7 from top to bottm, and white piece goes from bottom to top (OPPOSITE DIRECTION)
            direction = -1
        else:
            #the piece is lowecase, meaning its black
            #black pieces are placed on the top of the board, so the direction would be positive as its coming down
            #the rows are labelled from 0 to 7 from top to bottm, and black piece comes from top to bottom
            direction = 1 
        
        #if the piece is uppercase, then its white
        #white pawn starts from row 6 from rows 0 to 7, one index before the last row
        #intial row is 6 because it starts from the bottom of the board
        if piece.isupper():
            intial_row = 6
        #if the piece is lowercase, its black
        else:
            #black pawn starts from row 1 from rows 0 to 7, one index after the first row
            #initial row is 1 because it starts from the top of the board
            intial_row = 1

        #empty array to store the moves made
        moves_made = []
        #checking if the move made to the new place is empty and within the bounds of the board
        if 0 <= row + direction < 8 and self.board[row + direction][col] == '':
            #if empty, add the move to the moves_made array
            moves_made.append((row + direction, col))
            
            #checking if the piece hasn't moved, i.e, is at its starting point
            #if true, it will allow the user to move 2 steps forward, according to the chess rules
            if row == intial_row and self.board[row + (2 * direction)][col] == '':
                #adding to the moves_made array
                moves_made.append((row + (2 * direction), col))
        
        #this is the CAPTURE move
        #checking if a piece is available diagonally
        # [-1,1] checks in both directions, left or right (col+1 or col-1)
        for diag_col in [-1, 1]:
            #the updated column will be the initial col + diag_col
            new_col = col + diag_col
            #checking if in bounds
            if 0 <= new_col < 8 and 0 <= row + direction < 8:
                #this takes any piece present diagonally and label it as the target
                target = self.board[row + direction][new_col]
                #if the recognised piece, which is present diagonally, is of opposite color
                #checking if the piece is of opposite color, for example, if the white pawn has to capture a black piece diagonally, it means its white's turn 
                #this proves that its not the turn on black, and if its not diagonal piece's turn, its the opposite color
                if target and self.get_piece_color(target) != self.turn:
                    moves_made.append((row + direction, new_col)) #adding the move to the moves_made array

        #return the moves made
        return moves_made

    #checking the rook's moves
    def get_rook_moves(self, row, col):
        #as we know, rook moves either vertically or horizontally, in a straight line
        #so the directions will be (-1, 0) [down, vertical], (1, 0) [up, vertical], (0, -1) [left, horizontal], (0, 1) [right, horizontal] 
        #this covers all possible directions it can move in
        #passing it in linear moves func, then returning the result
        return self.get_linear_moves(row, col, [(-1, 0), (1, 0), (0, -1), (0, 1)])

    #checking bishop's moves
    def get_bishop_moves(self, row, col):
        #bishop moves diagonally 
        #the possible moves can be (-1, -1) [bottom-left], (-1, 1) [bottom-right], (1, -1) [top-left], (1, 1) [top-right]
        #this covers all the possible moves of bishop
        #passing it in linear moves func, then returning the result
        return self.get_linear_moves(row, col, [(-1, -1), (-1, 1), (1, -1), (1, 1)])

    #checking queen's moves
    def get_queen_moves(self, row, col):
        #queen is a mix of bishop and rook moves, it can straight or diagonally in any direction
        #possible directions can be rook moves --> [(-1, 0), (1, 0), (0, -1), (0, 1)], bishop moves --> [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        #passing the combination in linear moves func, and returning the result
        return self.get_linear_moves(row, col, [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)])

    #checking king's moves
    def get_king_moves(self, row, col):
        #moves made are stored in an array
        moves_made = []

        #king moves one step in any direction
        #(-1,-1)  (-1,0)   (-1,1)
        #(0,-1)    KING    (0,1)   [KING'S POSITION = (0,0)]
        #(1,-1)   (1,0)    (1,1)
        #possible rows it can move to: -1, 0, 1
        #possible cols it can move to: -1, 0, 1
        
        #looping through the coordinates of the row
        for sel_row in [-1, 0, 1]:
            #looping through the coordinates of the col
            for sel_col in [-1, 0, 1]:
                #skipping if the move where king moves to (0,0), as it is its current pos 
                if sel_row == 0 and sel_col == 0:
                    continue

                #CAPTURING PIECES
                #calculating the coordinates of the target piece
                r, c = row + sel_row, col + sel_col
                #if the target is in bounds
                if 0 <= r < 8 and 0 <= c < 8:
                    #calculating the location of the target on the board 
                    target = self.board[r][c]
                    #checking if the target piece we are pointing at is empty or of opposite color
                    #if true, then we can move the king diagonally as a capture move (if the piece is of opp color)
                    if target == '' or self.get_piece_color(target) != self.turn:
                        moves_made.append((r, c)) #adding the move to the moves_made array
        #retrning the moves_made array
        return moves_made

    #checking tge knight's moves
    def get_knight_moves(self, row, col):
        #same procedure, setting up an empty movesmade array to store the valid moves
        moves_made = []
        #knight moves in an L shape, that means, 2 steps in one direction and one step in any direction horizontally
        #setting up an array of directions the knight can move to
        knight_directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

        #iterating over the offsets (directions) of the knight, in each direction
        # (x,y) --> offsets
        for x, y in knight_directions:
            #r and c are the new row and new col respectively
            #the new rows/cols will be the intiial rows/cols + the direction knight is moving in
            r, c = row + x, col + y

            #capturing piece
            #checking if in bounds
            if 0 <= r < 8 and 0 <= c < 8:
                #assigning any piece detected diagonally as target
                target = self.board[r][c]
                #if the target is empty or of opponent's color, we can move the bishop to that place
                if target == '' or self.get_piece_color(target) != self.turn:
                    moves_made.append((r, c)) #adding in the moves made array as a legal move

        return moves_made

    #function to calculate the valid moves of each piece
    def get_valid_moves(self, row, col):
        #selecting the piece at the passed coordinates 
        piece = self.board[row][col]
        #if no piece is found at the selected coordinate, or the piece found is of opponent's, then return nothing
        #this skips the part, returning an empty array
        if not piece or self.get_piece_color(piece) != self.turn:
            return []
        
        #defining an empty array to store all the moves
        total_moves = []
        
        #if the piece has a string value of 'p' or 'P', then its a pawn
        if piece.upper() == 'P':
            total_moves = self.get_pawn_moves(row, col, piece)
        #if the piece has a string value of 'r' or 'R', then its a rook  
        elif piece.upper() == 'R':
            total_moves = self.get_rook_moves(row, col)
        #if the piece has a string value of 'n' or 'N', then its a knight
        elif piece.upper() == 'N':
            total_moves = self.get_knight_moves(row, col)
        #if the piece has a string value of 'b' or 'B', then its a bishop
        elif piece.upper() == 'B':
            total_moves = self.get_bishop_moves(row, col)
        #if the piece has a string value of 'q' or 'Q', then its a queen
        elif piece.upper() == 'Q':  
            total_moves = self.get_queen_moves(row, col)
        #if the piece has a string value of 'k' or 'K', then its a king
        elif piece.upper() == 'K':
            total_moves = self.get_king_moves(row, col)

        #we collected all of the moves that our pieces can make, however, only a fraction of those moves will be legal
        #to find the legal moves, creating an empty array to store it
        legal_moves = []
        #looping through the array of total_moves
        for move in total_moves:
            #creating a temporary copy of the board
            board_copy_temp = [row.copy() for row in self.board]
            #getting the initial position of the selected piece
            start_row, start_col = row, col
            #getting the final/ending position of the piece
            ending_row, ending_col = move
            #making the move by shifting the piece to the specified coordinates
            board_copy_temp[ending_row][ending_col] = board_copy_temp[start_row][start_col]
            #setting the initial position as null, leaving it vacant
            board_copy_temp[start_row][start_col] = ''
            
            #converting the board to FEN 
            #it is essential to convert the moves to FEN in order to communicate with STOCKFISH
            fen = self.to_fen(board_copy_temp)

            #creating an object from the FEN string
            board = chess.Board(fen)
            #checking if the KING is in check, if false --> add the legal move to the legal_moves array
            #this is done to ensure that the player is not able to move any piece when their king is in check
            if not board.is_check():
                legal_moves.append(move)

        return legal_moves
    
    #function to make a move on the board
    def make_move(self, start, end):

        #start and end are tuples, so we need to unpack them
        #start is the initial position of the piece, and end is the final position of the piece
        start_row, start_col = start
        end_row, end_col = end
        
        # Get the piece at the start position
        piece = self.board[start_row][start_col]
        
        # Check if this move is a capture
        is_capture = self.board[end_row][end_col] != ''
        
        # Move the piece
        self.board[end_row][end_col] = piece
        self.board[start_row][start_col] = ''
        
        # Play the appropriate sound
        if is_capture and 'capture' in self.sounds:
            self.sounds['capture'].play()
        elif 'move' in self.sounds:
            self.sounds['move'].play()
    
        # Handle pawn promotion
        if piece.upper() == 'P' and (end_row == 0 or end_row == 7):
            self.board[end_row][end_col] = 'Q' if piece.isupper() else 'q'
            if piece.isupper():
                tkinter.messagebox.showinfo("Promotion", "White Pawn promoted to Queen!")
            else:
                tkinter.messagebox.showinfo("Promotion", "Black Pawn promoted to Queen!")
            
        
        # Update turn
        if self.turn == 'w':
            self.turn = 'b'
        else:
            self.turn = 'w'
        
        # Check for check or checkmate after move
        board = chess.Board(self.to_fen(self.board))
        if board.is_checkmate():
            if 'checkmate' in self.sounds:
                self.sounds['checkmate'].play()
            tkinter.messagebox.showinfo("Game Over", "Checkmate! AI wins!")
            self.running = False
        elif board.is_check():
            if 'check' in self.sounds:
                self.sounds['check'].play()

    #function to convert the board state to FEN notation
    def to_fen(self, board_state):

        #an empty array to store the FEN rows
        fen_rows = []
        #iterating through each row of the board state
        for row in board_state:
            #converting the row to FEN format
            fen_row = ''
            #counting the number of empty squares in the row, initially set to 0
            empty = 0

            #iterating through each piece in the row
            for piece in row:
                #if the piece is empty, increment the empty counter
                if piece == '':
                    empty += 1 #incrementing the empty counter

                #if the piece is not empty, we need to add it to the FEN row
                else:
                    #if there are empty squares before the piece, we need to add the count of empty squares to the FEN row
                    if empty > 0:
                        fen_row += str(empty) #adding the count of empty squares to the FEN row
                        empty = 0 #resetting the empty counter to 0
                        
                    #adding the piece to the FEN row
                    fen_row += piece
            #if there are any empty squares left at the end of the row, we need to add the count of empty squares to the FEN row
            #this is done to ensure that the FEN row is complete
            if empty > 0:
                #adding the count of empty squares to the FEN row
                fen_row += str(empty)
            
            #adding the FEN row to the fen_rows array
            fen_rows.append(fen_row)
        
        #joining the FEN rows with '/' to create the final FEN string and returning it
        #the format of the FEN string is: 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1
        #'w' or 'b' indicates the turn, and '-' indicates no castling rights
        #if castling rights are applicable, we can add 'KQkq' to the FEN string
        return '/'.join(fen_rows) + f" {'w' if self.turn == 'w' else 'b'} - - 0 1"

    #function to make the AI move
    def ai_move(self):
        #passing the current board state to the FEN function to convert it to FEN notation
        #this is done to ensure that the AI can understand the current state of the board
        board = chess.Board(self.to_fen(self.board))
        #checking if the AI is in checkmate, if true, then the game is over
        if board.is_checkmate():
            #showing a message box to the user indicating that the they have won
            tkinter.messagebox.showinfo("Game Over", "Checkmate! You win!")
            self.running = False
            return

        #checking if the AI is in stalemate, if true, then the game is a draw
        if board.is_stalemate():
            tkinter.messagebox.showinfo("Game Over", "Stalemate! It's a draw!")
            self.running = False
            return

        #calculating the best move for the AI using Stockfish engine
        #using the chess.engine.Limit to limit the time taken by the engine to calculate the move, setting it to 0.1 seconds for quick response
        #using play function to get the best move
        result = self.engine.play(board, chess.engine.Limit(time=0.1))
        #setting the move to the result of the engine's calculation
        move = result.move

        #making the move on the board
        #converting the chess positions returned by Stockfish to row and column indices
        #the fen notation gives us the square numbers, so we need to convert them to row and column indices
        #fen returns numbers from 0 to 64, whereas we need row and column indices from 0 to 7
        #to convert the square number to row and column indices, we can use the following formula: 
        start_row = 7 - (move.from_square // 8) #the reason we are subtracting from 7 is because the rows are labelled from 0 to 7, and the square numbers are labelled from 0 to 63
        #lets say the square number is 25, then the row will be 7 - (25 // 8) = 7 - 3 = 4, the 4th row from the top

        #similarly, the column will be the square number % 8
        #for the same square number 25, the column will be 25 % 8 = 1, the 1st column from the left
        start_col = move.from_square % 8
        end_row = 7 - (move.to_square // 8)
        end_col = move.to_square % 8

        #storing the AI move data to animate it later
        #storing it as a dictionary with start and end positions, and the time of the move
        self.ai_move_data = {
            'start': (start_row, start_col),
            'end': (end_row, end_col),
            'time': time.time()
        }

    #function to handle the click
    #pos is a tuple containing the x and y coordinates of the mouse click
    def handle_click(self, pos):

        #setting the row and col based on the position clicked
        #pos[0] is the x-coordinate, pos[1] is the y-coordinate
        #just like in c++, the row is the y-coordinate divided by the tile size, and col is the x-coordinate divided by the tile size
        #this is done to convert the pixel position to the row and col of the board
        col = pos[0] // TILE_SIZE #assigning the first value of the tuple to col, because COLUMNS (c1 -> c2 -> c3, we go horizontally) run horizontally so we use the x-coordinate
        row = pos[1] // TILE_SIZE #assigning the second value of the tuple to row, because ROWS (r1 -> r2 -> r3, we go vertically) run vertically so we use the y-coordinate

        #if the piece is selected, then we will check if the clicked position is a valid move
        if self.selected:
            #checking if the clicked position is a valid move
            if (row, col) in self.valid_moves:
                #getting the piece at the selected position
                piece = self.board[self.selected[0]][self.selected[1]]
                
                #animating the move
                self.animate_move(self.selected, (row, col), piece)
                
                #making the piece move on the board
                self.make_move(self.selected, (row, col))
                #deselecting the piece after the move is made
                self.selected = None
                #as the piece has been moved, we need to reset the valid moves
                self.valid_moves = []
                
                #making the AI move after the player's move
                self.ai_move()
            
            #if the clicked position is not a valid move
            else:
                #setting the selected piece to the clicked position
                self.selected = (row, col)
                #calculating the valid moves for the newly selected piece
                self.valid_moves = self.get_valid_moves(row, col)

        #if no piece is selected
        else:
            #setting the clicked position as the selected piece
            self.selected = (row, col)
            #calculating the valid moves for the selected piece
            self.valid_moves = self.get_valid_moves(row, col)

    #function to change the skill level of the AI
    def change_skill_level(self, level):
        #setting the skill level between 0 and 20
        self.skill_level = max(0, min(20, level))  #min is 0, max is 20
        #configuring the engine with the new skill level
        self.engine.configure({"Skill Level": self.skill_level})

    #screen to display the skill level of the AI, and allows the user to adjust it
    #this screen will be displayed when the user presses 'S' on the keyboard
    def stats_screen(self):
        #background color for the screen
        self.screen.fill((115, 14, 6))
        
        #creating font objects for the title and info text
        title_font = pygame.font.SysFont('impact', 36)
        info_font = pygame.font.SysFont('impact', 24)

        #drawing title for the screen
        title_text = title_font.render("CHESS ADJUSTMENTS", True, (255, 255, 255))
        self.screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 50))
        
        #typing the current skill level of the AI
        #by default, it will be set to 10
        level_text = info_font.render(f"Stockfish Skill Level: {self.skill_level}/20", True, (255, 255, 255))
        #blit function to center the text on the screen
        #the text will be displayed at the center of the screen, with a margin of 150 pixels from the top
        self.screen.blit(level_text, (WIDTH//2 - level_text.get_width()//2, 150))
        
        #drawing instructions for adjusting the skill level
        #this will tell the user to use UP and DOWN arrows to adjust the difficulty
        adjust_text = info_font.render("Use UP/DOWN arrows to adjust difficulty", True, (200, 200, 200))
        self.screen.blit(adjust_text, (WIDTH//2 - adjust_text.get_width()//2, 190))
        
        #setting bar dimensions for the skill level
        bar_width = 400
        bar_height = 30

        #drawing the skill level bar
        #drawing a grey rectangle for the background of the bar
        pygame.draw.rect(self.screen, (100, 100, 100), (WIDTH//2 - bar_width//2, 230, bar_width, bar_height))
        #calculating the width of the green rectangle based on the skill level
        #the width will be a percentage of the bar width, based on the skill level (0 to 20)
        level_width = int(bar_width * (self.skill_level / 20))
        #drawing a green rectangle for the skill level
        #the green rectangle will be drawn on top of the grey rectangle, with the width calculated above
        pygame.draw.rect(self.screen, (0, 200, 0), (WIDTH//2 - bar_width//2, 230, level_width, bar_height))

        restart_text = info_font.render("Press 'R' to restart the game", True, (200, 200, 200))
        self.screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, 390))

        #drawing instructions for the user to return to the game
        #this will tell the user to press 'S' to return to the game
        back_text = info_font.render("Press 'S' to return to the game", True, (200, 200, 200))
        self.screen.blit(back_text, (WIDTH//2 - back_text.get_width()//2, 500))

    def reset_game(self):
    # Reset the board to initial position
        self.board = self.create_board()
        
        #resetting the skill level to 10
        self.skill_level = 10
        #reconfiguring the engine with the new skill level
        self.engine.configure({"Skill Level": self.skill_level})
        #resetting to no piece selected
        self.selected = None
        #resetting the valid moves to an empty array
        self.valid_moves = []
        #resetting to white's turn
        self.turn = 'w'  
        #resetting the AI move data to None
        self.ai_move_data = None
    
    #playing a sound effect when the game is reset
        if 'restart' in self.sounds:
            self.sounds['restart'].play()

    #function to run the game
    def run(self):

        #while the game is running
        while self.running:
            #setting the clock to tick at the defined FPS
            self.clock.tick(FPS)

            #for loop to handle events
            for event in pygame.event.get():
                #if the event is quit, then we will exit the game
                if event.type == pygame.QUIT:
                    #game is closed, not running anymore
                    self.running = False

                #resetting the game if the user presses 'R'
                elif event.type == pygame.KEYDOWN:
                    #if the 'R' key is pressed, reset the game
                    if event.key == pygame.K_r: 
                        self.show_stats_screen = False
                        self.reset_game()
                    #if the 'S' key is pressed, toggle the stats screen
                    if event.key == pygame.K_s:  
                        self.show_stats_screen = not self.show_stats_screen

                    #handling the stockfish skill level change with up and down arrow keys
                    #if the up arrow key is pressed, increase the skill level
                    if event.key == pygame.K_UP:
                        #if the skill level is less than 20, increase it by 1
                        if self.skill_level < 20:
                            self.change_skill_level(self.skill_level + 1)
                            print(f"Stockfish Skill Level: {self.skill_level}")
                        else:
                            #limit reached, cannot increase skill level beyond 20
                            print("Maximum skill level reached -> 20.")

                    #if the down arrow key is pressed, decrease the skill level
                    elif event.key == pygame.K_DOWN: 
                        #if the skill level is greater than 0, decrease it by 1
                        if self.skill_level > 0:
                            self.change_skill_level(self.skill_level - 1)
                            print(f"Stockfish Skill Level: {self.skill_level}")
                        else:
                            #limit reached, cannot decrease skill level below 0
                            print("Minimum skill level reached -> 0.")

                #if the mouse button is clicked, then we will handle the click
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    #if the left mouse button is clicked and the player is white, then we will handle the click
                    if event.button == 1:  
                        #if the turn is white
                        if self.turn == 'w':
                            #handle the click  
                            self.handle_click(event.pos)


            #processing AI move if it's the AI's turn
            #if the AI move data is valid and enough time has passed, which is 1 second as a delay
            if self.ai_move_data and time.time() - self.ai_move_data['time'] >= 1.0:
                #assigning the start position as the start position of the AI move data from the ai_move_data dictionary
                start = self.ai_move_data['start']
                #assigning the end position as the end position of the AI move data from the ai_move_data dictionary
                end = self.ai_move_data['end']
                #getting the piece at the start position, i.e, the piece that the AI is moving
                piece = self.board[start[0]][start[1]]
                
                #animating the AI move
                #this will animate the move of the piece from start to end position
                self.animate_move(start, end, piece)
                
                #making the AI move on the board
                self.make_move(start, end)
                
                #setting the ai_move_data to None after the move is made
                #this is done to ensure that the AI does not make the same move again
                self.ai_move_data = None
                
                #redrawing the board and pieces after the AI move
                self.draw_board()
                #using placing_pieces to place the pieces on the board after the AI move
                #this will redraw the pieces on the board after the AI move, making the editions visible
                self.placing_pieces() 
                #updating the screen to show the changes made by the AI 
                pygame.display.update()
                
                #checking if the AI's move results in checkmate
                #converting the board to FEN notation to check for checkmate
                board = chess.Board(self.to_fen(self.board))
                #if the board is in checkmate state, then we will show a message box indicating that the AI has won
                if board.is_checkmate():
                    #if checkmate, playing the checkmate sound effect 
                    if 'checkmate' in self.sounds:
                        self.sounds['checkmate'].play()
                    tkinter.messagebox.showinfo("Game Over", "Checkmate! AI wins!")
                    self.running = False

            #stats screen will be shown if the user presses 'S'
            if self.show_stats_screen:
                #display the stats screen
                self.stats_screen()
            #otherwise, if the stats screen is not shown, we will draw the chess board and place the pieces on it
            else:
                #draw the chess board
                self.draw_board()
                #placing the pieces on the board
                self.placing_pieces()

            #updating the display
            pygame.display.update()
        
        #function to quit the game and stockfish engine
        self.engine.quit()
        #quitting pygame and exiting the game
        pygame.quit()
        #terminating the program
        sys.exit()

#starting the game
if __name__ == '__main__':
    load_images()
    game = ChessInPython()
    game.run()
