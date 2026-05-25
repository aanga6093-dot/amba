#!/usr/bin/env python3
"""
Sudoku Game for Termux
Fitur lengkap dengan generator random, solver, hint, dan undo
"""

import random
import copy
import os
import sys

class SudokuGame:
    def __init__(self):
        self.board = [[0]*9 for _ in range(9)]
        self.solution = [[0]*9 for _ in range(9)]
        self.initial_board = [[0]*9 for _ in range(9)]
        self.cursor_row = 0
        self.cursor_col = 0
        self.history = []
        self.mistakes = 0
        self.hints_used = 0
        
    def clear_screen(self):
        os.system('clear')
        
    def is_valid(self, board, row, col, num):
        """Check if number is valid in position"""
        # Check row
        if num in board[row]:
            return False
            
        # Check column
        if num in [board[i][col] for i in range(9)]:
            return False
            
        # Check 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if board[i][j] == num:
                    return False
        return True
    
    def solve(self, board):
        """Solve sudoku using backtracking"""
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    numbers = list(range(1, 10))
                    random.shuffle(numbers)
                    for num in numbers:
                        if self.is_valid(board, row, col, num):
                            board[row][col] = num
                            if self.solve(board):
                                return True
                            board[row][col] = 0
                    return False
        return True
    
    def generate_puzzle(self, difficulty='medium'):
        """Generate a new random sudoku puzzle"""
        # Create empty board
        self.board = [[0]*9 for _ in range(9)]
        
        # Fill diagonal 3x3 boxes first (independent)
        for box in range(0, 9, 3):
            nums = list(range(1, 10))
            random.shuffle(nums)
            idx = 0
            for i in range(3):
                for j in range(3):
                    self.board[box + i][box + j] = nums[idx]
                    idx += 1
        
        # Solve the rest
        self.solve(self.board)
        self.solution = copy.deepcopy(self.board)
        
        # Remove numbers based on difficulty
        difficulty_levels = {
            'easy': 35,      # Remove 35 numbers (46 given)
            'medium': 45,    # Remove 45 numbers (36 given)
            'hard': 55,      # Remove 55 numbers (26 given)
            'expert': 64     # Remove 64 numbers (17 given)
        }
        
        cells_to_remove = difficulty_levels.get(difficulty, 45)
        cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(cells)
        
        for i in range(cells_to_remove):
            row, col = cells[i]
            self.board[row][col] = 0
        
        self.initial_board = copy.deepcopy(self.board)
        self.history = []
        self.mistakes = 0
        self.hints_used = 0
    
    def print_board(self):
        """Print the sudoku board with colors and cursor"""
        self.clear_screen()
        
        print("╔═══════════════════════════════════╗")
        print("║     SUDOKU GAME - TERMUX         ║")
        print("╠═══════════════════════════════════╣")
        print(f"║ Mistakes: {self.mistakes}/3  Hints: {self.hints_used}     ║")
        print("╚═══════════════════════════════════╝\n")
        
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("      ─────────┼─────────┼─────────")
            
            row_str = "      "
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    row_str += "│ "
                
                cell_value = self.board[i][j]
                
                # Color coding
                if i == self.cursor_row and j == self.cursor_col:
                    # Cursor position (highlighted)
                    if cell_value == 0:
                        row_str += "\033[47m\033[30m . \033[0m"
                    else:
                        row_str += f"\033[47m\033[30m {cell_value} \033[0m"
                elif self.initial_board[i][j] != 0:
                    # Initial numbers (cyan/blue - fixed)
                    row_str += f"\033[96m {cell_value} \033[0m"
                elif cell_value != 0:
                    # User input (green if correct, red if wrong)
                    if cell_value == self.solution[i][j]:
                        row_str += f"\033[92m {cell_value} \033[0m"
                    else:
                        row_str += f"\033[91m {cell_value} \033[0m"
                else:
                    row_str += " . "
            
            print(row_str)
        
        print("\n╔═══════════════════════════════════╗")
        print("║ Controls:                        ║")
        print("║ WASD/Arrow - Move cursor         ║")
        print("║ 1-9 - Enter number               ║")
        print("║ 0/Delete - Clear cell            ║")
        print("║ h - Hint  u - Undo  n - New game ║")
        print("║ s - Solve  q - Quit              ║")
        print("╚═══════════════════════════════════╝")
    
    def get_hint(self):
        """Provide a hint for current position"""
        if self.board[self.cursor_row][self.cursor_col] == 0:
            correct_num = self.solution[self.cursor_row][self.cursor_col]
            self.board[self.cursor_row][self.cursor_col] = correct_num
            self.hints_used += 1
            return True
        return False
    
    def undo(self):
        """Undo last move"""
        if self.history:
            row, col, old_val = self.history.pop()
            self.board[row][col] = old_val
            return True
        return False
    
    def make_move(self, num):
        """Make a move on the board"""
        row, col = self.cursor_row, self.cursor_col
        
        # Can't modify initial cells
        if self.initial_board[row][col] != 0:
            return False
        
        # Save history
        self.history.append((row, col, self.board[row][col]))
        
        # Update board
        old_val = self.board[row][col]
        self.board[row][col] = num
        
        # Check if wrong
        if num != 0 and num != self.solution[row][col]:
            self.mistakes += 1
        
        return True
    
    def is_complete(self):
        """Check if puzzle is solved"""
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != self.solution[i][j]:
                    return False
        return True
    
    def auto_solve(self):
        """Show solution"""
        self.board = copy.deepcopy(self.solution)

