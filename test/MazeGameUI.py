import torch
import random
import tkinter as tk

class MazeGame:
    def __init__(self, size):
        self.size = size
        self.maze = torch.full((size, size), -1)  # -1 means unfilled
        self.player_position = (0, 0)
        self.exit_position = (size - 1, size - 1)
        self.create_solution_path()
        self.fill_remaining_cells()
    
    def create_solution_path(self):
        """Creates a guaranteed path from start to exit before filling in the rest."""
        x, y = 0, 0
        self.maze[x, y] = 0  # Mark start position
        
        while (x, y) != self.exit_position:
            possible_moves = []
            if x < self.size - 1:
                possible_moves.append((x + 1, y))  # Down
            if y < self.size - 1:
                possible_moves.append((x, y + 1))  # Right

            # Randomly choose a next step
            x, y = random.choice(possible_moves)
            self.maze[x, y] = 0  # Mark as part of solution path

    def fill_remaining_cells(self):
        """Fills remaining empty (-1) cells randomly with obstacles (1) or open paths (0)."""
        for i in range(self.size):
            for j in range(self.size):
                if self.maze[i, j] == -1:  # Only modify unfilled spots
                    self.maze[i, j] = random.choice([0, 1])  # Random open path or obstacle

    def move_player(self, direction):
        """Moves player if the move is valid."""
        x, y = self.player_position
        new_position = x, y

        if direction == 'up' and x > 0 and self.maze[x - 1, y] == 0:
            new_position = (x - 1, y)
        elif direction == 'down' and x < self.size - 1 and self.maze[x + 1, y] == 0:
            new_position = (x + 1, y)
        elif direction == 'left' and y > 0 and self.maze[x, y - 1] == 0:
            new_position = (x, y - 1)
        elif direction == 'right' and y < self.size - 1 and self.maze[x, y + 1] == 0:
            new_position = (x, y + 1)

        if new_position == self.player_position:
            return "Invalid move! Try again."
        else:
            self.player_position = new_position
            if self.player_position == self.exit_position:
                return "Congratulations! You win!"
            return "Move successful!"

    def get_maze_display(self):
        """Returns a string representation of the maze for the UI."""
        maze_str = ""
        for i in range(self.size):
            for j in range(self.size):
                if (i, j) == self.player_position:
                    maze_str += 'P '
                elif (i, j) == self.exit_position:
                    maze_str += 'E '
                elif self.maze[i, j] == 1:
                    maze_str += '# '
                else:
                    maze_str += '. '
            maze_str += '\n'
        return maze_str

# GUI Class
class MazeGameUI:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.root.title("Maze Game")

        # Maze Display
        self.maze_label = tk.Label(root, text=self.game.get_maze_display(), font=("Courier", 14), justify="left")
        self.maze_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        # Movement Buttons
        self.btn_up = tk.Button(root, text="Up", command=lambda: self.move("up"), width=10, height=2)
        self.btn_left = tk.Button(root, text="Left", command=lambda: self.move("left"), width=10, height=2)
        self.btn_right = tk.Button(root, text="Right", command=lambda: self.move("right"), width=10, height=2)
        self.btn_down = tk.Button(root, text="Down", command=lambda: self.move("down"), width=10, height=2)

        self.btn_up.grid(row=1, column=1)
        self.btn_left.grid(row=2, column=0)
        self.btn_right.grid(row=2, column=2)
        self.btn_down.grid(row=3, column=1)

        # Status Label
        self.status_label = tk.Label(root, text="Use the buttons to move!", font=("Arial", 12))
        self.status_label.grid(row=4, column=0, columnspan=3, pady=10)

    def move(self, direction):
        """Handles player movement and updates the UI."""
        status = self.game.move_player(direction)
        self.maze_label.config(text=self.game.get_maze_display())
        self.status_label.config(text=status)
        if "win" in status.lower():
            self.disable_buttons()

    def disable_buttons(self):
        """Disables movement buttons after the game is won."""
        self.btn_up.config(state=tk.DISABLED)
        self.btn_down.config(state=tk.DISABLED)
        self.btn_left.config(state=tk.DISABLED)
        self.btn_right.config(state=tk.DISABLED)

# Run the Game with GUI
if __name__ == "__main__":
    game = MazeGame(10)  # Change the size of the maze here
    root = tk.Tk()
    app = MazeGameUI(root, game)
    root.mainloop()
