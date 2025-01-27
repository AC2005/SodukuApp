import cv2
import numpy as np
from pytesseract import image_to_string
import matplotlib.pyplot as plt

def remove_artifacts(cell):
    # remove small/extraneous features from grid cell
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    cleaned = cv2.morphologyEx(cell, cv2.MORPH_CLOSE, kernel)

    return cleaned

def enhance_digit(cell):
    # make digit strokes thicker so digits are more prominent
    kernel = np.ones((2, 2), np.uint8)
    enhanced = cv2.dilate(cell, kernel, iterations=1)
    return enhanced

def preprocess_image(image_path):
    image = cv2.imread(image_path)

    # make image black and white
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    binary = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
    )
    
    # grid line features
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))

    # find and remove lines
    horizontal_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, horizontal_kernel)
    vertical_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, vertical_kernel)
    grid_lines = cv2.add(horizontal_lines, vertical_lines)
    cleaned = cv2.subtract(binary, grid_lines)

    return cleaned


def extract_cells(grid_image):
    # split grid into individual cells
    cells = []
    height, width = grid_image.shape

    row_boundaries = [round(i * height / 9) for i in range(10)] 
    col_boundaries = [round(i * width / 9) for i in range(10)]   

    for i in range(9):
        row = []
        for j in range(9):
            y_start, y_end = row_boundaries[i], row_boundaries[i + 1]
            x_start, x_end = col_boundaries[j], col_boundaries[j + 1]

            # extract and enhance cell
            cell = grid_image[y_start:y_end, x_start:x_end]
            cell = enhance_digit(remove_artifacts(cell))
            row.append(cell)
        cells.append(row)
    return cells

def recognize_digit(cell):
    resized_cell = cv2.resize(cell, (28, 28), interpolation=cv2.INTER_AREA)
    
    # Set up OCR so that it only reads digits
    config = "--psm 10 -c tessedit_char_whitelist=123456789"
    text = image_to_string(resized_cell, config=config).strip()
    
    return text if text.isdigit() else ""

def process_sudoku(image_path):
    # read and process a sudoku board

    preprocessed_image = preprocess_image(image_path)
    cells = extract_cells(preprocessed_image)
    board = []
    for row in cells:
        digits = [recognize_digit(cell) for cell in row]
        board.append(digits)
    
    return board

def print_board(board):
    for row in board:
        print(row)