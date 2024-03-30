
import random
import re  
# create board to represent the minesweeper game 

class Board:
    def __init__(self, dim_size, num_bombs):
        self.dim_size = dim_size
        self.num_bombs = num_bombs
       

        # create board 
        # helper function
        self.board = self.make_new_board() # plant the bombs
        self.assign_values_to_board() 

        
        
        
        self.dug=set() # keep track of where we have dug
        # if we dig at 1 , 0 then self.dug = {(1,0)}}

    def make_new_board(self):
            board=[[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]

            bombs_planted = 0
            while bombs_planted < self.num_bombs:
                loc = random.randint(0, self.dim_size**2-1)
                row = loc// self.dim_size
                col = loc % self.dim_size

                if board[row][col] == '*':
                    # means we've actually planted a bomb there already. 
                    continue 

                # plant bomb
                board[row][col] = '*'
                bombs_planted += 1

            return board
        
    def assign_values_to_board(self):
            for r in range(self.dim_size):
                for c in range(self.dim_size):
                    if self.board[r][c] == '*':
                        continue
                    self.board[r][c] = self.get_num_neighboring_bombs(r, c)

    def get_num_neighboring_bombs(self, row, col):
        num_neighboring_bombs = 0
        # sets limits so we do not check out of bounds
        for r in range(max(0,row-1), min(self.dim_size-1, row+1)+1):
             for c in range(max(0,col-1), min(self.dim_size-1, col+1)+1):
                if r == row and c == col:
                    continue
                if self.board[r][c] == '*':
                    num_neighboring_bombs += 1
        return num_neighboring_bombs
    
    def dig(self, row, col):
        #   dig at that location
        #   return the value or bomb if hit bomb    
         
        self.dug.add((row,col))

        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True
        
        for r in range(max(0,row-1), min(self.dim_size-1, row+1)+1):
             for c in range(max(0,col-1), min(self.dim_size-1, col+1)+1):
                if (r, c) in self.dug:
                    # dont dig where you've already dug 
                    continue
                self.dig(r, c)
        # recursively dig neighbors if this spot was not a bomb
        return True 
    
    def __str__(self):
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row,col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '

        # put this in a string
                    
        string_rep = ''
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key=len)
                    )
                )
        # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '  '
        cells = []

        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row+= " |".join(cells)
        indices_row += " |\n"

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = "%-" + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'
        
        str_len = int(len(string_rep)/self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep+ '-'*str_len
        return string_rep


# play game
def play(dim_size = 10, num_bombs=10):
    # step 1: create the board and plant bombs
    board = Board(dim_size, num_bombs)
    # step 2: show the user the board and ask where they want to dig 

    # step 3: if location is a bomb, show game over message 
    # step 3b: if location is not a bomb, dig recursively until each square is next to a bomb
    #step 4: repeat 2 and 3 until no more spots to dig. 
    # step 5: show user the board and congratulate them on winning
    
    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print(board)
        user_input = re.split(',(\\s)*' , input("Where would you like to dig? Input as row, col: "))
        row, col = int(user_input[0]), int(user_input[-1])

        if row < 0 or row >= board.dim_size or col < 0 or col >= board.dim_size:
            print("Invalid location. Try again.")
            continue

        # if it is valid, we dig 
        safe = board.dig(row, col)

        if not safe:
            # dug a bomb.....sorry. Game is over
            break

    if safe:
        print("Congratulations! You found a safe spot.")
        play_again = input("Would you like to play again? Y/N ").lower()
        return play_again
    else:
        print(f"You hit a bomb at {row}, {col}. Game over.")
        board.dug=[(r,c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)
        play_again = input("Would you like to play again? Y/N ").lower()
        return play_again

    

if __name__ == '__main__':
    play()
    play_again = play()
    if play_again == "y":
        play()