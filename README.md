# 🔢 Sudoku Solver Web App

A full-stack Sudoku solver that uses deep learning and computer vision to recognize Sudoku digits from an image and solve them using backtracking.

- 🔍 **Frontend**: React (Vite)
- 🧠 **Backend**: Flask (Python + TensorFlow)
- 🧠 **Model**: Trained using CNN with OpenCV preprocessing
- 📷 **Feature**: Upload Sudoku image → digit prediction → puzzle solving

---

## 📁 Folder Structure

```
/sudoku
  ├── frontend/            # React app (Vite)
  └── backend/             # Flask API
        ├── final_sudoku.h5   # Trained model file
        └── sudokuCv.ipynb    # Model training & prediction notebook
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/mrranger939/sudoku.git
cd sudoku
```

---

### 2. Backend Setup (Flask + TensorFlow)

#### ✅ Linux / macOS

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

#### ✅ Windows

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

> ⚠️ Ensure `final_sudoku.h5` is present in the `backend/` directory.  
> The notebook `sudokuCv.ipynb` contains the full pipeline using OpenCV for image preprocessing and CNN for digit recognition.

---

### 3. Frontend Setup (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

Create a `.env` file in the `frontend/` directory:

```
VITE_API_URL=http://localhost:8000
```

---

## 🧪 Features

- [x] Manual Sudoku input
- [x] Solve sudoku using Peter Norvig’s algorithm
- [x] Upload image to auto-fill the grid using CNN + OpenCV
- [x] alerts for prediction or solving errors
- [x] Responsive layout for mobile
- [x] Reset functionality

---

## 🛠️ Tech Stack

| Frontend       | Backend     | Machine Learning & CV |
|----------------|-------------|------------------------|
| React (Vite)   | Flask       | TensorFlow (Keras)     |
| HTML/CSS/JS    | Python 3.12 | OpenCV + CNN (custom model) |

---

## 🧠 Model Info

- Trained using a custom Convolutional Neural Network
- Image preprocessed with OpenCV (grayscale, thresholding, contour detection)
- Jupyter notebook: [`sudokuCv.ipynb`](backend/sudokuCv.ipynb)
- Final model saved as: `final_sudoku.h5`

---

## 🖼️ Screenshots

<img width="1358" height="650" alt="image" src="https://github.com/user-attachments/assets/79cb84f7-202e-4c49-8e8f-acf8f78faf92" />
<img width="1358" height="650" alt="image" src="https://github.com/user-attachments/assets/86b39dee-bb7a-4133-b270-ff406f8658e1" />
<img width="1358" height="650" alt="image" src="https://github.com/user-attachments/assets/25bcac73-deed-498d-b211-61987b82ffe2" />
<img width="1358" height="650" alt="image" src="https://github.com/user-attachments/assets/ab005295-f79d-4d96-ab54-29b252da10cb" />





---

## 🔮 Future Improvements

- Increase model accuracy with larger dataset
- Difficulty-level estimation
- Visual solving animation
- Export solved Sudoku as image or PDF

---

## 👨‍💻 Author

**Mohammed Shujath Nawaz**

> Contributions, stars, and forks are welcome!

---

## 📄 License

MIT License
