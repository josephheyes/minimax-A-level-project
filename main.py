from math import inf
from random import randrange
from tkinter import *
from tkinter import messagebox

human = -1
computer = +1

board = [[0,0,0],
         [0,0,0],
         [0,0,0]]

score_dict = {-1: "X", 1: "O", 0: " "}

boarddisplay = Tk()
boarddisplay.geometry("300x300")
boarddisplay.title("Noughts and Crosses")
waitvar = IntVar()

def wins(board, player):
    """
    Checks if the player has won the game
    :param board: current board state
    :param player: human or computer
    :return: True if player wins, False otherwise
    """
    win_possibilities = [[board[0][0], board[0][1], board[0][2]],[board[1][0], board[1][1], board[1][2]],
                        [board[2][0], board[2][1], board[2][2]], [board[0][0], board[1][0], board[2][0]],
                        [board[0][1], board[1][1], board[2][1]], [board[0][2], board[1][2], board[2][2]],
                        [board[0][0], board[1][1], board[2][2]], [board[0][2], board[1][1], board[2][0]]]

    if [player, player, player] in win_possibilities:
        return True
    else:
        return False

def eval(board):
    """
    A heuristic evaluation of the board state, used during minimax recursion
    :param board: current state of board
    :return: +1 if computer will win, -1 if human will win, 0 if draw
    """
    if wins(board, computer):
        score = +1
    elif wins(board, human):
        score = -1
    else:
        score = 0

    return score

def isEmpty(x,y):
    """
    Checks if a cell is empty
    :param x: column
    :param y: row
    :return: True if empty, False if not
    """
    if board[y][x] == 0:
        return True
    else:
        return False

def emptyCells(board):
    """
    Checks current board state to find all empty cells
    :param board: current board state
    :return: a list of the coordinates of all empty cells
    """
    empty_cells = []

    for y in range(3):
        for x in range(3):
            if isEmpty(x,y):
                empty_cells.append([x,y])
    return empty_cells

def gameOver(board):
    """
    Checks if either the human or computer has won
    :param board: current board state
    :return: True if someone wins, False otherwise
    """
    if wins(board, computer) or wins(board, human):
        return True
    else:
        return False

def playMove(x, y, player):
    """
    Plays the move chosen by the player
    :param x: column
    :param y: row
    :param player: human or computer
    """
    if isEmpty(x,y):
        board[y][x] = player
    else:
        messagebox.showwarning("Invalid move","Please choose an empty cell.")
        # waits until player has played a valid move
        boarddisplay.wait_variable(waitvar)
    if player == human:
        # modifies waitvar allowing code to continue
        waitvar.set(1)

def minimax(board, depth, player):
    """
    AI function to choose the best move
    :param board: the current board state
    :param depth: the node index of the game tree (length of the empty_cells array)
    :param player: human or computer
    :return: a list in the format [best move x-coord, best move y-coord, best score]
    """

    if player == computer:
        best = [-1, -1, -inf]
    else:
        best = [-1, -1, inf]

    if depth == 0 or gameOver(board):
        score = eval(board)
        return [-1, -1, score]

    for cell in emptyCells(board):
        x = cell[0]
        y = cell[1]
        board[y][x] = player
        score = minimax(board, depth-1, -player)
        board[y][x] = 0
        score[0] = x
        score[1] = y

        if player == computer:
            if score[2] > best[2]:
                best = score
        else:
            if score[2] < best[2]:
                best = score

    return best

