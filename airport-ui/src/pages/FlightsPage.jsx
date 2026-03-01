import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Plane, Clock, Calendar, ChevronLeft, ChevronRight } from 'lucide-react';
import { flightService } from '../api/flightService';

const statusBadge = (status) => `badge badge-${status}`;

const formatDate = (dt) => {
    if (!dt) return '—';
    const d = new Date(dt);
    return d.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' });
};

const formatTime = (dt) => {
    if (!dt) return '—';
    const d = new Date(dt);
    return d.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' });
};

export default function FlightsPage() {
    const [flights, setFlights] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [page, setPage] = useState(1);
    const [pagination, setPagination] = useState({ next: null, previous: null, count: 0 });
    const [statusFilter, setStatusFilter] = useState('');

    const fetchFlights = async (pageNum, status) => {
        setLoading(true);
        setError('');
        try {
            const params = { page: pageNum };
            if (status) params.status = status;
            const { data } = await flightService.getFlights(params);
            setFlights(data.results || []);
            setPagination({ next: data.next, previous: data.previous, count: data.count || 0 });
        } catch (err) {
            setError('Failed to load flights. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchFlights(page, statusFilter);
    }, [page, statusFilter]);

    const handleFilter = (status) => {
        setStatusFilter(status);
        setPage(1);
    };

    if (loading) {
        return (
            <div className="loading-container">
                <div className="spinner" />
                <p style={{ color: 'var(--color-text-secondary)' }}>Loading flights...</p>
            </div>
        );
    }

    return (
        <div>
            <div className="page-header">
                <h1 className="page-title">Flights</h1>
                <p className="page-subtitle">Browse all available flights and their schedules</p>
            </div>

            {/* Filters */}
            <div className="filter-bar">
                <select
                    className="form-input"
                    value={statusFilter}
                    onChange={(e) => handleFilter(e.target.value)}
                    style={{ flex: '0 0 200px', minWidth: '150px' }}
                >
                    <option value="">All Statuses</option>
                    <option value="scheduled">Scheduled</option>
                    <option value="boarding">Boarding</option>
                    <option value="departed">Departed</option>
                    <option value="delayed">Delayed</option>
                    <option value="cancelled">Cancelled</option>
                </select>
                <div style={{ flex: 1 }} />
                <span className="pagination-info" style={{ alignSelf: 'center' }}>
                    {pagination.count} flight{pagination.count !== 1 ? 's' : ''} found
                </span>
            </div>

            {error && <div className="alert alert-error">{error}</div>}

            {flights.length === 0 ? (
                <div className="empty-state">
                    <div className="empty-state-icon">✈️</div>
                    <div className="empty-state-title">No flights found</div>
                    <p>Try changing your filters or check back later.</p>
                </div>
            ) : (
                <div className="card-grid">
                    {flights.map((flight) => (
                        <Link
                            key={flight.id}
                            to={`/flights/${flight.id}`}
                            style={{ textDecoration: 'none', color: 'inherit' }}
                        >
                            <div className="card">
                                <div style={{
                                    display: 'flex',
                                    justifyContent: 'space-between',
                                    alignItems: 'center',
                                    marginBottom: 'var(--space-3)'
                                }}>
                                    <span style={{
                                        fontWeight: 700,
                                        fontSize: 'var(--font-size-lg)',
                                        color: 'var(--color-accent)'
                                    }}>
                                        {flight.number}
                                    </span>
                                    <span className={statusBadge(flight.status)}>
                                        {flight.status}
                                    </span>
                                </div>

                                <div className="flight-route">
                                    <div className="flight-airport">
                                        <div className="flight-airport-code">
                                            {flight.origin_iata || flight.origin}
                                        </div>
                                        <div className="flight-airport-name">
                                            {flight.origin_name || ''}
                                        </div>
                                    </div>
                                    <div className="flight-path">
                                        <div className="flight-path-line" />
                                    </div>
                                    <div className="flight-airport">
                                        <div className="flight-airport-code">
                                            {flight.destination_iata || flight.destination}
                                        </div>
                                        <div className="flight-airport-name">
                                            {flight.destination_name || ''}
                                        </div>
                                    </div>
                                </div>

                                <div className="flight-meta">
                                    <div className="flight-meta-item">
                                        <Calendar size={16} />
                                        <span>{formatDate(flight.departure_time)}</span>
                                    </div>
                                    <div className="flight-meta-item">
                                        <Clock size={16} />
                                        <span>{formatTime(flight.departure_time)} → {formatTime(flight.arrival_time)}</span>
                                    </div>
                                </div>
                            </div>
                        </Link>
                    ))}
                </div>
            )}

            {/* Pagination */}
            {(pagination.next || pagination.previous) && (
                <div className="pagination">
                    <button
                        className="btn btn-secondary btn-sm"
                        onClick={() => setPage(p => p - 1)}
                        disabled={!pagination.previous}
                    >
                        <ChevronLeft size={16} />
                        Previous
                    </button>
                    <span className="pagination-info">Page {page}</span>
                    <button
                        className="btn btn-secondary btn-sm"
                        onClick={() => setPage(p => p + 1)}
                        disabled={!pagination.next}
                    >
                        Next
                        <ChevronRight size={16} />
                    </button>
                </div>
            )}
        </div>
    );
}
