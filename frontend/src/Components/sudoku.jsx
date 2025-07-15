import React, { useState } from "react";
import "./sudoku.css"; // CSS file for styles
import axios from "axios";
import spinner from "/loadd.gif"; // Add your loading spinner image path
import ImageUploader from "./imageUploader";


const SudokuTable = () => {
  // Initialize the grid state
  const [errorAlert, setErrorAlert] = useState(false);
  const [gotImage, setGotImage] = useState(false)
  const [warning, setWarning] = useState(false);
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
      setLoading(true); 
      setErrorAlert(false);
      try {
          const response = await axios.post('http://localhost:8000/solve', { grid });
          const answer = response.data;
          console.log(answer)
          setGrid(answer)
      // for (let i = 0; i < answer.length; i++) {
      //   await new Promise((resolve) => {
      //     setTimeout(() => {
      //       const newGrid = [...answer[i]];
      //       const updatedGrid = newGrid.map((row, rowIndex) =>
      //         row.map((cell, colIndex) =>
      //           userInput[rowIndex][colIndex] ? grid[rowIndex][colIndex] : cell
      //         )
      //       );
      //       setGrid(updatedGrid);
      //       resolve();
      //     }, 0.01);
      //   });
      // }
      setIsSolved(true); // Set solved status
    } catch (error) {
      console.error("Error posting the Sudoku grid:", error);
      if (error.response && error.response.status === 400) {
        setErrorAlert(true); 
      }
    } finally {
      setLoading(false)
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
    setErrorAlert(false)
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
          <ImageUploader setGrid={setGrid} setLoading={setLoading} isSolved={isSolved} resetGrid={resetGrid} setGotImage={setGotImage} setWarning={setWarning} gotImage={gotImage} warning={warning} />
        </>
      )}
{errorAlert && (
  <div
    className="modal fade show "
    style={{ display: "block", backgroundColor: "rgba(0, 0, 0, 0.5)" }}
    tabIndex="-1"
    role="dialog"
  >
    <div className="modal-dialog "  role="document">
      <div className="modal-content" style={{backgroundColor:"#2c0b0e", color:"#ea868f"}}>
        <div className="modal-header">
          <h5 className="modal-title">Sudoku Cannot Be Solved</h5>
          <button
            type="button"
            className="btn-close"
            onClick={() => setErrorAlert(false)}
          ></button>
        </div>
        <div className="modal-body">
          <p>
            The given Sudoku puzzle cannot be solved. Please check your input
            or reset the grid.
          </p>
        </div>
        <div className="modal-footer">
          <button
            type="button"
            className="btn btn-danger"
            onClick={() => {
              resetGrid();
              setErrorAlert(false);
            }}
            style={{ fontSize: "0.85rem" }} // smaller text
          >
            Reset Sudoku
          </button>
        </div>
      </div>
    </div>
  </div>
)}
  {gotImage && (
    <div
      className="modal fade show "
      style={{ display: "block", backgroundColor: "rgba(0, 0, 0, 0.5)" }}
      tabIndex="-1"
      role="dialog"
    >
      <div className="modal-dialog "  role="document">
        <div className="modal-content" style={{backgroundColor:"#2c0b0e", color:"#ea868f"}}>
          <div className="modal-header">
            <h5 className="modal-title">Cannot get sudoku from uploaded image</h5>
            <button
              type="button"
              className="btn-close"
              onClick={() => setGotImage(false)}
            ></button>
          </div>
          <div className="modal-body">
            <p>
              From the uploaded image sudoku cannot be extracted
            </p>
          </div>
          <div className="modal-footer">
            <button
              type="button"
              className="btn btn-danger"
              onClick={() => {
                resetGrid();
                setGotImage(false);
              }}
              style={{ fontSize: "0.85rem" }} // smaller text
            >
              Reset Sudoku
            </button>
          </div>
        </div>
      </div>
    </div>
  )}
  {warning && (
    <div
      className="modal fade show "
      style={{ display: "block", backgroundColor: "rgba(0, 0, 0, 0.5)" }}
      tabIndex="-1"
      role="dialog"
    >
      <div className="modal-dialog "  role="document">
        <div className="modal-content" style={{backgroundColor:"#332701", color:"#ffda6a"}}>
          <div className="modal-header">
            <h5 className="modal-title">Model can be wrong</h5>
            <button
              type="button"
              className="btn-close"
              onClick={() => setWarning(false)}
            ></button>
          </div>
          <div className="modal-body">
            <p>
              Please recheck all the cells of sudoku because some digits can be predicted wrong by the model
            </p>
          </div>
          {/* <div className="modal-footer">
            <button
              type="button"
              className="btn btn-danger"
              onClick={() => {
                resetGrid();
                setWarning(false);
              }}
              style={{ fontSize: "0.85rem" }} // smaller text
            >
              Reset Sudoku
            </button>
          </div> */}
        </div>
      </div>
    </div>
  )}


    </>
  );
};

export default SudokuTable;
