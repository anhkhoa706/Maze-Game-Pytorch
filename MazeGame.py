import torch
import random
from collections import deque

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

    def solve_maze(self):
        """Finds the shortest path using BFS and returns the list of moves."""
        queue = deque([(self.player_position, [])])
        visited = set([self.player_position])

        while queue:
            (x, y), path = queue.popleft()
            if (x, y) == self.exit_position:
                return path  # Return the shortest path

            for direction, (dx, dy) in [("up", (-1, 0)), ("down", (1, 0)), ("left", (0, -1)), ("right", (0, 1))]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.size and 0 <= ny < self.size and self.maze[nx, ny] == 0 and (nx, ny) not in visited:
                    queue.append(((nx, ny), path + [direction]))
                    visited.add((nx, ny))

        return []  # No solution found

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