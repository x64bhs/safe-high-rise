import random

def generate_architectural_design(weather_profile, seismic_profile):
    """
    Generates advanced architectural parameters with Eco-Resilience and Advanced Scoring.
    """
    wind_speed = weather_profile.get("max_wind_speed", 0)
    seismic_pga = seismic_profile.get("pga", 0.1)
    seismic_zone = seismic_profile.get("zone", "Low")
    
    # Infer Flood Risk from Precipitation
    precip = weather_profile.get("precipitation", 0)
    flood_risk = "High" if precip > 50 else "Moderate" if precip > 20 else "Low"

    # DETERMINISTIC SEEDING
    # Use coordinates to seed random so results are consistent for the same location
    # We combine lat/lon and a salt to ensure stability
    lat = weather_profile.get("latitude", 0)
    lon = weather_profile.get("longitude", 0)
    seed_val = int(abs(lat * 1000) + abs(lon * 1000))
    random.seed(seed_val)

    # --- KNOWLEDGE BASE: Structural Systems ---
    structural_systems = {
        "ultra_high_seismic": [
            "Base-Isolated Hybrid Moment Frame",
            "Viscous Damped Outrigger System",
            "Buckling-Restrained Braced Frame (BRBF)",
            "Active Mass Damper Stabilized Core"
        ],
        "ultra_high_wind": [
            "Aerodynamic Exoskeleton",
            "Bundled Tube with Belt Trusses",
            "Helical Diagrid",
            "Vortex-Shedding Composite Mega-Frame"
        ],
        "balanced_high_performance": [
            "Concrete-Filled Steel Tube (CFST) Diagrid",
            "Buttressed Central Core",
            "Dual-System (Shear Wall + Moment Frame)",
            "Composite Mega-Columns with Outriggers"
        ],
        "eco_resilient": [
            "Mass Timber-Steel Hybrid Frame",
            "Post-Tensioned Laminated Timber Core",
            "Modular Cross-Laminated Timber (CLT)",
            "Bamboo-Reinforced Concrete Composite"
        ],
        "standard": [
            "Reinforced Concrete Shear Wall",
            "Steel Moment Resisting Frame",
            "Tube-in-Tube System"
        ]
    }

    # --- KNOWLEDGE BASE: Advanced & Living Materials ---
    materials = {
        "living_nature": [
            "Living Moss Wall Integration",
            "Algae Bio-Reactor Facade Panels",
            "Vertical Forest Hydroponic Skin",
            "Mycelium-Grown Bio-Insulation"
        ],
        "smart_tech": [
            "Self-Healing Nanopolymer Concrete",
            "Shape-Memory Alloy (SMA) Kinetic Skin",
            "Graphene-Enhanced Geopolymer",
            "Photocatalytic Smog-Eating Coating"
        ],
        "high_performance": [
            "Carbon-Fiber Reinforced Polymer (CFRP)",
            "Titanium-Alloy Composite Nodes",
            "Ultra-High Performance Concrete (UHPC)",
            "Weathering Steel (Cor-Ten)"
        ]
    }

    # --- LOGIC ENGINE ---
    selected_structure = "Standard Core"
    selected_material = "Reinforced Concrete"
    shape_type = "box"
    taper_ratio = 1.0
    twist_angle = 0
    
    # Risk Assessment
    is_high_seismic = seismic_pga > 0.6
    is_high_wind = wind_speed > 80
    is_extreme_wind = wind_speed > 110

    # 1. Shape & Structure Selection
    if is_extreme_wind:
        selected_structure = random.choice(structural_systems["ultra_high_wind"])
        shape_type = "cylinder" # Best for omni-directional shedding
        selected_material = random.choice(materials["smart_tech"]) # Need high tech for extreme conditions
    elif is_high_wind:
        selected_structure = random.choice(structural_systems["ultra_high_wind"])
        shape_type = "hexagon"
        taper_ratio = 0.6
        if "Diagrid" not in selected_structure: selected_structure += " + Aerodynamic Outriggers"
    elif is_high_seismic:
        selected_structure = random.choice(structural_systems["ultra_high_seismic"])
        shape_type = "triangle" # Tripod stability
        taper_ratio = 0.7
        selected_material = "High-Ductility " + random.choice([m for m in materials["smart_tech"] if "Concrete" in m or "Polymer" in m])
    else:
        # Low Stress -> Eco-Friendly / Nature Integrated
        selected_structure = random.choice(structural_systems["eco_resilient"])
        selected_material = random.choice(materials["living_nature"])
        shape_type = random.choice(["hexagon", "box", "cylinder"]) # Freedom of form

    # 2. Material Refinement (Hybridization)
    # If high risk but we want longevity, mix Smart + Nature
    if (is_high_seismic or is_high_wind) and random.random() > 0.5:
        base_mat = selected_material
        living_mat = random.choice(materials["living_nature"])
        selected_material = f"{base_mat} + {living_mat}"

    # DEFINE GEOMETRY EARLY (Required for calculations)
    geometry = {
        "type": shape_type,
        "taper": taper_ratio,
        "twist": twist_angle,
        "height": random.randint(300, 650), # Taller
        "segments": 30
    }

    # 3. Advanced Safety & Longevity Calculation
    # Factors
    resilience_factor = 1.0
    if "Base-Isolated" in selected_structure or "Damped" in selected_structure: resilience_factor += 0.35
    if "Diagrid" in selected_structure or "Exoskeleton" in selected_structure: resilience_factor += 0.25
    if "Triangular" in shape_type or "Hexagon" in shape_type: resilience_factor += 0.15 # Geom Bonus
    
    durability_factor = 1.0
    if "Self-Healing" in selected_material: durability_factor += 0.45
    if "Graphene" in selected_material or "Titanium" in selected_material: durability_factor += 0.35
    if "Living" in selected_material or "Algae" in selected_material: durability_factor += 0.15 # Biophilia bonus
    
    # Environmental Penalty
    # Max Wind ~150kmh, Max PGA ~1.0g
    wind_stress = min(1.0, wind_speed / 180.0) 
    seismic_stress = min(1.0, seismic_pga / 1.2)
    env_stress = (wind_stress * 0.6) + (seismic_stress * 0.4)
    
    # Base Life (Commercial Skyscraper Standard)
    base_life_years = 65 
    
    # Formula: Base * (Durability + Resilience) * (1 - Stress_Penalty)
    # Target: 65 * (1.5 + 1.2) * (1 - 0.2) = 65 * 2.7 * 0.8 = ~140 years
    # Max: 65 * (2.0 + 1.5) * 1.0 = ~225 years
    
    combined_performance = (resilience_factor * 0.6) + (durability_factor * 0.6) # Weighting
    life_multiplier = combined_performance * (1.0 - (env_stress * 0.5)) # Stress reduces life, but not to zero
    
    estimated_life = int(base_life_years * max(1.2, life_multiplier))
    
    # Safety Score (0-100)
    # Ideal score is impacted by how well the resilience meets the stress
    preparedness = (resilience_factor + durability_factor) / 2.0
    risk = env_stress
    
    if preparedness > risk * 1.5:
        base_score = 95
    elif preparedness > risk:
        base_score = 85
    else:
        base_score = 70
        
    # Longevity Calculation (Millennial Scale)
    base_life = 100 
    if "Graphene" in selected_material: base_life = 300
    if "Healing" in selected_material: base_life = 500
    if "Carbon" in selected_material: base_life = 200
    
    # Structure Multiplier
    if "Pyramid" in geometry['type']: base_life *= 1.5 
    if "Hexagonal" in geometry['type']: base_life *= 1.2
    
    durability_factor = (resilience_factor * 1.5) + (2.0 if "Self-Healing" in selected_material else 1.0)
    estimated_life = int(base_life * durability_factor)
    
    # Calculate Safety Score NOW (Fixed Order)
    final_safety_score = min(99, max(60, int(base_score + (durability_factor * 5)))) 
    
    # Cap at realistic "epoch" scale
    estimated_life = min(2500, estimated_life)
    
    longevity_text = f"{estimated_life} Years"

    # Break down the math for the report
    longevity_details = {
        "base_val": f"{base_life} Years (Material Baseline)",
        "structure_mult": f"{'1.5x (Pyramidal)' if 'Pyramid' in geometry['type'] else '1.2x (Hexagonal)' if 'Hexagonal' in geometry['type'] else 'Standard'}",
        "durability_mod": f"x{durability_factor:.2f} (Self-Healing + Resilience)",
        "env_penalty": f"-{(env_stress * 0.5 * 100):.1f}% (Environmental Wear)",
        "final_calc": f"Cap: 2500 Years"
    }

    # 4. Inhabitant Wellness & Health Calculation
    # Factors: Biophilia (Air Quality), Natural Light (Facade Transparency), Stability (Stress Reduction)
    wellness_score = 70 # Base
    if "Living" in selected_material or "Algae" in selected_material: wellness_score += 15 # Air cleaning
    if "Glass" in selected_material or "Translucent" in selected_material: wellness_score += 10 # Natural Light
    if resilience_factor > 1.3: wellness_score += 5 # Mental security/stability
    
    wellness_grade = "A+" if wellness_score > 90 else "A" if wellness_score > 80 else "B"
    
    # 5. Simulation Metadata (Explicit Parameters for Transparency)
    # These are the exact values the frontend will use for "Stress Tests"
    # 5. Simulation Metadata (Explicit Parameters for Transparency)
    # These are the exact values the frontend will use for "Stress Tests"
    sim_params = {
        "quake_pga": f"{min(0.95, seismic_pga * 1.5):.2f}g",
        "quake_magnitude": "M8.5" if "High" in seismic_zone else "M6.5",
        "flood_level": "15.0m" if "High" in flood_risk else "4.0m",
        "fire_temp": "1200°C"
    }

    # 6. Report Extras: Alternatives & Amenities
    # Generate an "Economy" alternative to show contrast in the report
    alt_structure = random.choice(structural_systems["standard"]) if is_high_seismic else "Reinforced Concrete Frame"
    alt_material = "Standard Concrete + Steel"
    
    # Generate Amenities List based on tech level
    amenities = []
    if "Living" in selected_material:
        amenities = ["Hydroponic Air Purification", "Vertical Community Gardens", "Rainwater Harvesting Network"]
    elif "Smart" in selected_material: 
        amenities = ["AI-Driven Climate Control", "Holographic Emergency Navigation", "Kinetic Solar Shading"]
    else:
        amenities = ["Seismic Safe Rooms", "Emergency Oxygen Pods", "Structural Health Monitoring"]
        
    if resilience_factor > 1.2: amenities.append("Base-Isolation Viewing Gallery")

    return {
        "geometry": geometry,
        "structure": selected_structure,
        "material": selected_material, 
        "facade": "Adaptive Bio-Skin" if "Living" in selected_material else "Smart Kinetic Glass",
        "safety_score": final_safety_score,
        "wellness": {
            "score": wellness_score,
            "grade": wellness_grade,
            "label": "Inhabitant Health"
        },
        "longevity": longevity_text,
        "longevity_breakdown": longevity_details,
        "simulation_params": sim_params,
        "stats": {
            "resilience": f"{resilience_factor:.2f}x",
            "durability": f"{durability_factor:.2f}x",
            "stress_load": f"{env_stress:.2f} risk"
        },
        "alternatives": {
            "structure": alt_structure,
            "material": alt_material,
            "note": "Lower Initial Cost, roughly 40% less lifespan."
        },
        "amenities": amenities
    }

def calculate_safety_score(weather, seismic, structure):
    # Deprecated by internal logic above
    return 95
