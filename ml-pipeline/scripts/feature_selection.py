import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
import joblib

def main():
    print("=== STEP 2: FEATURE SELECTION ===")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)
    data_dir = os.path.join(base_dir, "data")
    saved_models_dir = os.path.join(base_dir, "saved_models")
    outputs_dir = os.path.join(base_dir, "outputs")
    
    print("Loading scaled data...")
    X_train_scaled = np.load(os.path.join(data_dir, "X_train_scaled.npy"))
    X_test_scaled = np.load(os.path.join(data_dir, "X_test_scaled.npy"))
    y_train = np.load(os.path.join(data_dir, "y_train.npy"))
    feature_names = joblib.load(os.path.join(data_dir, "feature_names.joblib"))
    
    print(f"X_train_scaled shape: {X_train_scaled.shape}")
    
    print("Training RandomForestClassifier for feature importance ranking...")
    rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    rf.fit(X_train_scaled, y_train)
    
    importances = rf.feature_importances_
    indices = np.argsort(importances)[::-1]
    
    top_n = 20
    top_indices = indices[:top_n]
    selected_features = [feature_names[i] for i in top_indices]
    
    print(f"Selected top {top_n} features:")
    for rank, idx in enumerate(top_indices, 1):
        print(f"  {rank}. {feature_names[idx]} ({importances[idx]:.4f})")
        
    # Save selected feature names
    joblib.dump(selected_features, os.path.join(saved_models_dir, "selected_features.joblib"))
    joblib.dump(selected_features, os.path.join(data_dir, "selected_features.joblib"))
    
    # Save reduced datasets
    X_train_selected = X_train_scaled[:, top_indices]
    X_test_selected = X_test_scaled[:, top_indices]
    
    np.save(os.path.join(data_dir, "X_train_selected.npy"), X_train_selected)
    np.save(os.path.join(data_dir, "X_test_selected.npy"), X_test_selected)
    
    # Generate Feature Importance Chart
    print("Generating feature_importance.png...")
    plt.style.use('dark_background')
    plt.figure(figsize=(10, 8))
    
    top_importances = importances[top_indices][::-1]
    top_feature_names_rev = [feature_names[i] for i in top_indices][::-1]
    
    plt.barh(range(top_n), top_importances, color='#3b82f6')
    plt.yticks(range(top_n), top_feature_names_rev, fontsize=10)
    plt.xlabel("Feature Importance Score", fontsize=12)
    plt.title("Top 20 Most Important Features for Intrusion Detection", fontsize=14, pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(outputs_dir, "feature_importance.png"), dpi=300)
    plt.close()
    
    print("Feature selection completed successfully!")

if __name__ == "__main__":
    main()
