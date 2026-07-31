import os
import joblib
import pandas as pd
import numpy as np
from app.config import MODELS_DIR
from app.utils.preprocessing import preprocess_input

class MLService:
    def __init__(self):
        print("Loading ML model artifacts into memory...")
        
        binary_model_path = os.path.join(MODELS_DIR, "best_model_binary.joblib")
        if not os.path.exists(binary_model_path):
            binary_model_path = os.path.join(MODELS_DIR, "best_model.joblib")
            
        multi_model_path = os.path.join(MODELS_DIR, "best_model_multi.joblib")
        scaler_path = os.path.join(MODELS_DIR, "scaler.joblib")
        label_encoders_path = os.path.join(MODELS_DIR, "label_encoders.joblib")
        feature_names_path = os.path.join(MODELS_DIR, "feature_names.joblib")
        selected_features_path = os.path.join(MODELS_DIR, "selected_features.joblib")
        attack_cat_encoder_path = os.path.join(MODELS_DIR, "attack_cat_encoder.joblib")
        
        self.binary_model = joblib.load(binary_model_path)
        self.multi_model = joblib.load(multi_model_path) if os.path.exists(multi_model_path) else None
        self.scaler = joblib.load(scaler_path)
        self.label_encoders = joblib.load(label_encoders_path)
        self.feature_names = joblib.load(feature_names_path)
        self.selected_features = joblib.load(selected_features_path)
        self.attack_cat_encoder = joblib.load(attack_cat_encoder_path)
        
        print("All ML artifacts successfully loaded!")

    def predict(self, df: pd.DataFrame) -> dict:
        total_packets = len(df)
        if total_packets == 0:
            return {
                "success": False,
                "error": "Uploaded CSV file contains no data rows."
            }
            
        # 1. Preprocess input DataFrame
        X_scaled = preprocess_input(
            df=df,
            scaler=self.scaler,
            label_encoders=self.label_encoders,
            feature_names=self.feature_names,
            selected_features=self.selected_features
        )
        
        # 2. Binary prediction (0 = Normal, 1 = Attack)
        binary_preds = self.binary_model.predict(X_scaled)
        
        if hasattr(self.binary_model, "predict_proba"):
            probs = self.binary_model.predict_proba(X_scaled)
            confidences = np.max(probs, axis=1)
        else:
            confidences = np.ones(total_packets)
            
        # 3. Multi-class prediction for attack types
        if self.multi_model is not None:
            multi_preds_encoded = self.multi_model.predict(X_scaled)
            multi_preds_decoded = self.attack_cat_encoder.inverse_transform(multi_preds_encoded)
        else:
            multi_preds_decoded = np.full(total_packets, "Attack")
            
        predictions = []
        normal_count = 0
        attack_count = 0
        attack_breakdown = {}
        
        for i in range(total_packets):
            is_attack = int(binary_preds[i]) == 1
            pred_label = "Attack" if is_attack else "Normal"
            
            if is_attack:
                attack_count += 1
                attack_type = str(multi_preds_decoded[i])
                if attack_type == "Normal":
                    attack_type = "Generic Attack"
                attack_breakdown[attack_type] = attack_breakdown.get(attack_type, 0) + 1
            else:
                normal_count += 1
                attack_type = "Normal"
                
            predictions.append({
                "row": i,
                "prediction": pred_label,
                "attack_type": attack_type,
                "confidence": round(float(confidences[i]), 4)
            })
            
        attack_percentage = round((attack_count / total_packets) * 100, 2) if total_packets > 0 else 0.0
        
        return {
            "success": True,
            "total_packets": total_packets,
            "normal_count": normal_count,
            "attack_count": attack_count,
            "attack_percentage": attack_percentage,
            "attack_breakdown": attack_breakdown,
            "predictions": predictions
        }

# Singleton instance
ml_service = MLService()
