import os  # Import os to check for directory existence
import pandas as pd
import numpy as np

def generate_simulated_data():
    # Ensure the 'data' directory exists
    if not os.path.exists('data'):
        os.makedirs('data')  # Create the directory if it doesn't exist

    appliances = ['Fridge', 'Washing Machine', 'AC', 'Heater', 'TV']
    timestamps = pd.date_range(start='2023-01-01', end='2023-01-02', freq='H')
    data = [] 

    for appliance in appliances:
        for timestamp in timestamps:
            power_usage = np.random.normal(loc=1.0, scale=0.5)  # Simulated power usage
            data.append({'timestamp': timestamp, 'appliance': appliance, 'power_usage': max(0, power_usage)})

    df = pd.DataFrame(data)
    df.to_csv('data/simulated_data.csv', index=False)  # Save the file
    return df

def load_data(file_path):
    df = pd.read_csv(file_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    return df

def aggregate_data(df, freq='h'):  # Change 'H' to 'h'
    return df.groupby([pd.Grouper(freq=freq), 'appliance']).sum().reset_index()