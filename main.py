import tkinter as tk
from tkinter import messagebox
from typing import Literal

def create_widgets():
    global  wins_entry, x_wins, o_wins, label_x, label_o
    label_title = tk.Label()
    label_title.config(text='Игра крестики-нолики!', font=('Arial', 16))
    label_title.grid(row=0, column=0, columnspan=4, pady=10)
    label_question = tk.Label()
    label_question.config(text='До скольки побед?', font=('Arial', 12))
    label_question.grid(row=1, column=3, padx=10)
    wins_entry = tk.Entry()
    wins_entry.config(width=5, font=('Arial', 12))
    wins_entry.grid(row=2, column=3, padx=10)
    wins_entry.insert(0, '3')
    label_x = tk.Label()
    label_o = tk.Label()
    label_x.config(text='Побед X: ' + str(x_wins), font=('Arial', 12))
    label_x.grid(row=4, column=0, columnspan=3, pady=(10, 0))
    label_o.config(text='Побед O: ' + str(o_wins), font=('Arial', 12))
    label_o.grid(row=5, column=0, columnspan=3)
    reset_btn = tk.Button(text='Начать заново', font=('Arial', 12), command=on_click_reset)
    reset_btn.grid(row=3, column=3, padx=10)

    window.grid_columnconfigure(3, minsize=220)

def get_valid_max_wins():
    try:
        wins = int(wins_entry.get())
        if wins < 1:
            raise ValueError
        return wins
    except ValueError:
        messagebox.showerror('Ошибка в поле ввода', 'Неверно указано число в поле ввода количества побед. \nУстановлено значение по умолчанию: 3.')
        wins_entry.config(state='normal')
        wins_entry.delete(0, tk.END)
        wins_entry.insert(0, '3')
        wins_entry.config(state='disabled')
        return 3

def on_click_reset():
    global current_player, x_wins, o_wins, label_x, label_o
    clean_board()
    current_player = 'X'
    buttons_activate('normal')
    wins_entry.config(state='normal')
    x_wins = 0
    o_wins = 0
    label_x.config(text='Побед X: ' + str(x_wins))
    label_o.config(text='Побед O: ' + str(o_wins))


def on_click(row, col):
    global current_player, x_wins, o_wins
    if buttons[row][col]['text'] == '':
        buttons[row][col]['text'] = current_player
        if check_winner():
            if current_player == 'X':
                x_wins += 1
                label_x.config(text='Побед X: ' + str(x_wins))
                wins_entry.config(state='disabled')
                if x_wins == get_valid_max_wins():
                    messagebox.showinfo('Конец игры!', f'Окончательная победа у {current_player}')
                    buttons_activate('disabled')
                    return
            else:
                o_wins += 1
                label_o.config(text='Побед O: ' + str(o_wins))
                wins_entry.config(state='disabled')
                if o_wins == get_valid_max_wins():
                    messagebox.showinfo('Конец игры!', f'Окончательная победа у {current_player}')
                    buttons_activate('disabled')
                    return

            messagebox.showinfo('Победа!', f'Победил {current_player}')
            clean_board()
            current_player = 'X'
        else:
            if is_board_full():
                messagebox.showinfo('Конец!', f'Ничья!')
                clean_board()
                current_player = 'X'
            else:
                current_player = 'O' if current_player == 'X' else 'X'


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

def is_board_full():
    for i in range(3):
        for j in range(3):
            if buttons[i][j]['text'] == '':
                return False
    return True

def clean_board():
    for i in range(3):
        for j in range(3):
            buttons[i][j]['text'] = ''

def buttons_activate(action: Literal["normal", "disabled"]):
    if action not in ['normal', 'disabled']:
        raise ValueError("Недопустимое состояние кнопки. Используйте 'normal' или 'disabled'.")
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(state=action)






window = tk.Tk()
window.title('Крестики-нолики')
window.geometry('450x300')

current_player = 'X'
buttons = []
x_wins = 0
o_wins = 0

create_widgets()

for i in range(3):
    row = []
    for j in range(3):
        btn = tk.Button(window, text='', font=('Arial', 20),
                        width=4, height=1, bg='white',
                        command=lambda r=i, c=j: on_click(r,c))
        row.append(btn)
        if j == 0:
            btn.grid(row=i+1, column=j, padx=(20,0))
        else:
            btn.grid(row=i+1, column=j)
    buttons.append(row)

window.mainloop()
