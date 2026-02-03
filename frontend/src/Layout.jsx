import React from 'react';
import { Outlet, Link, useLocation } from 'react-router-dom';
import logo from './assets/logo.png';
import ChatWidget from './components/ChatWidget';

const Layout = () => {
    const location = useLocation();

    return (
        <div className="layout-root">
            <nav className="navbar">
                <div className="nav-brand">
                    <Link to="/" style={{ textDecoration: 'none', color: 'white', display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                        <img src={logo} alt="StrataMind Logo" style={{ width: '40px', height: '40px', objectFit: 'contain' }} />
                        <span style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>StrataMind</span>
                    </Link>
                </div>
                {/* Simplified Navigation: Just the brand link to Home. 
            User specifically asked for at most 2 links or chained flow. 
            Home -> Start Simulation -> Dashboard is a clear chain.
        */}
            </nav>

            <main className="content">
                <Outlet />
            </main>
            <ChatWidget />
        </div>
    );
};

export default Layout;
