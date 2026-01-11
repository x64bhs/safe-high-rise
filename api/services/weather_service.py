import httpx
import logging

logger = logging.getLogger(__name__)

async def get_weather_data(lat: float, lon: float):
    """
    Fetches comprehensive weather data from Open-Meteo.
    Returns climate profile with historical patterns for better AI decision-making.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "wind_speed_10m,precipitation,temperature_2m",
        "daily": "wind_speed_10m_max,precipitation_sum,temperature_2m_max,temperature_2m_min",
        "past_days": 7,  # Include past week for better assessment
        "forecast_days": 7,
        "timezone": "auto"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            
            # Extract current conditions
            current_wind = data.get("current", {}).get("wind_speed_10m", 0)
            current_temp = data.get("current", {}).get("temperature_2m", 15)
            current_precip = data.get("current", {}).get("precipitation", 0)
            
            # Extract daily data (past + forecast)
            daily = data.get("daily", {})
            wind_speeds = daily.get("wind_speed_10m_max", [])
            precipitation_sums = daily.get("precipitation_sum", [])
            temp_maxes = daily.get("temperature_2m_max", [])
            temp_mins = daily.get("temperature_2m_min", [])
            
            # Calculate climate statistics
            max_wind_observed = max(wind_speeds) if wind_speeds else current_wind
            avg_wind = sum(wind_speeds) / len(wind_speeds) if wind_speeds else current_wind
            
            total_precip = sum(precipitation_sums) if precipitation_sums else current_precip
            avg_daily_precip = total_precip / len(precipitation_sums) if precipitation_sums else 0
            
            max_temp = max(temp_maxes) if temp_maxes else current_temp
            min_temp = min(temp_mins) if temp_mins else current_temp
            
            # Enhanced risk assessment
            # Wind risk based on maximum observed speeds
            if max_wind_observed > 100:
                wind_risk = "Extreme"
            elif max_wind_observed > 80:
                wind_risk = "High"
            elif max_wind_observed > 50:
                wind_risk = "Moderate"
            else:
                wind_risk = "Low"
            
            # Precipitation risk (for flood assessment)
            if avg_daily_precip > 15:
                precip_risk = "High"
            elif avg_daily_precip > 8:
                precip_risk = "Moderate"
            else:
                precip_risk = "Low"
            
            # Store coordinates for generator use
            profile = {
                "latitude": lat,
                "longitude": lon,
                "avg_wind_speed": round(avg_wind, 1),
                "max_wind_speed": round(max_wind_observed, 1),
                "wind_risk": wind_risk,
                "precipitation": round(avg_daily_precip, 1),
                "total_precipitation_14d": round(total_precip, 1),
                "precip_risk": precip_risk,
                "temperature_range": {
                    "max": round(max_temp, 1),
                    "min": round(min_temp, 1),
                    "current": round(current_temp, 1)
                },
                "climate_severity": "High" if (max_wind_observed > 80 or avg_daily_precip > 12) else "Moderate" if (max_wind_observed > 50 or avg_daily_precip > 6) else "Low"
            }
            
            logger.info(f"Weather data retrieved for ({lat}, {lon}): Wind {max_wind_observed}km/h, Precip {avg_daily_precip}mm/day")
            return profile
            
    except Exception as e:
        logger.error(f"Weather API failed: {e}")
        # Fallback values with coordinates
        return {
            "latitude": lat,
            "longitude": lon,
            "avg_wind_speed": 15,
            "max_wind_speed": 35,
            "wind_risk": "Moderate",
            "precipitation": 2.5,
            "total_precipitation_14d": 35,
            "precip_risk": "Low",
            "temperature_range": {
                "max": 25,
                "min": 10,
                "current": 18
            },
            "climate_severity": "Low"
        }
