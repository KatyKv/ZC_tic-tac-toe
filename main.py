import tkinter as tk
from tkinter import messagebox

window = tk.Tk()
window.title('Крестики-нолики')
window.geometry('400x400')

current_player = 'X'
buttons = []

def on_click(row, col):
    global current_player
    if buttons[row][col]['text'] == '':
        buttons[row][col]['text'] = current_player
        if not check_winner():
            current_player = 'O' if current_player == 'X' else 'X'
        else:
            messagebox.showinfo('Победа!', f'Победил {current_player}')

def check_winner():
    for i in range(3):
        if (buttons[i][0]['text'] == buttons[i][1]['text'] == buttons[i][2]['text'] != '' or
            buttons[0][i]['text'] == buttons[1][i]['text'] == buttons[2][i]['text'] != ''
            ):
            return True
    if (buttons[0][0]['text'] == buttons[1][1]['text'] == buttons[2][2]['text'] != '' or
        buttons[0][2]['text'] == buttons[1][1]['text'] == buttons[2][0]['text'] != ''
        ):
        return True
    return False


for i in range(3):
    row = []
    for j in range(3):
        btn = tk.Button(window, text='', font=('Arial', 20),
                        width=4, height=1,
                        command=lambda r=i, c=j: on_click(r,c))
        row.append(btn)
        btn.grid(row=i, column=j)
    buttons.append(row)

window.mainloop()
