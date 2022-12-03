# This was written by 3y3l3ss0ur0b0r0s on 03/18/2022.
    # GitHub: https://github.com/3y3l3ss0ur0b0r0s
# This was written using Kylie Ying's tutorial (https://www.youtube.com/watch?v=8ext9G7xspg&t=5236s).

import random
import re

class Board:
    def __init__(self,dim_size,num_mines):
        self.dim_size=dim_size
        self.num_mines=num_mines

        # Creating the board
        # Helper function
        self.board=self.make_new_board() # For planting mines
        self.assign_values_to_board()

        # Initializing a set to keep track of uncovered locations
            # Saving (row,col) tuples into this set

        # If we dig at (0,0), then self.dug={(0,0)}
        self.dug=set()

    def make_new_board(self):
        # Constructing a new board based on dim_size and num_mines
            # Constructing list of lists here (for a 2D board, a list of lists is the best representation)

        # Generating a new square board (list of lists containing None)
        board=[[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]

        # Planting the mines
        mines_planted=0
        while mines_planted < self.num_mines:
            loc=random.randint(0,self.dim_size**2-1)    # Returns a random integer between bounds of the spaces on the board (dim_size**2-1)
            row=loc//self.dim_size  # Finds the row to look in (how many dim_size can go into loc)
            col=loc%self.dim_size   # The remainder shows what index in the column (index in row) to look in
                # Consider a 3 by 3 board
                    # Each space would have an index/ID between (inclusively) 0 and 8
                    # If an index/ID of 7 is generated, you would know that the space is in the second row since 9//3=2
                        # Since 9%3=1, that is the index within the row (column) that the space would be
            # If there's already a mine ("*"), we are not planting another mine there
            if board[row][col]=='*':
                    continue

            # Planting mine and incrementing counter
            board[row][col]='*'
            mines_planted+=1

        return board

    def assign_values_to_board(self):
        # After mines are planted, we are assigning a number from 0-8 to each empty space; that will represent how many neighboring mines there already
            # Computing these beforehand helps save time by preventing us from needing to check around the board later on
        for r in range(self.dim_size):  # Rows
            for c in range(self.dim_size):  # Columns
                # If there is a mine in the space already, calculations aren't needed
                if self.board[r][c]=='*':
                    continue
                self.board[r][c]=self.get_num_neighboring_mines(r,c)

    def get_num_neighboring_mines(self,row,col):
        # Iterating through each neighboring position and summing the number of mines
            # Be sure not to go out of bounds
        num_neighboring_mines=0
        for r in range(max(0,row-1),min(self.dim_size-1,row+1)+1): # max() and min() keep our rows and columns in bounds; for example, if row=0, max(0,row-1)=max(0,-1), and the larger number (0) will be returned
            for c in range(max(0,col-1),min(self.dim_size-1,col+1)+1):
                # If we're in the current row, you don't need to check for a mine
                if r==row and c==col:
                    continue
                if self.board[r][c]=='*':
                    num_neighboring_mines+=1

        return num_neighboring_mines

    def dig(self,row,col):
        # Digging at user-specified location
            # Returning True if successful; returning False if mine is # DEBUG:

        self.dug.add((row,col)) # Save that we already dug at this spot

        if self.board[row][col]=='*':
            return False
        elif self.board[row][col]>0:    # Did not hit a bomb; return True because we can still continue playing
            return True

        # self.board[row][col]==c
        # If we already dug here, do not do it (add to self.dug) again
        for r in range(max(0,row-1),min(self.dim_size-1,row+1)+1):
            for c in range(max(0,col-1),min(self.dim_size-1,col+1)+1):
                if (r,c) in self.dug:
                    continue
                self.dig(r,c)

        return True

    def __str__(self):
        # Output string

        # Creating an array representing what the user would specified
        visible_board=[[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row,col) in self.dug:   # If it's dug already, we show the value
                    visible_board[row][col]=str(self.board[row][col])
                else:   # If it's not dug, we don't show the value yet
                    visible_board[row][col]=' '

        string_rep=""
        # List of columns
        widths=[]
        for index in range(self.dim_size):
            columns=map(lambda x: x[index],visible_board)
            widths.append(len(max(columns,key=len)))

        # Printing the CSV strings
        indices=[i for i in range(self.dim_size)]
        indices_row='\n  | '
        cells=[]
        for index, col in enumerate(indices):
            format='%-' + str(widths[index])+"s"
            cells.append(format%(col))
        indices_row+='   '.join(cells)
        indices_row+=' \n'

        for i in range(len(visible_board)):
            row=visible_board[i]
            string_rep+=f'{i} | '
            cells=[]
            for index,col in enumerate(row):
                format = '%-' + str(widths[index])+"s"
                cells.append(format%(col))
            string_rep+=' | '.join(cells)
            string_rep+=' |\n'

        str_len=int(len(string_rep)/self.dim_size)
        string_rep="\n\t-------------------------\n\t\tDEMINER\n\t-------------------------\n"+indices_row+'-'*str_len+'\n'+string_rep+'-'*str_len

        return string_rep

# Function for playing the game
def play(dim_size=10,num_mines=10):
    # 1. Create the board and plant the mines
    board=Board(dim_size,num_mines)

    # 2: Show the user the board and ask where they want to dig
    # 3a: If location is a mine, show "GAME OVER" message
    # 3b: If location is not a mine, dig recursively until each square is at least next to a mine
    # 4: Repeat steps 2 and 3a/3b until there are no more places to dig (if there are no places left, the player has won)

    # While there are spaces that are not mines, we can continue to dig

    safe=True

    while len(board.dug)<board.dim_size**2-num_mines:
        print(board)
        # Splitting whatever's between the comma and however many (*) spaces ((\\s))
        user_input= re.split(',(\\s)*',input("\nWhere are we digging? Use row,col format: "))
        row,col=int(user_input[0]),int(user_input[-1])
        if row<0 or row>=board.dim_size or col<0 or col>=dim_size:
            print("\nChoose a place within bounds, please!")
            continue
        if (row,col) in board.dug:
            print("\nThis spot's already dug out. Try somewhere else!")
            continue

        # If the location is within bounds, dig
        safe=board.dig(row,col)
        # If not safe, game over
        if not safe:
            break

    if safe:
        print("\n\t==============================\n\t\tYOU WIN!!!\n\t==============================\n")
    else:
        print("\n\t==============================\n\t\tGAME OVER!!!\n\t==============================\n")
        # Revealing the board
        board.dug=[(r,c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)

# __name__=='__main__' means that this will only run in this file, even if imported into another file
if __name__=='__main__':
    play()
