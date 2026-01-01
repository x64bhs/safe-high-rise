
import React, { useRef, useMemo, useState } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Stars, Environment, ContactShadows, Html } from '@react-three/drei';
import * as THREE from 'three';
import './Viewer3D.css';

const DetailedBuilding = ({ params, isCutaway, simulationMode }) => {
    const groupRef = useRef();
    const waterRef = useRef();

    // Parse Parameters
    const geoParams = params?.geometry_params || {};
    const height = geoParams.height || 300;
    const floorCount = 30;
    const floorHeight = 1.2;
    const taperRatio = geoParams.taper || 1.0;
    const twistTotal = (geoParams.twist || 0) * (Math.PI / 180);

    // Simulation Intensity Factors
    const seismicPGA = params?.profile?.seismic_zone?.includes("High") ? 0.05 : 0.02; // Scale sway
    const floodRisk = params?.profile?.flood_risk?.includes("High") ? 15 : 5; // Simulation water height

    // Clipping Plane for Cutaway
    const clipPlanes = useMemo(() => {
        if (!isCutaway) return [];
        const plane = new THREE.Plane(new THREE.Vector3(-1, 0, 0), 0);
        return [plane];
    }, [isCutaway]);

    // Parse Material & Structure Recommendations
    const materialRec = params?.recommendations?.material?.toLowerCase() || "";
    const structureRec = params?.recommendations?.structure?.toLowerCase() || "";

    // Determine Visual Style based on AI Output (Advanced Regex Mapping)
    const materialStyle = useMemo(() => {
        const mat = materialRec;

        // Living / Eco / Nature
        if (mat.includes("living") || mat.includes("moss") || mat.includes("forest") || mat.includes("algae") || mat.includes("bio")) {
            return { color: "#4d7c0f", roughness: 1.0, metalness: 0.1, name: "Living Bio-Skin", emissive: "#14532d", emissiveIntensity: 0.2 }; // Lush Green
        }

        // High-Tech / Carbon
        if (mat.includes("carbon") || mat.includes("graphene") || mat.includes("fiber")) {
            return { color: "#0f172a", roughness: 0.2, metalness: 0.6, name: "Carbon Composite", emissive: "#000000" };
        }

        // Smart / Shape Memory
        if (mat.includes("smart") || mat.includes("kinetic") || mat.includes("memory") || mat.includes("self-healing")) {
            return { color: "#6366f1", roughness: 0.1, metalness: 0.9, name: "Smart Nano-Alloy", emissive: "#312e81", emissiveIntensity: 0.3 }; // Sci-fi Indigo sheen
        }

        // Advanced Concrete / Map specific types
        if (mat.includes("concrete") || mat.includes("uhpc") || mat.includes("geopolymer")) {
            return { color: "#cbd5e1", roughness: 0.6, metalness: 0.1, name: "High-Tech Concrete" };
        }

        // Default
        return { color: "#94a3b8", roughness: 0.3, metalness: 0.7, name: "Advanced Composite" };
    }, [materialRec]);

    // Structural Visualization Logic
    // We map complex terms to visual primitives
    const hasDiagrid = structureRec.includes("diagrid") || structureRec.includes("exoskeleton") || structureRec.includes("helical");
    const hasThickColumns = structureRec.includes("tube") || structureRec.includes("mega") || structureRec.includes("buttressed");
    const hasOutriggers = structureRec.includes("outrigger") || structureRec.includes("belt");

    // Generate Floors
    const floors = useMemo(() => {
        return Array.from({ length: floorCount }).map((_, i) => {
            const progress = i / floorCount;
            const currentScale = 1.0 - (1.0 - taperRatio) * progress;
            const currentRotation = twistTotal * progress;

            return {
                y: i * floorHeight * 2.5,
                scale: currentScale,
                rotation: currentRotation,
                id: i,
                isDiagridNode: i % 4 === 0 // Diagrid nodes every 4 floors
            };
        });
    }, [floorCount, taperRatio, twistTotal]);

    useFrame((state) => {
        // 1. Base Rotation
        if (simulationMode !== 'quake' && !isCutaway && groupRef.current) {
            groupRef.current.rotation.y += 0.002;
        } else if (groupRef.current && isCutaway) {
            groupRef.current.rotation.y = THREE.MathUtils.lerp(groupRef.current.rotation.y, 0, 0.1);
        }

        // 2. Seismic Simulation (Shake Table)
        if (simulationMode === 'quake' && groupRef.current) {
            const time = state.clock.getElapsedTime();
            // Complex multi-frequency shake
            const swayX = Math.sin(time * 5) * seismicPGA * 2;
            const swayZ = Math.cos(time * 4) * seismicPGA * 2;
            const twist = Math.sin(time * 8) * (seismicPGA / 2);

            groupRef.current.rotation.z = swayX;
            groupRef.current.rotation.x = swayZ;
            if (!isCutaway) groupRef.current.rotation.y += twist; // Torsional stress
        } else if (simulationMode !== 'quake' && groupRef.current) {
            // Restore upright position
            groupRef.current.rotation.z = THREE.MathUtils.lerp(groupRef.current.rotation.z, 0, 0.1);
            groupRef.current.rotation.x = THREE.MathUtils.lerp(groupRef.current.rotation.x, 0, 0.1);
        }

        // 3. Flood Simulation (Water Rise)
        if (simulationMode === 'flood' && waterRef.current) {
            // Rise water to flood level
            const targetHeight = floodRisk; // e.g., 15 meters
            waterRef.current.position.y = THREE.MathUtils.lerp(waterRef.current.position.y, targetHeight / 2, 0.02);
            waterRef.current.material.opacity = THREE.MathUtils.lerp(waterRef.current.material.opacity, 0.8, 0.02);
        } else if (waterRef.current) {
            // Recede
            waterRef.current.position.y = THREE.MathUtils.lerp(waterRef.current.position.y, -5, 0.05);
            waterRef.current.material.opacity = THREE.MathUtils.lerp(waterRef.current.material.opacity, 0, 0.05);
        }
    });

    // Fire Pulse Style
    const fireEmissive = simulationMode === 'fire' ? "#ef4444" : materialStyle.emissive || "#000000";
    const fireIntensity = simulationMode === 'fire' ? 2.0 : materialStyle.emissiveIntensity || 0;

    return (
        <group>
            {/* FLOOD PLANE */}
            <mesh ref={waterRef} position={[0, -5, 0]} rotation={[-Math.PI / 2, 0, 0]}>
                <planeGeometry args={[1000, 1000]} />
                <meshPhysicalMaterial color="#3b82f6" transmission={0.9} opacity={0} transparent roughness={0.05} />
            </mesh>

            <group ref={groupRef} position={[0, -15, 0]}>
                {/* Central Core - CROSS SECTION VISIBLE */}
                <mesh position={[0, (floorCount * floorHeight * 2.5) / 2, 0]}>
                    <cylinderGeometry args={[1.5, 1.5, floorCount * floorHeight * 2.5, 8]} />
                    <meshStandardMaterial
                        color={simulationMode === 'fire' ? "#7f1d1d" : "#475569"} // Core heats up 
                        roughness={0.8}
                        clippingPlanes={clipPlanes}
                        side={THREE.DoubleSide}
                        emissive={simulationMode === 'fire' ? "#ef4444" : "#000000"}
                        emissiveIntensity={simulationMode === 'fire' ? 0.5 : 0}
                    />
                </mesh>

                {floors.map((floor, i) => (
                    <group key={floor.id} position={[0, floor.y, 0]} rotation={[0, floor.rotation, 0]} scale={[floor.scale, 1, floor.scale]}>
                        {/* Floor Slab */}
                        <mesh position={[0, 0, 0]} castShadow receiveShadow>
                            {geoParams.type === 'cylinder' && <cylinderGeometry args={[5 * floor.scale, 5 * floor.scale, 0.5, 32]} />}
                            {geoParams.type === 'hexagon' && <cylinderGeometry args={[5 * floor.scale, 5 * floor.scale, 0.5, 6]} />}
                            {geoParams.type === 'triangle' && <cylinderGeometry args={[6 * floor.scale, 6 * floor.scale, 0.5, 3]} />}
                            {(geoParams.type === 'box' || geoParams.type === 'tapered' || geoParams.type === 'twisted') && <boxGeometry args={[10, 0.5, 10]} />}

                            <meshStandardMaterial
                                color={materialStyle.color}
                                metalness={materialStyle.metalness}
                                roughness={materialStyle.roughness}
                                clippingPlanes={clipPlanes}
                                emissive={fireEmissive} // Pulse red in fire mode
                                emissiveIntensity={fireIntensity}
                            />
                        </mesh>

                        {/* Internal Girders / Ribs (Visible in Cutaway) */}
                        {isCutaway && (
                            <group>
                                {[0, 90, 180, 270].map((angle, idx) => (
                                    <mesh key={`rib - ${idx} `} rotation={[0, angle * (Math.PI / 180), 0]}>
                                        <boxGeometry args={[4.5, 0.3, 0.2]} />
                                        <meshStandardMaterial color="#64748b" /> {/* Steel Grey Ribs */}
                                    </mesh>
                                ))}
                            </group>
                        )}

                        {/* Glass Facade */}
                        <mesh position={[0, 1, 0]}>
                            {geoParams.type === 'cylinder' && <cylinderGeometry args={[4.9 * floor.scale, 4.9 * floor.scale, 2, 32]} />}
                            {geoParams.type === 'hexagon' && <cylinderGeometry args={[4.9 * floor.scale, 4.9 * floor.scale, 2, 6]} />}
                            {geoParams.type === 'triangle' && <cylinderGeometry args={[5.8 * floor.scale, 5.8 * floor.scale, 2, 3]} />}
                            {(geoParams.type === 'box' || geoParams.type === 'tapered' || geoParams.type === 'twisted') && <boxGeometry args={[9.8, 2, 9.8]} />}

                            <meshPhysicalMaterial
                                color={simulationMode === 'fire' ? "#fca5a5" : "#bae6fd"} // Glass reflects fire
                                transmission={0.3}
                                opacity={simulationMode === 'fire' ? 0.3 : 0.6}
                                transparent
                                roughness={0.1}
                                thickness={1.5} // Physical thickness
                                clippingPlanes={clipPlanes}
                                side={THREE.DoubleSide} // Render inside of glass too
                            />
                        </mesh>

                        {/* Structural Overlay: Reactive to Geometry Type */}
                        {(() => {
                            // Calculate Column Positions dynamically
                            const radius = 4.5 * floor.scale;
                            let colPositions = [];

                            if (geoParams.type === 'cylinder') {
                                // 8 radial columns
                                for (let j = 0; j < 8; j++) {
                                    const angle = (j / 8) * Math.PI * 2;
                                    colPositions.push([Math.cos(angle) * radius, Math.sin(angle) * radius]);
                                }
                            } else if (geoParams.type === 'hexagon') {
                                // 6 corner columns
                                for (let j = 0; j < 6; j++) {
                                    const angle = (j / 6) * Math.PI * 2;
                                    colPositions.push([Math.cos(angle) * radius, Math.sin(angle) * radius]);
                                }
                            } else if (geoParams.type === 'triangle') {
                                // 3 corner columns
                                for (let j = 0; j < 3; j++) {
                                    const angle = (j / 3) * Math.PI * 2 + (Math.PI / 6); // Offset to align flat side
                                    colPositions.push([Math.cos(angle) * (radius * 1.2), Math.sin(angle) * (radius * 1.2)]);
                                }
                            } else {
                                // Box (Standard 4 corners)
                                colPositions = [
                                    [4.5, 4.5], [-4.5, 4.5], [4.5, -4.5], [-4.5, -4.5]
                                ];
                            }

                            // Render Structural Elements at calculated positions
                            return (
                                <>
                                    {hasDiagrid ? (
                                        // Diagrid Nodes (Angled)
                                        colPositions.map((pos, idx) => (
                                            <mesh key={`diag - node - ${idx} `} position={[pos[0], 1, pos[1]]} rotation={[0, 0, (idx % 2 === 0 ? Math.PI / 4 : -Math.PI / 4)]}>
                                                <cylinderGeometry args={[0.2, 0.2, 5, 4]} />
                                                <meshStandardMaterial color="#0f172a" metalness={0.8} roughness={0.2} clippingPlanes={clipPlanes} />
                                            </mesh>
                                        ))
                                    ) : hasThickColumns ? (
                                        // Mega Columns
                                        colPositions.map((pos, idx) => (
                                            <mesh key={`mega - col - ${idx} `} position={[pos[0], 1, pos[1]]}>
                                                <cylinderGeometry args={[0.6, 0.6, 2, 8]} />
                                                <meshStandardMaterial color="#334155" clippingPlanes={clipPlanes} />
                                            </mesh>
                                        ))
                                    ) : (
                                        // Standard Columns
                                        colPositions.map((pos, idx) => (
                                            <mesh key={`std - col - ${idx} `} position={[pos[0], 1, pos[1]]}>
                                                <cylinderGeometry args={[0.25, 0.25, 2, 8]} />
                                                <meshStandardMaterial color="#334155" clippingPlanes={clipPlanes} />
                                            </mesh>
                                        ))
                                    )}

                                    {/* Outriggers (Belt Truss) */}
                                    {hasOutriggers && (i % 10 === 0) && (
                                        <mesh position={[0, 0.5, 0]}>
                                            {geoParams.type === 'cylinder' || geoParams.type === 'hexagon' ? (
                                                <cylinderGeometry args={[radius + 0.5, radius + 0.5, 0.8, 32]} />
                                            ) : (
                                                <boxGeometry args={[10.2, 0.8, 10.2]} />
                                            )}
                                            <meshStandardMaterial color="#ef4444" emissive="#7f1d1d" emissiveIntensity={0.5} clippingPlanes={clipPlanes} />
                                        </mesh>
                                    )}
                                </>
                            );
                        })()}
                    </group>
                ))}
            </group>
        </group>
    );
};

