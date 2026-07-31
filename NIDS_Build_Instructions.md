# BUILD INSTRUCTIONS: Optimized Network Intrusion Detection System (NIDS)

> **PURPOSE OF THIS FILE:** This file contains every instruction needed to build the full NIDS product from scratch. Follow each step in order. Do not skip steps. Do not improvise. If something is unclear, re-read the section.

---

## TABLE OF CONTENTS

1. [Project Overview](#1-project-overview)
2. [Folder Structure](#2-folder-structure)
3. [Phase 1: ML Pipeline](#3-phase-1-ml-pipeline)
4. [Phase 2: FastAPI Backend](#4-phase-2-fastapi-backend)
5. [Phase 3: React Frontend](#5-phase-3-react-frontend)
6. [Phase 4: Integration and Testing](#6-phase-4-integration-and-testing)
7. [Styling Guide](#7-styling-guide)
8. [How to Run the Project](#8-how-to-run-the-project)

---

## 1. PROJECT OVERVIEW

### What We Are Building

A web application that detects cyber attacks in network traffic using machine learning.

### How It Works (Simple Explanation)

1. A user opens a website (React app) in their browser.
2. The user uploads a CSV file containing network traffic data.
3. The website sends that file to a Python server (FastAPI).
4. The Python server runs the file through a trained machine learning model.
5. The model classifies each row as either "Normal" traffic or a specific "Attack" type.
6. The results are sent back to the website and displayed as charts, statistics, and a table.

### Three Parts of the System

```
PART 1: ML Pipeline (Python scripts)
  - Downloads and cleans the dataset
  - Trains machine learning models
  - Saves the best model as a file

PART 2: Backend API (FastAPI - Python)
  - Loads the saved model
  - Accepts CSV file uploads via HTTP
  - Returns predictions as JSON

PART 3: Frontend UI (React + Vite)
  - Lets users upload CSV files
  - Shows results as charts and tables
  - Looks modern and professional
```

### Technology Stack

| Tool | What It Does | Version |
|------|-------------|---------|
| Python | Backend language | 3.10+ |
| Pandas | Data manipulation | Latest |
| NumPy | Numerical computation | Latest |
| Scikit-learn | ML algorithms, preprocessing | Latest |
| XGBoost | Gradient boosting ML model | Latest |
| LightGBM | Fast gradient boosting ML model | Latest |
| Matplotlib | Generate charts/plots | Latest |
| Seaborn | Beautiful statistical charts | Latest |
| FastAPI | Python web API framework | Latest |
| Uvicorn | ASGI server to run FastAPI | Latest |
| Joblib | Save/load ML models | Latest |
| Node.js | JavaScript runtime for React | 18+ |
| React | Frontend UI library | 18+ |
| Vite | Frontend build tool | Latest |
| Recharts | React charting library | Latest |
| Axios | HTTP client for API calls | Latest |

### Dataset: UNSW-NB15

- **What:** A network traffic dataset with normal and attack traffic.
- **Source:** University of New South Wales, Canberra, Australia.
- **Download:** https://research.unsw.edu.au/projects/unsw-nb15-dataset
- **Alternative download:** The dataset has 4 CSV files (UNSW-NB15_1.csv to UNSW-NB15_4.csv) plus a features list file and a ground truth file.
- **For this project, use the pre-split training and testing sets:**
  - `UNSW_NB15_training-set.csv` (175,341 rows)
  - `UNSW_NB15_testing-set.csv` (82,332 rows)
- **Features:** 49 columns describing network connections.
- **Target columns:**
  - `label` — Binary: 0 = Normal, 1 = Attack
  - `attack_cat` — Multi-class: Normal, Fuzzers, Analysis, Backdoors, DoS, Exploits, Generic, Reconnaissance, Shellcode, Worms
- **Cost:** FREE. Publicly available for academic use.

---

## 2. FOLDER STRUCTURE

Create this exact folder structure. Every file listed below MUST be created.

```
nids-project/
│
├── ml-pipeline/
│   ├── data/
│   │   ├── UNSW_NB15_training-set.csv      ← (downloaded manually)
│   │   └── UNSW_NB15_testing-set.csv       ← (downloaded manually)
│   │
│   ├── notebooks/
│   │   └── exploration.ipynb                ← (optional, for EDA)
│   │
│   ├── scripts/
│   │   ├── preprocess.py                    ← Step 1: Clean and prepare data
│   │   ├── feature_selection.py             ← Step 2: Select best features
│   │   ├── train_models.py                  ← Step 3: Train all 5 ML models
│   │   └── evaluate_models.py               ← Step 4: Compare models, generate charts
│   │
│   ├── saved_models/                        ← Output: saved .joblib files
│   │   ├── best_model.joblib
│   │   ├── scaler.joblib
│   │   ├── label_encoders.joblib
│   │   └── selected_features.joblib
│   │
│   ├── outputs/                             ← Output: charts and figures
│   │   ├── attack_distribution.png
│   │   ├── correlation_heatmap.png
│   │   ├── feature_importance.png
│   │   ├── model_comparison.png
│   │   ├── confusion_matrix.png
│   │   └── roc_curves.png
│   │
│   └── requirements.txt
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                          ← FastAPI entry point
│   │   ├── config.py                        ← Configuration settings
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   └── predict.py                   ← Prediction API endpoints
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   └── ml_service.py                ← Model loading and inference
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── preprocessing.py             ← Data preprocessing functions
│   │
│   ├── models/                              ← Copy saved models here from ml-pipeline
│   │   ├── best_model.joblib
│   │   ├── scaler.joblib
│   │   ├── label_encoders.joblib
│   │   └── selected_features.joblib
│   │
│   ├── requirements.txt
│   └── README.md
│
├── frontend/
│   ├── public/
│   │   └── favicon.ico
│   │
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx                   ← Top navigation bar
│   │   │   ├── FileUpload.jsx               ← Drag-and-drop file upload
│   │   │   ├── StatsCards.jsx               ← Summary statistic cards
│   │   │   ├── AttackPieChart.jsx           ← Pie chart: Normal vs Attack
│   │   │   ├── AttackBarChart.jsx           ← Bar chart: Attack type breakdown
│   │   │   ├── PredictionsTable.jsx         ← Scrollable results table
│   │   │   └── LoadingSpinner.jsx           ← Loading animation
│   │   │
│   │   ├── pages/
│   │   │   ├── HomePage.jsx                 ← Landing page with upload
│   │   │   └── ResultsPage.jsx              ← Dashboard with results
│   │   │
│   │   ├── services/
│   │   │   └── api.js                       ← Axios API calls to FastAPI
│   │   │
│   │   ├── styles/
│   │   │   ├── global.css                   ← Global styles, CSS variables
│   │   │   ├── Navbar.css
│   │   │   ├── FileUpload.css
│   │   │   ├── StatsCards.css
│   │   │   ├── Charts.css
│   │   │   ├── PredictionsTable.css
│   │   │   ├── HomePage.css
│   │   │   └── ResultsPage.css
│   │   │
│   │   ├── App.jsx                          ← Main app with routing
│   │   ├── App.css
│   │   └── main.jsx                         ← React entry point
│   │
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
└── README.md                                ← Project-level documentation
```

---

## 3. PHASE 1: ML PIPELINE

This phase creates the machine learning model. Follow steps 1 through 4 in order.

### 3.1 Setup

Create the file `ml-pipeline/requirements.txt`:

```
pandas
numpy
scikit-learn
xgboost
lightgbm
matplotlib
seaborn
joblib
imbalanced-learn
```

Run:
```bash
cd ml-pipeline
python3 -m venv venv
source venv/bin/activate    # On Mac/Linux
pip install -r requirements.txt
```

### 3.2 Download the Dataset

Download these two files from the UNSW-NB15 official source and place them in `ml-pipeline/data/`:
- `UNSW_NB15_training-set.csv`
- `UNSW_NB15_testing-set.csv`

If the official source is unavailable, search Kaggle for "UNSW-NB15" — the same files are mirrored there for free.

### 3.3 Step 1: preprocess.py

**File:** `ml-pipeline/scripts/preprocess.py`

**What this script does:**
1. Loads the training and testing CSV files.
2. Removes the `id` column (it is just a row number, not useful).
3. Cleans the `attack_cat` column — strips whitespace, replaces empty strings with "Normal".
4. Handles missing values — drops rows with NaN (there are very few).
5. Encodes categorical columns (`proto`, `service`, `state`) using LabelEncoder.
6. Separates features (X) from targets (y_binary for label, y_multi for attack_cat).
7. Applies StandardScaler to normalize all numerical features.
8. Saves the cleaned data, scaler, and label encoders to `saved_models/`.

**Important details for the code:**
- The categorical columns in UNSW-NB15 are: `proto`, `service`, `state`.
- The target columns are: `label` (binary 0/1) and `attack_cat` (string category name).
- When encoding `attack_cat`, use LabelEncoder and save the encoder so we can decode predictions later.
- Save outputs using joblib:
  - `saved_models/scaler.joblib` — the fitted StandardScaler
  - `saved_models/label_encoders.joblib` — dict of fitted LabelEncoders for each categorical column
  - `saved_models/attack_cat_encoder.joblib` — the LabelEncoder for attack_cat
- Save preprocessed arrays as:
  - `data/X_train_scaled.npy`, `data/X_test_scaled.npy`
  - `data/y_train.npy`, `data/y_test.npy` (binary labels)
  - `data/y_train_multi.npy`, `data/y_test_multi.npy` (multi-class labels)
  - `data/feature_names.joblib` — list of feature column names after encoding

**Also generate these EDA charts and save to `outputs/`:**
- `attack_distribution.png` — Bar chart showing count of each attack category in the training set. Use seaborn, with a dark background style. Title: "Distribution of Attack Categories in UNSW-NB15".
- `correlation_heatmap.png` — Heatmap of top 20 most correlated features. Use seaborn, with `coolwarm` colormap. Title: "Feature Correlation Heatmap".

### 3.4 Step 2: feature_selection.py

**File:** `ml-pipeline/scripts/feature_selection.py`

**What this script does:**
1. Loads the preprocessed training data (`X_train_scaled.npy`, `y_train.npy`, `feature_names.joblib`).
2. Trains a quick Random Forest model (100 trees) to calculate feature importances.
3. Ranks all features by importance.
4. Selects the top 20 most important features.
5. Saves the list of selected feature names to `saved_models/selected_features.joblib`.
6. Saves the reduced datasets: `data/X_train_selected.npy`, `data/X_test_selected.npy`.

**Also generate this chart:**
- `outputs/feature_importance.png` — Horizontal bar chart of top 20 features ranked by importance. Use matplotlib. Title: "Top 20 Most Important Features for Intrusion Detection".

### 3.5 Step 3: train_models.py

**File:** `ml-pipeline/scripts/train_models.py`

**What this script does:**
1. Loads the feature-selected training data (`X_train_selected.npy`, `y_train.npy`).
2. Trains these 5 models on the training data:

**Model 1: Decision Tree**
```python
from sklearn.tree import DecisionTreeClassifier
dt = DecisionTreeClassifier(max_depth=10, random_state=42)
```

**Model 2: Random Forest**
```python
from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier(n_estimators=200, max_depth=15, random_state=42, n_jobs=-1)
```

**Model 3: Support Vector Machine (SVM)**
```python
from sklearn.svm import SVC
svm = SVC(kernel='rbf', C=1.0, gamma='scale', probability=True, random_state=42)
```
> **IMPORTANT NOTE FOR SVM:** SVM is very slow on large datasets. To make it feasible, train it on a random sample of 20,000 rows from the training set, NOT the full dataset. Use `from sklearn.utils import resample` to sample.

**Model 4: XGBoost**
```python
from xgboost import XGBClassifier
xgb = XGBClassifier(
    n_estimators=200,
    max_depth=7,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    use_label_encoder=False,
    eval_metric='logloss',
    random_state=42,
    n_jobs=-1
)
```

**Model 5: LightGBM**
```python
from lightgbm import LGBMClassifier
lgbm = LGBMClassifier(
    n_estimators=200,
    max_depth=7,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    n_jobs=-1,
    verbose=-1
)
```

3. After training each model, evaluate it on the TEST set using:
   - `accuracy_score`
   - `precision_score` (weighted average)
   - `recall_score` (weighted average)
   - `f1_score` (weighted average)
   - `roc_auc_score` (use `predict_proba` with `multi_class='ovr'` for multi-class, or binary if using label)

4. Print all results to the console in a clean table format.

5. Save ALL trained models to `saved_models/`:
   - `decision_tree.joblib`
   - `random_forest.joblib`
   - `svm_model.joblib`
   - `xgboost_model.joblib`
   - `lightgbm_model.joblib`

6. Identify the best model (highest F1-score) and save it as `best_model.joblib`.

7. Save the results as a dictionary to `saved_models/model_results.joblib` for the evaluate script.

### 3.6 Step 4: evaluate_models.py

**File:** `ml-pipeline/scripts/evaluate_models.py`

**What this script does:**
1. Loads `saved_models/model_results.joblib` and all trained models.
2. Loads test data.
3. Generates these charts and saves them to `outputs/`:

**Chart 1: `model_comparison.png`**
- Grouped bar chart comparing all 5 models.
- X-axis: Model names.
- Groups: Accuracy, Precision, Recall, F1-Score.
- Use distinct colors for each metric.
- Title: "Performance Comparison of ML Models for NIDS"
- Include value labels on top of each bar.

**Chart 2: `confusion_matrix.png`**
- Confusion matrix heatmap for the BEST model only.
- Use `sklearn.metrics.confusion_matrix` and `seaborn.heatmap`.
- Show actual numbers inside each cell.
- Title: "Confusion Matrix — [Best Model Name]"

**Chart 3: `roc_curves.png`**
- ROC curves for all 5 models on the same plot.
- Use different colors for each model.
- Include AUC value in the legend for each model.
- Include the diagonal baseline (random classifier).
- Title: "ROC Curves — Model Comparison"

**Chart 4: `classification_report.txt`**
- Save the full `classification_report` text output from scikit-learn for the best model.

---

## 4. PHASE 2: FASTAPI BACKEND

### 4.1 Setup

Create `backend/requirements.txt`:

```
fastapi
uvicorn[standard]
python-multipart
pandas
numpy
scikit-learn
xgboost
lightgbm
joblib
pydantic
```

Run:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4.2 Copy Saved Models

Copy these files from `ml-pipeline/saved_models/` into `backend/models/`:
- `best_model.joblib`
- `scaler.joblib`
- `label_encoders.joblib`
- `selected_features.joblib`
- `attack_cat_encoder.joblib`

### 4.3 File: backend/app/config.py

```python
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")
```

### 4.4 File: backend/app/utils/preprocessing.py

**What this file does:**
- Contains a function `preprocess_input(df)` that takes a raw DataFrame (from an uploaded CSV).
- Applies the EXACT same preprocessing steps as the training pipeline:
  1. Drop the `id` column if it exists.
  2. Drop `label` and `attack_cat` columns if they exist (these are targets, not inputs).
  3. Encode categorical columns (`proto`, `service`, `state`) using the saved LabelEncoders. If a category was not seen during training, map it to a default value (0).
  4. Select only the features listed in `selected_features.joblib`.
  5. Apply the saved `StandardScaler`.
- Returns the preprocessed numpy array ready for prediction.

### 4.5 File: backend/app/services/ml_service.py

**What this file does:**
- Loads all saved model artifacts when the module is imported (on app startup):
  - `best_model.joblib` → the trained model
  - `scaler.joblib` → the StandardScaler
  - `label_encoders.joblib` → dict of LabelEncoders for categorical cols
  - `selected_features.joblib` → list of selected feature names
  - `attack_cat_encoder.joblib` → LabelEncoder for decoding attack_cat predictions
- Provides a function `predict(df)` that:
  1. Calls `preprocess_input(df)` to clean the data.
  2. Runs `model.predict(preprocessed_data)` to get binary predictions (0 or 1).
  3. Runs `model.predict_proba(preprocessed_data)` to get confidence scores.
  4. Returns a dictionary with:
     - `predictions`: list of "Normal" or "Attack" for each row
     - `confidence`: list of confidence percentages
     - `attack_types`: list of predicted attack category names (decoded using attack_cat_encoder)
     - `summary`: dict with total_packets, normal_count, attack_count, attack_breakdown (count per attack type)

**IMPORTANT:** If the best model was trained on binary labels (label column), then for multi-class predictions, load a separate multi-class model OR use the binary predictions. The simplest approach: train the best model on binary labels for the main prediction, and optionally train a second multi-class model for attack type classification. For simplicity, train the best algorithm (e.g., XGBoost) on BOTH binary and multi-class targets and save both:
- `best_model_binary.joblib` → predicts Normal (0) vs Attack (1)
- `best_model_multi.joblib` → predicts the specific attack type

The predict function should:
1. Use the binary model to predict Normal vs Attack.
2. For rows predicted as Attack, use the multi-class model to predict the specific attack type.
3. For rows predicted as Normal, set attack_type to "Normal".

### 4.6 File: backend/app/routes/predict.py

**Endpoints to create:**

**Endpoint 1: POST /api/predict**
- Accepts: A CSV file upload (multipart/form-data).
- Process:
  1. Read the uploaded file into a Pandas DataFrame.
  2. Validate that it has the expected columns (or at least most of them).
  3. Call `ml_service.predict(df)`.
  4. Return the results as JSON.
- Response format:
```json
{
  "success": true,
  "total_packets": 1000,
  "normal_count": 750,
  "attack_count": 250,
  "attack_percentage": 25.0,
  "attack_breakdown": {
    "DoS": 80,
    "Exploits": 60,
    "Fuzzers": 45,
    "Generic": 30,
    "Reconnaissance": 20,
    "Backdoors": 10,
    "Shellcode": 3,
    "Worms": 2
  },
  "predictions": [
    {"row": 0, "prediction": "Normal", "confidence": 0.95},
    {"row": 1, "prediction": "Attack", "attack_type": "DoS", "confidence": 0.88},
    ...
  ]
}
```
- If there is an error (bad file, wrong format), return:
```json
{
  "success": false,
  "error": "Description of what went wrong"
}
```

**Endpoint 2: GET /api/model-info**
- Returns metadata about the loaded model:
```json
{
  "model_type": "XGBoost",
  "features_used": 20,
  "feature_names": ["sttl", "ct_state_ttl", ...],
  "training_accuracy": 0.986,
  "dataset": "UNSW-NB15"
}
```

**Endpoint 3: GET /api/health**
- Simple health check. Returns:
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

### 4.7 File: backend/app/main.py

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import predict

app = FastAPI(
    title="NIDS Prediction API",
    description="Network Intrusion Detection System powered by Machine Learning",
    version="1.0.0"
)

# CORS — allow React dev server to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "NIDS API is running"}
```

### 4.8 Running the Backend

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.
API docs will be at `http://localhost:8000/docs`.

---

## 5. PHASE 3: REACT FRONTEND

### 5.1 Setup

```bash
cd nids-project
npx -y create-vite@latest frontend -- --template react
cd frontend
npm install
npm install axios recharts react-router-dom react-icons react-dropzone
```

### 5.2 vite.config.js

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
```

This proxy configuration means: any request from the React app to `/api/*` will be automatically forwarded to the FastAPI backend at port 8000. This avoids CORS issues during development.

### 5.3 File: src/services/api.js

**What this file does:**
- Exports functions that call the FastAPI backend using axios.
- Functions:
  1. `uploadFile(file)` — sends a POST request to `/api/predict` with the CSV file as FormData. Returns the response data.
  2. `getModelInfo()` — sends a GET request to `/api/model-info`. Returns model metadata.
  3. `checkHealth()` — sends a GET request to `/api/health`. Returns health status.

### 5.4 File: src/App.jsx

**What this file does:**
- Sets up React Router with two routes:
  - `/` → HomePage (landing page with file upload)
  - `/results` → ResultsPage (dashboard showing results)
- Uses `useState` to hold the prediction results data.
- Passes results data and a setter function as props or via context.
- Includes the Navbar component on every page.

### 5.5 File: src/pages/HomePage.jsx

**What this page looks like:**
- A clean, centered landing page.
- Large heading: "Network Intrusion Detection System"
- Subtitle: "Upload network traffic data to detect cyber threats using Machine Learning"
- The FileUpload component centered on the page.
- Below the upload area: 3 small info cards showing:
  - "5 ML Models Compared"
  - "98%+ Detection Accuracy"
  - "Real-time Analysis"

**Behavior:**
- When a file is successfully uploaded and results are received, navigate to `/results` with the data.

### 5.6 File: src/pages/ResultsPage.jsx

**What this page looks like:**
- A dashboard layout with multiple sections.
- Top: StatsCards row (4 cards side by side).
- Middle: Two charts side by side (PieChart on left, BarChart on right).
- Bottom: PredictionsTable (full width).
- A "Upload New File" button to go back to HomePage.

### 5.7 File: src/components/Navbar.jsx

- Fixed at the top of every page.
- Left side: Shield icon + "NIDS" text.
- Right side: Navigation links (Home, About).
- Background: dark navy blue (see Styling Guide).

### 5.8 File: src/components/FileUpload.jsx

**What this component does:**
- Uses `react-dropzone` to create a drag-and-drop zone.
- Accepts only `.csv` files.
- Shows a dashed border box with an upload icon and text "Drag & drop a CSV file here, or click to browse".
- When a file is dropped:
  1. Shows the filename and file size.
  2. Shows an "Analyze" button.
  3. When "Analyze" is clicked, shows a loading spinner.
  4. Calls `api.uploadFile(file)`.
  5. On success, navigates to ResultsPage with the results.
  6. On error, shows an error message in red.

### 5.9 File: src/components/StatsCards.jsx

**What this component does:**
- Receives `results` data as props.
- Displays 4 cards in a row:
  1. **Total Packets** — shows `total_packets` with a blue network icon.
  2. **Normal Traffic** — shows `normal_count` with a green checkmark icon.
  3. **Attacks Detected** — shows `attack_count` with a red warning icon.
  4. **Attack Rate** — shows `attack_percentage` with an orange percentage icon.
- Each card has an icon, a large number, and a label below.

### 5.10 File: src/components/AttackPieChart.jsx

**What this component does:**
- Receives `normal_count` and `attack_count` as props.
- Renders a Recharts PieChart showing the proportion of Normal vs Attack traffic.
- Colors: Green for Normal, Red for Attack.
- Shows percentage labels on each slice.
- Includes a legend at the bottom.

### 5.11 File: src/components/AttackBarChart.jsx

**What this component does:**
- Receives `attack_breakdown` object as props (e.g., `{"DoS": 80, "Exploits": 60, ...}`).
- Renders a Recharts BarChart showing the count of each attack type.
- Each bar has a distinct color.
- X-axis: Attack type names.
- Y-axis: Count.
- Include value labels on top of each bar.

### 5.12 File: src/components/PredictionsTable.jsx

**What this component does:**
- Receives `predictions` array as props.
- Renders a scrollable, paginated table.
- Columns: Row #, Prediction, Attack Type, Confidence.
- "Normal" rows have a green background tint.
- "Attack" rows have a red/orange background tint.
- Show 25 rows per page with Previous/Next pagination buttons.
- Show a search/filter box to filter by prediction type.

### 5.13 File: src/components/LoadingSpinner.jsx

- A simple CSS-animated spinning circle.
- Displays centered on screen with text "Analyzing traffic..." below it.

---

## 6. PHASE 4: INTEGRATION AND TESTING

### 6.1 Start Both Servers

**Terminal 1 (Backend):**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

### 6.2 Test the Full Flow

1. Open `http://localhost:3000` in a browser.
2. Upload the `UNSW_NB15_testing-set.csv` file (or a portion of it).
3. Verify:
   - The loading spinner appears while processing.
   - The results page loads with correct statistics.
   - The pie chart shows Normal vs Attack.
   - The bar chart shows attack type breakdown.
   - The table shows individual predictions.
   - All numbers are consistent (totals match, percentages are correct).

### 6.3 Edge Case Testing

Test these scenarios:
- Upload an empty CSV → should show an error message.
- Upload a non-CSV file (e.g., .txt, .jpg) → should reject the file before upload.
- Upload a CSV with wrong columns → should show a meaningful error.
- Upload a very large file (100K+ rows) → should still work (may take a few seconds).

---

## 7. STYLING GUIDE

This section defines EVERY visual decision. Follow these rules exactly.

### 7.1 Color Palette

```css
:root {
  /* Primary Colors */
  --color-primary: #0a1628;          /* Very dark navy — main background */
  --color-primary-light: #111d35;    /* Slightly lighter navy — card backgrounds */
  --color-primary-lighter: #1a2744;  /* Lighter navy — hover states, borders */

  /* Accent Colors */
  --color-accent: #3b82f6;          /* Bright blue — buttons, links, highlights */
  --color-accent-hover: #2563eb;    /* Darker blue — button hover */
  --color-accent-glow: rgba(59, 130, 246, 0.15);  /* Blue glow for cards */

  /* Status Colors */
  --color-success: #22c55e;         /* Green — normal traffic, safe */
  --color-danger: #ef4444;          /* Red — attacks, threats */
  --color-warning: #f59e0b;         /* Amber — warnings, percentages */
  --color-info: #06b6d4;            /* Cyan — informational */

  /* Text Colors */
  --color-text-primary: #f1f5f9;    /* Almost white — main text */
  --color-text-secondary: #94a3b8;  /* Light gray — secondary text */
  --color-text-muted: #64748b;      /* Medium gray — muted text */

  /* Borders and Surfaces */
  --color-border: #1e293b;          /* Subtle border */
  --color-surface: #0f172a;         /* Cards and surfaces */
  --color-glass: rgba(15, 23, 42, 0.8);  /* Glassmorphism background */

  /* Chart Colors — use these for the bar chart and pie chart */
  --chart-1: #3b82f6;  /* Blue */
  --chart-2: #22c55e;  /* Green */
  --chart-3: #ef4444;  /* Red */
  --chart-4: #f59e0b;  /* Amber */
  --chart-5: #8b5cf6;  /* Purple */
  --chart-6: #06b6d4;  /* Cyan */
  --chart-7: #ec4899;  /* Pink */
  --chart-8: #f97316;  /* Orange */
  --chart-9: #14b8a6;  /* Teal */
}
```

### 7.2 Typography

```css
/* Import Google Font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  font-size: 16px;
  color: var(--color-text-primary);
  background-color: var(--color-primary);
}

/* Font sizes */
h1 { font-size: 2.5rem; font-weight: 800; }
h2 { font-size: 1.75rem; font-weight: 700; }
h3 { font-size: 1.25rem; font-weight: 600; }
body { font-size: 1rem; font-weight: 400; }
.small { font-size: 0.875rem; }
.tiny { font-size: 0.75rem; }
```

### 7.3 Card Style (Used for Stats Cards, Charts, Tables)

```css
.card {
  background: var(--color-primary-light);
  border: 1px solid var(--color-border);
  border-radius: 16px;
  padding: 24px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.2);
}

.card:hover {
  border-color: var(--color-accent);
  box-shadow: 0 4px 32px var(--color-accent-glow);
  transform: translateY(-2px);
}
```

### 7.4 Button Style

```css
.btn-primary {
  background: var(--color-accent);
  color: white;
  font-weight: 600;
  font-size: 1rem;
  padding: 12px 32px;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3);
}

.btn-primary:hover {
  background: var(--color-accent-hover);
  transform: translateY(-2px);
  box-shadow: 0 6px 24px rgba(59, 130, 246, 0.4);
}
```

### 7.5 Navbar Style

```css
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 64px;
  background: var(--color-glass);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--color-border);
  z-index: 1000;
  display: flex;
  align-items: center;
  padding: 0 32px;
}
```

### 7.6 File Upload Zone Style

```css
.upload-zone {
  border: 2px dashed var(--color-accent);
  border-radius: 20px;
  padding: 60px 40px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background: var(--color-primary-light);
}

.upload-zone:hover {
  border-color: var(--color-accent-hover);
  background: var(--color-accent-glow);
}

/* When a file is dragged over */
.upload-zone.active {
  border-color: var(--color-success);
  background: rgba(34, 197, 94, 0.08);
}
```

### 7.7 Stats Cards Layout

```css
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 32px;
}

/* Make responsive: 2 columns on small screens */
@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
```

### 7.8 Table Style

```css
.predictions-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  font-size: 0.875rem;
}

.predictions-table th {
  background: var(--color-primary-lighter);
  color: var(--color-text-secondary);
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.75rem;
  letter-spacing: 0.05em;
  padding: 12px 16px;
  text-align: left;
  position: sticky;
  top: 0;
}

.predictions-table td {
  padding: 10px 16px;
  border-bottom: 1px solid var(--color-border);
}

.predictions-table tr:hover td {
  background: var(--color-primary-lighter);
}

/* Row coloring based on prediction */
.row-normal { background: rgba(34, 197, 94, 0.05); }
.row-attack { background: rgba(239, 68, 68, 0.05); }
```

### 7.9 Animations

```css
/* Fade in animation for page transitions */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.page-enter {
  animation: fadeIn 0.5s ease forwards;
}

/* Pulse animation for loading */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.loading { animation: pulse 1.5s infinite; }

/* Spin animation for spinner */
@keyframes spin {
  to { transform: rotate(360deg); }
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid var(--color-border);
  border-top: 4px solid var(--color-accent);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}
```

### 7.10 Overall Design Rules

1. **DARK THEME ONLY.** The entire app uses a dark background. No light theme.
2. **NO sharp corners.** All cards, buttons, and inputs use `border-radius: 12px` or more.
3. **Glassmorphism** on the navbar: use `backdrop-filter: blur(12px)` with a semi-transparent background.
4. **Subtle shadows** everywhere: use `box-shadow` with very dark, diffused shadows.
5. **Hover effects** on ALL interactive elements: buttons, cards, table rows. Use `transform: translateY(-2px)` and a subtle shadow increase.
6. **Status colors are critical:** Green = safe/normal. Red = danger/attack. Amber = warning. Blue = informational/accent.
7. **Spacing:** Use consistent padding of 24px inside cards and 20px gap between grid items.
8. **The app should feel like a cybersecurity command center** — professional, dark, and clean.

---

## 8. HOW TO RUN THE PROJECT

### Prerequisites

1. Python 3.10 or higher installed.
2. Node.js 18 or higher installed.
3. npm installed (comes with Node.js).

### Step-by-Step

```bash
# ===== STEP 1: ML PIPELINE =====
cd nids-project/ml-pipeline

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download dataset files into data/ folder first, then:
python scripts/preprocess.py
python scripts/feature_selection.py
python scripts/train_models.py
python scripts/evaluate_models.py

# Deactivate when done
deactivate


# ===== STEP 2: COPY MODELS =====
cp saved_models/*.joblib ../backend/models/


# ===== STEP 3: BACKEND =====
cd ../backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the API server
uvicorn app.main:app --reload --port 8000

# Keep this terminal running!


# ===== STEP 4: FRONTEND =====
# Open a NEW terminal
cd nids-project/frontend

# Install dependencies
npm install

# Start the dev server
npm run dev

# Keep this terminal running!


# ===== STEP 5: USE THE APP =====
# Open http://localhost:3000 in your browser
# Upload UNSW_NB15_testing-set.csv to test
```

---

## FINAL CHECKLIST

Before considering the product complete, verify ALL of the following:

- [ ] ML pipeline runs without errors and generates all 5 trained models.
- [ ] At least one model achieves 95%+ accuracy on the test set.
- [ ] All 6 charts/outputs are generated in `ml-pipeline/outputs/`.
- [ ] FastAPI backend starts without errors on port 8000.
- [ ] `/api/health` returns `{"status": "healthy", "model_loaded": true}`.
- [ ] `/api/predict` accepts a CSV and returns correct JSON predictions.
- [ ] `/api/model-info` returns model metadata.
- [ ] React frontend starts without errors on port 3000.
- [ ] Homepage shows with the file upload zone.
- [ ] Uploading a CSV file shows a loading spinner, then navigates to results.
- [ ] Results page shows 4 stats cards with correct numbers.
- [ ] Pie chart renders Normal vs Attack correctly.
- [ ] Bar chart renders attack type breakdown correctly.
- [ ] Predictions table renders with correct color coding (green/red rows).
- [ ] Pagination works on the table.
- [ ] "Upload New File" button navigates back to HomePage.
- [ ] The app looks premium, dark, and professional — NOT basic or plain.
- [ ] No console errors in the browser or terminal.

---

> **END OF BUILD INSTRUCTIONS**
