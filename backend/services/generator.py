import random
import hashlib
import json

def get_local_signature(lat, lon):
    """
    Creates a unique float signature from coordinates to ensure 
    reproducible variety across neighboring locations.
    """
    coord_str = f"{round(lat, 3)}{round(lon, 3)}"
    hash_obj = hashlib.md5(coord_str.encode())
    # Convert first 4 bytes of hash to a float between 0.8 and 1.2
    hash_val = int(hash_obj.hexdigest()[:8], 16)
    return 0.8 + (hash_val % 40) / 100.0


def score_structural_system(system_type, seismic_pga, wind_speed, combined_risk, local_bias=1.0):
    """
    Score a structural system based on environmental factors.
    Returns a score from 0-100 indicating suitability.
    """
    scores = {
        # Ultra High Seismic Systems
        "Base-Isolated Hybrid Moment Frame": {
            "seismic": 95 if seismic_pga > 0.6 else 70 if seismic_pga > 0.4 else 40,
            "wind": 60,
            "combined": 85 if combined_risk > 0.7 else 60
        },
        "Viscous Damped Outrigger System": {
            "seismic": 90 if seismic_pga > 0.6 else 75 if seismic_pga > 0.4 else 45,
            "wind": 70,
            "combined": 80 if combined_risk > 0.7 else 65
        },
        "Buckling-Restrained Braced Frame (BRBF)": {
            "seismic": 92 if seismic_pga > 0.6 else 80 if seismic_pga > 0.4 else 50,
            "wind": 55,
            "combined": 75 if combined_risk > 0.7 else 60
        },
        "Active Mass Damper Stabilized Core": {
            "seismic": 88 if seismic_pga > 0.6 else 72 if seismic_pga > 0.4 else 48,
            "wind": 75,
            "combined": 82 if combined_risk > 0.7 else 68
        },
        "Friction-Pendulum Isolated Core": {
            "seismic": 98 if seismic_pga > 0.7 else 75,
            "wind": 50,
            "combined": 80
        },
        
        # Ultra High Wind Systems
        "Aerodynamic Exoskeleton": {
            "seismic": 50,
            "wind": 95 if wind_speed > 110 else 80 if wind_speed > 80 else 50,
            "combined": 75 if combined_risk > 0.7 else 55
        },
        "Bundled Tube with Belt Trusses": {
            "seismic": 60,
            "wind": 90 if wind_speed > 110 else 85 if wind_speed > 80 else 55,
            "combined": 80 if combined_risk > 0.7 else 60
        },
        "Helical Diagrid": {
            "seismic": 65,
            "wind": 92 if wind_speed > 110 else 88 if wind_speed > 80 else 60,
            "combined": 85 if combined_risk > 0.7 else 65
        },
        "Vortex-Shedding Composite Mega-Frame": {
            "seismic": 55,
            "wind": 93 if wind_speed > 110 else 82 if wind_speed > 80 else 52,
            "combined": 78 if combined_risk > 0.7 else 58
        },
        "Permeable Lattice Shell": {
            "seismic": 45,
            "wind": 96 if wind_speed > 120 else 85,
            "combined": 70
        },
        
        # Balanced High Performance
        "Concrete-Filled Steel Tube (CFST) Diagrid": {
            "seismic": 75,
            "wind": 75,
            "combined": 90 if combined_risk > 0.7 else 80
        },
        "Buttressed Central Core": {
            "seismic": 78,
            "wind": 72,
            "combined": 88 if combined_risk > 0.7 else 78
        },
        "Dual-System (Shear Wall + Moment Frame)": {
            "seismic": 80,
            "wind": 70,
            "combined": 85 if combined_risk > 0.7 else 75
        },
        "Composite Mega-Columns with Outriggers": {
            "seismic": 76,
            "wind": 78,
            "combined": 87 if combined_risk > 0.7 else 77
        },
        "Hybrid Steel-Concrete Outrigger": {
            "seismic": 77, "wind": 77, "combined": 85
        },
        
        # Eco-Resilient (Low Stress)
        "Mass Timber-Steel Hybrid Frame": {
            "seismic": 30 if seismic_pga > 0.6 else 50 if seismic_pga > 0.4 else 85,
            "wind": 35 if wind_speed > 110 else 55 if wind_speed > 80 else 80,
            "combined": 40 if combined_risk > 0.7 else 90
        },
        "Post-Tensioned Laminated Timber Core": {
            "seismic": 28 if seismic_pga > 0.6 else 48 if seismic_pga > 0.4 else 82,
            "wind": 32 if wind_speed > 110 else 52 if wind_speed > 80 else 78,
            "combined": 38 if combined_risk > 0.7 else 88
        },
        "Modular Cross-Laminated Timber (CLT)": {
            "seismic": 25 if seismic_pga > 0.6 else 45 if seismic_pga > 0.4 else 80,
            "wind": 30 if wind_speed > 110 else 50 if wind_speed > 80 else 75,
            "combined": 35 if combined_risk > 0.7 else 85
        },
        "Bamboo-Reinforced Concrete Composite": {
            "seismic": 32 if seismic_pga > 0.6 else 52 if seismic_pga > 0.4 else 83,
            "wind": 38 if wind_speed > 110 else 58 if wind_speed > 80 else 77,
            "combined": 42 if combined_risk > 0.7 else 87
        },
        
        # Standard Systems
        "Reinforced Concrete Shear Wall": {
            "seismic": 65,
            "wind": 60,
            "combined": 70
        },
        "Steel Moment Resisting Frame": {
            "seismic": 70,
            "wind": 65,
            "combined": 72
        },
        "Tube-in-Tube System": {
            "seismic": 68,
            "wind": 68,
            "combined": 75
        }
    }
    
    if system_type not in scores:
        return 50  # Default score
    
    system_scores = scores[system_type]
    
    # Base score selection
    if seismic_pga > 0.6 or wind_speed > 110:
        if seismic_pga > wind_speed / 150:
            base_score = system_scores["seismic"] * 0.7 + system_scores["combined"] * 0.3
        else:
            base_score = system_scores["wind"] * 0.7 + system_scores["combined"] * 0.3
    elif combined_risk > 0.5:
        base_score = system_scores["combined"] * 0.6 + (system_scores["seismic"] + system_scores["wind"]) * 0.2
    else:
        base_score = (system_scores["seismic"] + system_scores["wind"] + system_scores["combined"]) / 3
        
    return base_score * local_bias


