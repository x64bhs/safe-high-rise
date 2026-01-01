import httpx
import logging

logger = logging.getLogger(__name__)

async def get_weather_data(lat: float, lon: float):
    """
    Fetches historical weather data (wind, precipitation) from Open-Meteo.
    Using 'forecast' or 'archive' API. For MVP we use forecast for 'current' conditions
    and simple max value assumptions.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "wind_speed_10m,precipitation",
        "daily": "wind_speed_10m_max,precipitation_sum",
        "timezone": "auto"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, timeout=5.0)
            response.raise_for_status()
            data = response.json()
            
            # Extract relevant metrics
            current_wind = data.get("current", {}).get("wind_speed_10m", 0)
            max_wind_daily = data.get("daily", {}).get("wind_speed_10m_max", [0])[0]
            
            # Simple logic to determine "Climate Profile"
            profile = {
                "avg_wind_speed": current_wind,
                "max_wind_speed": max_wind_daily,
                "wind_risk": "High" if max_wind_daily > 30 else "Moderate" if max_wind_daily > 15 else "Low",
                "precipitation": data.get("current", {}).get("precipitation", 0)
            }
            return profile
            
    except Exception as e:
        logger.error(f"Weather API failed: {e}")
        # Fallback values
        return {
            "avg_wind_speed": 10,
            "max_wind_speed": 25,
            "wind_risk": "Moderate",
            "precipitation": 0
        }
