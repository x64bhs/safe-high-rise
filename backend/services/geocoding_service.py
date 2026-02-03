import httpx

async def get_location_name(lat: float, lon: float):
    """
    Identifies the location name (City, Country).
    Uses reverse geocoding from Nominatim or Open-Meteo.
    """
    city = "Unknown Location"
    country = ""
    
    # Strategy 1: Nominatim
    try:
        url = "https://nominatim.openstreetmap.org/reverse"
        params = {"lat": lat, "lon": lon, "format": "json", "accept-language": "en"}
        headers = {"User-Agent": "SafeHighRiseAI/2.0"}
        
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params=params, headers=headers, timeout=2.0)
            if resp.status_code == 200:
                data = resp.json()
                address = data.get("address", {})
                city = address.get("city") or address.get("town") or address.get("village") or address.get("county") or address.get("state")
                country = address.get("country", "")
    except Exception:
        pass

    # Strategy 2: Open-Meteo (Backup)
    if not city or city == "Unknown Location":
        try:
            url = "https://geocoding-api.open-meteo.com/v1/reverse"
            params = {"latitude": lat, "longitude": lon, "count": 1, "language": "en"}
            async with httpx.AsyncClient() as client:
                resp = await client.get(url, params=params, timeout=2.0)
                if resp.status_code == 200:
                    results = resp.json().get("results", [])
                    if results:
                        city = results[0].get("name")
                        country = results[0].get("country", "")
        except Exception:
            pass

    if not city or city == "Unknown Location":
        return f"Site ({lat:.2f}, {lon:.2f})", "Remote Region"
        
    return city, country

def generate_location_description(city: str, country: str, weather_profile: dict, seismic_profile: dict):
    """
    Generates a 4-line description based on identified location and risk stats.
    """
    pga = seismic_profile.get("pga", 0)
    wind = weather_profile.get("max_wind_speed", 0)
    
    lines = [
        f"Selected Site: {city}, {country}.",
        f"Environmental scan indicates {seismic_profile['zone'].lower()} seismic activity (PGA: {pga}g).",
        f"Wind analysis detects peak gusts of {wind} km/h, requiring aerodynamic optimization.",
        "Proposed structure adapts to these specific micro-climatic conditions."
    ]
    
    return {
        "name": f"{city}, {country}",
        "description": "\n".join(lines)
    }

async def get_location_info(lat, lon, weather, seismic):
    """Compatibility wrapper for main.py"""
    city, country = await get_location_name(lat, lon)
    return generate_location_description(city, country, weather, seismic)
