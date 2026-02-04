import os
# Infrastructure
DB_URL = "https://cubesat-5403b-default-rtdb.asia-southeast1.firebasedatabase.app/"
SERVICE_ACCOUNT = "service_account.json"
# ML Governance
MLFLOW_URI = "sqlite:///mlflow.db"
EXPERIMENT_NAME = "CubeSat_3D_Anomaly_Engine"
MODEL_PATH = "models/isolation_forest_latest.pkl"
# Hyperparameters
CONTAMINATION = 0.05
N_ESTIMATORS = 200
ROLLING_WINDOW = 5

