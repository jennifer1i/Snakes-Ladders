import random
import tkinter as tk
from tkinter import messagebox


class Player:
    def __init__(self, name, color):
        self.name = name
        self.position = 1
        self.color = color
        self.circle = None


    def move(self, steps):
        self.position += steps
        if self.position > 100:
            self.position = 100

    def __str__(self):
        return f"{self.name} is at position {self.position}"


class Board:
    def __init__(self):
        self.snakes = {
            16: 6,
            46: 25,
            49: 11,
            62: 19,
            64: 60,
            74: 53,
            89: 68,
            92: 88,
            95: 75,
            99: 80
        }
        self.ladders = {
            2: 38,
            7: 14,
            8: 31,
            15: 26,
            28: 84,
            36: 44,
            51: 67,
            71: 91,
            78: 98,
            87: 94
        }

    def check_snake_or_ladder(self, position):
        if position in self.snakes:
            return (self.snakes[position], "snake")
        elif position in self.ladders:
            return (self.ladders[position], "ladder")
        return (position, None)


class Game:
    def __init__(self, players, canvas):
        self.board = Board()
        self.players = [Player(name, color) for name, color in players]
        self.canvas = canvas
        self.winner = None
        self.current_player_index = 0

    def roll_dice(self):
        return random.randint(1, 6)

    def play_turn(self):
        player = self.players[self.current_player_index]
        dice_roll = self.roll_dice()
        messagebox.showinfo("Dice Roll", f"{player.name} rolls a {dice_roll}!")
        player.move(dice_roll)

        new_position, entity = self.board.check_snake_or_ladder(player.position)
        if entity == "snake":
            messagebox.showinfo("Snake!", f"Oh no! {player.name} slides down to {new_position}!")
        elif entity == "ladder":
            messagebox.showinfo("Ladder!", f"Yay! {player.name} climbs to {new_position}!")
        player.position = new_position

        self.update_player_position(player)

        if player.position == 100:
            self.winner = player
            messagebox.showinfo("Winner!", f"🎉 Congratulations, {player.name} wins the game! 🎉")
            return True

        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        return False

    def update_player_position(self, player):
        row, col = self.get_position_on_board(player.position)
        if player.circle:
            self.canvas.coords(player.circle, col * 60 + 30, row * 60 + 30)
        else:
            player.circle = self.canvas.create_oval(
                col * 60 + 10, row * 60 + 10,
                col * 60 + 50, row * 60 + 50,
                fill=player.color
            )

    def get_position_on_board(self, position):
        row = (100 - position) // 10
        col = (position - 1) % 10
        if row % 2 == 1:
            col = 9 - col
        return row, col


def start_game():
    player_names = entry.get().split(",")
    if len(player_names) < 2:
        messagebox.showerror("Error", "Please enter at least two player names, separated by commas.")
        return

    colors = ['red', 'blue', 'green', 'yellow']
    players = [(name.strip(), colors[i % len(colors)]) for i, name in enumerate(player_names)]

    root.destroy()
    game_window = tk.Tk()
    game_window.title("Snakes and Ladders")

    canvas = tk.Canvas(game_window, width=600, height=600, bg='light pink')
    canvas.pack()

    game = Game(players, canvas)

    def draw_board():
        for row in range(10):
            for col in range(10):
                x1, y1 = col * 60, row * 60
                x2, y2 = x1 + 60, y1 + 60
                canvas.create_rectangle(x1, y1, x2, y2, outline="black")
                canvas.create_text(x1 + 30, y1 + 30, text=str(100 - row * 10 - col))

        for start, end in game.board.snakes.items():
            start_row, start_col = game.get_position_on_board(start)
            end_row, end_col = game.get_position_on_board(end)
            canvas.create_line(
                start_col * 60 + 30, start_row * 60 + 30,
                end_col * 60 + 30, end_row * 60 + 30,
                fill="red", width=3
            )

        for start, end in game.board.ladders.items():
            start_row, start_col = game.get_position_on_board(start)
            end_row, end_col = game.get_position_on_board(end)
            canvas.create_line(
                start_col * 60 + 30, start_row * 60 + 30,
                end_col * 60 + 30, end_row * 60 + 30,
                fill="green", width=3
            )

    draw_board()

    def next_turn():
        if not game.winner:
            if game.play_turn():
                next_button.config(state=tk.DISABLED)
        player_info.set("\n".join(str(player) for player in game.players))

    player_info = tk.StringVar()
    player_info.set("\n".join(str(player) for player in game.players))
    tk.Label(game_window, textvariable=player_info, font=("Arial", 14)).pack()

    next_button = tk.Button(game_window, text="Next Turn", command=next_turn)
    next_button.pack()

    game_window.mainloop()


root = tk.Tk()
root.title("Snakes and Ladders Setup")

instructions = tk.Label(root, text="Enter player names separated by commas:", font=("Arial", 14))
instructions.pack(pady=10)

entry = tk.Entry(root, font=("Arial", 14))
entry.pack(pady=10)

start_button = tk.Button(root, text="Start Game", command=start_game)
start_button.pack(pady=10)

root.mainloop()
