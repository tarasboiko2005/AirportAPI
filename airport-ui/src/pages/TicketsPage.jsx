import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
    Ticket, Plane, Clock, Calendar, ShoppingCart,
    ChevronLeft, ChevronRight, CheckCircle, Filter
} from 'lucide-react';
import { ticketService } from '../api/ticketService';
import { orderService } from '../api/orderService';
import { authService } from '../api/authService';

const formatDate = (dt) => {
    if (!dt) return '—';
    return new Date(dt).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' });
};

const formatTime = (dt) => {
    if (!dt) return '—';
    return new Date(dt).toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' });
};

export default function TicketsPage() {
    const isAuth = authService.isAuthenticated();

    const [tickets, setTickets] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [selectedTickets, setSelectedTickets] = useState([]);
    const [bookingLoading, setBookingLoading] = useState(false);
    const [bookingSuccess, setBookingSuccess] = useState('');
    const [statusFilter, setStatusFilter] = useState('available');

    const fetchTickets = async () => {
        setLoading(true);
        setError('');
        try {
            const params = {};
            if (statusFilter) params.status = statusFilter;
            const { data } = await ticketService.getTickets(params);
            setTickets(data.results || data || []);
        } catch (err) {
            setError('Failed to load tickets. Please log in to view available tickets.');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (isAuth) {
            fetchTickets();
        } else {
            setLoading(false);
        }
    }, [statusFilter, isAuth]);

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
        setBookingSuccess('');
        try {
            await orderService.createOrder({
                tickets: selectedTickets,
                payment_method: 'card',
                currency: 'USD',
            });
            setBookingSuccess(`Order created with ${selectedTickets.length} ticket(s)! Go to My Orders to pay.`);
            setSelectedTickets([]);
            fetchTickets();
        } catch (err) {
            const data = err.response?.data;
            setError(data ? (typeof data === 'string' ? data : JSON.stringify(data)) : 'Booking failed.');
        } finally {
            setBookingLoading(false);
        }
    };

    const selectedTotal = tickets
        .filter(t => selectedTickets.includes(t.id))
        .reduce((sum, t) => sum + parseFloat(t.price), 0);

    if (loading) {
        return (
            <div className="loading-container">
                <div className="spinner" />
                <p style={{ color: 'var(--color-text-secondary)' }}>Loading tickets...</p>
            </div>
        );
    }

    if (!isAuth) {
        return (
            <div className="empty-state">
                <div className="empty-state-icon">🎫</div>
                <div className="empty-state-title">Sign in to browse tickets</div>
                <p style={{ color: 'var(--color-text-secondary)', marginBottom: 'var(--space-6)' }}>
                    You need to be logged in to view and book available tickets.
                </p>
                <Link to="/login" className="btn btn-primary">Sign In</Link>
            </div>
        );
    }

    return (
        <div>
            <div className="page-header">
                <h1 className="page-title">Browse Tickets</h1>
                <p className="page-subtitle">Find and book your perfect flight tickets</p>
            </div>

            {/* Filters */}
            <div className="filter-bar">
                <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)' }}>
                    <Filter size={16} style={{ color: 'var(--color-text-muted)' }} />
                    <select
                        className="form-input"
                        value={statusFilter}
                        onChange={(e) => {
                            setStatusFilter(e.target.value);
                            setSelectedTickets([]);
                        }}
                        style={{ width: '180px', minWidth: '150px' }}
                    >
                        <option value="available">Available</option>
                        <option value="booked">Booked</option>
                        <option value="">All Tickets</option>
                    </select>
                </div>
                <div style={{ flex: 1 }} />
                <span className="pagination-info">
                    {tickets.length} ticket{tickets.length !== 1 ? 's' : ''} found
                </span>
            </div>

            {error && <div className="alert alert-error">{error}</div>}
            {bookingSuccess && (
                <div className="alert alert-success">
                    <CheckCircle size={16} />{bookingSuccess}
                    <Link to="/orders" style={{ marginLeft: 'var(--space-2)', fontWeight: 700 }}>
                        View Orders →
                    </Link>
                </div>
            )}

            {tickets.length === 0 ? (
                <div className="empty-state">
                    <div className="empty-state-icon">🎫</div>
                    <div className="empty-state-title">No tickets found</div>
                    <p>Try changing your filters or check back later.</p>
                </div>
            ) : (
                <>
                    {/* Selection Bar */}
                    {statusFilter === 'available' && selectedTickets.length > 0 && (
                        <div className="card" style={{
                            position: 'sticky',
                            top: '72px',
                            zIndex: 50,
                            marginBottom: 'var(--space-5)',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'space-between',
                            background: 'rgba(99, 102, 241, 0.12)',
                            borderColor: 'var(--color-accent)',
                        }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)' }}>
                                <Ticket size={18} style={{ color: 'var(--color-accent)' }} />
                                <span style={{ fontWeight: 600 }}>
                                    {selectedTickets.length} ticket{selectedTickets.length > 1 ? 's' : ''} selected
                                </span>
                                <span style={{
                                    fontWeight: 800,
                                    fontSize: 'var(--font-size-xl)',
                                    color: 'var(--color-success)',
                                }}>
                                    ${selectedTotal.toFixed(2)}
                                </span>
                            </div>
                            <button
                                className="btn btn-success"
                                onClick={handleBook}
                                disabled={bookingLoading}
                            >
                                <ShoppingCart size={16} />
                                {bookingLoading ? 'Creating Order...' : 'Create Order'}
                            </button>
                        </div>
                    )}

                    <div className="ticket-list">
                        {tickets.map(ticket => {
                            const fi = ticket.flight_info;
                            const isSelected = selectedTickets.includes(ticket.id);
                            const isAvailable = ticket.status === 'available';

                            return (
                                <div
                                    key={ticket.id}
                                    className="card"
                                    onClick={() => isAvailable && toggleTicket(ticket.id)}
                                    style={{
                                        cursor: isAvailable ? 'pointer' : 'default',
                                        borderColor: isSelected ? 'var(--color-accent)' : undefined,
                                        background: isSelected ? 'rgba(99, 102, 241, 0.08)' : undefined,
                                        marginBottom: 'var(--space-3)',
                                    }}
                                >
                                    <div style={{
                                        display: 'flex',
                                        justifyContent: 'space-between',
                                        alignItems: 'center',
                                        flexWrap: 'wrap',
                                        gap: 'var(--space-3)',
                                    }}>
                                        {/* Left: flight info */}
                                        <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-4)', flex: '1 1 300px' }}>
                                            <div style={{
                                                width: 44, height: 44,
                                                borderRadius: 'var(--radius-lg)',
                                                background: isSelected
                                                    ? 'linear-gradient(135deg, var(--color-accent), var(--color-accent-secondary))'
                                                    : 'rgba(99, 102, 241, 0.1)',
                                                display: 'flex', alignItems: 'center', justifyContent: 'center',
                                                flexShrink: 0,
                                                transition: 'all var(--transition-fast)',
                                            }}>
                                                {isSelected
                                                    ? <CheckCircle size={20} style={{ color: 'white' }} />
                                                    : <Plane size={20} style={{ color: 'var(--color-accent)' }} />
                                                }
                                            </div>
                                            <div>
                                                <div style={{ fontWeight: 700, fontSize: 'var(--font-size-base)' }}>
                                                    {fi ? `${fi.origin_iata} → ${fi.destination_iata}` : `Flight #${ticket.flight}`}
                                                </div>
                                                <div style={{
                                                    fontSize: 'var(--font-size-sm)',
                                                    color: 'var(--color-text-secondary)',
                                                    display: 'flex',
                                                    gap: 'var(--space-3)',
                                                    marginTop: 2,
                                                }}>
                                                    {fi && (
                                                        <>
                                                            <span style={{ color: 'var(--color-accent)' }}>{fi.number}</span>
                                                            <span>
                                                                <Calendar size={12} style={{ verticalAlign: 'middle', marginRight: 2 }} />
                                                                {formatDate(fi.departure_time)}
                                                            </span>
                                                            <span>
                                                                <Clock size={12} style={{ verticalAlign: 'middle', marginRight: 2 }} />
                                                                {formatTime(fi.departure_time)}
                                                            </span>
                                                        </>
                                                    )}
                                                </div>
                                            </div>
                                        </div>

                                        {/* Middle: seat */}
                                        <div style={{ textAlign: 'center', minWidth: 80 }}>
                                            <div style={{
                                                fontSize: 'var(--font-size-xs)',
                                                color: 'var(--color-text-muted)',
                                                textTransform: 'uppercase',
                                                letterSpacing: '0.05em',
                                            }}>Seat</div>
                                            <div style={{
                                                fontWeight: 800,
                                                fontSize: 'var(--font-size-xl)',
                                                marginTop: 2,
                                            }}>{ticket.seat_number}</div>
                                        </div>

                                        {/* Right: price + status */}
                                        <div style={{
                                            display: 'flex',
                                            alignItems: 'center',
                                            gap: 'var(--space-4)',
                                        }}>
                                            <span className={`badge badge-${ticket.status}`}>
                                                {ticket.status}
                                            </span>
                                            <span style={{
                                                fontWeight: 800,
                                                fontSize: 'var(--font-size-xl)',
                                                color: 'var(--color-success)',
                                                minWidth: 80,
                                                textAlign: 'right',
                                            }}>
                                                ${ticket.price}
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                </>
            )}
        </div>
    );
}