def updateBoard():
    """
    Creates a 3x3 grid of buttons to represent the board
    """

    cell1 = Button(boarddisplay, fg="#f5f6fa", bg="#40739e", height=6, width=13, command=lambda: playMove(0, 0, human), text=score_dict[board[0][0]])
    cell1.grid(column=1, row=1)
    cell2 = Button(boarddisplay, fg="#f5f6fa", bg="#40739e", height=6, width=13, command=lambda: playMove(1, 0, human), text=score_dict[board[0][1]])
    cell2.grid(column=2, row=1)
    cell3 = Button(boarddisplay, fg="#f5f6fa", bg="#40739e", height=6, width=13, command=lambda: playMove(2, 0, human), text=score_dict[board[0][2]])
    cell3.grid(column=3, row=1)
    cell4 = Button(boarddisplay, fg="#f5f6fa", bg="#40739e", height=6, width=13, command=lambda: playMove(0, 1, human), text=score_dict[board[1][0]])
    cell4.grid(column=1, row=2)
    cell5 = Button(boarddisplay, fg="#f5f6fa", bg="#40739e", height=6, width=13, command=lambda: playMove(1, 1, human), text=score_dict[board[1][1]])
    cell5.grid(column=2, row=2)
    cell6 = Button(boarddisplay, fg="#f5f6fa", bg="#40739e", height=6, width=13, command=lambda: playMove(2, 1, human), text=score_dict[board[1][2]])
    cell6.grid(column=3, row=2)
    cell7 = Button(boarddisplay, fg="#f5f6fa", bg="#40739e", height=6, width=13, command=lambda: playMove(0, 2, human), text=score_dict[board[2][0]])
    cell7.grid(column=1, row=3)
    cell8 = Button(boarddisplay, fg="#f5f6fa", bg="#40739e", height=6, width=13, command=lambda: playMove(1, 2, human), text=score_dict[board[2][1]])
    cell8.grid(column=2, row=3)
    cell9 = Button(boarddisplay, fg="#f5f6fa", bg="#40739e", height=6, width=13, command=lambda: playMove(2, 2, human), text=score_dict[board[2][2]])
    cell9.grid(column=3, row=3)

def computerMove():
    """
    Calls minimax to find best move, unless depth = 9 (beginning of game), in which case chooses random cell
    """
    depth = len(emptyCells(board))

    if depth == 0 or gameOver(board):
        return

    if depth == 9:
        final_x = randrange(0, 2)
        final_y = randrange(0, 2)

    else:
        move = minimax(board, depth, computer)
        final_x = move[0]
        final_y = move[1]
    playMove(final_x, final_y, computer)

    updateBoard()

def playAgain():
    """
    Displays a window giving the player the choice to play again
    """
    option_window = Toplevel(bg="#40739e")
    option_window.geometry("180x100")
    option_window.title("Noughts and Crosses")

    question = Label(option_window, text="Play again?", font=("Helvetica", 18), fg="#f5f6fa", bg="#40739e")
    question.pack()

    yes_choice = Button(option_window, command=mainloop, text="Yes", fg="#f5f6fa", bg="#44bd32")
    no_choice = Button(option_window, command=boarddisplay.destroy, text="No", fg="#f5f6fa", bg="#e84118")
    no_choice.pack(side=BOTTOM)
    yes_choice.pack(side=BOTTOM)

    option_window.mainloop()

def mainloop():
    """
    Main game loop
    """

    # clears board for new game
    for y in range(3):
        for x in range(3):
            board[x][y] = 0


    # loops until someone wins or there is a draw, the break is needed in order to escape the wait_variable
    while len(emptyCells(board)) > 0 and not gameOver(board):
        computerMove()
        boarddisplay.update()
        if len(emptyCells(board)) == 0 or gameOver(board):
            break
        boarddisplay.wait_variable(waitvar)
        boarddisplay.update()

    # checking result at end of game
    if wins(board, computer):
        messagebox.showinfo("Game Over", "You lost to the computer.")
        result = "AI win"
    elif wins(board, human):
        messagebox.showinfo("Game Over", "You won!")
        result = "Player win"
    else:
        messagebox.showinfo("Game Over", "It was a draw!")
        result = "Draw"

    playAgain()

    # this call prevents the window from freezing at the end
    boarddisplay.mainloop()

if __name__ == "__main__":
    mainloop()