def score_material(material_name, seismic_pga, wind_speed, combined_risk, longevity_target, local_bias=1.0):
    """
    Score a material based on environmental factors and durability needs.
    """
    scores = {
        # High-Stress Composites
        "Graphene-Enhanced Titanium Composite": {
            "stress": 95, "eco": 40, "longevity": 98, "seismic": 92, "wind": 95
        },
        "Carbon-Fiber Reinforced Nanopolymer": {
            "stress": 90, "eco": 50, "longevity": 92, "seismic": 95, "wind": 90
        },
        "Self-Healing Shape-Memory Alloy": {
            "stress": 85, "eco": 60, "longevity": 95, "seismic": 90, "wind": 85
        },
        "High-Ductility Graphene Steel": {
            "stress": 92, "eco": 45, "longevity": 94, "seismic": 96, "wind": 88
        },
        
        # Eco-Resilient / Bio-Materials
        "Cross-Laminated Living Moss Timber": {
            "stress": 45, "eco": 98, "longevity": 75, "seismic": 60, "wind": 50
        },
        "Bio-Mineralized Algae Composite": {
            "stress": 50, "eco": 95, "longevity": 80, "seismic": 55, "wind": 55
        },
        "Mycelium-Insulated Carbon Hybrid": {
            "stress": 55, "eco": 92, "longevity": 82, "seismic": 58, "wind": 60
        },
        "Engineered Bamboo-Polymer Matrix": {
            "stress": 60, "eco": 90, "longevity": 78, "seismic": 65, "wind": 65
        },
        
        # Advanced Concretes
        "Ultra-High Performance Concrete (UHPC)": {
            "stress": 80, "eco": 55, "longevity": 88, "seismic": 75, "wind": 80
        },
        "Self-Cleaning Bio-Concrete": {
            "stress": 75, "eco": 70, "longevity": 85, "seismic": 70, "wind": 75
        },
        "Carbon-Sequestering Geopolymer": {
            "stress": 72, "eco": 88, "longevity": 82, "seismic": 68, "wind": 72
        },
        "Nano-Silica Reinforced Concrete": {
            "stress": 78, "eco": 62, "longevity": 86, "seismic": 74, "wind": 78
        }
    }
    
    if material_name not in scores:
        return 50
        
    m = scores[material_name]
    
    # Selection logic based on priorities
    stress_factor = max(seismic_pga * 80, wind_speed / 1.5)
    
    base_score = (
        m["stress"] * (0.4 if stress_factor > 60 else 0.2) +
        m["eco"] * (0.4 if stress_factor < 40 else 0.2) +
        m["longevity"] * 0.3 +
        m["seismic"] * (0.1 if seismic_pga > 0.5 else 0) +
        m["wind"] * (0.1 if wind_speed > 90 else 0)
    )
    
    return base_score * local_bias


