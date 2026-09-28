import pandas as pd
import numpy as np

def add_engineered_features(X: pd.DataFrame) -> pd.DataFrame:
    """
    Apply feature engineering to raw input data.
    X should contain the original 9 features.
    """
    X = X.copy()
    
    # Engineer new features based on training script
    X['energy_efficiency'] = X['TEY'] / (X['TIT'] - X['TAT'])
    X['pressure_ratio'] = X['CDP'] / X['AP']
    X['temp_diff'] = X['TIT'] - X['TAT']
    
    # Avoid division by zero for thermal_load
    at_safe = X['AT'].replace(0, np.nan)
    X['thermal_load'] = (X['TIT'] * X['CDP']) / at_safe
    
    # Handle inf values that may arise
    X = X.replace([np.inf, -np.inf], np.nan)
    return X

def prepare_input(data_dict: dict, medians: dict) -> pd.DataFrame:
    """
    Prepare data for the model:
    1. Create DataFrame
    2. Engineer features
    3. Fill NA values
    4. Ensure exact column order
    """
    df = pd.DataFrame([data_dict])
    df = add_engineered_features(df)
    
    # Fill NAs
    for col in df.columns:
        if df[col].isna().any():
            df[col] = df[col].fillna(medians.get(col, 0))
            
    return df
