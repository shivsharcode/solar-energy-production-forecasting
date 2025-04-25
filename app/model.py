# Function for loading the model and making predictions

import joblib
import numpy as np

# Load the trained model and scaler
best_model_rf = joblib.load('best_model_rf.pkl')
scaler = joblib.load('scaler.pkl')

import numpy as np
import pandas as pd

def get_prediction(model, scaler, weather_data):
    """
    This function automatically gets the weather data and predicts SystemProduction.
    It also calculates DaySin, DayCos, YearSin, and YearCos internally based on the current date.
    """
    energy_pred_arr = []
    date_arr = []
    parameters_arr = []

    for data in weather_data:
        date_input = data['Date']

        # Calculate DaySin, DayCos, YearSin, YearCos from the input date
        date = pd.to_datetime(date_input)  # Convert input to datetime object
        hour_of_day = date.hour  # Get the hour of the day (0-23)
        day_of_year = date.dayofyear  # Get the day of the year (1-365)

        # Calculate DaySin and DayCos based on hour of the day
        day_sin = np.sin(2 * np.pi * hour_of_day / 24)
        day_cos = np.cos(2 * np.pi * hour_of_day / 24)

        # Calculate YearSin and YearCos based on day of the year
        year_sin = np.sin(2 * np.pi * day_of_year / 365.2425)
        year_cos = np.cos(2 * np.pi * day_of_year / 365.2425)

        # Prepare input dictionary with the calculated values
        input_values = {
            'WindSpeed': data['WindSpeed'],
            'Sunshine': data['Sunshine'],  # Adjust based on actual radiation or sunlight
            'AirPressure': data['AirPressure'],
            'Radiation': data['Radiation'],
            'AirTemperature': round(float(data['AirTemperature']-273.15), 2),  # Convert from Kelvin to Celsius
            'RelativeAirHumidity': data['RelativeAirHumidity'],
            'DaySin': day_sin,
            'DayCos': day_cos,
            'YearSin': year_sin,
            'YearCos': year_cos,
        }
        
        

        # Convert input dictionary to DataFrame for consistency with training data
        input_df = pd.DataFrame([input_values])

        # Apply scaling on the input (using the fitted scaler)
        input_scaled = scaler.transform(input_df)

        # Make prediction using the best trained model
        predicted_value = model.predict(input_scaled)

        energy_pred = predicted_value[0] / 1000  # Convert to MW

        energy_pred_arr.append(round( float(energy_pred), 2 ))
        date_arr.append(date_input)
        parameters_arr.append(input_values)
        
        
    return energy_pred_arr, date_arr, parameters_arr



