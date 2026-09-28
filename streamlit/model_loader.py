import joblib
import streamlit as st
from pathlib import Path
from config import MODELS_DIR, MODEL_MAPPING

@st.cache_resource(show_spinner=False)
def load_model(target: str, display_name: str):
    """
    Load a trained model (Pipeline) from the Models directory based on target and clean name.
    Using st.cache_resource to avoid reloading the model on every UI interaction.
    """
    if target not in MODEL_MAPPING or display_name not in MODEL_MAPPING[target]:
        raise ValueError(f"Invalid model selection: {display_name} for target {target}")
        
    filename = MODEL_MAPPING[target][display_name]
    model_path = MODELS_DIR / filename
    
    if not model_path.exists():
        raise FileNotFoundError(f"Model file is unavailable: {filename}")
    
    model = joblib.load(model_path)
    return model


@st.cache_resource(show_spinner="Checking available models...")
def get_available_models():
    """Return (usable, skipped). A model is usable only if both CO and NOx files load and predict."""
    import pandas as pd
    from config import MODELS_UI_NAMES, DEFAULT_MEDIANS, ALL_FEATURES
    probe = pd.DataFrame([DEFAULT_MEDIANS])[ALL_FEATURES]
    ok, skipped = [], []
    for name in MODELS_UI_NAMES:
        try:
            for t in ('CO', 'NOX'):
                load_model(t, name).predict(probe)
            ok.append(name)
        except Exception:
            skipped.append(name)
    return ok, skipped
