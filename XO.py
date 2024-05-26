import tkinter as tk
from tkinter import messagebox

board = {1: ' ', 2: ' ', 3: ' ',
         4: ' ', 5: ' ', 6: ' ',
         7: ' ', 8: ' ', 9: ' '}

player = 'O'
bot = 'X'

def printBoard(board):
    print(board[1] + '|' + board[2] + '|' + board[3])
    print('-----')
    print(board[4] + '|' + board[5] + '|' + board[6])
    print('-----')
    print(board[7] + '|' + board[8] + '|' + board[9])
    print("\n")

def spaceIsFree(position):
    return board[position] == ' '

def checkForWin():
    if (board[1] == board[2] and board[1] == board[3] and board[1] != ' '):
        return True
    elif (board[4] == board[5] and board[4] == board[6] and board[4] != ' '):
        return True
    elif (board[7] == board[8] and board[7] == board[9] and board[7] != ' '):
        return True
    elif (board[1] == board[4] and board[1] == board[7] and board[1] != ' '):
        return True
    elif (board[2] == board[5] and board[2] == board[8] and board[2] != ' '):
        return True
    elif (board[3] == board[6] and board[3] == board[9] and board[3] != ' '):
        return True
    elif (board[1] == board[5] and board[1] == board[9] and board[1] != ' '):
        return True
    elif (board[7] == board[5] and board[7] == board[3] and board[7] != ' '):
        return True
    else:
        return False

def checkDraw():
    return all(board[key] != ' ' for key in board)

def insertLetter(letter, position):
    if spaceIsFree(position):
        board[position] = letter
        updateGUI()
        if checkDraw():
            messagebox.showinfo("Game Over", "It's a draw!")
            exit()
        if checkForWin():
            if letter == 'X':
                messagebox.showinfo("Game Over", "Bot wins!")
            else:
                messagebox.showinfo("Game Over", "Player wins!")
            exit()

def playerMove(position):
    insertLetter(player, position)
    compMove()

def compMove():
    bestScore = -100
    bestMove = 0
    for key in board.keys():
        if board[key] == ' ':
            board[key] = bot
            score = minimax(board, 0, False)
            board[key] = ' '
            if score > bestScore:
                bestScore = score
                bestMove = key

    insertLetter(bot, bestMove)

def minimax(board, depth, isMaximizing):
    if checkForWin():
        return 1
    elif checkDraw():
        return 0

    if isMaximizing:
        bestScore = -100
        for key in board.keys():
            if board[key] == ' ':
                board[key] = bot
                score = minimax(board, depth + 1, False)
                board[key] = ' '
                bestScore = max(score, bestScore)
        return bestScore
    else:
        bestScore = 100
        for key in board.keys():
            if board[key] == ' ':
                board[key] = player
                score = minimax(board, depth + 1, True)
                board[key] = ' '
                bestScore = min(score, bestScore)
        return bestScore

def updateGUI():
    for key, button in buttons.items():
        button.config(text=board[key])

def buttonClick(position):
    if spaceIsFree(position):
        playerMove(position)
    else:
        messagebox.showwarning("Invalid Move", "Can't insert there!")

root = tk.Tk()
root.title("Tic-Tac-Toe")

buttons = {}

for i in range(1, 10):
    row, col = divmod(i - 1, 3)
    buttons[i] = tk.Button(root, text=' ', font=('normal', 24), width=6, height=3,
                           command=lambda i=i: buttonClick(i))
    buttons[i].grid(row=row, column=col)

root.mainloop()
