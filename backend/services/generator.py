import random

def score_structural_system(system_type, seismic_pga, wind_speed, combined_risk):
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
    
    # Weighted scoring: prioritize based on risk levels
    if seismic_pga > 0.6 or wind_speed > 110:
        # High risk: prioritize specific resistance
        if seismic_pga > wind_speed / 150:
            return system_scores["seismic"] * 0.7 + system_scores["combined"] * 0.3
        else:
            return system_scores["wind"] * 0.7 + system_scores["combined"] * 0.3
    elif combined_risk > 0.5:
        # Moderate combined risk
        return system_scores["combined"] * 0.6 + (system_scores["seismic"] + system_scores["wind"]) * 0.2
    else:
        # Low risk: balanced or eco-friendly
        return (system_scores["seismic"] + system_scores["wind"] + system_scores["combined"]) / 3


def score_material(material_name, seismic_pga, wind_speed, combined_risk, longevity_target):
    """
    Score a material based on environmental factors and longevity requirements.
    Returns a score from 0-100.
    """
    scores = {
        # Living/Nature Materials
        "Living Moss Wall Integration": {
            "durability": 40, "stress_resistance": 30, "longevity_base": 50, "eco_bonus": 95
        },
        "Algae Bio-Reactor Facade Panels": {
            "durability": 45, "stress_resistance": 35, "longevity_base": 60, "eco_bonus": 90
        },
        "Vertical Forest Hydroponic Skin": {
            "durability": 42, "stress_resistance": 32, "longevity_base": 55, "eco_bonus": 92
        },
        "Mycelium-Grown Bio-Insulation": {
            "durability": 38, "stress_resistance": 28, "longevity_base": 45, "eco_bonus": 88
        },
        
        # Smart Tech Materials
        "Self-Healing Nanopolymer Concrete": {
            "durability": 95, "stress_resistance": 85, "longevity_base": 250, "eco_bonus": 60
        },
        "Shape-Memory Alloy (SMA) Kinetic Skin": {
            "durability": 88, "stress_resistance": 90, "longevity_base": 200, "eco_bonus": 55
        },
        "Graphene-Enhanced Geopolymer": {
            "durability": 92, "stress_resistance": 88, "longevity_base": 300, "eco_bonus": 65
        },
        "Photocatalytic Smog-Eating Coating": {
            "durability": 75, "stress_resistance": 70, "longevity_base": 150, "eco_bonus": 85
        },
        
        # High Performance Materials
        "Carbon-Fiber Reinforced Polymer (CFRP)": {
            "durability": 85, "stress_resistance": 92, "longevity_base": 180, "eco_bonus": 50
        },
        "Titanium-Alloy Composite Nodes": {
            "durability": 90, "stress_resistance": 95, "longevity_base": 220, "eco_bonus": 45
        },
        "Ultra-High Performance Concrete (UHPC)": {
            "durability": 88, "stress_resistance": 85, "longevity_base": 150, "eco_bonus": 55
        },
        "Weathering Steel (Cor-Ten)": {
            "durability": 80, "stress_resistance": 78, "longevity_base": 120, "eco_bonus": 60
        }
    }
    
    if material_name not in scores:
        return 50
    
    mat_scores = scores[material_name]
    
    # Calculate stress level
    stress_level = (seismic_pga / 1.2) * 0.5 + (min(wind_speed, 150) / 150) * 0.5
    
    # High stress environments need high durability
    if stress_level > 0.6:
        return mat_scores["stress_resistance"] * 0.7 + mat_scores["durability"] * 0.3
    elif stress_level < 0.3:
        # Low stress: prioritize eco-friendliness
        return mat_scores["eco_bonus"] * 0.6 + mat_scores["durability"] * 0.4
    else:
        # Balanced
        return (mat_scores["durability"] + mat_scores["stress_resistance"] + mat_scores["eco_bonus"]) / 3


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
    
    # --- STRUCTURAL SYSTEM SELECTION (AI-Driven Scoring) ---
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
    
    # Score all structural systems
    all_systems = []
    for category, systems in structural_systems.items():
        all_systems.extend(systems)
    
    system_scores = {}
    for system in all_systems:
        system_scores[system] = score_structural_system(system, seismic_pga, wind_speed, combined_risk)
    
    # Select top 3 systems and add small randomization for variety
    top_systems = sorted(system_scores.items(), key=lambda x: x[1], reverse=True)[:3]
    
    # Add ±5% randomization to top choices
    final_scores = []
    for system, score in top_systems:
        randomized_score = score * random.uniform(0.95, 1.05)
        final_scores.append((system, randomized_score))
    
    # Select the highest scoring system
    selected_structure = max(final_scores, key=lambda x: x[1])[0]
    structure_confidence = max(final_scores, key=lambda x: x[1])[1]
    
    # --- GEOMETRY SELECTION (Adaptive) ---
    # Shape selection based on environmental factors
    shape_scores = {
        "cylinder": 50 + (wind_stress * 40),  # Best for omni-directional wind
        "hexagon": 50 + (combined_risk * 30),  # Balanced geometry
        "triangle": 50 + (seismic_stress * 35),  # Tripod stability for seismic
        "box": 60 - (combined_risk * 20)  # Standard, worse in high risk
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
    
    # Score all materials
    all_materials = []
    for category, mats in materials.items():
        all_materials.extend(mats)
    
    material_scores = {}
    longevity_target = 200 if combined_risk > 0.6 else 300
    for material in all_materials:
        material_scores[material] = score_material(material, seismic_pga, wind_speed, combined_risk, longevity_target)
    
    # Select top material with small randomization
    top_materials = sorted(material_scores.items(), key=lambda x: x[1], reverse=True)[:3]
    final_mat_scores = [(mat, score * random.uniform(0.95, 1.05)) for mat, score in top_materials]
    selected_material = max(final_mat_scores, key=lambda x: x[1])[0]
    
    # Hybridization logic: combine materials if high combined risk
    if combined_risk > 0.65 and random.random() > 0.3:
        # Get a complementary material from different category
        primary_category = None
        for cat, mats in materials.items():
            if selected_material in mats:
                primary_category = cat
                break
        
        # Select from a different category
        other_categories = [cat for cat in materials.keys() if cat != primary_category]
        if other_categories:
            complement_category = random.choice(other_categories)
            complement_material = random.choice(materials[complement_category])
            selected_material = f"{selected_material} + {complement_material}"
    
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
