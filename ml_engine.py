import mlflow, mlflow.sklearn, pickle, os
from sklearn.ensemble import IsolationForest
import config 

class AnomalyEngine:
    def __init__(self):
        mlflow.set_tracking_uri(config.MLFLOW_URI)
        self._setup_exp()
        self.model = None

    def _setup_exp(self):
        if not mlflow.get_experiment_by_name(config.EXPERIMENT_NAME):
            mlflow.create_experiment(config.EXPERIMENT_NAME)
        mlflow.set_experiment(config.EXPERIMENT_NAME)

    def train(self, X):
        with mlflow.start_run(run_name="Satellite_Retrain"):
            self.model = IsolationForest(n_estimators=config.N_ESTIMATORS, contamination=config.CONTAMINATION)
            self.model.fit(X)
            mlflow.sklearn.log_model(self.model, "model")
            os.makedirs("models", exist_ok=True)
            with open(config.MODEL_PATH, "wb") as f: pickle.dump(self.model, f)
        return self.model

    def predict(self, X):
        if not self.model and os.path.exists(config.MODEL_PATH):
            with open(config.MODEL_PATH, "rb") as f: self.model = pickle.load(f)
        return self.model.predict(X), self.model.decision_function(X)