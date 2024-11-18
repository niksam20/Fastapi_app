import matplotlib.pyplot as plt
import pandas as pd  # Add this import statement

def plot_anomalies(df: pd.DataFrame, output_path: str):
    """Plot anomalies and save the plot."""
    plt.figure(figsize=(10, 6))
    plt.scatter(df['timestamp'], df['feature1'], c=df['anomaly'], cmap='coolwarm', label='Anomalies')
    plt.xlabel("Timestamp")
    plt.ylabel("Feature 1")
    plt.title("Anomaly Detection")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_path)
