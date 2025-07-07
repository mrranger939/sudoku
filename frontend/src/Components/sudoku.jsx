import React, { useState } from "react";
import "./sudoku.css"; // CSS file for styles
import axios from "axios";
import spinner from "/loadd.gif"; // Add your loading spinner image path
import ImageUploader from "./imageUploader";


const SudokuTable = () => {
  // Initialize the grid state
  const [grid, setGrid] = useState(
    Array(9)
      .fill()
      .map(() => Array(9).fill(""))
  );

  // Track whether each cell was filled by the user
  const [userInput, setUserInput] = useState(
    Array(9)
      .fill()
      .map(() => Array(9).fill(false))
  );

  // Track if the puzzle has been solved
  const [isSolved, setIsSolved] = useState(false);

  // Loading state to show spinner while waiting for server response
  const [loading, setLoading] = useState(false);

  // Check if the number is valid according to Sudoku rules
  const isValidInput = (rowIndex, colIndex, value) => {
    for (let i = 0; i < 9; i++) {
      if (grid[rowIndex][i] === value) return false;
      if (grid[i][colIndex] === value) return false;
    }

    const startRow = Math.floor(rowIndex / 3) * 3;
    const startCol = Math.floor(colIndex / 3) * 3;
    for (let i = 0; i < 3; i++) {
      for (let j = 0; j < 3; j++) {
        if (grid[startRow + i][startCol + j] === value) return false;
      }
    }
    return true;
  };

  const postSudoku = async () => {
      setLoading(true); // Set loading to true when request starts
      try {
          const response = await axios.post('http://localhost:8000/solve', { grid });
          const answer = response.data;
          setLoading(false);
      for (let i = 0; i < answer.length; i++) {
        await new Promise((resolve) => {
          setTimeout(() => {
            const newGrid = [...answer[i]];
            const updatedGrid = newGrid.map((row, rowIndex) =>
              row.map((cell, colIndex) =>
                userInput[rowIndex][colIndex] ? grid[rowIndex][colIndex] : cell
              )
            );
            setGrid(updatedGrid);
            resolve();
          }, 0.01);
        });
      }
      setIsSolved(true); // Set solved status
    } catch (error) {
      console.error("Error posting the Sudoku grid:", error);
    } finally {
      // Stop loading when response is received
    }
  };

  const handleInputChange = (rowIndex, colIndex, value) => {
    if (value === "" || isValidInput(rowIndex, colIndex, value)) {
      const newGrid = [...grid];
      newGrid[rowIndex][colIndex] = value;

      const newUserInput = [...userInput];
      newUserInput[rowIndex][colIndex] = true;

      setGrid(newGrid);
      setUserInput(newUserInput);
    } else {
      alert("Invalid move! Number already exists in the row, column, or subgrid.");
    }
  };

  const resetGrid = () => {
    setGrid(
      Array(9)
        .fill()
        .map(() => Array(9).fill(""))
    );
    setUserInput(
      Array(9)
        .fill()
        .map(() => Array(9).fill(false))
    );
    setIsSolved(false);
  };

  return (
    <>
      <h1 style={{ marginBottom: "2rem" }}>Solve SUDOKU</h1>
      {loading ? (
        <div style={{ textAlign: "center" }}>
          <img src={spinner} alt="Loading..." style={{ width: "10rem" }} />
          <h3>Analyzing...</h3>
        </div>
      ) : (
        <>
          <table className="sudoku-table">
            <tbody>
              {grid.map((row, rowIndex) => (
                <tr key={rowIndex} className="sudoku-row">
                  {row.map((cell, colIndex) => (
                    <td key={colIndex} className="sudoku-cell">
                      <input
                        type="text"
                        maxLength="1"
                        value={cell}
                        onInput={(e) => {
                          e.target.value = e.target.value.replace(/[^1-9]/g, "");
                        }}
                        className="sudoku-input"
                        onChange={(e) => {
                          handleInputChange(rowIndex, colIndex, e.target.value);
                        }}
                        style={{
                          color: userInput[rowIndex][colIndex] ? "#FFD700" : "white", 
                          fontWeight: "bold"
                        }}
                        disabled={isSolved}
                      />
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
          <button
            style={{ marginTop: '2rem' }}
            type="button"
            onClick={isSolved ? resetGrid : postSudoku}
            className="btn btn-outline-light mx-auto"
          >
            {isSolved ? "Reset Sudoku" : "Solve Sudoku"}
          </button> <br />
          <ImageUploader setGrid={setGrid}/>
        </>
      )}
    </>
  );
};

export default SudokuTable;
