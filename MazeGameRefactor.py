import tkinter as tk
import torch
import random
from collections import deque

# Maze Configuration Constants
MAZE_SIZE = 10  # Size of the maze grid
CELL_SIZE = 40  # Size of each cell in the grid

class MazeGame:
    """Class representing the Maze game logic."""
    def __init__(self, size):
        self.size = size
        self.maze = torch.full((size, size), -1)  # -1 means unfilled
        self.start_position = (0, 0)
        self.player_position = (0, 0)
        self.exit_position = (size - 1, size - 1)
        self.status_message = "Use buttons or arrow keys to move."
        
        # Generate maze
        self.create_solution_path()
        self.fill_remaining_cells()

    def create_solution_path(self):
        """Ensures at least one solution from start to exit."""
        x, y = 0, 0
        self.maze[x, y] = 0  # Mark start position as walkable

        while (x, y) != self.exit_position:
            possible_moves = []
            if x < self.size - 1:
                possible_moves.append((x + 1, y))  # Move Down
            if y < self.size - 1:
                possible_moves.append((x, y + 1))  # Move Right

            if possible_moves:
                x, y = random.choice(possible_moves)
                self.maze[x, y] = 0  # Mark cell as walkable

    def fill_remaining_cells(self):
        """Fills the rest of the maze with random walls (1) and paths (0)."""
        for i in range(self.size):
            for j in range(self.size):
                if self.maze[i, j] == -1:
                    self.maze[i, j] = random.choice([0, 1])  # Randomly open or block

    def move_player(self, direction):
        """Moves the player if the move is valid."""
        x, y = self.player_position
        moves = {'up': (x - 1, y), 'down': (x + 1, y), 'left': (x, y - 1), 'right': (x, y + 1)}
        
        if direction in moves:
            nx, ny = moves[direction]
            if 0 <= nx < self.size and 0 <= ny < self.size and self.maze[nx, ny] == 0:
                self.player_position = (nx, ny)
                return "Congratulations! You win!" if self.player_position == self.exit_position else "Move successful!"
        return "Invalid move! Try again."

    def find_shortest_path(self):
        """Finds the shortest path using BFS."""
        queue = deque([(self.player_position, [])])
        visited = set()
        
        while queue:
            (x, y), path = queue.popleft()
            visited.add((x, y))

            if (x, y) == self.exit_position:
                return path  # Return shortest path 

            for direction, (dx, dy) in [("up", (-1, 0)), ("down", (1, 0)), ("left", (0, -1)), ("right", (0, 1))]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.size and 0 <= ny < self.size and self.maze[nx, ny] == 0 and (nx, ny) not in visited:
                    queue.append(((nx, ny), path + [(nx, ny)]))
                    visited.add((nx, ny))

        return [] # No solution found  

    def reset(self):
        """Resets the game by generating the maze."""
        self.__init__(self.size)

