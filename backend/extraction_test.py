import cv2
import matplotlib.pyplot as plt
from grid_extraction import extract_cells, preprocess_image, recognize_digit, process_sudoku, print_board, preprocess_image_with_line_removal
image_path = "/Users/andrewchang/Downloads/9x9test.png"
preprocessed_image = preprocess_image(image_path)

# Display the original and preprocessed images
original_image = cv2.imread(image_path)
#preprocessed_image = preprocess_image_with_line_removal(original_image)
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.title("Original Image")
plt.imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))  # Convert BGR to RGB for display
plt.axis("off")

plt.subplot(1, 2, 2)
plt.title("Preprocessed Image")
plt.imshow(preprocessed_image, cmap="gray")
plt.axis("off")

plt.show() 

# Extract cells from the preprocessed image
cells = extract_cells(preprocessed_image)
# Display the first 9 cells for visualization
plt.figure(figsize=(10, 10))
for j in range(9):
    for i in range(9):
        plt.subplot(3, 3, i + 1)
        plt.title(f"Cell {i + 1}")
        plt.imshow(cells[j][i], cmap="gray")  # Display first row of cells
        plt.axis("off")

    plt.suptitle("Extracted Cells")
    plt.show()


board = process_sudoku(image_path)
print_board(board)

