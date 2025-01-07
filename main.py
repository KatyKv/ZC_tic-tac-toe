import tkinter as tk
from tkinter import messagebox
from typing import Literal
import random

def create_widgets():
    global  wins_entry, x_wins, o_wins, label_x, label_o, selected_option, start_btn, radiobutton1, radiobutton2
    label_title = tk.Label()
    label_title.config(text='Игра крестики-нолики!', font=('Arial', 18))
    label_title.grid(row=0, column=0, columnspan=4, pady=10)
    start_btn = tk.Button(text='Старт игры', font=('Arial', 12), bg='chartreuse', command=on_click_start)
    start_btn.grid(row=1, column=3, padx=10, pady=(0, 20))
    label_question = tk.Label()
    label_question.config(text='До скольки побед?', font=('Arial', 12))
    label_question.grid(row=2, column=3, padx=10, pady=(20, 0))
    wins_entry = tk.Entry()
    wins_entry.config(width=5, font=('Arial', 12))
    wins_entry.grid(row=3, column=3, padx=10, pady=(0, 25))
    wins_entry.insert(0, '3')
    label_x = tk.Label()
    label_o = tk.Label()
    label_x.config(text='Побед X: ' + str(x_wins), font=('Arial', 12))
    label_x.grid(row=4, column=0, columnspan=3, pady=(10, 0))
    label_o.config(text='Побед O: ' + str(o_wins), font=('Arial', 12))
    label_o.grid(row=5, column=0, columnspan=3)
    label_choose = tk.Label()
    label_choose.config(text='За кого играть?', font=('Arial', 12))
    label_choose.grid(row=4, column=3, padx=10)
    radiobutton1 = tk.Radiobutton(text="Играть за X", variable=selected_option, value="Игрок X", font=('Arial', 12))
    radiobutton2 = tk.Radiobutton(text="Играть за O", variable=selected_option, value="Игрок O", font=('Arial', 12))
    radiobutton1.grid(row=5, column=3, padx=10)
    radiobutton2.grid(row=6, column=3, padx=10)
    window.grid_columnconfigure(3, minsize=220)
    reset_btn = tk.Button(text='Начать заново', font=('Arial', 12), bg='khaki', command=on_click_reset)
    reset_btn.grid(row=6, column=0, columnspan=3, padx=10, pady=(20,0))

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

def on_click_start():
    global current_player, x_wins, o_wins
    clean_board()
    current_player = 'X'
    buttons_activate('normal')
    x_wins = 0
    o_wins = 0
    label_x.config(text='Побед игрока X: ' + str(x_wins))
    label_o.config(text='Побед игрока O: ' + str(o_wins))
    get_valid_max_wins()
    wins_entry.config(state='disabled')
    radiobutton1.config(state='disabled')
    radiobutton2.config(state='disabled')
    start_btn.config(state='disabled')
    if current_player == 'X' and selected_option.get() == 'Игрок O':
        computer_move()

def on_click_reset():
    clean_board()
    buttons_activate('disabled')
    wins_entry.config(state='normal')
    x_wins = 0
    o_wins = 0
    label_x.config(text='Побед игрока X: ' + str(x_wins))
    label_o.config(text='Побед игрока O: ' + str(o_wins))
    radiobutton1.config(state='normal')
    radiobutton2.config(state='normal')
    start_btn.config(state='normal')


def on_click(row, col):
    global current_player, x_wins, o_wins
    if buttons[row][col]['text'] == '':
        buttons[row][col]['text'] = current_player
        if check_winner():
            if current_player == 'X':
                x_wins += 1
                label_x.config(text='Побед игрока X: ' + str(x_wins))
                if x_wins == int(wins_entry.get()):
                    messagebox.showinfo('Конец игры!', f'Окончательная победа у {current_player}')
                    buttons_activate('disabled')
                    return
            else:
                o_wins += 1
                label_o.config(text='Побед игрока O: ' + str(o_wins))
                if o_wins == int(wins_entry.get()):
                    messagebox.showinfo('Конец игры!', f'Окончательная победа у {current_player}')
                    buttons_activate('disabled')
                    return

            messagebox.showinfo('Победа!', f'Победил {current_player}')
            clean_board()
            current_player = 'X'
            if current_player == 'X' and selected_option.get() == 'Игрок O':
                computer_move()
        else:
            if is_board_full():
                messagebox.showinfo('Конец!', f'Ничья!')
                clean_board()
                current_player = 'X'
            else:
                current_player = 'O' if current_player == 'X' else 'X'
                if current_player == 'O' and selected_option.get() == 'Игрок X':
                    computer_move()
                elif current_player == 'X' and selected_option.get() == 'Игрок O':
                    computer_move()

def computer_move():
    global current_player
    empty_cells = [(i, j) for i in range(3) for j in range(3) if buttons[i][j]['text'] == '']
    if empty_cells:
        row, col = random.choice(empty_cells)
        on_click(row, col)

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
window.geometry('450x350')

current_player = 'X'
buttons = []
x_wins = 0
o_wins = 0
selected_option = tk.StringVar(value="Игрок X")

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
buttons_activate("disabled")

window.mainloop()
