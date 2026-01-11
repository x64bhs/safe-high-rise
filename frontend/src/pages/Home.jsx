import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';

const Home = () => {
    return (
        <div className="home-container">
            <div className="hero-section">
                <h1 className="hero-title">
                    The Future of <span className="highlight-text">Resilient Architecture</span>
                </h1>
                <p className="hero-subtitle">
                    AI-driven generative design for skyscrapers that withstand earthquakes, hurricanes, and floods.
                    Optimized for safety, sustainability, and structure.
                </p>
                <Link to="/design" className="cta-button">
                    Start Design Simulation
                </Link>
            </div>

            <div className="features-grid">
                <div className="feature-card">
                    <h3>Open-Meteo Integration</h3>
                    <p>Real-time analysis of wind speeds and precipitation data for any geocoordinate.</p>
                </div>
                <div className="feature-card">
                    <h3>Seismic Intelligence</h3>
                    <p>Predictive modeling of tectonic risks to suggest damping systems and diagrids.</p>
                </div>
                <div className="feature-card">
                    <h3>Generative Geometry</h3>
                    <p>Automated 3D architecting of twisted and tapered forms to minimize drag.</p>
                </div>
            </div>
        </div>
    );
};

export default Home;
