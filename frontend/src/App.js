import React from "react";
import SudokuSolver from "./frontend";

function App() {
    return (
    <div className="App">
      <h1>Sudoku Solver</h1>
      <p>Upload an image of a 9x9 sudoku puzzle, and the sudoku will be solved for you! </p>
      <SudokuSolver />
    </div>
    );
}

export default App;
