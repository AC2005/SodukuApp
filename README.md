# SodukuApp

This project is a soduku app that allows the user to upload an image of a soduku puzzle and uses a machine learning model to parse the image. The app then solves it and displays an animation of the solving process. 

The main features of this project are:

1) Using the python OCR (Optical Character Recognition) model to process an unploaded picture of a sudoku puzzle to extract the digits.
2) An option to edit the board/cells after it's processed by clicking the "Edit" button and clicking on the cells you want to edit
3) A solve button that, Using a backtracking algorithm, solves the sudoku puzzle and displaying intermediate states
4) An option to pause/play and restart the animation at any time while it's running

This project took ~8-10 hours to develop.

The project is deployed at the following link: https://ocr-sudoku-app-058cbfeee458.herokuapp.com/ 

There's a folder on github called "test images" that contains sudoku puzzles that can be uploaded to the app (feel free to try your own too)