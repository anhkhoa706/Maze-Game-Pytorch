import torch
import random
from collections import deque
from typing import Tuple, List

class MazeGame:
    """
    MazeGame class representing the maze game logic.

    The maze is stored as a torch tensor where:
      - 0 represents a walkable path,
      - 1 represents a wall,
      - -1 indicates an unfilled cell.
    
    A guaranteed solution path is created from the start to the exit, and
    the remaining cells are randomly assigned as either open or blocked.
    """

    def __init__(self, size: int) -> None:
        self.size: int = size
        self.maze: torch.Tensor = torch.full((size, size), -1, dtype=torch.int8)  # -1 means unfilled
        self.start_position: Tuple[int, int] = (0, 0)
        self.player_position: Tuple[int, int] = (0, 0)
        self.exit_position: Tuple[int, int] = (size - 1, size - 1)
        self.status_message: str = "Use buttons or arrow keys to move."

        self._generate_maze()

    def _generate_maze(self) -> None:
        """Generates the maze by creating a solution path and filling remaining cells."""
        self._create_solution_path()
        self._fill_remaining_cells()

    def _create_solution_path(self) -> None:
        """
        Ensures at least one solution exists from start to exit by carving a path.
        This implementation randomly moves down or right from the start.
        """
        x, y = self.start_position
        self.maze[x, y] = 0  # Mark start as walkable

        while (x, y) != self.exit_position:
            possible_moves = []
            if x < self.size - 1:
                possible_moves.append((x + 1, y))  # Move down
            if y < self.size - 1:
                possible_moves.append((x, y + 1))  # Move right

            # Randomly choose one of the possible moves
            x, y = random.choice(possible_moves)
            self.maze[x, y] = 0  # Mark cell as walkable

    def _fill_remaining_cells(self) -> None:
        """
        Fills uninitialized cells (-1) in the maze with random walls (1) or open paths (0).
        """
        for i in range(self.size):
            for j in range(self.size):
                if self.maze[i, j] == -1:
                    self.maze[i, j] = random.choice([0, 1])

    def move_player(self, direction: str) -> str:
        """
        Moves the player in the given direction if the move is valid.

        Valid directions are: 'up', 'down', 'left', 'right'.
        Returns a status message based on the move result.
        """
        x, y = self.player_position
        moves = {
            'up': (x - 1, y),
            'down': (x + 1, y),
            'left': (x, y - 1),
            'right': (x, y + 1)
        }

        if direction not in moves:
            return "Invalid direction! Use 'up', 'down', 'left', or 'right'."

        nx, ny = moves[direction]
        if 0 <= nx < self.size and 0 <= ny < self.size and self.maze[nx, ny] == 0:
            self.player_position = (nx, ny)
            if self.player_position == self.exit_position:
                return "Congratulations! You win!"
            return "Move successful!"
        return "Invalid move! Try again."

    def find_shortest_path(self) -> List[Tuple[int, int]]:
        """
        Finds the shortest path from the player's current position to the exit using BFS.
        Returns a list of positions representing the path.
        If no path is found, returns an empty list.
        """
        queue = deque([(self.player_position, [])])
        visited = {self.player_position}

        while queue:
            (x, y), path = queue.popleft()
            if (x, y) == self.exit_position:
                return path

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.size and 0 <= ny < self.size and 
                    self.maze[nx, ny] == 0 and (nx, ny) not in visited):
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [(nx, ny)]))
        return []  # No solution found

    def reset(self) -> None:
        """Resets the game by regenerating the maze and resetting the player position."""
        self.maze = torch.full((self.size, self.size), -1, dtype=torch.int8)
        self.player_position = self.start_position
        self.status_message = "Use buttons or arrow keys to move."
        self._generate_maze()

    def __str__(self) -> str:
        """
        Returns a string representation of the maze.
        'S' marks the start, 'P' marks the player's current position,
        'E' marks the exit, ' ' (space) marks an open path, and '#' marks a wall.
        """
        maze_str = ""
        for i in range(self.size):
            row = []
            for j in range(self.size):
                if (i, j) == self.player_position:
                    row.append("P")
                elif (i, j) == self.start_position:
                    row.append("S")
                elif (i, j) == self.exit_position:
                    row.append("E")
                else:
                    row.append(" " if self.maze[i, j] == 0 else "#")
            maze_str += " ".join(row) + "\n"
        return maze_str

# Example usage:
if __name__ == "__main__":
    game = MazeGame(5)
    print("Initial Maze:")
    print(game)
    print(game.move_player('right'))
    print("Maze after move:")
    print(game)
    print("Shortest path to exit from current position:")
    print(game.find_shortest_path())
