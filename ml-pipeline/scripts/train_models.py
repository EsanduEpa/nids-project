import os
import time
import numpy as np
import pandas as pd
import joblib
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.utils import resample

def main():
    print("=== STEP 3: TRAIN ML MODELS ===")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)
    data_dir = os.path.join(base_dir, "data")
    saved_models_dir = os.path.join(base_dir, "saved_models")
    
    print("Loading feature-selected dataset...")
    X_train = np.load(os.path.join(data_dir, "X_train_selected.npy"))
    X_test = np.load(os.path.join(data_dir, "X_test_selected.npy"))
    y_train = np.load(os.path.join(data_dir, "y_train.npy"))
    y_test = np.load(os.path.join(data_dir, "y_test.npy"))
    y_train_multi = np.load(os.path.join(data_dir, "y_train_multi.npy"))
    y_test_multi = np.load(os.path.join(data_dir, "y_test_multi.npy"))
    
    models = {
        "Decision Tree": DecisionTreeClassifier(max_depth=10, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=200, max_depth=15, random_state=42, n_jobs=-1),
        "SVM": SVC(kernel='rbf', C=1.0, gamma='scale', probability=True, random_state=42),
        "XGBoost": XGBClassifier(
            n_estimators=200,
            max_depth=7,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            eval_metric='logloss',
            random_state=42,
            n_jobs=-1
        ),
        "LightGBM": LGBMClassifier(
            n_estimators=200,
            max_depth=7,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            n_jobs=-1,
            verbose=-1
        )
    }
    
    model_filename_map = {
        "Decision Tree": "decision_tree.joblib",
        "Random Forest": "random_forest.joblib",
        "SVM": "svm_model.joblib",
        "XGBoost": "xgboost_model.joblib",
        "LightGBM": "lightgbm_model.joblib"
    }
    
    results = {}
    best_model_name = None
    best_f1 = -1.0
    best_model_obj = None
    
    for name, model in models.items():
        print(f"\n--- Training {name} ---")
        start_time = time.time()
        
        if name == "SVM":
            print("Sampling 20,000 training rows for SVM to avoid long execution time...")
            X_train_sub, y_train_sub = resample(X_train, y_train, n_samples=20000, random_state=42, stratify=y_train)
            model.fit(X_train_sub, y_train_sub)
        else:
            model.fit(X_train, y_train)
            
        train_duration = time.time() - start_time
        print(f"Training took {train_duration:.2f} seconds.")
        
        y_pred = model.predict(X_test)
        if hasattr(model, "predict_proba"):
            y_proba = model.predict_proba(X_test)[:, 1]
        else:
            y_proba = y_pred
            
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average='weighted')
        rec = recall_score(y_test, y_pred, average='weighted')
        f1 = f1_score(y_test, y_pred, average='weighted')
        auc = roc_auc_score(y_test, y_proba)
        
        results[name] = {
            'accuracy': acc,
            'precision': prec,
            'recall': rec,
            'f1': f1,
            'roc_auc': auc,
            'y_pred': y_pred,
            'y_proba': y_proba
        }
        
        # Save model file
        model_path = os.path.join(saved_models_dir, model_filename_map[name])
        joblib.dump(model, model_path)
        print(f"Saved {name} to {model_filename_map[name]}")
        
        if f1 > best_f1:
            best_f1 = f1
            best_model_name = name
            best_model_obj = model
            
    # Display results table
    print("\n" + "="*70)
    print(f"{'Model':<15} | {'Accuracy':<10} | {'Precision':<10} | {'Recall':<10} | {'F1-Score':<10} | {'AUC':<10}")
    print("="*70)
    for name, m in results.items():
        print(f"{name:<15} | {m['accuracy']:<10.4f} | {m['precision']:<10.4f} | {m['recall']:<10.4f} | {m['f1']:<10.4f} | {m['roc_auc']:<10.4f}")
    print("="*70)
    
    print(f"\nBest Model: {best_model_name} (F1-Score: {best_f1:.4f})")
    
    # Save best binary model
    joblib.dump(best_model_obj, os.path.join(saved_models_dir, "best_model.joblib"))
    joblib.dump(best_model_obj, os.path.join(saved_models_dir, "best_model_binary.joblib"))
    
    # Train multi-class model using XGBoost or best algorithm on attack_cat target
    print(f"\nTraining multi-class XGBoost model for attack category prediction...")
    xgb_multi = XGBClassifier(
        n_estimators=200,
        max_depth=7,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        eval_metric='mlogloss',
        random_state=42,
        n_jobs=-1
    )
    xgb_multi.fit(X_train, y_train_multi)
    joblib.dump(xgb_multi, os.path.join(saved_models_dir, "best_model_multi.joblib"))
    print("Saved multi-class model to best_model_multi.joblib")
    
    # Save model results summary dictionary
    results_summary = {
        'best_model_name': best_model_name,
        'metrics': {k: {m: v[m] for m in ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']} for k, v in results.items()},
        'probas': {k: v['y_proba'] for k, v in results.items()},
        'preds': {k: v['y_pred'] for k, v in results.items()}
    }
    joblib.dump(results_summary, os.path.join(saved_models_dir, "model_results.joblib"))
    
    print("Model training completed successfully!")

if __name__ == "__main__":
    main()
