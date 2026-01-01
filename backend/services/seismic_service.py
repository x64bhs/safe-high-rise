def get_seismic_risk(lat: float, lon: float, description: str = ""):
    """
    Estimates seismic risk based on coordinates pure logic.
    """
    risk_level = "Low"
    pga = 0.1
    
    # Simple bounding boxes for known high seismic zones (Approximation for MVP)
    # California / West Coast US
    if (30 < lat < 50) and (-125 < lon < -115):
        risk_level = "Severe"
        pga = 0.85
    # Japan
    elif (30 < lat < 46) and (129 < lon < 146):
        risk_level = "Severe"
        pga = 0.9
    # Himalayan Belt
    elif (25 < lat < 36) and (70 < lon < 100):
        risk_level = "High"
        pga = 0.6
    # Pacific Ring of Fire (General)
    elif abs(lat) < 60 and (lon > 120 or lon < -70):
        risk_level = "Moderate" # conservative default for ring
        pga = 0.4
        
    return {
        "zone": risk_level,
        "pga": pga,
        "risk_score": 9 if risk_level == "Severe" else (7 if risk_level == "High" else 3)
    }
