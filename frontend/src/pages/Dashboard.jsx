import React, { useState, useRef } from 'react';
import { jsPDF } from 'jspdf';
import Viewer3D from '../components/Viewer3D';
import MapPicker from '../components/MapPicker';
import './Dashboard.css';
import logo from '../assets/logo.png';

const Dashboard = () => {
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [location, setLocation] = useState({ lat: '', lng: '' });
    const [activeSim, setActiveSim] = useState(null); // 'quake', 'flood', 'fire' or null
    const [useMap, setUseMap] = useState(true); // Toggle between map and manual input
    const viewerRef = useRef();

    const handleAnalyze = async () => {
        setLoading(true);
        setActiveSim(null); // Reset sim on new analysis
        try {
            const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
            const response = await fetch(`${API_URL}/analyze`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    latitude: parseFloat(location.lat) || 0,
                    longitude: parseFloat(location.lng) || 0
                })
            });
            const data = await response.json();
            setResult(data);
        } catch (e) {
            console.error("Error analyzing:", e);
        } finally {
            setLoading(false);
        }
    };

    const generatePDF = () => {
        if (!result) {
            console.error("No result data available for PDF generation");
            return;
        }

        try {
            const doc = new jsPDF();
            const pageWidth = doc.internal.pageSize.getWidth();
            const pageHeight = doc.internal.pageSize.getHeight();
            const margin = 20;

            // --- WATERMARK HELPER ---
            const addWatermark = () => {
                const logoSize = 60;
                const x = (pageWidth - logoSize) / 2;
                const y = (pageHeight - logoSize) / 2;
                try {
                    // Attempt to add transparent image (some jsPDF versions support this differently)
                    // For now, we add it plain centered.
                    try {
                        // Prefer using jsPDF graphics state if available
                        if (typeof doc.setGState === 'function' && typeof doc.GState === 'function') {
                            const gState = new doc.GState({ opacity: 0.15 });
                            doc.setGState(gState);
                            doc.addImage(logo, 'PNG', x, y, logoSize, logoSize);
                            // restore full opacity
                            doc.setGState(new doc.GState({ opacity: 1 }));
                        } else {
                            // Fallback: draw the logo onto an offscreen canvas with globalAlpha then add the data URL
                            const canvas = document.createElement('canvas');
                            canvas.width = logoSize;
                            canvas.height = logoSize;
                            const ctx = canvas.getContext('2d');
                            const img = new Image();
                            img.crossOrigin = 'anonymous';
                            img.onload = () => {
                                ctx.clearRect(0, 0, canvas.width, canvas.height);
                                ctx.globalAlpha = 0.25;
                                ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
                                const dataUrl = canvas.toDataURL('image/png');
                                doc.addImage(dataUrl, 'PNG', x, y, logoSize, logoSize);
                            };
                            img.onerror = (err) => console.error('Failed to load watermark image for canvas fallback', err);
                            img.src = logo;
                        }
                    } catch (e) {
                        console.error("Watermark error", e);
                    }
                } catch (e) {
                    console.error("Watermark error", e);
                }
            };

            let y = margin;

            // 1. Capture 3D Snapshot
            // Ensure the ref is attached to Viewer3D
            const imgData = viewerRef.current ? viewerRef.current.captureSnapshot() : null;

            // --- PAGE 1: COVER & EXECUTIVE SUMMARY ---
            addWatermark();
            // Header
            doc.setFontSize(24);
            doc.setTextColor(15, 23, 42); // Slate 900
            doc.text("Architectural Resilience Report", margin, y);
            y += 10;
            doc.setFontSize(12);
            doc.setTextColor(100);
            doc.text(`Project: StrataMind  |  Location: ${result.location.name}`, margin, y);
            y += 20;

            // Image
            if (imgData) {
                doc.addImage(imgData, 'PNG', margin, y, pageWidth - (margin * 2), 100);
                y += 160;
            }

            // Summary
            doc.setFontSize(16);
            doc.setTextColor(0);
            doc.text("Executive Summary", margin, y);
            y += 10;
            doc.setFontSize(11);
            doc.setTextColor(60);
            const splitDesc = doc.splitTextToSize(result.location.description, pageWidth - (margin * 2));
            doc.text(splitDesc, margin, y);

            // --- PAGE 2: STRUCTURAL SPECIFICATIONS ---
            doc.addPage();
            addWatermark();
            y = margin;
            doc.setFontSize(18);
            doc.setTextColor(0);
            doc.text("2. Structural System Analysis", margin, y);
            y += 15;

            doc.setFontSize(14);
            doc.text("Primary Structural Choice", margin, y);
            y += 10;
            doc.setFontSize(12);
            doc.setTextColor(40);
            doc.text(`System: ${result.recommendations.structure}`, margin, y);
            y += 10;

            // Comparison Table Logic
            y += 10;
            doc.setFillColor(241, 245, 249);
            doc.rect(margin, y, pageWidth - (margin * 2), 10, 'F');
            doc.setFont(undefined, 'bold');
            doc.text("Comparative Analysis", margin + 5, y + 7);
            doc.setFont(undefined, 'normal');
            y += 15;

            const alternatives = result.alternatives || { structure: "N/A", note: "Standard" };
            doc.text(`Proposed: ${result.recommendations.structure}`, margin, y);
            doc.text(`vs. Alternative: ${alternatives.structure}`, margin, y + 8);
            y += 20;
            doc.setFont(undefined, 'italic');
            doc.text(`Trade-off Note: ${alternatives.note}`, margin, y);

            // --- PAGE 3: MATERIAL INNOVATION ---
            doc.addPage();
            addWatermark();
            y = margin;
            doc.setFontSize(18);
            doc.setTextColor(0);
            doc.setFont(undefined, 'normal');
            doc.text("3. Material & Facade Technology", margin, y);
            y += 20;

            doc.text(`Selected Composite: ${result.recommendations.material}`, margin, y);
            y += 20;
            doc.text(`Smart Facade Layer: ${result.recommendations.features.find(f => f.includes('Bio-Skin') || f.includes('Glass')) || 'Standard Glazing'}`, margin, y);

            // Layer Details - Enhanced to match X-ray view
            y += 20;
            doc.setFontSize(14);
            doc.text("Multi-Layer Composite System (X-Ray View)", margin, y);
            y += 10;
            doc.setFontSize(11);
            doc.setTextColor(60);

            // Determine material-specific layering
            const mat = result.recommendations.material.toLowerCase();
            let layer2Description = "Structural Core (High-Strength Concrete/Steel)";
            let layer2Color = "Gray";

            if (mat.includes("self-healing") || mat.includes("graphene")) {
                layer2Description = "Smart Material Layer (Self-Healing Nanopolymer)";
                layer2Color = "Indigo - Active Repair System";
            } else if (mat.includes("living") || mat.includes("bio") || mat.includes("algae")) {
                layer2Description = "Bio-Active Layer (Living Vegetation/Algae Panels)";
                layer2Color = "Green - Air Purification Active";
            } else if (mat.includes("carbon") || mat.includes("titanium")) {
                layer2Description = "High-Performance Composite (Carbon Fiber/Titanium)";
                layer2Color = "Dark Metallic - Maximum Strength";
            }

            doc.text("Layer 1 (Outer): Adaptive Environmental Shield", margin, y);
            y += 6;
            doc.setFontSize(10);
            doc.text("   • UV/Impact resistant facade with smart glass technology", margin + 5, y);
            y += 5;
            doc.text("   • Color: Translucent Blue/Green (material-dependent)", margin + 5, y);
            y += 10;

            doc.setFontSize(11);
            doc.text(`Layer 2 (Mid): ${layer2Description}`, margin, y);
            y += 6;
            doc.setFontSize(10);
            doc.text(`   • Primary load-bearing and functional material layer`, margin + 5, y);
            y += 5;
            doc.text(`   • Color in X-Ray: ${layer2Color}`, margin + 5, y);
            y += 10;

            doc.setFontSize(11);
            doc.text("Layer 3 (Insulation): Damping/Thermal Control", margin, y);
            y += 6;
            doc.setFontSize(10);
            doc.text("   • Vibration damping and thermal insulation (visible every 3 floors)", margin + 5, y);
            y += 5;
            doc.text("   • Color in X-Ray: Amber/Yellow - Energy dissipation layer", margin + 5, y);
            y += 10;

            doc.setFontSize(11);
            doc.text("Layer 4 (Core): Structural Ribs & Central Column", margin, y);
            y += 6;
            doc.setFontSize(10);
            doc.text("   • Steel/reinforced concrete structural skeleton", margin + 5, y);
            y += 5;
            doc.text("   • Color in X-Ray: Dark Gray - Load path visualization", margin + 5, y);

            y += 15;
            doc.setFontSize(9);
            doc.setFont(undefined, 'italic');
            doc.setTextColor(100);
            doc.text("Note: Enable X-Ray View in the 3D visualization to see these layers interactively.", margin, y);

            // --- PAGE 4: DISASTER RESILIENCE PROFILE ---
            doc.addPage();
            addWatermark();
            y = margin;
            doc.setFontSize(18);
            doc.text("4. Disaster Resilience Factor", margin, y);
            y += 20;

            doc.setFontSize(12);
            doc.text(`Seismic Zone: ${result.profile.seismic_zone}`, margin, y);
            y += 10;
            doc.text(`Max Simulated Load: ${result.simulation_params?.quake_pga} (${result.simulation_params?.quake_magnitude})`, margin, y);
            y += 20;
            doc.text(`Flood Risk: ${result.profile.flood_risk}`, margin, y);
            y += 10;
            doc.text(`Precipitation Load: ${result.profile.precipitation}`, margin, y);

            // Safety Score Breakdown
            y += 20;
            doc.setDrawColor(22, 163, 74); // Green
            doc.setLineWidth(1);
            doc.rect(margin, y, 50, 20);
            doc.setTextColor(0);
            doc.text(`Safety Score: ${result.safety_score} / 100`, margin + 4, y + 12);

            // AI Confidence & Reasoning
            if (result.ai_confidence) {
                y += 30;
                doc.setFontSize(14);
                doc.setTextColor(0);
                doc.text("AI Recommendation Confidence", margin, y);
                y += 10;
                doc.setFontSize(11);
                doc.setTextColor(60);
                doc.text(`Structural System Score: ${result.ai_confidence.structure_score}/100`, margin, y);
                y += 8;
                doc.setFontSize(10);
                const explanationLines = doc.splitTextToSize(result.ai_confidence.explanation, pageWidth - (margin * 2));
                doc.text(explanationLines, margin, y);
                y += explanationLines.length * 6;
                y += 8;
                doc.setFont(undefined, 'italic');
                doc.setFontSize(9);
                doc.text("This design was selected through weighted scoring of environmental factors,", margin, y);
                y += 5;
                doc.text("prioritizing location-specific seismic and wind resistance requirements.", margin, y);
                doc.setFont(undefined, 'normal');
            }

            // --- PAGE 5: WELLNESS, AMENITIES & CONCLUSION ---
            doc.addPage();
            addWatermark();
            y = margin;
            doc.setFontSize(18);
            doc.text("5. Wellness & Amenities", margin, y);
            y += 20;

            doc.setFontSize(14);
            doc.text(`Wellness Grade: ${result.wellness?.grade} (${result.wellness?.score}/100)`, margin, y);
            y += 15;

            doc.text("Featured Amenities:", margin, y);
            y += 10;
            doc.setFontSize(12);
            (result.amenities || []).forEach(item => {
                doc.text(`• ${item}`, margin + 5, y);
                y += 8;
            });

            y += 100;
            doc.setFontSize(14);
            doc.text("Projected Lifespan", margin, y);
            doc.setFontSize(20);
            doc.setTextColor(22, 163, 74);
            doc.text(result.longevity || "N/A", margin, y + 10);

            y += 20;
            doc.setFontSize(14);
            doc.setTextColor(0);
            doc.text("Longevity Projection Analysis", margin, y);
            y += 10;
            doc.setFontSize(10);
            doc.setTextColor(60);

            const breakdown = result.longevity_breakdown || {};
            // Compact Table-like layout
            doc.text(`• Baseline Material Life: ${breakdown.base_val || 'N/A'}`, margin + 5, y); y += 6;
            doc.text(`• Geometry Multiplier: ${breakdown.structure_mult || 'N/A'}`, margin + 5, y); y += 6;
            doc.text(`• Durability Factor: ${breakdown.durability_mod || 'N/A'}`, margin + 5, y); y += 6;
            doc.text(`• Environmental Wear Penalty: ${breakdown.env_penalty || 'N/A'}`, margin + 5, y);

            y += 15;
            doc.setFontSize(9);
            doc.setFont(undefined, 'italic');
            doc.text("Note: Calculations assume maintenance of active self-healing systems.", margin, y);

            // save
            doc.save(`${result.location.name.replace(/ /g, '_')}_StrataMind_Report.pdf`);
        } catch (error) {
            console.error("Error generating PDF:", error);
            alert("Failed to generate PDF. Please check the console for details.");
        }
    };

    return (
        <div className="dashboard-container">
            {/* Sidebar / Controls */}
            {/* Sidebar / Controls */}
            <div className="sidebar">
                <div className="header">
                    <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
                        <img src={logo} alt="StrataMind Logo" style={{ width: '60px', height: '60px', objectFit: 'contain' }} />
                        <h1 className="title" style={{ fontSize: '2rem' }}>StrataMind</h1>
                    </div>
                    <p className="subtitle">Designing Structures that Think with the Earth.</p>
                </div>

                <div className="controls">
                    <div className="input-group">
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                            <label className="input-label">Location Selection</label>
                            <button
                                onClick={() => setUseMap(!useMap)}
                                style={{
                                    padding: '6px 12px',
                                    background: useMap ? '#6366f1' : '#475569',
                                    color: 'white',
                                    border: 'none',
                                    borderRadius: '6px',
                                    cursor: 'pointer',
                                    fontSize: '0.75rem',
                                    fontWeight: '600',
                                    transition: 'all 0.2s'
                                }}
                                title={useMap ? "Switch to Manual Input" : "Switch to Map"}
                            >
                                {useMap ? '🗺️ Map View' : '✏️ Manual Input'}
                            </button>
                        </div>

                        {useMap ? (
                            <MapPicker
                                location={location}
                                onLocationChange={setLocation}
                                height="300px"
                            />
                        ) : (
                            <div className="row">
                                <input
                                    type="number"
                                    placeholder="Latitude (N: + / S -)"
                                    className="styled-input"
                                    value={location.lat}
                                    onChange={(e) => setLocation({ ...location, lat: e.target.value })}
                                />
                                <input
                                    type="number"
                                    placeholder="Longitude (E: + / W -)"
                                    className="styled-input"
                                    value={location.lng}
                                    onChange={(e) => setLocation({ ...location, lng: e.target.value })}
                                />
                            </div>
                        )}
                    </div>

                    {/* Auto-Description Area */}
                    {result?.location?.description && (
                        <div className="info-box" style={{
                            padding: '12px',
                            backgroundColor: 'rgba(16, 185, 129, 0.1)',
                            borderRadius: '8px',
                            border: '1px solid rgba(16, 185, 129, 0.2)',
                            marginTop: '1rem'
                        }}>
                            <div style={{ color: '#6ee7b7', fontWeight: 'bold', fontSize: '0.9rem', marginBottom: '0.5rem' }}>
                                Auto-Detected Site Profile
                            </div>
                            <p style={{ fontSize: '0.85rem', color: '#cbd5e1', whiteSpace: 'pre-line', margin: 0, lineHeight: '1.4' }}>
                                {result.location.description}
                            </p>
                        </div>
                    )}

                    <button
                        onClick={handleAnalyze}
                        disabled={loading}
                        className="analyze-btn"
                        style={{ marginTop: result?.location?.description ? '1rem' : '0' }}
                    >
                        {loading ? 'Analyzing Site...' : 'Generate Design'}
                    </button>

                    {result && (
                        <button
                            onClick={generatePDF}
                            style={{
                                marginTop: '1rem', width: '100%',
                                background: '#14b8a6', color: 'white', border: 'none', borderRadius: '6px', // Teal-500
                                padding: '10px',
                                cursor: 'pointer', fontWeight: 'bold', fontSize: '0.9rem'
                            }}
                            title="Download Detailed PDF Report"
                        >
                            Download StrataMind Report PDF ⇩
                        </button>
                    )}
                </div>

                {result && (
                    <div className="results-panel">
                        {/* Simulation Control Panel */}
                        <div className="section" style={{ background: '#0f172a', padding: '1rem', borderRadius: '8px', border: '1px solid #1e293b' }}>
                            <h3 className="section-title" style={{ color: '#fbbf24', display: 'flex', alignItems: 'center', gap: '8px' }}>
                                <span>⚠️</span> Interactive Stress Tests
                            </h3>
                            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '8px', marginTop: '10px' }}>
                                <button
                                    onClick={() => setActiveSim(activeSim === 'quake' ? null : 'quake')}
                                    style={{
                                        padding: '10px',
                                        background: activeSim === 'quake' ? '#fbbf24' : '#334155',
                                        color: activeSim === 'quake' ? '#000' : '#fff',
                                        border: 'none', borderRadius: '6px', cursor: 'pointer', fontSize: '0.8rem', fontWeight: 'bold'
                                    }}
                                >
                                    Scale {result?.profile?.seismic_zone?.includes("High") ? '8.0' : '6.0'} Quake
                                </button>
                                <button
                                    onClick={() => setActiveSim(activeSim === 'flood' ? null : 'flood')}
                                    style={{
                                        padding: '10px',
                                        background: activeSim === 'flood' ? '#3b82f6' : '#334155',
                                        color: 'white',
                                        border: 'none', borderRadius: '6px', cursor: 'pointer', fontSize: '0.8rem', fontWeight: 'bold'
                                    }}
                                >
                                    Flash Flood
                                </button>
                                <button
                                    onClick={() => setActiveSim(activeSim === 'fire' ? null : 'fire')}
                                    style={{
                                        padding: '10px',
                                        background: activeSim === 'fire' ? '#ef4444' : '#334155',
                                        color: 'white',
                                        border: 'none', borderRadius: '6px', cursor: 'pointer', fontSize: '0.8rem', fontWeight: 'bold'
                                    }}
                                >
                                    Heat Stress
                                </button>
                            </div>
                            <p style={{ fontSize: '0.75rem', color: '#94a3b8', marginTop: '8px' }}>
                                Click to toggle real-time physics simulations on the 3D model.
                            </p>
                        </div>

                        <div className="score-card">
                            <div className="score-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', width: '100%' }}>
                                <div>
                                    <div className="score-label">Overall Safety Score</div>
                                    <div className="score-value">{result.safety_score}/100</div>
                                </div>
                                <div style={{ textAlign: 'right' }}>
                                    <div className="score-label">{result?.wellness?.label || "Wellness"}</div>
                                    <div className="score-value" style={{ color: '#22d3ee' }}>
                                        {result?.wellness?.score || 85}/100 <span style={{ fontSize: '0.6em', opacity: 0.8 }}>({result?.wellness?.grade || 'A'})</span>
                                    </div>
                                </div>
                            </div>
                            <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '1rem', borderTop: '1px solid rgba(255,255,255,0.1)', paddingTop: '0.5rem' }}>
                                <div>
                                    <div className="score-label" style={{ fontSize: '0.7rem' }}>Projected Lifespan</div>
                                    <div style={{ color: '#6ee7b7', fontWeight: 'bold' }}>{result.longevity || 'N/A'}</div>
                                </div>
                                <div style={{ textAlign: 'right' }}>
                                    <div className="score-label" style={{ fontSize: '0.7rem' }}>Stress Risk</div>
                                    <div style={{ color: '#f87171', fontWeight: 'bold' }}>{result?.stats?.stress_load || 'Low'}</div>
                                </div>
                            </div>
                        </div>

                        <div className="section">
                            <h3 className="section-title">Disaster Profile</h3>
                            <div className="profile-grid">
                                <div className="profile-label">Seismic Zone</div>
                                <div className="profile-value">{result?.profile?.seismic_zone}</div>
                                <div className="profile-label">Wind Load</div>
                                <div className="profile-value">{result?.profile?.max_wind_speed}</div>
                                <div className="profile-label">Flood Risk</div>
                                <div className="profile-value">{result?.profile?.flood_risk}</div>
                            </div>
                        </div>

                        <div className="section">
                            <h3 className="section-title">AI Recommendations</h3>
                            <div className="recommendations-list">
                                <div className="rec-item structure"
                                    onClick={() => {
                                        const struct = result?.recommendations?.structure.toLowerCase();
                                        let query = result?.recommendations?.structure;
                                        // ... (Keep existing link logic)
                                        if (struct.includes("diagrid")) query = "Diagrid";
                                        else if (struct.includes("outrigger")) query = "Outrigger_(structure)";
                                        else if (struct.includes("buttressed")) query = "Buttressed_core";
                                        else if (struct.includes("tube")) query = "Tube_(structure)";
                                        else if (struct.includes("exoskeleton")) query = "Structural_exoskeleton";
                                        else if (struct.includes("shear")) query = "Shear_wall";
                                        else if (struct.includes("moment")) query = "Moment-resisting_frame";
                                        else if (struct.includes("bundled")) query = "Bundled_tube";
                                        else if (struct.includes("mega")) query = "Megaframe";

                                        // Expanded Dictionary Check
                                        const directWiki = ["diagrid", "outrigger", "buttressed", "tube", "exoskeleton", "shear", "moment", "bundled", "mega"];
                                        const hasWiki = directWiki.some(term => struct.includes(term));

                                        const url = hasWiki
                                            ? `https://en.wikipedia.org/wiki/${query}`
                                            : `https://duckduckgo.com/?q=${query}+structural+system+architectural+definition&ia=web`; // DuckDuckGo often gives better instant answers/definitions than generic Google

                                        window.open(url, '_blank');
                                    }}
                                    style={{ cursor: 'pointer' }}
                                    title="Learn about this System"
                                >
                                    <div className="rec-label">Structure ↗</div>
                                    <div className="rec-value" style={{ textDecoration: 'underline' }}>{result?.recommendations?.structure}</div>
                                </div>
                                <div className="rec-item material"
                                    onClick={() => window.open(`https://www.google.com/search?q=${result?.recommendations?.material.replace(/ /g, '+')}+architecture+material+properties`, '_blank')}
                                    style={{ cursor: 'pointer' }}
                                    title="Search on Google"
                                >
                                    <div className="rec-label">Material ↗</div>
                                    <div className="rec-value" style={{ textDecoration: 'underline' }}>{result?.recommendations?.material}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                )}
            </div>

            {/* 3D Visualization Area */}
            <div className="viewer-container">
                {/* Key forces complete re-mount when result changes, ensuring geometry/material updates */}
                <Viewer3D
                    ref={viewerRef}
                    key={result ? result.safety_score : 'init'}
                    data={result || {}}
                    simulationMode={activeSim}
                />

                {/* Overlay Info */}
                {!result && (
                    <div className="overlay-message">
                        <div className="message-box">
                            <h2 className="message-title">Ready to Simulate</h2>
                            <p className="message-sub">
                                Enter location to auto-detect environmental hazards and generate resilient architecture.
                            </p>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Dashboard;