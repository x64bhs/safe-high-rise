from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import asyncio
from services.weather_service import get_weather_data
from services.seismic_service import get_seismic_risk
from services.flood_service import get_flood_risk, get_elevation, compute_flood_risk_sync
from services.generator import generate_architectural_design
from services.geocoding_service import get_location_name, generate_location_description
from services.ai_service import generate_chat_response
app = FastAPI()

# CORS configuration - allow specific origins in production, all in development
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",") if os.getenv("ALLOWED_ORIGINS") else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatMessage(BaseModel):
    query: str
    language: Optional[str] = "English"

class LocationData(BaseModel):
    latitude: float
    longitude: float
    description: Optional[str] = None

@app.get("/")
def read_root():
    return {"message": "Safe High-Rise API is running"}


@app.post("/analyze")
async def analyze_location(data: LocationData):
    # 1. Parallel Data Gathering (Async API calls)
    # We trigger Weather, Geocoding, and Elevation simultaneously
    weather_task = get_weather_data(data.latitude, data.longitude)
    location_task = get_location_name(data.latitude, data.longitude)
    elevation_task = get_elevation(data.latitude, data.longitude)
    
    # Wait for all primary data sources (Parallel)
    weather_profile, (city, country), elevation = await asyncio.gather(
        weather_task, location_task, elevation_task
    )
    
    # 2. Sequential/Local Logic (Fast)
    # Seismic risk is local math/DB lookup
    seismic_profile = get_seismic_risk(data.latitude, data.longitude, data.description or "")
    
    # Comprehensive Flood Risk (uses results from Step 1)
    flood_profile = compute_flood_risk_sync(
        data.latitude, 
        data.longitude, 
        weather_profile.get('precipitation', 0),
        elevation
    )
    
    # Generate Contextual Description
    location_info = generate_location_description(city, country, weather_profile, seismic_profile)
    
    # 3. Design Generation (CPU intensive but local)
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

@app.post("/chat")
async def chat_with_gemini(message: ChatMessage):
    response = generate_chat_response(message.query, message.language)
    return {"response": response}
