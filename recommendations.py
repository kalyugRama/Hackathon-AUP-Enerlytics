def detect_anomalies(df):
    threshold = df['power_usage'].mean() + 3 * df['power_usage'].std()
    anomalies = df[df['power_usage'] > threshold]
    return anomalies

def suggest_optimizations(df):
    suggestions = []
    for appliance in df['appliance'].unique():
        avg_usage = df[df['appliance'] == appliance]['power_usage'].mean()
        if avg_usage > 1.5:  # Example threshold
            suggestions.append(f"Consider upgrading your {appliance} to a more energy-efficient model.")
    return suggestions