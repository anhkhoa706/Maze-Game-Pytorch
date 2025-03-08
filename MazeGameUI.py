import tkinter as tk
from MazeGame import MazeGame 

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
        self.btn_auto = tk.Button(root, text="Auto", command=self.auto_solve, width=10, height=2)

        self.btn_up.grid(row=1, column=1)
        self.btn_left.grid(row=2, column=0)
        self.btn_auto.grid(row=2, column=1)  # Auto-solve button at the center
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

    def auto_solve(self):
        """Automatically moves the player along the shortest path."""
        solution_path = self.game.solve_maze()
        if not solution_path:
            self.status_label.config(text="No solution found!")
            return
        
        self.status_label.config(text="Auto-solving...")
        self.root.after(500, self.auto_move_step, solution_path)

    def auto_move_step(self, path):
        """Moves step by step along the solution path."""
        if not path:
            self.status_label.config(text="Solved!")
            self.disable_buttons()
            return

        direction = path.pop(0)
        self.move(direction)
        self.root.after(500, self.auto_move_step, path)

    def disable_buttons(self):
        """Disables movement buttons after the game is won."""
        self.btn_up.config(state=tk.DISABLED)
        self.btn_down.config(state=tk.DISABLED)
        self.btn_left.config(state=tk.DISABLED)
        self.btn_right.config(state=tk.DISABLED)
        self.btn_auto.config(state=tk.DISABLED)

# Run the Game with GUI
if __name__ == "__main__":
    game = MazeGame(10)  # Change the size of the maze here
    root = tk.Tk()
    app = MazeGameUI(root, game)
    root.mainloop()