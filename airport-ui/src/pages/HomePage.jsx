import { Link } from 'react-router-dom';
import { Plane, MapPin, ShoppingCart, Sparkles, Shield, Zap } from 'lucide-react';
import { authService } from '../api/authService';

export default function HomePage() {
    const isAuth = authService.isAuthenticated();

    return (
        <div>
            {/* Hero */}
            <section className="hero">
                <h1 className="hero-title">
                    Travel Smarter with{' '}
                    <span className="hero-title-gradient">SkyPort</span>
                </h1>
                <p className="hero-description">
                    Your premium airport management and flight booking platform.
                    Browse flights, book tickets, and manage your journeys — all in one place.
                </p>
                <div className="hero-actions">
                    <Link to="/flights" className="btn btn-primary btn-lg">
                        <Plane size={20} />
                        Browse Flights
                    </Link>
                    {!isAuth && (
                        <Link to="/register" className="btn btn-secondary btn-lg">
                            Get Started
                        </Link>
                    )}
                </div>
            </section>

            {/* Features */}
            <section className="stats-row" style={{ marginTop: '4rem' }}>
                <div className="stat-card">
                    <div style={{ color: 'var(--color-accent)', marginBottom: 'var(--space-3)' }}>
                        <Plane size={36} />
                    </div>
                    <div className="stat-label" style={{ fontSize: 'var(--font-size-base)', fontWeight: 600, color: 'var(--color-text-primary)', marginBottom: 'var(--space-2)' }}>
                        Real-Time Flights
                    </div>
                    <div className="stat-label">
                        Browse all scheduled, boarding, and departed flights with live status updates.
                    </div>
                </div>
                <div className="stat-card">
                    <div style={{ color: 'var(--color-accent-secondary)', marginBottom: 'var(--space-3)' }}>
                        <Shield size={36} />
                    </div>
                    <div className="stat-label" style={{ fontSize: 'var(--font-size-base)', fontWeight: 600, color: 'var(--color-text-primary)', marginBottom: 'var(--space-2)' }}>
                        Secure Payments
                    </div>
                    <div className="stat-label">
                        Pay securely through Stripe integration with real-time payment tracking.
                    </div>
                </div>
                <div className="stat-card">
                    <div style={{ color: 'var(--color-accent-warm)', marginBottom: 'var(--space-3)' }}>
                        <Sparkles size={36} />
                    </div>
                    <div className="stat-label" style={{ fontSize: 'var(--font-size-base)', fontWeight: 600, color: 'var(--color-text-primary)', marginBottom: 'var(--space-2)' }}>
                        AI Assistant
                    </div>
                    <div className="stat-label">
                        Ask our AI assistant anything about flights, routes, and bookings in natural language.
                    </div>
                </div>
                <div className="stat-card">
                    <div style={{ color: 'var(--color-success)', marginBottom: 'var(--space-3)' }}>
                        <Zap size={36} />
                    </div>
                    <div className="stat-label" style={{ fontSize: 'var(--font-size-base)', fontWeight: 600, color: 'var(--color-text-primary)', marginBottom: 'var(--space-2)' }}>
                        Instant Booking
                    </div>
                    <div className="stat-label">
                        Select your seats, create an order, and complete your booking in seconds.
                    </div>
                </div>
            </section>

            {/* Quick Links */}
            <section style={{ marginTop: '4rem' }}>
                <h2 style={{
                    fontSize: 'var(--font-size-2xl)',
                    fontWeight: 700,
                    marginBottom: 'var(--space-6)',
                    textAlign: 'center'
                }}>
                    Explore
                </h2>
                <div className="card-grid" style={{ maxWidth: '800px', margin: '0 auto' }}>
                    <Link to="/flights" style={{ textDecoration: 'none' }}>
                        <div className="card" style={{ textAlign: 'center' }}>
                            <Plane size={32} style={{ color: 'var(--color-accent)', marginBottom: 'var(--space-3)' }} />
                            <h3 style={{ fontSize: 'var(--font-size-lg)', marginBottom: 'var(--space-2)' }}>Flights</h3>
                            <p style={{ color: 'var(--color-text-secondary)', fontSize: 'var(--font-size-sm)' }}>
                                View all available flights with routes and schedules
                            </p>
                        </div>
                    </Link>
                    <Link to="/airports" style={{ textDecoration: 'none' }}>
                        <div className="card" style={{ textAlign: 'center' }}>
                            <MapPin size={32} style={{ color: 'var(--color-accent-secondary)', marginBottom: 'var(--space-3)' }} />
                            <h3 style={{ fontSize: 'var(--font-size-lg)', marginBottom: 'var(--space-2)' }}>Airports</h3>
                            <p style={{ color: 'var(--color-text-secondary)', fontSize: 'var(--font-size-sm)' }}>
                                Discover airports, airlines, and their connections
                            </p>
                        </div>
                    </Link>
                </div>
            </section>
        </div>
    );
}
