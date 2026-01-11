import httpx

async def get_location_info(lat: float, lon: float, weather_profile: dict, seismic_profile: dict):
    """
    Identifies the location and generates a 4-line description.
    Uses generic logic for description if reverse-geo fails or for MVP speed.
    """
    city = "Unknown Location"
    country = ""
    
    # 1. Reverse Geocoding (Open-Meteo or similar free service)
    # Using Open-Meteo Geocoding API (free)
    # Strategy 1: Nominatim (High fidelity)
    try:
        url = "https://nominatim.openstreetmap.org/reverse"
        params = {"lat": lat, "lon": lon, "format": "json", "accept-language": "en"}
        headers = {"User-Agent": "SafeHighRiseAI/2.0", "Accept-Language": "en"}  # Updated UA and Lang
        
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params=params, headers=headers, timeout=3.0)
            if resp.status_code == 200:
                data = resp.json()
                address = data.get("address", {})
                # Try specific to broad
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
                resp = await client.get(url, params=params, timeout=3.0)
                if resp.status_code == 200:
                    results = resp.json().get("results", [])
                    if results:
                        city = results[0].get("name")
                        country = results[0].get("country", "")
        except Exception:
            pass

    # Strategy 3: Fallback to Coordinates
    if not city or city == "Unknown Location":
        city = f"Remote Site ({lat:.2f}, {lon:.2f})"
        country = "Unknown Region"

    # 2. Generate Contextual Description
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