def get_key():
    """Get keyboard input for Termux"""
    import termios
    import tty
    
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        
        # Handle arrow keys and special keys
        if ch == '\x1b':  # ESC sequence
            ch2 = sys.stdin.read(1)
            if ch2 == '[':
                ch3 = sys.stdin.read(1)
                if ch3 == 'A': return 'UP'
                elif ch3 == 'B': return 'DOWN'
                elif ch3 == 'C': return 'RIGHT'
                elif ch3 == 'D': return 'LEFT'
        
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def main():
    game = SudokuGame()
    
    print("\n╔═══════════════════════════════════╗")
    print("║     SUDOKU GAME - TERMUX         ║")
    print("╠═══════════════════════════════════╣")
    print("║                                  ║")
    print("║  Select Difficulty:              ║")
    print("║                                  ║")
    print("║  1. Easy                         ║")
    print("║  2. Medium                       ║")
    print("║  3. Hard                         ║")
    print("║  4. Expert                       ║")
    print("║                                  ║")
    print("╚═══════════════════════════════════╝")
    
    difficulty_map = {'1': 'easy', '2': 'medium', '3': 'hard', '4': 'expert'}
    
    while True:
        choice = get_key()
        if choice in difficulty_map:
            difficulty = difficulty_map[choice]
            break
    
    print(f"\nGenerating {difficulty} puzzle...")
    game.generate_puzzle(difficulty)
    
    while True:
        game.print_board()
        
        # Check win condition
        if game.is_complete():
            print("\n\033[92m╔═══════════════════════════════════╗\033[0m")
            print("\033[92m║   🎉 CONGRATULATIONS! YOU WON! 🎉 ║\033[0m")
            print("\033[92m╚═══════════════════════════════════╝\033[0m")
            print(f"\nMistakes: {game.mistakes}, Hints used: {game.hints_used}")
            print("\nPress any key to exit...")
            get_key()
            break
        
        # Check game over
        if game.mistakes >= 3:
            print("\n\033[91m╔═══════════════════════════════════╗\033[0m")
            print("\033[91m║      GAME OVER - 3 MISTAKES!      ║\033[0m")
            print("\033[91m╚═══════════════════════════════════╝\033[0m")
            print("\nPress any key to exit...")
            get_key()
            break
        
        key = get_key()
        
        # Movement
        if key in ['w', 'W', 'UP']:
            game.cursor_row = (game.cursor_row - 1) % 9
        elif key in ['s', 'S', 'DOWN']:
            game.cursor_row = (game.cursor_row + 1) % 9
        elif key in ['a', 'A', 'LEFT']:
            game.cursor_col = (game.cursor_col - 1) % 9
        elif key in ['d', 'D', 'RIGHT']:
            game.cursor_col = (game.cursor_col + 1) % 9
        
        # Number input
        elif key in '123456789':
            game.make_move(int(key))
        
        # Clear cell
        elif key in ['0', '\x7f']:  # 0 or Delete
            game.make_move(0)
        
        # Actions
        elif key in ['h', 'H']:
            game.get_hint()
        elif key in ['u', 'U']:
            game.undo()
        elif key in ['n', 'N']:
            main()  # Restart
            break
        elif key in ['s', 'S']:
            game.auto_solve()
        elif key in ['q', 'Q']:
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGame terminated. Thanks for playing!")
        sys.exit(0)
