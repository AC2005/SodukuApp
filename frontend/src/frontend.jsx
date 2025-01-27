import React, { useState, useEffect} from 'react';

function SudokuSolver() {
    const [file, setFile] = useState(null);
    const [board, setBoard] = useState(null);
    const [solution, setSolution] = useState(null);
    const [editableBoard, setEditableBoard] = useState(null); // Store the editable board
    const [isEditing, setIsEditing] = useState(false); // Toggle editing mode
    const [states, setStates] = useState([]); // Store intermediate backtracking states
    const [currentStep, setCurrentStep] = useState(0); // Track the current state being displayed
    const [isAnimating, setIsAnimating] = useState(false); // Animation toggle
    const [isProcessing, setIsProcessing] = useState(false);
    const [isOriginal, setIsOriginal] = useState(
        Array(9)
          .fill(null)
          .map(() => Array(9).fill(false))
      );
    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleSubmit = async () => {
        if (!file) {
            alert("Please select a file before submitting.");
            return;
        }
        const formData = new FormData();
        formData.append('image', file);
        console.log("File being sent:", file);
        setIsProcessing(true);
        try {
            const response = await fetch('/extract', {
                method: 'POST',
                body: formData,
            });
            const data = await response.json();
            if (response.ok) {
                //setSolution(data.solution);
                setBoard(data.board);
                console.log(data.board);
                const newIsOriginal = data.board.map((row) =>
                    row.map((cell) => cell !== "")
                  );
                setIsOriginal(newIsOriginal); // Persist the updated value in state
                setEditableBoard(JSON.parse(JSON.stringify(data.board))); // Clone the board for editing
                setIsEditing(false); // Reset editing mode
                setStates(0);
                setFile(null);
                console.log("hi", board);
            } else {
                alert("Error: Unable to load puzzle");
            }
        } catch (error) {
            console.error("Fetch error:", error);
            alert("Failed to connect to the server.");
        }

        setIsProcessing(false);
    };

    const renderBoard = (grid) => {
        console.log("Grid data for rendering:", grid);
        if (!grid) return null;
        console.log("isOriginal array:", isOriginal);
        return (
            <div className="sudoku-grid">
            {grid.flat().map((cell, index) => {
              const rowIndex = Math.floor(index / grid[0].length); // Calculate row index
              const colIndex = index % grid[0].length; // Calculate column index
      
              return (
                <div
                  key={index}
                  className={isOriginal[rowIndex][colIndex] ? "cell original" : "cell solver"}
                >
                  {cell !== 0 ? cell : ""}
                </div>
              );
            })}
          </div>
        );
    }

    const solveBoard = async () => {
        if (!board) {
            alert("No board to solve. Please extract a board first.");
            return;
        }

        try {
            const response = await fetch('/solve', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ board }),
            });

            if (!response.ok) {
                const errorMessage = await response.text();
                alert("Error solving the board.");
                return;
            }

            const data = await response.json();
            if (data.states) {
                setStates(data.states); // Set the intermediate states
                setCurrentStep(0); // Reset to the first state
                setIsAnimating(false);
            } else {
                alert("Unable to solve the board.");
            }
        } catch (error) {
            alert("Failed to connect to the server.");
        }
    };

    const handleCellChange = (rowIndex, colIndex, value) => {
        // Update the editable board
        const newBoard = [...editableBoard];
        newBoard[rowIndex][colIndex] = value === '' ? '': parseInt(value, 10).toString() || '';
        isOriginal[rowIndex][colIndex] = true;
        setEditableBoard(newBoard);
    };

    const saveEdits = () => {
        setBoard(editableBoard); // Save the edited board
        setIsEditing(false); // Exit editing mode
    };
    

    const renderEditableGrid = (grid) => {
        return (
            <div className="sudoku-grid">
                {grid.map((row, rowIndex) => (
                    <div key={rowIndex} className="sudoku-row">
                        {row.map((cell, colIndex) => (
                            <input
                                key={colIndex}
                                type="text"
                                value={cell !== 0 ? cell : ''}
                                onChange={(e) =>
                                    handleCellChange(rowIndex, colIndex, e.target.value)
                                }
                                maxLength="1"
                                className="sudoku-cell"
                            />
                        ))}
                    </div>
                ))}
            </div>
        );
    };
    
    // Automatically advance the animation
    useEffect(() => {
        if (isAnimating) {
            const interval = setInterval(() => {
                setCurrentStep((prevStep) => {
                    if (prevStep < states.length - 1) {
                        return prevStep + 1; // Move to the next state
                    } else {
                        setIsAnimating(false); // Stop animation at the last state
                        clearInterval(interval);
                        return prevStep;
                    }
                });
            }, 100); // Adjust the interval (e.g., 1000ms = 1 second)

            return () => clearInterval(interval); // Cleanup on component unmount or when animation stops
        }
    }, [isAnimating, states.length]);

    return (
        <div>
            <input type="file" onChange={handleFileChange} />
            <button onClick={handleSubmit}>Upload</button>
            {isProcessing && <p className="status-message">Processing your file... Please wait.</p>}

            {board && (
                <div>
                    <h3>{isEditing ? 'Edit the Board' : 'Extracted Board:'}</h3>
                    {isEditing
                        ? renderEditableGrid(editableBoard)
                        : renderBoard(board)}

                    {isEditing ? (
                        <button onClick={saveEdits}>Save Edits</button>
                    ) : (
                        <div>
                        <button onClick={() => setIsEditing(true)}>
                            Edit Board
                        </button>
                        <button onClick={solveBoard}>
                            Solve
                        </button>
                        </div>
                    )}
                </div>
            )}

        {states.length > 0 && (
                        <div>
                            <h3>Solve Animation:</h3>
                            {renderBoard(states[currentStep])}
                            <div className="controls">
                                <div>
                                <button onClick={() => setIsAnimating(!isAnimating)}>
                                    {isAnimating ? 'Pause' : 'Play'}
                                </button>
                                <button onClick={() => setCurrentStep(0)}>
                                    Restart Animation
                                </button>
                                </div>
                            </div>
                        </div>
                    )}
        </div>
    );
}

export default SudokuSolver;
