import random
import tkinter as tk
import json

class Game2048:
    def __init__(self):
        self.grid = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.history = []
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        empty_tiles = [(r, c) for r in range(4) for c in range(4) if self.grid[r][c] == 0]
        if empty_tiles:
            r, c = random.choice(empty_tiles)
            self.grid[r][c] = 2 if random.random() < 0.9 else 4

    def slide_left(self):
        moved = False
        for row in self.grid:
            tiles = [tile for tile in row if tile != 0]
            for i in range(len(tiles) - 1):
                if tiles[i] == tiles[i + 1]:
                    tiles[i] *= 2
                    self.score += tiles[i]
                    tiles[i + 1] = 0
            new_row = [tile for tile in tiles if tile != 0]
            new_row += [0] * (4 - len(new_row))
            if new_row != row:
                moved = True
            row[:] = new_row
        return moved

    def rotate_grid(self):
        self.grid = [list(row) for row in zip(*self.grid[::-1])]

    def move(self, direction):
        self.save_state()
        moved = False
        if direction == "Left":
            moved = self.slide_left()
        elif direction == "Right":
            self.rotate_grid()
            self.rotate_grid()
            moved = self.slide_left()
            self.rotate_grid()
            self.rotate_grid()
        elif direction == "Up":
            self.rotate_grid()
            self.rotate_grid()
            self.rotate_grid()
            moved = self.slide_left()
            self.rotate_grid()
        elif direction == "Down":
            self.rotate_grid()
            moved = self.slide_left()
            self.rotate_grid()
            self.rotate_grid()
            self.rotate_grid()
        if moved:
            self.add_new_tile()

    def check_game_over(self):
        if any(0 in row for row in self.grid):
            return False
        for row in self.grid:
            for i in range(3):
                if row[i] == row[i + 1]:
                    return False
        for col in range(4):
            for row in range(3):
                if self.grid[row][col] == self.grid[row + 1][col]:
                    return False
        return True

    def save_state(self):
        self.history.append((self.grid, self.score))

    def undo(self):
        if self.history:
            self.grid, self.score = self.history.pop()


class GUI2048:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.leaderboard = Leaderboard()
        self.game_over_shown = False  # Flag to prevent multiple game over dialogs
        self.setup_ui()
        self.update_ui()

    def setup_ui(self):
        self.root.title("2048 Game")
        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack()
        self.tiles = [[tk.Label(self.grid_frame, text="", width=4, height=2, font=("Helvetica", 32)) for _ in range(4)] for _ in range(4)]
        for r in range(4):
            for c in range(4):
                self.tiles[r][c].grid(row=r, column=c, padx=5, pady=5)

        self.score_label = tk.Label(self.root, text="Score: 0", font=("Helvetica", 24))
        self.score_label.pack()
        self.root.bind("<Key>", self.key_handler)

    def update_ui(self):
        for r in range(4):
            for c in range(4):
                value = self.game.grid[r][c]
                self.tiles[r][c].config(text=str(value) if value != 0 else "", bg=self.get_tile_color(value))
        self.score_label.config(text=f"Score: {self.game.score}")
        if self.game.check_game_over() and not self.game_over_shown:
            self.show_game_over()
        self.root.after(100, self.update_ui)

    def get_tile_color(self, value):
        colors = {
            0: "#cdc1b4", 2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
            16: "#f59563", 32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72",
            256: "#edcc61", 512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"
        }
        return colors.get(value, "#3c3a32")

    def key_handler(self, event):
        if event.keysym in ["Left", "Right", "Up", "Down"]:
            self.game.move(event.keysym)
        elif event.keysym == "u":
            self.game.undo()

    def show_game_over(self):
        self.game_over_shown = True  # Set the flag to indicate the game over dialog has been shown
        self.leaderboard.add_score(self.game.score)
        top = tk.Toplevel(self.root)
        top.title("Game Over")
        msg = tk.Label(top, text=f"Game Over!\nYour Score: {self.game.score}", font=("Helvetica", 24))
        msg.pack()
        leaderboard_msg = tk.Label(top, text=f"Highest Score: {self.leaderboard.highest_score}", font=("Helvetica", 16))
        leaderboard_msg.pack()
        new_game_button = tk.Button(top, text="New Game", command=lambda: self.new_game(top))
        new_game_button.pack()
        exit_button = tk.Button(top, text="Exit", command=self.root.destroy)
        exit_button.pack()
        top.geometry("300x200")
        top.transient(self.root)
        top.grab_set()
        self.root.wait_window(top)

    def new_game(self, top):
        top.destroy()  # Close the Game Over window
        self.game.__init__()  # Reinitialize the game
        self.game_over_shown = False  # Reset the game over flag
        self.update_ui()




class Leaderboard:
    def __init__(self, file_path="leaderboard.json"):
        self.file_path = file_path
        self.highest_score = self.load_score()

    def load_score(self):
        try:
            with open(self.file_path, 'r') as file:
                scores = json.load(file)
                # Ensure the highest score is an integer
                if scores:
                    return max(scores)
                else:
                    return 0
        except FileNotFoundError:
            return 0

    def save_score(self):
        with open(self.file_path, 'w') as file:
            json.dump([self.highest_score], file)

    def add_score(self, score):
        if score > self.highest_score:
            self.highest_score = score
            self.save_score()


def main():
    root = tk.Tk()
    game = Game2048()
    gui = GUI2048(root, game)
    root.mainloop()

if __name__ == "__main__":
    main()
