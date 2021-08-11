class SudokuSolver:
    def __init__(self):
        pass

    def fill_cells(self, grid, i, j):
        for x in range(i, 9):
            for y in range(j, 9):
                if grid[x][y] == 0:
                    return x, y
        for x in range(0, 9):
            for y in range(0, 9):
                if grid[x][y] == 0:
                    return x, y
        return -1, -1

    def is_valid(self, grid, i, j, e):
        rowOk = all([e != grid[i][x] for x in range(9)])
        if rowOk:
            columnOk = all([e != grid[x][j] for x in range(9)])
            if columnOk:
                secTopX, secTopY = 3 * (i // 3), 3 * (j // 3)
                for x in range(secTopX, secTopX + 3):
                    for y in range(secTopY, secTopY + 3):
                        if grid[x][y] == e:
                            return False
                return True
        return False

    def solve_sudoku(self, grid, i=0, j=0):
        i, j = self.fill_cells(grid, i, j)
        if i == -1:
            return True
        for e in range(1, 10):
            if self.is_valid(grid, i, j, e):
                grid[i][j] = e
                if self.solve_sudoku(grid, i, j):
                    return True
                grid[i][j] = 0
        return False
