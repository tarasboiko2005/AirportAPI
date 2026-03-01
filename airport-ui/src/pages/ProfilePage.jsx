import { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import {
    User, Mail, Calendar, ShoppingCart, Ticket,
    CreditCard, Clock, Plane, DollarSign, Package,
    CheckCircle, Timer, AlertTriangle
} from 'lucide-react';
import { userService } from '../api/userService';

const formatDate = (dt) => {
    if (!dt) return '—';
    return new Date(dt).toLocaleDateString('en-GB', {
        day: '2-digit', month: 'short', year: 'numeric',
    });
};

const formatDateTime = (dt) => {
    if (!dt) return '—';
    return new Date(dt).toLocaleDateString('en-GB', {
        day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit',
    });
};

const formatCountdown = (seconds) => {
    if (seconds <= 0) return '0:00';
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m}:${s.toString().padStart(2, '0')}`;
};

export default function ProfilePage() {
    const [profile, setProfile] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [timers, setTimers] = useState({});
    const intervalRef = useRef(null);

    useEffect(() => {
        const fetchProfile = async () => {
            try {
                const { data } = await userService.getProfile();
                setProfile(data);

                // Initialize timers
                const t = {};
                (data.orders || []).forEach(o => {
                    if (o.time_remaining != null && o.status === 'booked') {
                        t[o.id] = o.time_remaining;
                    }
                });
                setTimers(t);
            } catch (err) {
                setError('Failed to load profile.');
            } finally {
                setLoading(false);
            }
        };
        fetchProfile();
    }, []);

    // Countdown
    useEffect(() => {
        intervalRef.current = setInterval(() => {
            setTimers(prev => {
                const next = { ...prev };
                Object.keys(next).forEach(id => {
                    if (next[id] > 0) next[id] -= 1;
                });
                return next;
            });
        }, 1000);
        return () => clearInterval(intervalRef.current);
    }, []);

    if (loading) {
        return (
            <div className="loading-container">
                <div className="spinner" />
                <p style={{ color: 'var(--color-text-secondary)' }}>Loading profile...</p>
            </div>
        );
    }

    if (error || !profile) {
        return (
            <div className="empty-state">
                <div className="empty-state-icon">😕</div>
                <div className="empty-state-title">{error || 'Profile not found'}</div>
            </div>
        );
    }

    const orders = profile.orders || [];
    const paidOrders = orders.filter(o => o.status === 'paid');
    const totalSpent = paidOrders.reduce((sum, o) => sum + parseFloat(o.amount || 0), 0);
    const totalTickets = paidOrders.reduce((sum, o) => sum + (o.tickets_info?.length || 0), 0);
    const bookedOrders = orders.filter(o => o.status === 'booked');

    return (
        <div>
            <div className="page-header">
                <h1 className="page-title">My Cabinet</h1>
                <p className="page-subtitle">Your personal account overview</p>
            </div>

            {/* User Info Card */}
            <div className="card" style={{ marginBottom: 'var(--space-6)' }}>
                <div style={{
                    display: 'flex', alignItems: 'center',
                    gap: 'var(--space-5)', flexWrap: 'wrap',
                }}>
                    <div style={{
                        width: 72, height: 72,
                        borderRadius: 'var(--radius-full)',
                        background: 'linear-gradient(135deg, var(--color-accent), var(--color-accent-secondary))',
                        display: 'flex', alignItems: 'center', justifyContent: 'center',
                        fontSize: 'var(--font-size-3xl)',
                        fontWeight: 800, color: 'white', flexShrink: 0,
                    }}>
                        {(profile.username || 'U')[0].toUpperCase()}
                    </div>
                    <div style={{ flex: 1 }}>
                        <h2 style={{ fontSize: 'var(--font-size-2xl)', fontWeight: 700, marginBottom: 'var(--space-1)' }}>
                            {profile.username}
                        </h2>
                        <div style={{
                            display: 'flex', gap: 'var(--space-5)',
                            color: 'var(--color-text-secondary)',
                            fontSize: 'var(--font-size-sm)', flexWrap: 'wrap',
                        }}>
                            <span><Mail size={14} style={{ verticalAlign: 'middle', marginRight: 4 }} />{profile.email}</span>
                            <span><Calendar size={14} style={{ verticalAlign: 'middle', marginRight: 4 }} />Joined {formatDate(profile.date_joined)}</span>
                        </div>
                    </div>
                </div>
            </div>

            {/* Stats */}
            <div className="stats-row" style={{ marginBottom: 'var(--space-8)' }}>
                <div className="stat-card">
                    <div style={{ color: 'var(--color-accent)', marginBottom: 'var(--space-2)' }}>
                        <ShoppingCart size={24} />
                    </div>
                    <div className="stat-value">{orders.length}</div>
                    <div className="stat-label">Total Orders</div>
                </div>
                <div className="stat-card">
                    <div style={{ color: 'var(--color-success)', marginBottom: 'var(--space-2)' }}>
                        <DollarSign size={24} />
                    </div>
                    <div className="stat-value">${totalSpent.toFixed(2)}</div>
                    <div className="stat-label">Total Paid</div>
                </div>
                <div className="stat-card">
                    <div style={{ color: 'var(--color-accent-secondary)', marginBottom: 'var(--space-2)' }}>
                        <Ticket size={24} />
                    </div>
                    <div className="stat-value">{totalTickets}</div>
                    <div className="stat-label">Confirmed Tickets</div>
                </div>
                <div className="stat-card">
                    <div style={{ color: 'var(--color-warning)', marginBottom: 'var(--space-2)' }}>
                        <Timer size={24} />
                    </div>
                    <div className="stat-value">{bookedOrders.length}</div>
                    <div className="stat-label">Awaiting Payment</div>
                </div>
            </div>

            {/* Orders with Tickets */}
            <h2 style={{
                fontSize: 'var(--font-size-2xl)', fontWeight: 700,
                marginBottom: 'var(--space-5)',
                display: 'flex', alignItems: 'center', gap: 'var(--space-3)',
            }}>
                <Package size={24} style={{ color: 'var(--color-accent)' }} />
                My Orders & Tickets
            </h2>

            {orders.length === 0 ? (
                <div className="empty-state">
                    <div className="empty-state-icon">📦</div>
                    <div className="empty-state-title">No orders yet</div>
                    <p style={{ color: 'var(--color-text-secondary)', marginBottom: 'var(--space-5)' }}>
                        Browse available tickets and create your first booking!
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
                                {/* Order Header */}
                                <div style={{
                                    display: 'flex', justifyContent: 'space-between',
                                    alignItems: 'center', marginBottom: 'var(--space-4)',
                                    flexWrap: 'wrap', gap: 'var(--space-3)',
                                }}>
                                    <div>
                                        <h3 style={{ fontWeight: 700, fontSize: 'var(--font-size-lg)' }}>
                                            <ShoppingCart size={18} style={{ marginRight: 8, verticalAlign: 'middle', color: 'var(--color-accent)' }} />
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
                                        {/* Countdown */}
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
                                                    color: isUrgent ? 'var(--color-error)' : 'var(--color-warning)',
                                                }} />
                                                <span style={{
                                                    fontWeight: 800, fontSize: 'var(--font-size-lg)',
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

                                {/* Tickets */}
                                {order.tickets_info && order.tickets_info.length > 0 && (
                                    <div style={{
                                        padding: 'var(--space-4)',
                                        background: 'rgba(0,0,0,0.2)',
                                        borderRadius: 'var(--radius-lg)',
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
                                                        <span className={`badge badge-${t.status}`}>{t.status}</span>
                                                        <span style={{ fontWeight: 700, color: 'var(--color-success)' }}>${t.price}</span>
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                )}

                                {/* Status footer */}
                                {isPaid && (
                                    <div style={{
                                        display: 'flex', alignItems: 'center', justifyContent: 'center',
                                        gap: 'var(--space-2)', padding: 'var(--space-3)',
                                        marginTop: 'var(--space-4)',
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