def generate_architectural_design(weather_profile, seismic_profile, flood_profile=None):
    """
    Generates AI-driven architectural parameters based on environmental analysis.
    Uses weighted scoring instead of random selection.
    """
    wind_speed = weather_profile.get("max_wind_speed", 0)
    seismic_pga = seismic_profile.get("pga", 0.1)
    seismic_zone = seismic_profile.get("zone", "Low")
    
    # Use comprehensive flood risk assessment if available
    if flood_profile:
        flood_risk = flood_profile.get("risk_level", "Low")
        flood_depth = flood_profile.get("flood_depth_estimate", "2.0m")
    else:
        # Fallback to precipitation-based estimate
        precip = weather_profile.get("precipitation", 0)
        flood_risk = "High" if precip > 50 else "Moderate" if precip > 20 else "Low"
        flood_depth = "15.0m" if flood_risk == "High" else "4.0m"
    
    # Calculate combined risk factor
    wind_stress = min(1.0, wind_speed / 150.0)
    seismic_stress = min(1.0, seismic_pga / 1.2)
    combined_risk = (wind_stress * 0.6) + (seismic_stress * 0.4)
    
    # --- LOCAL SIGNATURE & VARIETY BIAS ---
    local_bias = get_local_signature(weather_profile.get("latitude", 0), weather_profile.get("longitude", 0))

    # --- STRUCTURAL SYSTEM SELECTION (AI-Driven Scoring) ---
    structural_systems = {
        "ultra_high_seismic": [
            "Base-Isolated Hybrid Moment Frame",
            "Viscous Damped Outrigger System",
            "Buckling-Restrained Braced Frame (BRBF)",
            "Active Mass Damper Stabilized Core",
            "Friction-Pendulum Isolated Core"
        ],
        "ultra_high_wind": [
            "Aerodynamic Exoskeleton",
            "Bundled Tube with Belt Trusses",
            "Helical Diagrid",
            "Vortex-Shedding Composite Mega-Frame",
            "Permeable Lattice Shell"
        ],
        "balanced_high_performance": [
            "Concrete-Filled Steel Tube (CFST) Diagrid",
            "Buttressed Central Core",
            "Dual-System (Shear Wall + Moment Frame)",
            "Composite Mega-Columns with Outriggers",
            "Hybrid Steel-Concrete Outrigger"
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
    
    # Score all structural systems
    all_systems = []
    for category, systems in structural_systems.items():
        all_systems.extend(systems)
    
    system_scores = {}
    for system in all_systems:
        system_scores[system] = score_structural_system(system, seismic_pga, wind_speed, combined_risk, local_bias)
    
    # Select top choice with coordinate-seeded randomization
    top_choices = sorted(system_scores.items(), key=lambda x: x[1], reverse=True)[:3]
    
    # Use local_bias to shift selection among top 3
    seed = int(local_bias * 1000)
    random.seed(seed)
    selected_structure = random.choice([c[0] for c in top_choices])
    structure_confidence = system_scores[selected_structure]
    random.seed() # reset seed

    
    # --- GEOMETRY SELECTION (Adaptive) ---
    # Shape selection based on environmental factors
    shape_scores = {
        "pyramid": 60 + (wind_stress * 35),  # Highly aerodynamic, excellent base stability
        "hexagon": 55 + (combined_risk * 25), # Superior structural balance
        "cylinder": 50 + (wind_stress * 30),  # Standard aerodynamic shape
        "triangle": 50 + (seismic_stress * 35),  # Tripod stability
        "prism": 50 + (combined_risk * 15), # Modern geometric aesthetic
        "box": 40 - (combined_risk * 10)  # Standard, penalized in high risk zones
    }
    
    shape_type = max(shape_scores.items(), key=lambda x: x[1])[0]
    
    # Adaptive taper ratio (more taper = better wind resistance)
    if wind_speed > 110:
        taper_ratio = random.uniform(0.55, 0.65)
    elif wind_speed > 80:
        taper_ratio = random.uniform(0.65, 0.75)
    elif seismic_pga > 0.6:
        taper_ratio = random.uniform(0.70, 0.80)
    else:
        taper_ratio = random.uniform(0.85, 1.0)
    
    # Adaptive height (lower in high seismic zones)
    if seismic_pga > 0.7:
        height = random.randint(250, 400)
    elif seismic_pga > 0.5:
        height = random.randint(300, 500)
    else:
        height = random.randint(350, 650)
    
    # Twist angle (only for vortex shedding benefit)
    twist_angle = random.randint(15, 45) if wind_speed > 100 and "Helical" not in selected_structure else 0
    
    geometry = {
        "type": shape_type,
        "taper": round(taper_ratio, 2),
        "twist": twist_angle,
        "height": height,
        "segments": 30
    }
    
    # --- MATERIAL SELECTION (AI-Driven Scoring) ---
    material_categories = {
        "high_stress": [
            "Graphene-Enhanced Titanium Composite", "Carbon-Fiber Reinforced Nanopolymer", 
            "Self-Healing Shape-Memory Alloy", "High-Ductility Graphene Steel"
        ],
        "eco_resilient": [
            "Cross-Laminated Living Moss Timber", "Bio-Mineralized Algae Composite",
            "Mycelium-Insulated Carbon Hybrid", "Engineered Bamboo-Polymer Matrix"
        ],
        "advanced_concrete": [
            "Ultra-High Performance Concrete (UHPC)", "Self-Cleaning Bio-Concrete",
            "Carbon-Sequestering Geopolymer", "Nano-Silica Reinforced Concrete"
        ]
    }
    
    # Select material among top 3
    final_materials = {}
    for mat in [
        "Graphene-Enhanced Titanium Composite", "Carbon-Fiber Reinforced Nanopolymer", 
        "Self-Healing Shape-Memory Alloy", "High-Ductility Graphene Steel",
        "Cross-Laminated Living Moss Timber", "Bio-Mineralized Algae Composite",
        "Mycelium-Insulated Carbon Hybrid", "Engineered Bamboo-Polymer Matrix",
        "Ultra-High Performance Concrete (UHPC)", "Self-Cleaning Bio-Concrete",
        "Carbon-Sequestering Geopolymer", "Nano-Silica Reinforced Concrete"
    ]:
        final_materials[mat] = score_material(mat, seismic_pga, wind_speed, combined_risk, 100, local_bias)
        
    top_mats = sorted(final_materials.items(), key=lambda x: x[1], reverse=True)[:3]
    random.seed(seed + 1)
    selected_material = random.choice([m[0] for m in top_mats])
    random.seed()
    
    # Hybridization logic: combine materials if high combined risk
    if combined_risk > 0.65 and random.random() > 0.3:
        # Get a complementary material from different category
        primary_category = "high_stress"
        for cat, mats in material_categories.items():
            if selected_material in mats:
                primary_category = cat
                break
        
        # Select from a different category
        other_categories = [cat for cat in material_categories.keys() if cat != primary_category]
        if other_categories:
            random.seed(seed + 2)
            complement_category = random.choice(other_categories)
            complement_material = random.choice(material_categories[complement_category])
            selected_material = f"{selected_material} + {complement_material}"
            random.seed()
    
    # --- RESILIENCE & DURABILITY FACTORS ---
    resilience_factor = 1.0
    if "Base-Isolated" in selected_structure or "Damped" in selected_structure:
        resilience_factor += 0.35
    if "Diagrid" in selected_structure or "Exoskeleton" in selected_structure:
        resilience_factor += 0.25
    if shape_type in ["triangle", "hexagon"]:
        resilience_factor += 0.15
    
    durability_factor = 1.0
    if "Self-Healing" in selected_material:
        durability_factor += 0.50
    if "Graphene" in selected_material or "Titanium" in selected_material:
        durability_factor += 0.35
    if "Living" in selected_material or "Algae" in selected_material:
        durability_factor += 0.20
    if "UHPC" in selected_material or "CFRP" in selected_material:
        durability_factor += 0.30
    
    # --- REALISTIC LONGEVITY CALCULATION ---
    # Base lifespan by material type
    if "Self-Healing" in selected_material or "Graphene" in selected_material:
        base_life = random.randint(200, 280)
    elif "Titanium" in selected_material or "CFRP" in selected_material:
        base_life = random.randint(150, 220)
    elif "UHPC" in selected_material or "Shape-Memory" in selected_material:
        base_life = random.randint(120, 180)
    elif "Living" in selected_material or "Timber" in selected_material:
        base_life = random.randint(60, 100)
    else:
        base_life = random.randint(80, 120)
    
    # Environmental degradation factor (reduces lifespan)
    degradation = 1.0 - (combined_risk * 0.35)  # Max 35% reduction
    
    # Resilience bonus (better structures last longer)
    resilience_bonus = 1.0 + ((resilience_factor - 1.0) * 0.4)
    
    # Durability bonus (better materials last longer)
    durability_bonus = 1.0 + ((durability_factor - 1.0) * 0.5)
    
    # Final calculation
    estimated_life = int(base_life * degradation * resilience_bonus * durability_bonus)
    
    # Cap at realistic maximum (500 years)
    estimated_life = min(500, max(50, estimated_life))
    
    longevity_text = f"{estimated_life} Years"
    
    # Longevity breakdown for transparency
    longevity_details = {
        "base_val": f"{base_life} Years (Material Baseline)",
        "structure_mult": f"{resilience_bonus:.2f}x (Structural Resilience)",
        "durability_mod": f"{durability_bonus:.2f}x (Material Durability)",
        "env_penalty": f"-{(1.0 - degradation) * 100:.1f}% (Environmental Stress)",
        "final_calc": f"Result: {estimated_life} Years (Capped at 500)"
    }
    
    # --- SAFETY SCORE CALCULATION ---
    preparedness = (resilience_factor + durability_factor) / 2.0
    risk = combined_risk
    
    if preparedness > risk * 1.8:
        base_score = 95
    elif preparedness > risk * 1.3:
        base_score = 88
    elif preparedness > risk:
        base_score = 80
    else:
        base_score = 72
    
    # Add bonuses for advanced systems
    score_bonus = 0
    if structure_confidence > 85:
        score_bonus += 3
    if durability_factor > 1.5:
        score_bonus += 2
    
    final_safety_score = min(99, max(65, base_score + score_bonus))
    
    # --- WELLNESS CALCULATION ---
    wellness_score = 70
    if "Living" in selected_material or "Algae" in selected_material:
        wellness_score += 15
    if "Photocatalytic" in selected_material:
        wellness_score += 10
    if resilience_factor > 1.3:
        wellness_score += 5
    if combined_risk < 0.3:
        wellness_score += 5
    
    wellness_grade = "A+" if wellness_score > 92 else "A" if wellness_score > 82 else "B+" if wellness_score > 75 else "B"
    
    # --- SIMULATION PARAMETERS ---
    sim_params = {
        "quake_pga": f"{min(1.2, seismic_pga * 1.5):.2f}g",
        "quake_magnitude": f"M{8.5 if seismic_pga > 0.7 else 7.5 if seismic_pga > 0.5 else 6.5}",
        "flood_level": flood_depth,  # Use comprehensive flood assessment
        "fire_temp": "1200°C"
    }
    
    # --- ALTERNATIVES & AMENITIES ---
    # Generate alternative (standard system for comparison)
    alt_structure = "Reinforced Concrete Shear Wall"
    alt_material = "Standard Concrete + Steel Rebar"
    
    # Amenities based on material/structure type
    amenities = []
    if "Living" in selected_material or "Algae" in selected_material:
        amenities = [
            "Hydroponic Air Purification System",
            "Vertical Community Gardens (Sky Terraces)",
            "Rainwater Harvesting & Recycling Network",
            "Bio-Integrated Climate Control"
        ]
    elif "Smart" in selected_material or "Shape-Memory" in selected_material:
        amenities = [
            "AI-Driven Adaptive Climate Control",
            "Holographic Emergency Navigation System",
            "Kinetic Solar Shading (Auto-Adjusting)",
            "Real-Time Structural Health Monitoring"
        ]
    else:
        amenities = [
            "Seismic Safe Rooms (Every 10 Floors)",
            "Emergency Oxygen Distribution Pods",
            "Advanced Structural Health Monitoring",
            "Automated Fire Suppression Network"
        ]
    
    if resilience_factor > 1.4:
        amenities.append("Base-Isolation Viewing Gallery (Ground Floor)")
    if "Diagrid" in selected_structure:
        amenities.append("Exposed Diagrid Architecture Tours")
    
    # Facade selection
    if "Living" in selected_material or "Vertical Forest" in selected_material:
        facade = "Adaptive Bio-Skin with Living Vegetation"
    elif "Smart" in selected_material or "Kinetic" in selected_material:
        facade = "Smart Kinetic Glass with Auto-Tinting"
    else:
        facade = "High-Performance Double-Skin Facade"
    
    return {
        "geometry": geometry,
        "structure": selected_structure,
        "material": selected_material,
        "facade": facade,
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
            "stress_load": f"{combined_risk:.2f} risk"
        },
        "alternatives": {
            "structure": alt_structure,
            "material": alt_material,
            "note": "Standard system: 40% lower initial cost, approximately 50% shorter lifespan."
        },
        "amenities": amenities,
        "ai_confidence": {
            "structure_score": round(structure_confidence, 1),
            "explanation": f"Selected based on {('seismic resistance' if seismic_pga > wind_speed/150 else 'wind resistance')} priority for this location."
        }
    }


def calculate_safety_score(weather, seismic, structure):
    """Deprecated - now calculated inline"""
    return 95
