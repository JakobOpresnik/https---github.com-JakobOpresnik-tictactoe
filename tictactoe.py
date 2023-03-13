import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk


# player X starts (set to True)
player = True
game_over = False


def checkFreeRows(matrix, player):
    count = 0
    if player == True:
        sign = "X"
    else:
        sign = "O"
    
    if (matrix[0][0] == 0 or matrix[0][0] == sign) and (matrix[0][1] == 0 or matrix[0][1] == sign) and (matrix[0][2] == 0 or matrix[0][2] == sign):
        count += 1
    if (matrix[1][0] == 0 or matrix[1][0] == sign) and (matrix[1][1] == 0 or matrix[1][1] == sign) and (matrix[1][2] == 0 or matrix[1][2] == sign):
        count += 1
    if (matrix[2][0] == 0 or matrix[2][0] == sign) and (matrix[2][1] == 0 or matrix[2][1] == sign) and (matrix[2][2] == 0 or matrix[2][2] == sign):
        count += 1
    
    return count


def checkFreeColumns(matrix, player):
    count = 0
    if player == True:
        sign = "X"
    else:
        sign = "O"

    if (matrix[0][0] == 0 or matrix[0][0] == sign) and (matrix[1][0] == 0 or matrix[1][0] == sign) and (matrix[2][0] == 0 or matrix[2][0] == sign):
        count += 1
    if (matrix[0][1] == 0 or matrix[0][1] == sign) and (matrix[1][1] == 0 or matrix[1][1] == sign) and (matrix[2][1] == 0 or matrix[2][1] == sign):
        count += 1
    if (matrix[0][2] == 0 or matrix[0][2] == sign) and (matrix[1][2] == 0 or matrix[1][2] == sign) and (matrix[2][2] == 0 or matrix[2][2] == sign):
        count += 1
    
    return count


def checkFreeDiagonals(matrix, player):
    count = 0
    if player == True:
        sign = "X"
    else:
        sign = "O"
    
    if (matrix[0][0] == 0 or matrix[0][0] == sign) and (matrix[1][1] == 0 or matrix[1][1] == sign) and (matrix[2][2] == 0 or matrix[2][2] == sign):
        count += 1
    if (matrix[0][2] == 0 or matrix[0][2] == sign) and (matrix[1][1] == 0 or matrix[1][1] == sign) and (matrix[2][0] == 0 or matrix[2][0] == sign):
        count += 1
    
    return count
    
    
# heuristic function returns score/heuristic assessment
# of the current given state
def heuristic(current_state):

    # heuristic score = (free rows + free columns + free diagonals for X)
    #                   - (free rows + free columns + free diagonals for O)

    free_rows_X = checkFreeRows(current_state, True)
    free_columns_X= checkFreeColumns(current_state, True)
    free_diagonals_X = checkFreeDiagonals(current_state, True)

    free_rows_O = checkFreeRows(current_state, False)
    free_columns_O = checkFreeColumns(current_state, False)
    free_diagonals_O = checkFreeDiagonals(current_state, False)

    score_X = free_rows_X + free_columns_X + free_diagonals_X
    score_O = free_rows_O + free_columns_O + free_diagonals_O

    h = score_X - score_O
    return h, current_state


# returns all next possible based on current state of the board
def nextMove(current_state, player):
    # save empty and occupied cell indices
    empty_cells = []
    occupied_cells = []
    for i in range(3):
        for j in range(3):
            if current_state[i][j] == 0:
                empty_cells.append([i, j])
            else:
                occupied_cells.append([i, j])

    # create all possible state permutations
    possibleStates = []
    for i in range(len(empty_cells)):
        new_state = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        empty_row = empty_cells[i][0]
        empty_column = empty_cells[i][1]
        for j in range(len(occupied_cells)):
            full_row = occupied_cells[j][0]
            full_column = occupied_cells[j][1]
            if current_state[full_row][full_column] != 0:
                new_state[full_row][full_column] = current_state[full_row][full_column]
        if player == True:
            new_state[empty_row][empty_column] = "X"
        else:
            new_state[empty_row][empty_column] = "O"
        possibleStates.append(new_state)
    
    return possibleStates



def isEndState(state):
    # check rows
    if state[0][0] == state[0][1] == state[0][2] != 0:
        return True
    if state[1][0] == state[1][1] == state[1][2] != 0:
        return True
    if state[2][0] == state[2][1] == state[2][2] != 0:
        return True
    
    # check columns
    if state[0][0] == state[1][0] == state[2][0] != 0:
        return True
    if state[0][1] == state[1][1] == state[2][1] != 0:
        return True
    if state[0][2] == state[1][2] == state[2][2] != 0:
        return True
    
    # check diagonals
    if state[0][0] == state[1][1] == state[2][2] != 0:
        return True
    if state[2][0] == state[1][1] == state[0][2] != 0:
        return True

    # check for tie
    empty_cells = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                empty_cells += 1
    
    if empty_cells == 0:
        return True
    
    return False


    


