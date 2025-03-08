import torch
import random

class MazeGame:
    def __init__(self, size):
        """
        Generate slovable maze 
        Step 1: 
            Create a full matrix -1 (-1 mean unfill).
        Step 2: 
            Initialize End point, Start point.
        Step 3: 
            Find the possible path, fill with 0.
        Step 4: 
            Fill the rest for generate the slovable maze, 
            Modify the unfill (-1) block with random 0 or 1.
        """
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
            print("Invalid move! Try again.")
        else:
            self.player_position = new_position

    def check_game_status(self):
        """Checks if player has won."""
        if self.player_position == self.exit_position:
            return 'Win'
        elif self.maze[self.player_position[0], self.player_position[1]] == 1:
            return 'Hit obstacle'
        else:
            return 'Continue'

    def display_game(self):
        """Prints the maze with player and exit positions."""
        print("\n" + "=" * (self.size * 2))
        for i in range(self.size):
            for j in range(self.size):
                if (i, j) == self.player_position:
                    print('P', end=' ')
                elif (i, j) == self.exit_position:
                    print('E', end=' ')
                elif self.maze[i, j] == 1:
                    print('#', end=' ')
                else:
                    print('.', end=' ')
            print()
        print("=" * (self.size * 2))

# Run the Maze Game
maze_game = MazeGame(10)

# Store the Maze Matrix Game 
# print(maze_game.maze)
# maze_game.display_game()

while True:
    maze_game.display_game()
    move = input("Enter your move (up, down, left, right): ").strip().lower()
    maze_game.move_player(move)
    status = maze_game.check_game_status()
    if status == 'Win':
        print("Congratulations! You win!")
        break
    else:
        print("Keep exploring...")
