import tkinter as tk
from tkinter import messagebox

class Game:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("XO Game")
        self.window.configure(bg="#333333")  # Set background color to dark gray
        self.buttons = [[None, None, None] for _ in range(3)]
        self.current_player = 'X'

        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.window, text='', font=('normal', 20), width=5, height=2,
                                               command=lambda row=i, col=j: self.make_move(row, col),
                                               bg="#555555",  # Set button background color to a darker shade
                                               fg="white")    # Set button text color to white
                self.buttons[i][j].grid(row=i, column=j)


    def make_move(self, row, col):
        if self.buttons[row][col]['text'] == '' and not self.is_game_over():
            self.buttons[row][col]['text'] = self.current_player

            if self.check_winner():
                self.show_winner()
            elif self.is_board_full():
                self.show_default_result()
            else:
                self.switch_player()
                self.computer_move()

    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def computer_move(self):
        if not self.is_game_over():
            score, move = self.minimax()
            row, col = move
            self.buttons[row][col]['text'] = self.current_player

            if self.check_winner():
                self.show_winner()
            elif self.is_board_full():
                self.show_default_result()
            else:
                self.switch_player()

    def minimax(self):
        best_score = float('-inf')
        best_move = None

        for i in range(3):
            for j in range(3):
                if self.buttons[i][j]['text'] == '':
                    self.buttons[i][j]['text'] = 'O'
                    score = self.minimax_helper(0, False)
                    self.buttons[i][j]['text'] = ''

                    if score > best_score:
                        best_score = score
                        best_move = (i, j)

        return best_score, best_move

    def minimax_helper(self, depth, is_maximizing):
        scores = {'X': -1, 'O': 1, 'Draw': 0}

        result = self.check_winner()
        if result is not None:
            return scores[result]

        if is_maximizing:
            best_score = float('-inf')
            for i in range(3):
                for j in range(3):
                    if self.buttons[i][j]['text'] == '':
                        self.buttons[i][j]['text'] = 'O'
                        score = self.minimax_helper(depth + 1, False)
                        self.buttons[i][j]['text'] = ''
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if self.buttons[i][j]['text'] == '':
                        self.buttons[i][j]['text'] = 'X'
                        score = self.minimax_helper(depth + 1, True)
                        self.buttons[i][j]['text'] = ''
                        best_score = min(score, best_score)
            return best_score

    def check_winner(self):
        for i in range(3):
            if self.buttons[i][0]['text'] == self.buttons[i][1]['text'] == self.buttons[i][2]['text'] != '':
                return self.buttons[i][0]['text']
            if self.buttons[0][i]['text'] == self.buttons[1][i]['text'] == self.buttons[2][i]['text'] != '':
                return self.buttons[0][i]['text']
        if self.buttons[0][0]['text'] == self.buttons[1][1]['text'] == self.buttons[2][2]['text'] != '':
            return self.buttons[0][0]['text']
        if self.buttons[0][2]['text'] == self.buttons[1][1]['text'] == self.buttons[2][0]['text'] != '':
            return self.buttons[0][2]['text']
        if all(self.buttons[i][j]['text'] != '' for i in range(3) for j in range(3)):
            return 'Draw'
        return None

    def is_board_full(self):
        return all(self.buttons[i][j]['text'] != '' for i in range(3) for j in range(3))

    def is_game_over(self):
        return self.check_winner() is not None or self.is_board_full()

    def show_winner(self):
        winner = self.check_winner()
        messagebox.showinfo("Game Over", f"{winner} made it!")
        self.close_game()

    def show_default_result(self):
        messagebox.showinfo("Game Over", "It's a draw!")
        self.close_game()

    def close_game(self):
        self.window.destroy()
        self._init_()
        self.run()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = Game()
    game.run()