const Viewer3D = React.forwardRef(({ data, simulationMode }, ref) => {
    const [isCutaway, setIsCutaway] = useState(false);

    // Expose Snapshot Method
    React.useImperativeHandle(ref, () => ({
        captureSnapshot: () => {
            const canvas = document.querySelector('canvas');
            return canvas ? canvas.toDataURL('image/png') : null;
        }
    }));

    return (
        <div className="viewer-wrapper">
            {/* Cutaway Toggle */}
            <div style={{ position: 'absolute', top: '10px', right: '10px', zIndex: 10, display: 'flex', gap: '10px' }}>
                <button
                    onClick={() => setIsCutaway(!isCutaway)}
                    style={{
                        padding: '8px 16px',
                        background: isCutaway ? '#ef4444' : '#0f172a',
                        color: 'white',
                        border: '1px solid #334155',
                        borderRadius: '6px',
                        cursor: 'pointer',
                        fontWeight: 'bold',
                        boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
                    }}
                >
                    {isCutaway ? 'Disable X-Ray' : 'Enable X-Ray View'}
                </button>
            </div>

            <Canvas
                shadows
                camera={{ position: [25, 20, 25], fov: 40 }}
                localClippingEnabled={true}
                gl={{ preserveDrawingBuffer: true }}
            >
                <fog attach="fog" args={simulationMode === 'fire' ? ['#450a0a', 10, 80] : ['#0f172a', 10, 80]} />
                <ambientLight intensity={simulationMode === 'fire' ? 0.3 : 0.7} />
                <directionalLight position={[50, 50, 25]} intensity={2} castShadow shadow-mapSize={[2048, 2048]} />
                <Environment preset={simulationMode === 'fire' ? "sunset" : "city"} />

                <DetailedBuilding params={data} isCutaway={isCutaway} simulationMode={simulationMode} />

                <ContactShadows resolution={1024} scale={100} blur={2} opacity={0.5} far={10} color="#000000" />
                <OrbitControls autoRotate={!isCutaway && !simulationMode} autoRotateSpeed={0.5} enableZoom={true} maxPolarAngle={Math.PI / 2} minPolarAngle={0} />

                {/* Simulation HUD (Heads-Up Display) */}
                {simulationMode && data?.simulation_params && (
                    <Html position={[0, 10, 0]} center>
                        <div style={{ pointerEvents: 'none', width: '300px', textAlign: 'center' }}>
                            <div style={{
                                background: 'rgba(15, 23, 42, 0.9)',
                                padding: '12px',
                                borderRadius: '8px',
                                border: '1px solid #ef4444',
                                color: '#ef4444',
                                fontFamily: 'monospace',
                                boxShadow: '0 0 20px rgba(239, 68, 68, 0.4)'
                            }}>
                                <h3 style={{ margin: 0, fontSize: '1.2rem', textTransform: 'uppercase' }}>⚠ PHYSICS SIMULATION ACTIVE</h3>
                                <hr style={{ borderColor: '#334155', margin: '8px 0' }} />
                                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.9rem', color: '#fff' }}>
                                    <span>TYPE:</span>
                                    <span style={{ fontWeight: 'bold' }}>{simulationMode.toUpperCase()} TEST</span>
                                </div>
                                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '1.1rem', color: '#fbbf24', marginTop: '5px' }}>
                                    {simulationMode === 'quake' && <span>INTENSITY: {data.simulation_params.quake_pga} ({data.simulation_params.quake_magnitude})</span>}
                                    {simulationMode === 'flood' && <span>SURGE LEVEL: {data.simulation_params.flood_level}</span>}
                                    {simulationMode === 'fire' && <span>TEMP LOAD: {data.simulation_params.fire_temp}</span>}
                                </div>
                            </div>
                        </div>
                    </Html>
                )}
            </Canvas>

            {/* Simulation Overlay Badge */}
            <div className="simulation-badge">
                <h3 className="badge-title">
                    {simulationMode ? `STRESS SIMULATION: ${simulationMode.toUpperCase()} ` : 'Micro-Level Simulation'}
                </h3>
                <p className="badge-desc">
                    {simulationMode === 'quake' && `Testing Structural Integrity against ${data?.simulation_params?.quake_magnitude || 'M8.0'} Seismic Activity.`}
                    {simulationMode === 'flood' && `Simulating Storm Surge Resilience: ${data?.simulation_params?.flood_level || '15m'} Water Rise.`}
                    {simulationMode === 'fire' && `Testing Material Thermal Resistance(${data?.simulation_params?.fire_temp || '1200°C'}).`}
                    {!simulationMode && `Visualizing internal core, floor plates, and structural load paths relative to ${data?.location?.name || 'Local'} conditions.`}
                </p>
            </div>
        </div>
    );
});

export default Viewer3D;
