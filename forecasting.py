from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
import pandas as pd

def train_forecasting_model(df):
    # Ensure 'timestamp' is in datetime format
    if not pd.api.types.is_datetime64_any_dtype(df['timestamp']):
        raise ValueError("The 'timestamp' column must be in datetime format.")

    # Extract hour and day of the week from the timestamp
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek

    # Define features and target variable
    X = df[['hour', 'day_of_week']]
    y = df['power_usage']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and train the model
    model = XGBRegressor()
    model.fit(X_train, y_train)

    return model

def predict_usage(model, future_data):
    # Ensure future_data is in the correct format
    if not isinstance(future_data, pd.DataFrame):
        raise ValueError("future_data must be a pandas DataFrame.")
    
    return model.predict(future_data)