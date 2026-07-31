# Optimized Network Intrusion Detection System (NIDS)

An AI-powered Network Intrusion Detection System built with **Python**, **FastAPI**, **XGBoost Machine Learning**, and **React + Vite**.

![NIDS Architecture](https://img.shields.io/badge/Architecture-FastAPI%20%2B%20React%20%2B%20XGBoost-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Dataset](https://img.shields.io/badge/Dataset-UNSW--NB15-orange)

---

## 📌 Project Overview

This project detects and classifies cyber threats in network traffic using machine learning. Users can upload raw network packet CSV logs via a modern web interface, which are processed by a trained XGBoost dual-stage prediction engine to classify normal traffic vs. attack traffic and identify specific threat categories in real time.

---

## ⚡ Features

- **Dual-Stage Machine Learning Engine**: 
  - **Binary Classification**: Detects Normal traffic vs. Attack intrusions with **0.9860 AUC**.
  - **Multi-Class Categorization**: Identifies 9 distinct attack categories (**DoS**, **Exploits**, **Fuzzers**, **Reconnaissance**, **Backdoor**, **Shellcode**, **Worms**, **Analysis**, **Generic**).
- **High Performance ML Pipeline**: Feature selection narrowed 42 network features down to the top 20 most impactful features.
- **RESTful API**: Fast and robust asynchronous API endpoints using FastAPI and Uvicorn.
- **Modern Dashboard UI**: Built with React, Vite, Recharts, and Glassmorphism styling.
- **Interactive Analytics**: Interactive pie charts, category bar charts, metric summary cards, and paginated logs with confidence meters.

---

## 📊 Machine Learning Model Benchmarks

5 classification algorithms were benchmarked on the official **UNSW-NB15** testing dataset (175,341 rows):

| Model | Accuracy | Precision | Recall | F1-Score | AUC | Selected |
|---|---|---|---|---|---|---|
| **Decision Tree** | 88.11% | 90.75% | 88.11% | 0.8846 | 0.9750 | |
| **Random Forest** | 89.59% | 91.71% | 89.59% | 0.8987 | 0.9859 | |
| **SVM (resampled)** | 87.30% | 89.82% | 87.30% | 0.8766 | 0.9577 | |
| **XGBoost** | **89.80%** | **91.80%** | **89.80%** | **0.9007** | **0.9860** | **🏆 Best Model** |
| **LightGBM** | 89.78% | 91.78% | 89.78% | 0.9005 | 0.9852 | |

---

## 📁 Repository Structure

```
nids-project/
│
├── ml-pipeline/                 ← Phase 1: Data Preprocessing & Model Training
│   ├── data/                    ← UNSW-NB15 Datasets (ignored in Git)
│   ├── scripts/
│   │   ├── preprocess.py        ← Cleaning, encoding, scaling & EDA charts
│   │   ├── feature_selection.py ← Top 20 feature selection
│   │   ├── train_models.py      ← Benchmark 5 ML models & save XGBoost
│   │   └── evaluate_models.py   ← Generates ROC curves, confusion matrix, reports
│   ├── saved_models/            ← Saved .joblib model binaries
│   └── outputs/                 ← Generated charts & evaluation metrics
│
├── backend/                     ← Phase 2: FastAPI REST Service
│   ├── app/
│   │   ├── main.py              ← FastAPI entrypoint & CORS middleware
│   │   ├── config.py            ← Environment paths
│   │   ├── routes/predict.py    ← API endpoints (/predict, /model-info, /health)
│   │   ├── services/ml_service.py ← Model loading & inference engine
│   │   └── utils/preprocessing.py ← Input stream cleaner & scaler
│   └── models/                  ← Production model binaries
│
├── frontend/                    ← Phase 3: React + Vite Web UI
│   ├── src/
│   │   ├── components/          ← Navbar, FileUpload, StatsCards, Charts, Table
│   │   ├── pages/               ← HomePage, ResultsPage
│   │   ├── services/api.js      ← Axios API client
│   │   └── styles/              ← Global CSS design system & component styles
│   ├── index.html
│   └── vite.config.js           ← Port 3000 & API proxy
│
└── README.md
```

---

## 🚀 How to Run the Project

### Prerequisites

- **Python 3.10+**
- **Node.js 18+** & **npm**

---

### Step 1: Start the FastAPI Backend Server

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate    # On Mac/Linux

# Install requirements
pip install -r requirements.txt

# Start Uvicorn server on port 8000
uvicorn app.main:app --reload --port 8000
```

- API Base URL: `http://localhost:8000`
- Interactive API Documentation (Swagger UI): `http://localhost:8000/docs`

---

### Step 2: Start the React Frontend Application

Open a second terminal window:

```bash
# Navigate to frontend directory
cd frontend

# Install npm dependencies
npm install

# Start Vite development server
npm run dev
```

- Web Interface: `http://localhost:3000` (or Vite assigned port)

---

## 🔌 API Endpoints Summary

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | API Root Health Check |
| `GET` | `/api/health` | Returns backend service status and model loading state |
| `GET` | `/api/model-info` | Returns model metadata, training accuracy, and top 20 features |
| `POST` | `/api/predict` | Uploads network CSV dataset and returns full intrusion analytics |

---

## 🧪 Testing full prediction flow

1. Open `http://localhost:3000` in your web browser.
2. Drag and drop or browse for `UNSW_NB15_testing-set.csv` (or any sample network CSV log).
3. Click **Analyze Traffic**.
4. View real-time threat rates, traffic proportions, attack breakdowns, and individual packet predictions!
