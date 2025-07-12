import numpy as np
import cv2
from tensorflow.keras.models import load_model
model = load_model("final_sudoku.h5")

def preprocess_image(path):
    image = cv2.imread(path)
    image = cv2.resize(image, (450, 450))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 6)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                   cv2.THRESH_BINARY_INV, 11, 2)
    return image, thresh

def detect_grid_lines(thresh):
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 30))
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 1))
    vertical = cv2.erode(thresh, vertical_kernel, iterations=1)
    vertical = cv2.dilate(vertical, vertical_kernel, iterations=1)
    horizontal = cv2.erode(thresh, horizontal_kernel, iterations=1)
    horizontal = cv2.dilate(horizontal, horizontal_kernel, iterations=1)
    grid = cv2.addWeighted(vertical, 0.5, horizontal, 0.5, 0.0)
    return grid

def reorder_points(pts):
    pts = pts.reshape((4, 2))
    new_pts = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    new_pts[0] = pts[np.argmin(s)]
    new_pts[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    new_pts[1] = pts[np.argmin(diff)]
    new_pts[3] = pts[np.argmax(diff)]
    return new_pts

def warp_perspective(image, grid_mask):
    contours, _ = cv2.findContours(grid_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in sorted(contours, key=cv2.contourArea, reverse=True):
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
        if len(approx) == 4:
            pts = reorder_points(approx)
            dst = np.array([[0, 0], [449, 0], [449, 449], [0, 449]], dtype="float32")
            M = cv2.getPerspectiveTransform(pts, dst)
            warp = cv2.warpPerspective(image, M, (450, 450))
            return warp
    return None

def extract_cells(warped_grid, cell_size=50,margin=5):
    cells = []
    warped_grid = cv2.resize(warped_grid, (450, 450))  # Ensure consistent size
    for row in range(9):
        for col in range(9):
            x_start = col * cell_size
            y_start = row * cell_size
            cell = warped_grid[y_start:y_start + cell_size, x_start:x_start + cell_size]
            cropped = cell[margin:cell_size - margin, margin:cell_size - margin]
            cells.append(cropped)
    return cells  

def preprocess_digit(cell):
    gray = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return np.zeros((32, 32), dtype=np.uint8)  # Return blank if no contour found
    c = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(c)
    if w == 0 or h == 0:
        return np.zeros((32, 32), dtype=np.uint8)  # Avoid zero-sized crop
    roi = thresh[y:y + h, x:x + w]
    digit = cv2.resize(roi, (20, 20), interpolation=cv2.INTER_AREA)
    padded = np.pad(digit, ((6, 6), (6, 6)), "constant", constant_values=0)
    return padded

def predict_digit(cell_img, model):
    processed = preprocess_digit(cell_img)  
    norm = processed.astype("float32") / 255.0
    norm = norm.reshape(1, 32, 32, 1)
    prediction = model.predict(norm, verbose=0)
    digit = np.argmax(prediction)
    confidence = np.max(prediction)
    if confidence < 0.5:
        return 0 
    return digit

def predictSudoku(imagePath):
    image, thresh = preprocess_image(imagePath)
    grid_mask = detect_grid_lines(thresh)
    warped_grid = warp_perspective(image, grid_mask)
    if warped_grid is not None:
        print("✅ Grid successfully extracted and warped.")
        cells = extract_cells(warped_grid)
        sudoku_grid = []
        for i in range(9):
            row = []
            for j in range(9):
                idx = i * 9 + j
                digit = predict_digit(cells[idx], model)
                row.append(int(digit))
            sudoku_grid.append(row)   
        return sudoku_grid
    else:
        print("❌ Grid could not be found.")
        return None