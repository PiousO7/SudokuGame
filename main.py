from window import MainWindow
from Solved_grid import SudokuSolver

win = MainWindow()
solution = SudokuSolver()
solution.solve_sudoku(win.board_solved)
# print(win.board)
# print(win.board_solved)
win.sudoku_board(grid=win.board)
win.main_grid()




