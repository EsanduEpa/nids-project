import pandas as pd
import numpy as np

def preprocess_input(df: pd.DataFrame, scaler, label_encoders: dict, feature_names: list, selected_features: list) -> np.ndarray:
    """
    Preprocesses raw DataFrame uploaded via CSV to match the exact training pipeline:
    1. Drop 'id', 'label', 'attack_cat' if present.
    2. Encode categorical columns ('proto', 'service', 'state') using saved LabelEncoders.
    3. Align DataFrame columns with feature_names (all 42 features used during scaling).
    4. Scale features using saved StandardScaler.
    5. Filter array to include only top 20 selected_features expected by trained models.
    """
    df_clean = df.copy()
    
    # 1. Drop targets and id column if present
    cols_to_drop = ['id', 'label', 'attack_cat']
    for col in cols_to_drop:
        if col in df_clean.columns:
            df_clean = df_clean.drop(columns=[col])
            
    # 2. Encode categorical features ('proto', 'service', 'state')
    cat_cols = ['proto', 'service', 'state']
    for col in cat_cols:
        if col in df_clean.columns:
            encoder = label_encoders.get(col)
            if encoder:
                known_classes = set(encoder.classes_)
                df_clean[col] = df_clean[col].astype(str).apply(
                    lambda val: val if val in known_classes else encoder.classes_[0]
                )
                df_clean[col] = encoder.transform(df_clean[col])
            else:
                df_clean[col] = 0
        else:
            df_clean[col] = 0
            
    # 3. Ensure all 42 feature_names exist
    for feature in feature_names:
        if feature not in df_clean.columns:
            df_clean[feature] = 0.0
            
    df_all_features = df_clean[feature_names]
    
    # 4. Scale using StandardScaler fitted on all 42 features
    scaled_array = scaler.transform(df_all_features)
    
    # 5. Extract indices of selected 20 features
    selected_indices = [feature_names.index(f) for f in selected_features if f in feature_names]
    scaled_selected_array = scaled_array[:, selected_indices]
    
    return scaled_selected_array
