from sudoku_solver import solve_grid
from sudoku_image_solver import predictSudoku
input_grid = [
    ["1", "1", "7", "", "", "6", "4", "5", ""],
    ["", "2", "5", "3", "4", "", "", "", "8"],
    ["", "6", "", "", "", "1", "", "7", ""],
    ["", "5", "3", "", "", "", "", "2", "9"],
    ["6", "1", "", "", "", "9", "8", "", ""],
    ["", "", "", "6", "", "2", "", "", "7"],
    ["", "", "1", "", "9", "3", "2", "", ""],
    ["", "", "8", "", "", "", "", "", ""],
    ["", "4", "", "", "7", "8", "5", "9", "1"],
]

result = solve_grid(input_grid)

if result:
    print("Solved Grid:")
    for row in result:
        print(row)
else:
    print("Unsolvable grid")
print(predictSudoku('./Sudoku.jpg'))