import React, { useState, useCallback, useRef } from 'react';
import { MapContainer, TileLayer, Marker, useMapEvents } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import './MapPicker.css';
import L from 'leaflet';

// Fix for default marker icon issue in Leaflet with React
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
    iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
    iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
    shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

// Component to handle map click events
function LocationMarker({ position, onPositionChange }) {
    const markerRef = useRef(null);

    useMapEvents({
        click(e) {
            onPositionChange(e.latlng);
        },
    });

    const eventHandlers = {
        dragend() {
            const marker = markerRef.current;
            if (marker != null) {
                onPositionChange(marker.getLatLng());
            }
        },
    };

    return position ? (
        <Marker
            draggable={true}
            eventHandlers={eventHandlers}
            position={position}
            ref={markerRef}
        />
    ) : null;
}

const MapPicker = ({ location, onLocationChange, height = "400px" }) => {
    // Default to center of map if no location provided
    const defaultCenter = [20.5937, 78.9629]; // Center of India
    const initialPosition = location.lat && location.lng
        ? [parseFloat(location.lat), parseFloat(location.lng)]
        : null;

    const [position, setPosition] = useState(initialPosition);
    const center = position || defaultCenter;

    const handlePositionChange = useCallback((latlng) => {
        setPosition([latlng.lat, latlng.lng]);
        onLocationChange({
            lat: latlng.lat.toFixed(6),
            lng: latlng.lng.toFixed(6)
        });
    }, [onLocationChange]);

    return (
        <div className="map-picker-container" style={{ height }}>
            <MapContainer
                center={center}
                zoom={position ? 10 : 5}
                style={{ height: '100%', width: '100%', borderRadius: '8px' }}
            >
                <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                <LocationMarker position={position} onPositionChange={handlePositionChange} />
            </MapContainer>

            {position && (
                <div className="map-coordinates-display">
                    <span className="coord-label">Selected:</span>
                    <span className="coord-value">
                        {position[0].toFixed(4)}°, {position[1].toFixed(4)}°
                    </span>
                </div>
            )}

            <div className="map-hint">
                💡 Click anywhere on the map or drag the marker to select coordinates
            </div>
        </div>
    );
};

export default MapPicker;
