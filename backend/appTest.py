from flask import Flask, request,jsonify, redirect
from flask_cors import CORS
import copy
app = Flask(__name__)
CORS(app)
import numpy as np
import cv2
import tempfile
from sudoku_solver import solve_grid
from sudoku_image_solver import predictSudoku


@app.route('/process-image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    file = request.files['image']
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    file.save(temp_file.name)
    grid = predictSudoku(temp_file.name)
    if grid:
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                grid[i][j] = '' if grid[i][j] == 0 else str(grid[i][j])
        print(grid)
        return jsonify({'grid': grid})
    else:
        print('Cannot get sudoku from image')
        return jsonify({'error': 'Cannot get sudoku from image'}), 400



@app.route('/solve', methods=['POST'])
def solve_sudoku():
    data = request.json
    grid = data.get('grid')
    result = solve_grid(grid)
    if result:
        return jsonify([result]) , 200  
    else:
        print('Sudoku cannot be solved')
        return jsonify({'error': 'Sudoku cannot be solved'}), 400
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)