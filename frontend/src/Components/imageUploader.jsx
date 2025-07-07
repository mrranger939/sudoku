import React, { useRef } from "react";
import axios from "axios";

function ImageUploader({setGrid}) {
  const fileInputRef = useRef(null);

  const handleUploadClick = () => {
    fileInputRef.current.click(); // Open file picker
  };

  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("image", file);

    try {
      const res = await axios.post("http://localhost:8000/process-image", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      const grid = res.data.grid; // e.g., [[5,3,0,...],[6,...],...]
      console.log("Received Grid:", grid);
      setGrid(grid)
      // TODO: Pass grid to solver or render it

    } catch (error) {
      console.error("Upload failed:", error);
    }
  };

  return (
    <div style={{ marginTop: '2rem' }}>
      <button onClick={handleUploadClick} className="btn btn-outline-light mx-auto">
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
  );
}

export default ImageUploader;
