import pandas as pd
import streamlit as st
from sklearn.inspection import permutation_importance
from config import DATASET_PATH, ALL_FEATURES, ORIGINAL_FEATURES
from preprocessing import prepare_input

@st.cache_data(show_spinner="Loading and preprocessing dataset for explainability...")
def load_sample_data(n_samples=500):
    if not DATASET_PATH.exists():
        return None
    df = pd.read_csv(DATASET_PATH)
    # Ensure correct columns
    if df.columns[0] not in ORIGINAL_FEATURES + ['CO', 'NOX']:
        df = df.drop(columns=df.columns[0])
    
    # Take a sample
    df_sample = df.sample(n=min(n_samples, len(df)), random_state=42)
    
    # Separate targets and features
    if 'CO' in df_sample.columns and 'NOX' in df_sample.columns:
        X_raw = df_sample[ORIGINAL_FEATURES]
        y_co = df_sample['CO']
        y_nox = df_sample['NOX']
    else:
        return None
        
    # Preprocess
    X_processed = []
    from config import DEFAULT_MEDIANS
    for idx, row in X_raw.iterrows():
        X_processed.append(prepare_input(row.to_dict(), DEFAULT_MEDIANS).iloc[0])
    X_processed = pd.DataFrame(X_processed)[ALL_FEATURES]
    
    return X_processed, y_co, y_nox

def get_feature_importance(model, model_name: str, target_name: str):
    """
    Returns a dataframe of feature importances.
    If the model is tree-based, uses feature_importances_.
    If MLP, uses permutation importance if data is available, otherwise returns None.
    """
    final_estimator = model.named_steps['model']
    
    if hasattr(final_estimator, 'feature_importances_'):
        importances = final_estimator.feature_importances_
        return pd.DataFrame({
            'Feature': ALL_FEATURES,
            'Importance': importances,
            'Type': 'Native Feature Importance'
        }).sort_values('Importance', ascending=False)
    else:
        # Compute permutation importance
        data = load_sample_data()
        if data is None:
            return None
            
        X, y_co, y_nox = data
        y = y_co if target_name == 'CO' else y_nox
        
        # We catch potential errors gracefully
        try:
            with st.spinner("Calculating permutation importance (this may take a moment)..."):
                result = permutation_importance(
                    model, X, y, n_repeats=5, random_state=42, n_jobs=-1
                )
                
            return pd.DataFrame({
                'Feature': ALL_FEATURES,
                'Importance': result.importances_mean,
                'Type': 'Permutation Importance'
            }).sort_values('Importance', ascending=False)
        except Exception as e:
            st.error(f"Error calculating permutation importance: {e}")
            return None
