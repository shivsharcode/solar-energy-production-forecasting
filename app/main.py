# FastAPI app file


from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
from app.weather_api import get_coordinates, get_weather_forecast
from app.model import get_prediction

import joblib
import numpy as np

# Load the trained model and scaler
best_model_rf = joblib.load('best_model_rf.pkl')
scaler = joblib.load('scaler.pkl')

# Initialize FastAPI
app = FastAPI()

class CityName(BaseModel):
    city_name: str
    
    
import os
from dotenv import load_dotenv
load_dotenv()

apiKey = os.getenv("API_KEY")
    
    
@app.post("/predict")
async def predict(city: CityName):
    # Fetch coordinates using OpenWeatherMap API
    
    city_name = city.city_name.strip()
    lat, lon = await get_coordinates(city_name, apiKey)
    
    if lat is not None:
        # Get 15-day forecast
        weather_data = await get_weather_forecast(lat, lon, cnt=15, api_key= apiKey)
        
        if weather_data:
            # Use the model to predict for the fetched weather data
            energy_pred_arr, date_arr, parameters_arr = get_prediction(best_model_rf, scaler, weather_data)

            return {"predictions": energy_pred_arr,
                    "dates": date_arr,
                    "parameters": parameters_arr
                    }
    
    return {"error": "Unable to fetch data for the city"}