import { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import {
    ShoppingCart, Clock, CreditCard, Ticket, Plane,
    CheckCircle, AlertTriangle, Timer
} from 'lucide-react';
import { orderService } from '../api/orderService';
import { paymentService } from '../api/paymentService';

const formatDateTime = (dt) => {
    if (!dt) return '—';
    return new Date(dt).toLocaleDateString('en-GB', {
        day: '2-digit', month: 'short', year: 'numeric',
        hour: '2-digit', minute: '2-digit',
    });
};

const formatCountdown = (seconds) => {
    if (seconds <= 0) return '0:00';
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m}:${s.toString().padStart(2, '0')}`;
};

export default function OrdersPage() {
    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [payingId, setPayingId] = useState(null);
    const [timers, setTimers] = useState({});
    const intervalRef = useRef(null);

    const fetchOrders = async () => {
        setLoading(true);
        try {
            const { data } = await orderService.getOrders();
            const list = data.results || data || [];
            setOrders(list);

            // Initialize timers from time_remaining
            const t = {};
            list.forEach(o => {
                if (o.time_remaining != null && o.status === 'booked') {
                    t[o.id] = o.time_remaining;
                }
            });
            setTimers(t);
        } catch (err) {
            setError('Failed to load orders.');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchOrders();
    }, []);

    // Countdown timer
    useEffect(() => {
        intervalRef.current = setInterval(() => {
            setTimers(prev => {
                const next = { ...prev };
                let anyExpired = false;
                Object.keys(next).forEach(id => {
                    if (next[id] > 0) {
                        next[id] -= 1;
                    }
                    if (next[id] <= 0) {
                        anyExpired = true;
                    }
                });
                if (anyExpired) {
                    // Re-fetch to clean up expired orders
                    setTimeout(() => fetchOrders(), 500);
                }
                return next;
            });
        }, 1000);

        return () => clearInterval(intervalRef.current);
    }, []);

    const handlePay = async (orderId) => {
        setPayingId(orderId);
        try {
            const { data } = await paymentService.createCheckoutSession(orderId);
            if (data.url) {
                window.location.href = data.url;
            }
        } catch (err) {
            setError('Failed to initiate payment. Please try again.');
            setPayingId(null);
        }
    };

    if (loading) {
        return (
            <div className="loading-container">
                <div className="spinner" />
                <p style={{ color: 'var(--color-text-secondary)' }}>Loading orders...</p>
            </div>
        );
    }

    return (
        <div>
            <div className="page-header">
                <h1 className="page-title">My Orders</h1>
                <p className="page-subtitle">Manage your flight bookings and payments</p>
            </div>

            {error && <div className="alert alert-error">{error}</div>}

            {orders.length === 0 ? (
                <div className="empty-state">
                    <div className="empty-state-icon">📦</div>
                    <div className="empty-state-title">No orders yet</div>
                    <p style={{ color: 'var(--color-text-secondary)', marginBottom: 'var(--space-5)' }}>
                        Browse available tickets to create your first booking!
                    </p>
                    <Link to="/tickets" className="btn btn-primary">
                        <Ticket size={16} /> Browse Tickets
                    </Link>
                </div>
            ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-5)' }}>
                    {orders.map(order => {
                        const isBooked = order.status === 'booked';
                        const isPaid = order.status === 'paid';
                        const remaining = timers[order.id];
                        const isUrgent = remaining != null && remaining < 120;

                        return (
                            <div key={order.id} className="card">
                                {/* Header */}
                                <div style={{
                                    display: 'flex', justifyContent: 'space-between',
                                    alignItems: 'center', flexWrap: 'wrap',
                                    gap: 'var(--space-3)', marginBottom: 'var(--space-4)',
                                }}>
                                    <div>
                                        <h3 style={{ fontWeight: 700, fontSize: 'var(--font-size-lg)' }}>
                                            <ShoppingCart size={18} style={{
                                                marginRight: 8, verticalAlign: 'middle',
                                                color: 'var(--color-accent)'
                                            }} />
                                            Order #{order.id}
                                        </h3>
                                        <div style={{
                                            display: 'flex', gap: 'var(--space-4)',
                                            marginTop: 'var(--space-2)',
                                            fontSize: 'var(--font-size-sm)',
                                            color: 'var(--color-text-secondary)',
                                            flexWrap: 'wrap',
                                        }}>
                                            <span>
                                                <Clock size={14} style={{ verticalAlign: 'middle', marginRight: 4 }} />
                                                {formatDateTime(order.created_at)}
                                            </span>
                                            <span>
                                                <CreditCard size={14} style={{ verticalAlign: 'middle', marginRight: 4 }} />
                                                {order.payment_method}
                                            </span>
                                        </div>
                                    </div>

                                    <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)' }}>
                                        {/* Countdown timer for booked orders */}
                                        {isBooked && remaining != null && (
                                            <div style={{
                                                display: 'flex', alignItems: 'center',
                                                gap: 'var(--space-2)',
                                                padding: 'var(--space-2) var(--space-3)',
                                                borderRadius: 'var(--radius-md)',
                                                background: isUrgent ? 'rgba(239, 68, 68, 0.15)' : 'rgba(245, 158, 11, 0.15)',
                                                border: `1px solid ${isUrgent ? 'rgba(239, 68, 68, 0.3)' : 'rgba(245, 158, 11, 0.3)'}`,
                                                animation: isUrgent ? 'pulse 1s infinite' : 'none',
                                            }}>
                                                <Timer size={16} style={{
                                                    color: isUrgent ? 'var(--color-error)' : 'var(--color-warning)'
                                                }} />
                                                <span style={{
                                                    fontWeight: 800,
                                                    fontSize: 'var(--font-size-lg)',
                                                    fontVariantNumeric: 'tabular-nums',
                                                    color: isUrgent ? 'var(--color-error)' : 'var(--color-warning)',
                                                }}>
                                                    {formatCountdown(remaining)}
                                                </span>
                                            </div>
                                        )}

                                        <span className={`badge badge-${order.status}`}>
                                            {isPaid && <CheckCircle size={12} style={{ marginRight: 4 }} />}
                                            {order.status}
                                        </span>
                                        <span style={{
                                            fontWeight: 800, fontSize: 'var(--font-size-2xl)',
                                            color: 'var(--color-success)',
                                        }}>
                                            ${order.amount}
                                        </span>
                                    </div>
                                </div>

                                {/* Timer warning */}
                                {isBooked && isUrgent && (
                                    <div style={{
                                        display: 'flex', alignItems: 'center', gap: 'var(--space-2)',
                                        padding: 'var(--space-3) var(--space-4)',
                                        marginBottom: 'var(--space-4)',
                                        background: 'rgba(239, 68, 68, 0.1)',
                                        borderRadius: 'var(--radius-md)',
                                        border: '1px solid rgba(239, 68, 68, 0.2)',
                                        fontSize: 'var(--font-size-sm)',
                                        color: 'var(--color-error)',
                                    }}>
                                        <AlertTriangle size={16} />
                                        <span>Hurry! This booking expires soon. Pay now to secure your tickets.</span>
                                    </div>
                                )}

                                {/* Tickets */}
                                {order.tickets_info && order.tickets_info.length > 0 && (
                                    <div style={{
                                        padding: 'var(--space-4)',
                                        background: 'rgba(0,0,0,0.2)',
                                        borderRadius: 'var(--radius-lg)',
                                        marginBottom: isBooked ? 'var(--space-4)' : 0,
                                    }}>
                                        <div style={{
                                            fontSize: 'var(--font-size-xs)', fontWeight: 600,
                                            textTransform: 'uppercase', color: 'var(--color-text-muted)',
                                            marginBottom: 'var(--space-3)', letterSpacing: '0.05em',
                                        }}>
                                            <Ticket size={12} style={{ marginRight: 4, verticalAlign: 'middle' }} />
                                            Tickets ({order.tickets_info.length})
                                        </div>
                                        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-2)' }}>
                                            {order.tickets_info.map(t => (
                                                <div key={t.id} style={{
                                                    display: 'flex', justifyContent: 'space-between',
                                                    alignItems: 'center',
                                                    padding: 'var(--space-3) var(--space-4)',
                                                    background: 'var(--color-bg-card)',
                                                    border: '1px solid var(--color-border)',
                                                    borderRadius: 'var(--radius-md)',
                                                    flexWrap: 'wrap', gap: 'var(--space-2)',
                                                }}>
                                                    <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)' }}>
                                                        <Plane size={14} style={{ color: 'var(--color-accent)' }} />
                                                        <span style={{ fontWeight: 600 }}>
                                                            {t.flight_info
                                                                ? `${t.flight_info.origin_iata} → ${t.flight_info.destination_iata}`
                                                                : `Flight #${t.flight}`}
                                                        </span>
                                                        {t.flight_info && (
                                                            <span style={{ color: 'var(--color-text-muted)', fontSize: 'var(--font-size-sm)' }}>
                                                                {t.flight_info.number}
                                                            </span>
                                                        )}
                                                    </div>
                                                    <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-4)' }}>
                                                        <span style={{ fontWeight: 700 }}>Seat {t.seat_number}</span>
                                                        <span style={{ fontWeight: 700, color: 'var(--color-success)' }}>
                                                            ${t.price}
                                                        </span>
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                )}

                                {/* Pay button for booked orders */}
                                {isBooked && (
                                    <button
                                        className="btn btn-success btn-lg"
                                        style={{ width: '100%' }}
                                        onClick={() => handlePay(order.id)}
                                        disabled={payingId === order.id}
                                    >
                                        <CreditCard size={18} />
                                        {payingId === order.id ? 'Redirecting to payment...' : 'Pay Now'}
                                    </button>
                                )}

                                {/* Paid badge */}
                                {isPaid && (
                                    <div style={{
                                        display: 'flex', alignItems: 'center', justifyContent: 'center',
                                        gap: 'var(--space-2)', padding: 'var(--space-3)',
                                        background: 'rgba(34, 197, 94, 0.1)',
                                        border: '1px solid rgba(34, 197, 94, 0.2)',
                                        borderRadius: 'var(--radius-md)',
                                        color: 'var(--color-success)', fontWeight: 700,
                                    }}>
                                        <CheckCircle size={18} /> Payment confirmed
                                    </div>
                                )}
                            </div>
                        );
                    })}
                </div>
            )}
        </div>
    );
}
