def get_seismic_risk(lat: float, lon: float, description: str = ""):
    """
    Estimates seismic risk based on coordinates with enhanced granularity.
    Returns detailed seismic profile for AI-driven structural selection.
    """
    risk_level = "Low"
    pga = 0.08  # Peak Ground Acceleration in g
    
    # Enhanced seismic zone detection with more granular PGA values
    
    # Pacific Ring of Fire - Japan (Very High Risk)
    if (30 < lat < 46) and (129 < lon < 146):
        risk_level = "Extreme"
        pga = 0.95 + (abs(lat - 35) * 0.01)  # Varies by latitude
    
    # California / West Coast US (High Risk)
    elif (32 < lat < 42) and (-125 < lon < -115):
        risk_level = "Severe"
        pga = 0.75 + (abs(lat - 37) * 0.02)
    
    # Himalayan Belt - Nepal, North India (High Risk)
    elif (25 < lat < 36) and (70 < lon < 95):
        risk_level = "Severe"
        pga = 0.65 + (abs(lat - 28) * 0.015)
    
    # Turkey, Iran (Moderate-High Risk)
    elif (35 < lat < 42) and (25 < lon < 60):
        risk_level = "High"
        pga = 0.55
    
    # Indonesia, Philippines (High Risk)
    elif (-10 < lat < 15) and (95 < lon < 135):
        risk_level = "Severe"
        pga = 0.70
    
    # Chile, Peru (Pacific Coast South America)
    elif (-45 < lat < -15) and (-75 < lon < -65):
        risk_level = "Severe"
        pga = 0.72
    
    # New Zealand (Moderate-High)
    elif (-47 < lat < -34) and (165 < lon < 180):
        risk_level = "High"
        pga = 0.58
    
    # Mediterranean - Italy, Greece (Moderate)
    elif (35 < lat < 45) and (10 < lon < 25):
        risk_level = "Moderate"
        pga = 0.42
    
    # Pacific Ring General (Moderate)
    elif abs(lat) < 60 and (lon > 120 or lon < -70):
        risk_level = "Moderate"
        pga = 0.35
    
    # Central/Eastern US, Europe, Australia (Low)
    elif (25 < lat < 50) and (-100 < lon < -70):
        risk_level = "Low"
        pga = 0.15
    
    # Stable Continental Regions (Very Low)
    else:
        risk_level = "Very Low"
        pga = 0.08
    
    # Cap PGA at realistic maximum
    pga = min(1.2, pga)
    
    # Risk score for quick reference
    risk_scores = {
        "Extreme": 10,
        "Severe": 9,
        "High": 7,
        "Moderate": 5,
        "Low": 3,
        "Very Low": 1
    }
    
    return {
        "zone": risk_level,
        "pga": round(pga, 2),
        "risk_score": risk_scores.get(risk_level, 3),
        "description": f"PGA {pga:.2f}g - {risk_level} seismic activity expected"
    }
