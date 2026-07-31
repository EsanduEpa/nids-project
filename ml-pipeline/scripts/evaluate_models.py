import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, auc

def main():
    print("=== STEP 4: EVALUATE MODELS & GENERATE CHARTS ===")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)
    data_dir = os.path.join(base_dir, "data")
    saved_models_dir = os.path.join(base_dir, "saved_models")
    outputs_dir = os.path.join(base_dir, "outputs")
    
    results = joblib.load(os.path.join(saved_models_dir, "model_results.joblib"))
    y_test = np.load(os.path.join(data_dir, "y_test.npy"))
    
    best_model_name = results['best_model_name']
    metrics_data = results['metrics']
    probas_data = results['probas']
    preds_data = results['preds']
    
    plt.style.use('dark_background')
    
    # -------------------------------------------------------------
    # Chart 1: model_comparison.png (Grouped Bar Chart)
    # -------------------------------------------------------------
    print("Generating model_comparison.png...")
    models = list(metrics_data.keys())
    metrics_list = ['accuracy', 'precision', 'recall', 'f1']
    metric_labels = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
    
    x = np.arange(len(models))
    width = 0.18
    
    fig, ax = plt.subplots(figsize=(14, 7))
    colors = ['#3b82f6', '#22c55e', '#f59e0b', '#ef4444']
    
    for i, metric in enumerate(metrics_list):
        values = [metrics_data[m][metric] for m in models]
        rects = ax.bar(x + (i - 1.5) * width, values, width, label=metric_labels[i], color=colors[i])
        # Add value labels
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.3f}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8, rotation=90)
            
    ax.set_ylabel('Score', fontsize=12)
    ax.set_title('Performance Comparison of ML Models for NIDS', fontsize=14, pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(models, fontsize=11)
    ax.set_ylim(0.7, 1.05)
    ax.legend(loc='lower right', fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(outputs_dir, "model_comparison.png"), dpi=300)
    plt.close()
    
    # -------------------------------------------------------------
    # Chart 2: confusion_matrix.png (Best Model)
    # -------------------------------------------------------------
    print("Generating confusion_matrix.png...")
    best_preds = preds_data[best_model_name]
    cm = confusion_matrix(y_test, best_preds)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False,
                xticklabels=['Normal (0)', 'Attack (1)'],
                yticklabels=['Normal (0)', 'Attack (1)'])
    plt.xlabel('Predicted Label', fontsize=12)
    plt.ylabel('True Label', fontsize=12)
    plt.title(f'Confusion Matrix — {best_model_name}', fontsize=14, pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(outputs_dir, "confusion_matrix.png"), dpi=300)
    plt.close()
    
    # -------------------------------------------------------------
    # Chart 3: roc_curves.png
    # -------------------------------------------------------------
    print("Generating roc_curves.png...")
    plt.figure(figsize=(10, 8))
    
    curve_colors = ['#3b82f6', '#22c55e', '#f59e0b', '#ef4444', '#a855f7']
    
    for idx, model_name in enumerate(models):
        y_proba = probas_data[model_name]
        fpr, tpr, _ = roc_curve(y_test, y_proba)
        roc_auc_val = auc(fpr, tpr)
        plt.plot(fpr, tpr, color=curve_colors[idx % len(curve_colors)], lw=2,
                 label=f'{model_name} (AUC = {roc_auc_val:.4f})')
        
    plt.plot([0, 1], [0, 1], color='gray', linestyle='--', label='Random Classifier')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate', fontsize=12)
    plt.ylabel('True Positive Rate', fontsize=12)
    plt.title('ROC Curves — Model Comparison', fontsize=14, pad=15)
    plt.legend(loc="lower right", fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(outputs_dir, "roc_curves.png"), dpi=300)
    plt.close()
    
    # -------------------------------------------------------------
    # Text output: classification_report.txt (Best Model)
    # -------------------------------------------------------------
    print("Saving classification_report.txt...")
    report_text = f"Full Classification Report for Best Model: {best_model_name}\n"
    report_text += "=" * 60 + "\n\n"
    report_text += classification_report(y_test, best_preds, target_names=['Normal', 'Attack'])
    
    with open(os.path.join(outputs_dir, "classification_report.txt"), "w") as f:
        f.write(report_text)
        
    print("Evaluation completed successfully!")

if __name__ == "__main__":
    main()
