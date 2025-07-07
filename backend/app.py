from flask import Flask, request,jsonify, redirect
from flask_cors import CORS
import copy
app = Flask(__name__)
CORS(app)
from tensorflow.keras.models import load_model
import numpy as np
import cv2
import tempfile
model = load_model("sudoku_digit_cnn.h5")

""" Grid data work """
def preprocess_image(path, fallback=False):
    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if fallback:
        # Fallback mode: use light blur
        gray = cv2.GaussianBlur(gray, (5, 5), 0)

    else:
        # Normal mode: sharpen
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])
        gray = cv2.filter2D(gray, -1, kernel)

    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY_INV,
        15, 4
    )

    kernel_morph = np.ones((3, 3), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel_morph)

    return image, gray, thresh


def find_sudoku_contour(thresh_img, image_shape):
    contours, _ = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    h, w = image_shape[:2]
    img_area = h * w

    max_valid_contour = None
    max_area = 0

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 0.1 * img_area or area > 0.9 * img_area:
            continue

        perimeter = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * perimeter, True)

        if len(approx) != 4:
            continue  # Not a 4-corner polygon

        # Aspect ratio check
        x, y, w_box, h_box = cv2.boundingRect(approx)
        ratio = w_box / float(h_box)
        if ratio < 0.8 or ratio > 1.2:
            continue

        # Save largest valid square-ish contour
        if area > max_area:
            max_area = area
            max_valid_contour = approx

    return max_valid_contour

def reorder_points(pts):
    pts = pts.reshape((4, 2))
    new_pts = np.zeros((4, 2), dtype="float32")

    # Sum of (x + y) will be min for top-left, max for bottom-right
    s = pts.sum(axis=1)
    new_pts[0] = pts[np.argmin(s)]  # top-left
    new_pts[2] = pts[np.argmax(s)]  # bottom-right

    # Difference (y - x) will be min for top-right, max for bottom-left
    diff = np.diff(pts, axis=1)
    new_pts[1] = pts[np.argmin(diff)]  # top-right
    new_pts[3] = pts[np.argmax(diff)]  # bottom-left

    return new_pts

def warp_sudoku(image, contour, output_size=450):
    pts = reorder_points(contour)

    dst_pts = np.array([
        [0, 0],
        [output_size - 1, 0],
        [output_size - 1, output_size - 1],
        [0, output_size - 1]
    ], dtype="float32")

    matrix = cv2.getPerspectiveTransform(pts, dst_pts)
    warped = cv2.warpPerspective(image, matrix, (output_size, output_size))
    return warped

def tillStep3(imgPath):
    image, gray, thresh = preprocess_image(imgPath)
    contour = find_sudoku_contour(thresh, image.shape)

    if contour is None:
        print("[Primary] Contour not found, retrying with fallback...")
        image, gray, thresh = preprocess_image(imgPath, fallback=True)
        contour = find_sudoku_contour(thresh, image.shape)

    if contour is not None:
        print("[Success] Contour found.")
        warped = warp_sudoku(image, contour)
        return warped
    else:
        print("[Failure] Contour not found in either mode.")
        return None

def extract_cells(warped, cell_size=50):
    cells = []
    for row in range(9):
        for col in range(9):
            x_start = col * cell_size
            y_start = row * cell_size
            cell = warped[y_start:y_start + cell_size, x_start:x_start + cell_size]
            cells.append(cell)
    return cells  # List of 81 cell images

def predict_digits_from_cells(cells, model):
    digits = []

    for cell in cells:
        gray = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (32, 32))
        norm = resized.astype('float32') / 255.0
        norm = norm.reshape(1, 32, 32, 1)

        pred = model.predict(norm, verbose=0)
        digit = np.argmax(pred)

        # Optional: you can threshold low confidence predictions as 0
        confidence = np.max(pred)
        if confidence < 0.5:
            digit = 0

        digits.append(digit)

    return digits  # Length = 81


@app.route('/process-image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    file.save(temp_file.name)

    # Step: Run tillStep3
    warped = tillStep3(temp_file.name)
    if warped is None:
        return jsonify({'error': 'Failed to process image'}), 500

    cells = extract_cells(warped)
    digits = predict_digits_from_cells(cells, model)
    # grid = np.array(digits).reshape((9, 9)).tolist()
    grid = [[str(d) if d != 0 else "" for d in digits[i * 9:(i + 1) * 9]] for i in range(9)]


    return jsonify({'grid': grid})

""" Grid data work """



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