# GUI Class for MazeGame
class MazeGameUI:
    def __init__(self, root, game):
        """Handles the graphical interface of the maze game."""
        self.root = root
        self.game = game
        self.root.title("Maze Game")

        # Frames
        self.game_frame = tk.Frame(root)
        self.game_frame.grid(row=0, column=0, padx=10, pady=10)

        self.control_panel = tk.Frame(root, width=200)
        self.control_panel.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        # Maze Display using Canvas
        self.canvas = tk.Canvas(self.game_frame, width=MAZE_SIZE * CELL_SIZE, height=MAZE_SIZE * CELL_SIZE)
        self.canvas.grid(row=0, column=0)

        # Status Label
        self.status_label = tk.Label(self.control_panel, text=self.game.status_message, font=("Arial", 12), wraplength=180)
        self.status_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Buttons
        self.btn_up = tk.Button(self.control_panel, text="Up", command=lambda: self.move("up"), width=10, height=2)
        self.btn_left = tk.Button(self.control_panel, text="Left", command=lambda: self.move("left"), width=10, height=2)
        self.btn_right = tk.Button(self.control_panel, text="Right", command=lambda: self.move("right"), width=10, height=2)
        self.btn_down = tk.Button(self.control_panel, text="Down", command=lambda: self.move("down"), width=10, height=2)
        self.btn_auto = tk.Button(self.control_panel, text="Auto", command=self.auto_solve, width=10, height=2)
        self.btn_reset = tk.Button(self.control_panel, text="Reset", command=self.reset_game, width=10, height=2)

        # Layout Control Buttons
        self.btn_up.grid(row=1, column=1, pady=5)
        self.btn_left.grid(row=2, column=0, pady=5)
        self.btn_auto.grid(row=2, column=1, pady=5)  # Auto button in center
        self.btn_right.grid(row=2, column=2, pady=5)
        self.btn_down.grid(row=3, column=1, pady=5)
        self.btn_reset.grid(row=4, column=1, pady=10)

        self.solution_path = []
        self.draw_solution_path = False

        self.draw_maze()

    def draw_maze(self):
        """Draws the maze using colors for paths and walls."""
        self.canvas.delete("all")
        for i in range(self.game.size):
            for j in range(self.game.size):
                x1, y1, x2, y2 = j * CELL_SIZE, i * CELL_SIZE, (j + 1) * CELL_SIZE, (i + 1) * CELL_SIZE
                color = "gray" if self.game.maze[i, j] == 0 else "black"
                if (i, j) == self.game.exit_position:
                    color = "blue"
                elif (i, j) == self.game.player_position:
                    color = "green"
                elif (i,j) == self.game.start_position:
                    color = "yellow"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="white")
        
        # Shortest path
        if self.draw_solution_path and self.solution_path:
            for i in range(self.game.size):
                for j in range(self.game.size):
                    x1, y1, x2, y2 = j * CELL_SIZE, i * CELL_SIZE, (j + 1) * CELL_SIZE, (i + 1) * CELL_SIZE
                    if (i, j) in self.solution_path:
                        # If i, j not start, player, exit position
                        if (i, j) not in [self.game.start_position, self.game.player_position, self.game.exit_position]:
                            # Red Dot
                            dot_size = 10
                            self.canvas.create_oval(x1 + (CELL_SIZE - dot_size) / 2, y1 + (CELL_SIZE - dot_size) / 2,
                                x1 + (CELL_SIZE + dot_size) / 2, y1 + (CELL_SIZE + dot_size) / 2,fill="red")

    def move(self, direction):
        status = self.game.move_player(direction)
        self.draw_maze()
        self.status_label.config(text=status)
        if "win" in status.lower():
            self.disable_buttons(True)

    def auto_solve(self):
        """Moves player step by step along the shortest path and displays it after winning."""
        self.solution_path = self.game.find_shortest_path()
        solution_path = list(self.solution_path)
        if not solution_path:
            self.status_label.config(text="No solution found!")
            return
        
        self.status_label.config(text="Auto-solving...")
        self.root.after(500, self.auto_move_step, solution_path)

    def auto_move_step(self, path):
        """Moves step by step along the solution path."""
        if not path:
            # Draw the shortest_path 
            self.draw_solution_path = True
            self.draw_maze()
            self.status_label.config(text="Solved!")
            self.disable_buttons(True)
            return
        
        next_move = path.pop(0)
        self.game.player_position = next_move
        self.draw_maze()
        self.root.after(500, self.auto_move_step, path)

    def reset_game(self):
        self.game.reset()
        # Reset 
        self.disable_buttons(False)
        self.draw_solution_path = False
        self.status_label.config(text=self.game.status_message)
        # Draw
        self.draw_maze()
        
    def disable_buttons(self, disable: True):
        """Disables movement buttons after the game is won."""
        if disable:
            self.btn_up.config(state=tk.DISABLED)
            self.btn_down.config(state=tk.DISABLED)
            self.btn_left.config(state=tk.DISABLED)
            self.btn_right.config(state=tk.DISABLED)
            self.btn_auto.config(state=tk.DISABLED)
        else:
            self.btn_up.config(state=tk.ACTIVE)
            self.btn_down.config(state=tk.ACTIVE)
            self.btn_left.config(state=tk.ACTIVE)
            self.btn_right.config(state=tk.ACTIVE)
            self.btn_auto.config(state=tk.ACTIVE)

# Run the Game
if __name__ == "__main__":
    game = MazeGame(MAZE_SIZE)
    root = tk.Tk()
    app = MazeGameUI(root, game)
    root.mainloop()
