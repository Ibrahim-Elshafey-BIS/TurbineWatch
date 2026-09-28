import pandas as pd
from model_loader import load_model
from preprocessing import prepare_input
from config import DEFAULT_MEDIANS, ALL_FEATURES

def get_emission_status(value: float, target: str, thresholds: dict) -> str:
    """
    Determine emission status based on reference thresholds.
    """
    target = target.upper()
    if target not in thresholds:
        return '⚪ Unknown'
        
    t = thresholds[target]
    if value >= t['red']:
        return '🔴 Red'
    elif value >= t['yellow']:
        return '🟡 Yellow'
    else:
        return '🟢 Green'

def predict_emissions(input_data: dict, model_co_name: str, model_nox_name: str):
    """
    Generate predictions for both CO and NOx.
    1. Preprocess data
    2. Load models
    3. Predict
    """
    # Preprocess
    df = prepare_input(input_data, DEFAULT_MEDIANS)
    
    # Ensure column order matches ALL_FEATURES exactly
    df = df[ALL_FEATURES]
    
    # Load Models
    model_co = load_model('CO', model_co_name)
    model_nox = load_model('NOX', model_nox_name)
    
    # Predict (Pipeline handles scaling)
    co_pred = model_co.predict(df)[0]
    nox_pred = model_nox.predict(df)[0]
    
    return co_pred, nox_pred

def predict_batch(df_raw: pd.DataFrame, selected_co_models: list, selected_nox_models: list, thresholds: dict) -> pd.DataFrame:
    """
    Predict for a batch (DataFrame) of inputs supporting multiple models and statuses.
    Vectorized prediction.
    """
    results = df_raw.copy()
    
    # 1. Prepare entire batch
    df_processed = []
    for idx, row in df_raw.iterrows():
        df_processed.append(prepare_input(row.to_dict(), DEFAULT_MEDIANS).iloc[0])
        
    df_processed = pd.DataFrame(df_processed)
    df_processed = df_processed[ALL_FEATURES]
    
    # 2. Predict CO for selected models
    for m in selected_co_models:
        model = load_model('CO', m)
        base_name = m.replace(' ', '_').replace('(', '').replace(')', '')
        col_name = f'{base_name}_CO'
        results[col_name] = model.predict(df_processed)
        results[f'{col_name}_Status'] = results[col_name].apply(lambda x: get_emission_status(x, 'CO', thresholds))
        
    # 3. Predict NOx for selected models
    for m in selected_nox_models:
        model = load_model('NOX', m)
        base_name = m.replace(' ', '_').replace('(', '').replace(')', '')
        col_name = f'{base_name}_NOx'
        results[col_name] = model.predict(df_processed)
        results[f'{col_name}_Status'] = results[col_name].apply(lambda x: get_emission_status(x, 'NOX', thresholds))
        
    return results


def predict_target(input_data: dict, target: str, model_name: str) -> float:
    """Predict a single target (CO or NOX) with one model."""
    df = prepare_input(input_data, DEFAULT_MEDIANS)[ALL_FEATURES]
    return float(load_model(target, model_name).predict(df)[0])
