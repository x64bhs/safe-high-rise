from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from services.weather_service import get_weather_data
from services.seismic_service import get_seismic_risk
from services.flood_service import get_flood_risk
from services.generator import generate_architectural_design

from services.geocoding_service import get_location_info
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LocationData(BaseModel):
    latitude: float
    longitude: float
    description: Optional[str] = None

@app.get("/api")
def read_root():
    return {"message": "Safe High-Rise API is running"}

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}


@app.post("/api/analyze")
async def analyze_location(data: LocationData):
    # 1. Gather Real/Estimated Environmental Data
    weather_profile = await get_weather_data(data.latitude, data.longitude)
    seismic_profile = get_seismic_risk(data.latitude, data.longitude, data.description or "")
    
    # 1.5 Comprehensive Flood Risk Assessment
    flood_profile = await get_flood_risk(
        data.latitude, 
        data.longitude, 
        weather_profile.get('precipitation', 0)
    )
    
    # 1.6 Auto-Description
    location_info = await get_location_info(data.latitude, data.longitude, weather_profile, seismic_profile)
    
    # 2. Generate Logic-Driven Design (pass flood data)
    design_result = generate_architectural_design(weather_profile, seismic_profile, flood_profile)
    
    # 3. Construct Response
    recommendations = {
        "structure": f"{design_result['structure'].replace('_', ' ').title()} System",
        "material": design_result['material'], # Use the AI-generated material logic
        "features": ["Aerodynamic Tapering"] if design_result['geometry']['taper'] < 1.0 else ["Standard Core"]
    }
    
    if design_result['facade'] == "vertical_forest":
        recommendations["features"].append("Vertical Forests (Sky Gardens)")
    if design_result['geometry']['type'] == "twisted":
        recommendations["features"].append("Vortex-Shedding Twist Geometry")

    return {
        "location": {**data.dict(), "description": location_info["description"], "name": location_info["name"]},
        "profile": {
            "seismic_zone": seismic_profile["zone"],
            "max_wind_speed": f"{weather_profile['max_wind_speed']} km/h",
            "flood_risk": flood_profile["risk_level"],
            "flood_explanation": flood_profile["explanation"],
            "elevation": f"{flood_profile['elevation']}m",
            "precipitation": f"{weather_profile['precipitation']} mm/day"
        },
        "recommendations": recommendations,
        "geometry_params": design_result['geometry'], 
        "safety_score": design_result['safety_score'],
        "wellness": design_result.get('wellness'),
        "longevity": design_result.get('longevity'),
        "simulation_params": design_result.get('simulation_params'),
        "stats": design_result.get('stats'),
        "alternatives": design_result.get('alternatives'),
        "amenities": design_result.get('amenities')
    }
