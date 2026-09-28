import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR.parent / 'Models'

# Features
ORIGINAL_FEATURES = ['AT', 'AP', 'AH', 'AFDP', 'GTEP', 'TIT', 'TAT', 'TEY', 'CDP']
ENGINEERED_FEATURES = ['energy_efficiency', 'pressure_ratio', 'temp_diff', 'thermal_load']
ALL_FEATURES = ORIGINAL_FEATURES + ENGINEERED_FEATURES

# Feature labels
FEATURE_LABELS = {
    'AT': 'AT (Ambient Temperature) | درجة حرارة الهواء',
    'AP': 'AP (Ambient Pressure) | الضغط الجوي',
    'AH': 'AH (Ambient Humidity) | الرطوبة',
    'AFDP': 'AFDP (Air Filter Difference Pressure) | فرق ضغط فلتر الهواء',
    'GTEP': 'GTEP (Gas Turbine Exhaust Pressure) | ضغط عادم التوربين',
    'TIT': 'TIT (Turbine Inlet Temperature) | حرارة مدخل التوربين',
    'TAT': 'TAT (Turbine After Temperature) | حرارة ما بعد التوربين',
    'TEY': 'TEY (Turbine Energy Yield) | الطاقة المنتجة',
    'CDP': 'CDP (Compressor Discharge Pressure) | ضغط تفريغ الضاغط'
}

# Available Models for each target (Clean Names)
MODELS_UI_NAMES = [
    'Decision Tree',
    'Random Forest',
    'XGBoost',
    'Neural Network (MLP)'
]

# Mapping UI Names to actual file names
MODEL_MAPPING = {
    'CO': {
        'Decision Tree': 'Decision_Tree_CO.pkl',
        'Random Forest': 'Random_Forest_CO.pkl',
        'XGBoost': 'XGBoost_CO.pkl',
        'Neural Network (MLP)': 'Neural_Network_MLP_CO.pkl'
    },
    'NOX': {
        'Decision Tree': 'Decision_Tree_NOX.pkl',
        'Random Forest': 'Random_Forest_NOX.pkl',
        'XGBoost': 'XGBoost_NOX.pkl',
        'Neural Network (MLP)': 'Neural_Network_MLP_NOX.pkl'
    }
}

# Imputation defaults (medians from original training data, rough estimates to prevent app crash if not provided)
# It is better to use the user input if possible.
DEFAULT_MEDIANS = {
    'AT': 17.8,
    'AP': 1013.25,
    'AH': 75.0,
    'AFDP': 4.0,
    'GTEP': 25.0,
    'TIT': 1083.0,
    'TAT': 545.0,
    'TEY': 130.0,
    'CDP': 12.0,
    'energy_efficiency': 0.24,
    'pressure_ratio': 11.8,
    'temp_diff': 538.0,
    'thermal_load': 720.0
}

# Offline Evaluation Metrics (From previous training)
OFFLINE_METRICS = {
    'CO': {
        'Decision Tree': {'CV RMSE': 1.3255, 'Test RMSE': 1.3143, 'Test R²': 0.6651},
        'Random Forest': {'CV RMSE': 1.1915, 'Test RMSE': 1.1277, 'Test R²': 0.7535},
        'XGBoost': {'CV RMSE': 1.2011, 'Test RMSE': 1.1398, 'Test R²': 0.7482},
        'Neural Network (MLP)': {'CV RMSE': 1.2340, 'Test RMSE': 1.1975, 'Test R²': 0.7220}
    },
    'NOX': {
        'Decision Tree': {'CV RMSE': 5.8955, 'Test RMSE': 5.6763, 'Test R²': 0.7562},
        'Random Forest': {'CV RMSE': 5.1899, 'Test RMSE': 5.0147, 'Test R²': 0.8097},
        'XGBoost': {'CV RMSE': 5.3982, 'Test RMSE': 5.3253, 'Test R²': 0.7854},
        'Neural Network (MLP)': {'CV RMSE': 5.3967, 'Test RMSE': 4.8746, 'Test R²': 0.8202}
    }
}

# User-configurable reference thresholds (NOT official regulatory limits)
REFERENCE_THRESHOLDS = {
    'CO': {'yellow': 2.0, 'red': 4.0}, 
    'NOX': {'yellow': 40.0, 'red': 60.0}
}

DATASET_PATH = BASE_DIR.parent / 'gt_full.csv'

# Slider ranges (min, max, default) for interactive inputs
SENSOR_RANGES = {
    'AT': (-7.0, 38.0, 17.8), 'AP': (985.0, 1037.0, 1013.25), 'AH': (20.0, 100.0, 75.0),
    'AFDP': (2.0, 8.0, 4.0), 'GTEP': (17.0, 41.0, 25.0), 'TIT': (1000.0, 1100.0, 1083.0),
    'TAT': (510.0, 552.0, 545.0), 'TEY': (100.0, 180.0, 130.0), 'CDP': (9.5, 15.5, 12.0)
}
