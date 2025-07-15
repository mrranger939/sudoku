import React, { useRef, useState } from "react";
import axios from "axios";
const apiUrl = import.meta.env.VITE_API_URL;

function ImageUploader({setGrid, setLoading, isSolved, resetGrid, setWarning, warning, gotImage, setGotImage}) {

  const fileInputRef = useRef(null);

  const handleUploadClick = () => {
    fileInputRef.current.click(); // Open file picker
  };

  const handleFileChange = async (event) => {
    setLoading(true)

    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("image", file);

    try {
      const res = await axios.post(`${apiUrl}/process-image`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      const grid = res.data.grid; 
      console.log("Received Grid:", grid);
      setGrid(grid)
      setWarning(true)
      // TODO: Pass grid to solver or render it

    } catch (error) {
      console.error("Upload failed:", error);
      if (error.response && error.response.status === 400) {
        setGotImage(true); 
      }
    }
    finally{
      setLoading(false)
    }
  };

  return (
    <>
    <div style={{ marginTop: '2rem' }}>
      <button onClick={handleUploadClick} className={`btn btn-outline-light mx-auto ${isSolved ? 'disabled' : ''}`}>
        Upload Image
      </button>
      <input
        type="file"
        accept="image/*"
        ref={fileInputRef}
        onChange={handleFileChange}
        style={{ display: "none" }}
      />
    </div>
    </>
    
  );
}

export default ImageUploader;
