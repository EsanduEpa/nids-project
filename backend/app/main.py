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
