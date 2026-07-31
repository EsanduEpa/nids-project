import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib

def main():
    print("=== STEP 1: PREPROCESSING DATA ===")
    
    # 1. Paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)
    data_dir = os.path.join(base_dir, "data")
    saved_models_dir = os.path.join(base_dir, "saved_models")
    outputs_dir = os.path.join(base_dir, "outputs")
    
    os.makedirs(saved_models_dir, exist_ok=True)
    os.makedirs(outputs_dir, exist_ok=True)
    
    train_path = os.path.join(data_dir, "UNSW_NB15_training-set.csv")
    test_path = os.path.join(data_dir, "UNSW_NB15_testing-set.csv")
    
    print(f"Loading datasets from {data_dir}...")
    df_train = pd.read_csv(train_path)
    df_test = pd.read_csv(test_path)
    
    print(f"Train set shape: {df_train.shape}")
    print(f"Test set shape: {df_test.shape}")
    
    # 2. Remove 'id' column if present
    for df in [df_train, df_test]:
        if 'id' in df.columns:
            df.drop(columns=['id'], inplace=True)
            
    # 3. Clean 'attack_cat' column
    for df in [df_train, df_test]:
        if 'attack_cat' in df.columns:
            df['attack_cat'] = df['attack_cat'].astype(str).str.strip()
            df['attack_cat'] = df['attack_cat'].replace({'': 'Normal', 'nan': 'Normal', 'NaN': 'Normal'})
            df['attack_cat'] = df['attack_cat'].fillna('Normal')
            
    # 4. Handle missing values
    df_train.dropna(inplace=True)
    df_test.dropna(inplace=True)
    
    # Generate EDA Chart 1: Attack Distribution
    print("Generating attack_distribution.png...")
    plt.style.use('dark_background')
    plt.figure(figsize=(12, 6))
    attack_counts = df_train['attack_cat'].value_counts()
    ax = sns.barplot(x=attack_counts.index, y=attack_counts.values, palette="viridis")
    plt.title("Distribution of Attack Categories in UNSW-NB15", fontsize=14, pad=15)
    plt.xlabel("Attack Category", fontsize=12)
    plt.ylabel("Count", fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(outputs_dir, "attack_distribution.png"), dpi=300)
    plt.close()
    
    # 5. Categorical columns encoding
    cat_cols = ['proto', 'service', 'state']
    label_encoders = {}
    
    for col in cat_cols:
        le = LabelEncoder()
        # Combine train and test unique values to ensure complete fitting
        combined_series = pd.concat([df_train[col].astype(str), df_test[col].astype(str)], axis=0)
        le.fit(combined_series)
        df_train[col] = le.transform(df_train[col].astype(str))
        df_test[col] = le.transform(df_test[col].astype(str))
        label_encoders[col] = le
        
    # Fit LabelEncoder for target attack_cat
    attack_cat_encoder = LabelEncoder()
    combined_attacks = pd.concat([df_train['attack_cat'], df_test['attack_cat']], axis=0)
    attack_cat_encoder.fit(combined_attacks)
    
    y_train_multi = attack_cat_encoder.transform(df_train['attack_cat'])
    y_test_multi = attack_cat_encoder.transform(df_test['attack_cat'])
    
    y_train = df_train['label'].values
    y_test = df_test['label'].values
    
    # 6. Separate features X and targets
    X_train = df_train.drop(columns=['label', 'attack_cat'])
    X_test = df_test.drop(columns=['label', 'attack_cat'])
    
    feature_names = list(X_train.columns)
    print(f"Total features after encoding: {len(feature_names)}")
    
    # Generate EDA Chart 2: Correlation Heatmap
    print("Generating correlation_heatmap.png...")
    # Calculate correlation with y_train label to find top 20 correlated features
    df_corr = X_train.copy()
    df_corr['label'] = y_train
    corr_matrix = df_corr.corr().abs()
    top_corr_features = corr_matrix['label'].sort_values(ascending=False).head(21).index
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(df_corr[top_corr_features].corr(), annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5)
    plt.title("Feature Correlation Heatmap", fontsize=14, pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(outputs_dir, "correlation_heatmap.png"), dpi=300)
    plt.close()
    
    # 7. StandardScaler
    print("Normalizing features with StandardScaler...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # 8. Save artifacts
    print("Saving processed data and model helper objects...")
    joblib.dump(scaler, os.path.join(saved_models_dir, "scaler.joblib"))
    joblib.dump(label_encoders, os.path.join(saved_models_dir, "label_encoders.joblib"))
    joblib.dump(attack_cat_encoder, os.path.join(saved_models_dir, "attack_cat_encoder.joblib"))
    joblib.dump(feature_names, os.path.join(data_dir, "feature_names.joblib"))
    joblib.dump(feature_names, os.path.join(saved_models_dir, "feature_names.joblib"))
    
    np.save(os.path.join(data_dir, "X_train_scaled.npy"), X_train_scaled)
    np.save(os.path.join(data_dir, "X_test_scaled.npy"), X_test_scaled)
    np.save(os.path.join(data_dir, "y_train.npy"), y_train)
    np.save(os.path.join(data_dir, "y_test.npy"), y_test)
    np.save(os.path.join(data_dir, "y_train_multi.npy"), y_train_multi)
    np.save(os.path.join(data_dir, "y_test_multi.npy"), y_test_multi)
    
    print("Preprocessing completed successfully!")

if __name__ == "__main__":
    main()
