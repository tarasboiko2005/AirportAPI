import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
    Plane, Clock, Calendar, ArrowLeft,
    Ticket, ShoppingCart, CheckCircle
} from 'lucide-react';
import { flightService } from '../api/flightService';
import { ticketService } from '../api/ticketService';
import { orderService } from '../api/orderService';
import { authService } from '../api/authService';

const formatDate = (dt) => {
    if (!dt) return '—';
    return new Date(dt).toLocaleDateString('en-GB', {
        weekday: 'long', day: '2-digit', month: 'long', year: 'numeric'
    });
};

const formatTime = (dt) => {
    if (!dt) return '—';
    return new Date(dt).toLocaleTimeString('en-GB', {
        hour: '2-digit', minute: '2-digit'
    });
};

export default function FlightDetailPage() {
    const { id } = useParams();
    const navigate = useNavigate();
    const isAuth = authService.isAuthenticated();

    const [flight, setFlight] = useState(null);
    const [tickets, setTickets] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selectedTickets, setSelectedTickets] = useState([]);
    const [bookingLoading, setBookingLoading] = useState(false);
    const [bookingSuccess, setBookingSuccess] = useState('');
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [flightRes, ticketRes] = await Promise.all([
                    flightService.getFlight(id),
                    isAuth ? ticketService.getTickets({ flight: id }) : Promise.resolve({ data: [] })
                ]);
                setFlight(flightRes.data);
                const tData = ticketRes.data;
                setTickets(tData.results || tData || []);
            } catch (err) {
                setError('Failed to load flight details.');
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, [id, isAuth]);

    const toggleTicket = (ticketId) => {
        setSelectedTickets(prev =>
            prev.includes(ticketId)
                ? prev.filter(t => t !== ticketId)
                : [...prev, ticketId]
        );
    };

    const handleBook = async () => {
        if (selectedTickets.length === 0) return;
        setBookingLoading(true);
        setError('');
        try {
            await orderService.createOrder({
                tickets: selectedTickets,
                payment_method: 'card',
                currency: 'USD'
            });
            setBookingSuccess('Order created! Go to Orders to complete payment.');
            setSelectedTickets([]);
            const ticketRes = await ticketService.getTickets({ flight: id });
            const tData = ticketRes.data;
            setTickets(tData.results || tData || []);
        } catch (err) {
            const data = err.response?.data;
            setError(
                data ? (typeof data === 'string' ? data : JSON.stringify(data)) : 'Booking failed.'
            );
        } finally {
            setBookingLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="loading-container">
                <div className="spinner" />
                <p style={{ color: 'var(--color-text-secondary)' }}>Loading flight details...</p>
            </div>
        );
    }

    if (!flight) {
        return (
            <div className="empty-state">
                <div className="empty-state-title">Flight not found</div>
                <button className="btn btn-primary" onClick={() => navigate('/flights')}>
                    <ArrowLeft size={16} /> Back to Flights
                </button>
            </div>
        );
    }

    const availableTickets = tickets.filter(t => t.status === 'available');
    const selectedTotal = tickets
        .filter(t => selectedTickets.includes(t.id))
        .reduce((sum, t) => sum + parseFloat(t.price), 0);

    return (
        <div>
            <button
                className="btn btn-secondary btn-sm"
                onClick={() => navigate('/flights')}
                style={{ marginBottom: 'var(--space-6)' }}
            >
                <ArrowLeft size={16} /> Back to Flights
            </button>

            {error && <div className="alert alert-error">{error}</div>}
            {bookingSuccess && <div className="alert alert-success"><CheckCircle size={16} />{bookingSuccess}</div>}

            <div className="detail-grid">
                {/* Left column — flight info */}
                <div>
                    <div className="card" style={{ marginBottom: 'var(--space-6)' }}>
                        <div style={{
                            display: 'flex',
                            justifyContent: 'space-between',
                            alignItems: 'center',
                            marginBottom: 'var(--space-4)'
                        }}>
                            <h1 style={{
                                fontSize: 'var(--font-size-3xl)',
                                fontWeight: 800,
                                color: 'var(--color-accent)'
                            }}>
                                Flight {flight.number}
                            </h1>
                            <span className={`badge badge-${flight.status}`}>{flight.status}</span>
                        </div>

                        <div className="flight-route" style={{ margin: 'var(--space-6) 0' }}>
                            <div className="flight-airport">
                                <div className="flight-airport-code" style={{ fontSize: 'var(--font-size-4xl)' }}>
                                    {flight.origin_iata || flight.origin}
                                </div>
                                <div className="flight-airport-name">
                                    {flight.origin_name || 'Origin'}
                                </div>
                            </div>
                            <div className="flight-path">
                                <div className="flight-path-line" />
                            </div>
                            <div className="flight-airport">
                                <div className="flight-airport-code" style={{ fontSize: 'var(--font-size-4xl)' }}>
                                    {flight.destination_iata || flight.destination}
                                </div>
                                <div className="flight-airport-name">
                                    {flight.destination_name || 'Destination'}
                                </div>
                            </div>
                        </div>

                        <div className="detail-section">
                            <div className="detail-row">
                                <span className="detail-label"><Calendar size={14} style={{ marginRight: 4, verticalAlign: 'middle' }} />Departure</span>
                                <span className="detail-value">{formatDate(flight.departure_time)} at {formatTime(flight.departure_time)}</span>
                            </div>
                            <div className="detail-row">
                                <span className="detail-label"><Calendar size={14} style={{ marginRight: 4, verticalAlign: 'middle' }} />Arrival</span>
                                <span className="detail-value">{formatDate(flight.arrival_time)} at {formatTime(flight.arrival_time)}</span>
                            </div>
                            <div className="detail-row">
                                <span className="detail-label"><Plane size={14} style={{ marginRight: 4, verticalAlign: 'middle' }} />Airplane</span>
                                <span className="detail-value">#{flight.airplane}</span>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Right column — tickets */}
                <div>
                    <div className="card">
                        <div className="detail-section-title">
                            <Ticket size={20} />
                            Available Tickets ({availableTickets.length})
                        </div>

                        {!isAuth ? (
                            <div style={{
                                textAlign: 'center',
                                padding: 'var(--space-6)',
                                color: 'var(--color-text-secondary)'
                            }}>
                                <p style={{ marginBottom: 'var(--space-4)' }}>
                                    Please login to view and book tickets
                                </p>
                                <button
                                    className="btn btn-primary"
                                    onClick={() => navigate('/login')}
                                >
                                    Sign In
                                </button>
                            </div>
                        ) : availableTickets.length === 0 ? (
                            <p style={{
                                color: 'var(--color-text-secondary)',
                                textAlign: 'center',
                                padding: 'var(--space-6)'
                            }}>
                                No available tickets for this flight.
                            </p>
                        ) : (
                            <>
                                <div style={{
                                    display: 'flex',
                                    flexDirection: 'column',
                                    gap: 'var(--space-2)',
                                    maxHeight: '400px',
                                    overflowY: 'auto',
                                    marginBottom: 'var(--space-4)'
                                }}>
                                    {availableTickets.map(ticket => {
                                        const isSelected = selectedTickets.includes(ticket.id);
                                        return (
                                            <div
                                                key={ticket.id}
                                                onClick={() => toggleTicket(ticket.id)}
                                                style={{
                                                    display: 'flex',
                                                    justifyContent: 'space-between',
                                                    alignItems: 'center',
                                                    padding: 'var(--space-3) var(--space-4)',
                                                    borderRadius: 'var(--radius-md)',
                                                    border: `1px solid ${isSelected ? 'var(--color-accent)' : 'var(--color-border)'}`,
                                                    background: isSelected ? 'rgba(99, 102, 241, 0.1)' : 'transparent',
                                                    cursor: 'pointer',
                                                    transition: 'all var(--transition-fast)',
                                                }}
                                            >
                                                <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)' }}>
                                                    {isSelected && <CheckCircle size={16} style={{ color: 'var(--color-accent)' }} />}
                                                    <span style={{ fontWeight: 600 }}>Seat {ticket.seat_number}</span>
                                                </div>
                                                <span style={{
                                                    color: 'var(--color-success)',
                                                    fontWeight: 700,
                                                    fontSize: 'var(--font-size-lg)'
                                                }}>
                                                    ${ticket.price}
                                                </span>
                                            </div>
                                        );
                                    })}
                                </div>

                                {selectedTickets.length > 0 && (
                                    <div>
                                        <div style={{
                                            display: 'flex',
                                            justifyContent: 'space-between',
                                            alignItems: 'center',
                                            padding: 'var(--space-3) 0',
                                            marginBottom: 'var(--space-3)',
                                            borderTop: '1px solid var(--color-border)',
                                            fontSize: 'var(--font-size-sm)',
                                            color: 'var(--color-text-secondary)',
                                        }}>
                                            <span>{selectedTickets.length} ticket{selectedTickets.length > 1 ? 's' : ''} selected</span>
                                            <span style={{ fontWeight: 700, color: 'var(--color-success)', fontSize: 'var(--font-size-lg)' }}>
                                                Total: ${selectedTotal.toFixed(2)}
                                            </span>
                                        </div>
                                        <button
                                            className="btn btn-success btn-lg"
                                            style={{ width: '100%' }}
                                            onClick={handleBook}
                                            disabled={bookingLoading}
                                        >
                                            <ShoppingCart size={18} />
                                            {bookingLoading
                                                ? 'Creating order...'
                                                : `Book ${selectedTickets.length} ticket${selectedTickets.length > 1 ? 's' : ''}`
                                            }
                                        </button>
                                    </div>
                                )}
                            </>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}
