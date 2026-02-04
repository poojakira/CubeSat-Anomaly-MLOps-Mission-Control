import pandas as pd
from firebase_admin import db, credentials, initialize_app
import config, time, logging
from ml_engine import AnomalyEngine

logging.basicConfig(level=logging.INFO)

class MLOrchestrator:
    def __init__(self):
        if not len(db._apps):
            cred = credentials.Certificate(config.SERVICE_ACCOUNT)
            initialize_app(cred, {"databaseURL": config.DB_URL})
        self.engine = AnomalyEngine()

    def fetch_and_process(self):
        # FIX: Added .order_by_key() before .limit_to_last()
        raw = db.reference("/SENSOR_DATA").order_by_key().limit_to_last(500).get()
        if not raw: return None
        df = pd.DataFrame(raw).T
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values("timestamp")
        for f in df['face'].unique():
            df.loc[df['face']==f, "rolling_mean"] = df.loc[df['face']==f, "distance_cm"].rolling(5).mean()
            df.loc[df['face']==f, "rolling_std"] = df.loc[df['face']==f, "distance_cm"].rolling(5).std()
        return df.dropna()

    def run_cycle(self):
        df = self.fetch_and_process()
        if df is None: return
        features = df[["distance_cm", "rolling_mean", "rolling_std"]]
        self.engine.train(features) # Auto-logs to MLflow
        preds, _ = self.engine.predict(features)
        df["anomaly"] = preds
        
        # Push Alerts
        anoms = df[df["anomaly"] == -1]
        if not anoms.empty:
            db.reference("/ML_ALERTS").push(anoms.tail(1).to_dict('records'))
            logging.warning(f"ALERT: {len(anoms)} anomalies detected!")

if __name__ == "__main__":
    orchestrator = MLOrchestrator()
    while True:
        orchestrator.run_cycle()
        time.sleep(60)