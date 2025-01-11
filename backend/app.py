from flask import Flask, request,jsonify, redirect
from flask_cors import CORS
import copy
app = Flask(__name__)
CORS(app)


def process_data(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == '':
                grid[i][j] = 0
            else:
                grid[i][j] = int(grid[i][j])

def encode_data(g):
    grid = copy.deepcopy(g)
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                grid[i][j] = ''
            else:
                grid[i][j] = str(grid[i][j])
    return grid


def check_horizontally(matrix, r, n):
    if n in matrix[r]:
        return False
    return True

def check_vertically(matrix, c, n):
    for i in range(0, 9):
        if matrix[i][c] == n:
            return False
    return True
def give_base(x):
    if x >= 6:
        return 6
    elif x >= 3:
        return 3
    else:
        return 0



def check_group(matrix, r, c, n):
    cb = give_base(c)
    rb = give_base(r)
    for i in range(3):
        for j in range(3):
            if matrix[rb+i][cb+j] == n:
                return False
    return True
def check_if_match(matrix, r, c, n):
    if check_horizontally(matrix, r, n) and check_vertically(matrix, c, n) and check_group(matrix, r, c, n):
        return True
    return False
final_list = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 
5), (6, 6), (6, 7), (6, 8), (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8), (8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8)]

def find_sol(matrix, i, final_res):
    r,c = final_list[i]
    if matrix[r][c] == 0:
        for j in range(1,10):
            if check_if_match(matrix, r, c, j):
                matrix[r][c] = j
                final_res.append(encode_data(matrix))
                
                if r == 8 and c == 8:
                    return True
                if find_sol(matrix, i+1, final_res):
                    return True
                else:
                    matrix[r][c] = 0
                    continue
        return False
    else:
        if r == 8 and c == 8:
            return True
        return find_sol(matrix, i+1, final_res)

@app.route('/solve', methods=['POST'])
def solve_sudoku():

    data = request.json
    grid = data.get('grid')
    process_data(grid)
    
    final_res = []
    find_sol(grid, 0, final_res)
    print(len(final_res))
    print(final_res[-1])
  
  
    encode_data(grid)
    return jsonify(final_res) , 200  

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)