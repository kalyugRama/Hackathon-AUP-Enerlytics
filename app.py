from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from data_processing import load_data, generate_simulated_data, aggregate_data
from forecasting import train_forecasting_model, predict_usage  # type: ignore
from recommendations import detect_anomalies, suggest_optimizations
from database import SessionLocal, engine
from models import Base  # Import Base from models
import os
import pandas as pd

app = FastAPI()

# Dependency to get the database session
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create 'data' directory and simulated data if not present
if not os.path.exists('data'):
    os.makedirs('data')

if not os.path.exists('data/simulated_data.csv'):
    generate_simulated_data('data/simulated_data.csv')

df = load_data('data/simulated_data.csv')
aggregated_data = aggregate_data(df)
model = train_forecasting_model(aggregated_data)
Base.metadata.create_all(bind=engine)  # Ensure Base is defined

@app.get("/api/power-usage")
async def get_power_usage():
    return aggregated_data.to_dict(orient='records')

@app.get("/api/predict-usage")
async def predict_power_usage():
    future_data = pd.DataFrame({
        'hour': [i for i in range(24)],
        'day_of_week': [0] * 24
    })
    predictions = predict_usage(model, future_data)
    return predictions.tolist()

@app.get("/api/anomalies")
async def get_anomalies():
    anomalies = detect_anomalies(aggregated_data)
    return anomalies.to_dict(orient='records')

@app.get("/api/optimizations")
async def get_optimizations():
    optimizations = suggest_optimizations(aggregated_data)
    return optimizations

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)