def minimax(current_state, depth, player, alpha, beta):
    # if lowest depth is reached or if a reached state is an end state (tie or win/loss)
    if depth == 0 or isEndState(current_state):
        return heuristic(current_state)

    if player == True:
        best_value = -1000000
    elif player == False:
        best_value = 1000000
    
    possibleStates = nextMove(current_state, player)
    best_move = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for i in range(len(possibleStates)):
        # recursive minimax call for current possible move
        value, move = minimax(possibleStates[i], depth-1, not player, alpha, beta)
        for j in range(3):
            for k in range(3):
                if current_state[j][k] != move[j][k] and current_state[j][k] != player:
                    move[j][k] = 0
        
        # check for best heuristic value
        if player == True:
            if value > best_value:
                best_value = value
                best_move = move
                if best_value > alpha:
                    alpha = best_value
        elif player == False:
            if value < best_value:
                best_value = value
                best_move = move
                if best_value < beta:
                    beta = best_value
        
        # alpha-beta pruning
        if alpha >= beta:
            return best_value, best_move

    return best_value, best_move

        

# when a button is clicked
def click(row, column):
    global player

    # player X starts
    if player == True and states[row][column] == 0 and game_over == False:
        cells[row][column].configure(text="X", fg="blue")
        states[row][column] = "X"
        player = not player

        # AI (player X) responds
        if player == False and game_over == False:
            _, move = minimax(states, depth, player, -1000000, 1000000)
            for i in range(3):
                for j in range(3):
                    if move[i][j] != states[i][j]:
                        cells[i][j].configure(text="O", fg="red")
                        states[i][j] = "O"
                        player = not player
    
    # check if game is over
    isGameOver()



def isGameOver():
    global game_over

    # check all rows
    for i in range(3):
        cells = [states[i][0], states[i][1], states[i][2]]
        game_over = checkCells(cells)
    
    # check all columns
    for i in range(3):
        cells = [states[0][i], states[1][i], states[2][i]]
        game_over = checkCells(cells)
    
    # check both diagonals
    cells = [states[0][0], states[1][1], states[2][2]]
    game_over = checkCells(cells)

    cells = [states[0][2], states[1][1], states[2][0]]
    game_over = checkCells(cells)

    # determine winner
    if game_over:
        winner = ""
        if player == True:
            winner = "O"
        else:
            winner = "X"
        messagebox.showinfo("game over", winner + " won")
    # check for tie
    else:
        empty_cells = 0
        for i in range(3):
            for j in range(3):
                if states[i][j] == 0:
                    empty_cells += 1
        if empty_cells == 0:
            messagebox.showinfo("game over", "tie")



def checkCells(cells):
    global game_over
    if (len(cells) == 3):
        if cells[0] == cells[1] == cells[2] != 0:
            game_over = True
    return game_over




# create GUI window
root = Tk()
root.title("tic tac toe")
root.geometry("385x420")
root.resizable(0,0)     # disable resizing
root.configure(bg="white")


# matrix of cells
cells = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]]

# matrix of cell states
states = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]]


# create grid of buttons (playing board)
for i in range(3):
    for j in range(3):
        cells[i][j] = Button(root, bg="white", height=2, width=5, font=("bold", 20), padx=10, pady=10, command=lambda row = i, column = j : click(row, column))
        cells[i][j].grid(padx=10, pady=10, row = i, column = j)


# default depth
depth = 1

# create a frame for the dropdown and the confirm button
frame = tk.Frame(root)
frame.grid(row=3, column=0, columnspan=3)
frame.configure(bg="white")

# define a list of predefined values (depths) for the dropdown menu
depths = [1, 2, 3, 4, 5]

# create a StringVar to store selected depth
selected_depth = tk.StringVar()

# create a Combobox widget with predefined values
dropdown = ttk.Combobox(frame, textvariable=selected_depth, values=depths)

# initial dropdown value
dropdown.current(0)
dropdown.configure(width=2)

# called when changing value in dropdown menu
def onSelect(event):
    global depth
    depth = int(selected_depth.get())
    print("dropdown selected depth = ", depth)

# bind function to dropdown
dropdown.bind("<<ComboboxSelected>>", onSelect)

# called when confirming selection of new depth
def selectDepth():
    global depth
    depth = int(selected_depth.get())
    print("confirmed selected depth = ", depth)

# create dropdown button
depth_btn = ttk.Button(frame, text="Select depth", command=selectDepth)


# resets game state and button values
def resetGame():
    global game_over, player
    game_over = False
    player = True
    for i in range(3):
        for j in range(3):
            if states[i][j] != 0:
                cells[i][j].configure(text="")
                states[i][j] = 0


# create reset button
reset_btn = Button(frame, text="Reset game", command=resetGame)

# add the button and the dropdown to the frame using the grid geometry manager
depth_btn.grid(row=0, column=1, padx=5, pady=5)
dropdown.grid(row=0, column=2, padx=5, pady=5)
reset_btn.grid(row=0, column=0, padx=5, pady=5)
reset_btn.configure(bg="red", fg="white")

root.mainloop()