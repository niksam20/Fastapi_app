from sklearn.ensemble import IsolationForest
import pandas as pd

def detect_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    """Detect anomalies and return DataFrame with anomaly labels."""
    model = IsolationForest(contamination=0.05)  # Adjust contamination rate
    df['anomaly'] = model.fit_predict(df[["feature1", "feature2"]])
    return df[df['anomaly'] == -1]
