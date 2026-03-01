import { useState, useEffect } from 'react';
import { MapPin, Globe, ChevronLeft, ChevronRight, Map as MapIcon } from 'lucide-react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { airportService } from '../api/airportService';

// Fix default Leaflet marker icons
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
    iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
    iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
    shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

const airportIcon = new L.DivIcon({
    className: 'airport-marker',
    html: `<div style="
        width: 32px; height: 32px;
        background: linear-gradient(135deg, #6366f1, #06b6d4);
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        color: white; font-size: 14px; font-weight: 800;
        border: 2px solid white;
        box-shadow: 0 2px 10px rgba(99,102,241,0.5);
    ">✈</div>`,
    iconSize: [32, 32],
    iconAnchor: [16, 16],
    popupAnchor: [0, -18],
});

export default function AirportsPage() {
    const [airports, setAirports] = useState([]);
    const [allAirports, setAllAirports] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [page, setPage] = useState(1);
    const [pagination, setPagination] = useState({ next: null, previous: null, count: 0 });
    const [viewMode, setViewMode] = useState('map'); // 'map' or 'list'

    // Fetch paginated for list
    useEffect(() => {
        const fetchAirports = async () => {
            setLoading(true);
            try {
                const { data } = await airportService.getAirports({ page });
                setAirports(data.results || []);
                setPagination({ next: data.next, previous: data.previous, count: data.count || 0 });
            } catch (err) {
                setError('Failed to load airports.');
            } finally {
                setLoading(false);
            }
        };
        fetchAirports();
    }, [page]);

    // Fetch ALL for map (no pagination)
    useEffect(() => {
        const fetchAll = async () => {
            try {
                let all = [];
                let pg = 1;
                let hasMore = true;
                while (hasMore) {
                    const { data } = await airportService.getAirports({ page: pg });
                    all = [...all, ...(data.results || [])];
                    hasMore = !!data.next;
                    pg++;
                }
                setAllAirports(all);
            } catch (err) {
                // silently fail, list still works
            }
        };
        fetchAll();
    }, []);

    if (loading && airports.length === 0) {
        return (
            <div className="loading-container">
                <div className="spinner" />
                <p style={{ color: 'var(--color-text-secondary)' }}>Loading airports...</p>
            </div>
        );
    }

    const mapAirports = allAirports.filter(a => a.latitude && a.longitude);

    return (
        <div>
            <div className="page-header">
                <h1 className="page-title">Airports</h1>
                <p className="page-subtitle">{pagination.count} airports worldwide</p>
            </div>

            {/* View Toggle */}
            <div style={{
                display: 'flex', gap: 'var(--space-2)',
                marginBottom: 'var(--space-6)',
            }}>
                <button
                    className={`btn ${viewMode === 'map' ? 'btn-primary' : 'btn-secondary'} btn-sm`}
                    onClick={() => setViewMode('map')}
                >
                    <MapIcon size={16} /> Map View
                </button>
                <button
                    className={`btn ${viewMode === 'list' ? 'btn-primary' : 'btn-secondary'} btn-sm`}
                    onClick={() => setViewMode('list')}
                >
                    <Globe size={16} /> List View
                </button>
            </div>

            {error && <div className="alert alert-error">{error}</div>}

            {/* MAP VIEW */}
            {viewMode === 'map' && (
                <div className="card" style={{ padding: 0, overflow: 'hidden', marginBottom: 'var(--space-6)' }}>
                    <div style={{ height: '550px', width: '100%' }}>
                        {mapAirports.length > 0 ? (
                            <MapContainer
                                center={[30, 10]}
                                zoom={2}
                                style={{ height: '100%', width: '100%' }}
                                scrollWheelZoom={true}
                            >
                                <TileLayer
                                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                                    url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
                                />
                                {mapAirports.map(airport => (
                                    <Marker
                                        key={airport.id}
                                        position={[airport.latitude, airport.longitude]}
                                        icon={airportIcon}
                                    >
                                        <Popup>
                                            <div style={{
                                                fontFamily: 'Inter, sans-serif',
                                                minWidth: 180,
                                            }}>
                                                <div style={{
                                                    fontWeight: 800,
                                                    fontSize: '18px',
                                                    color: '#6366f1',
                                                    marginBottom: 4,
                                                }}>
                                                    {airport.iata_code}
                                                </div>
                                                <div style={{
                                                    fontWeight: 600,
                                                    fontSize: '14px',
                                                    color: '#1e293b',
                                                    marginBottom: 6,
                                                }}>
                                                    {airport.name}
                                                </div>
                                                <div style={{
                                                    fontSize: '12px',
                                                    color: '#64748b',
                                                    display: 'flex',
                                                    alignItems: 'center',
                                                    gap: 4,
                                                }}>
                                                    <span>🌍</span>
                                                    {airport.country?.name || '—'}
                                                </div>
                                                <div style={{
                                                    fontSize: '11px',
                                                    color: '#94a3b8',
                                                    marginTop: 4,
                                                }}>
                                                    {airport.latitude?.toFixed(4)}°, {airport.longitude?.toFixed(4)}°
                                                </div>
                                            </div>
                                        </Popup>
                                    </Marker>
                                ))}
                            </MapContainer>
                        ) : (
                            <div className="loading-container" style={{ height: '100%' }}>
                                <div className="spinner" />
                                <p style={{ color: 'var(--color-text-secondary)' }}>Loading map data...</p>
                            </div>
                        )}
                    </div>
                </div>
            )}

            {/* LIST VIEW */}
            {viewMode === 'list' && (
                <>
                    {airports.length === 0 ? (
                        <div className="empty-state">
                            <div className="empty-state-icon">🏢</div>
                            <div className="empty-state-title">No airports found</div>
                        </div>
                    ) : (
                        <div className="card-grid">
                            {airports.map((airport) => (
                                <div key={airport.id} className="card">
                                    <div style={{
                                        display: 'flex',
                                        justifyContent: 'space-between',
                                        alignItems: 'flex-start',
                                        marginBottom: 'var(--space-4)'
                                    }}>
                                        <div>
                                            <h3 style={{
                                                fontSize: 'var(--font-size-lg)',
                                                fontWeight: 700,
                                                marginBottom: 'var(--space-1)'
                                            }}>
                                                {airport.name}
                                            </h3>
                                            <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-2)' }}>
                                                <Globe size={14} style={{ color: 'var(--color-text-muted)' }} />
                                                <span style={{
                                                    color: 'var(--color-text-secondary)',
                                                    fontSize: 'var(--font-size-sm)'
                                                }}>
                                                    {airport.country?.name || '—'}
                                                </span>
                                            </div>
                                        </div>
                                        <span style={{
                                            background: 'linear-gradient(135deg, var(--color-accent), var(--color-accent-secondary))',
                                            color: 'white',
                                            padding: 'var(--space-1) var(--space-3)',
                                            borderRadius: 'var(--radius-md)',
                                            fontWeight: 800,
                                            fontSize: 'var(--font-size-lg)',
                                            letterSpacing: '0.1em'
                                        }}>
                                            {airport.iata_code}
                                        </span>
                                    </div>
                                    <div style={{
                                        display: 'flex',
                                        alignItems: 'center',
                                        gap: 'var(--space-2)',
                                        color: 'var(--color-text-muted)',
                                        fontSize: 'var(--font-size-xs)'
                                    }}>
                                        <MapPin size={12} />
                                        <span>
                                            {airport.latitude && airport.longitude
                                                ? `${airport.latitude.toFixed(2)}°, ${airport.longitude.toFixed(2)}°`
                                                : `Country Code: ${airport.country?.code || '—'}`
                                            }
                                        </span>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}

                    {(pagination.next || pagination.previous) && (
                        <div className="pagination">
                            <button
                                className="btn btn-secondary btn-sm"
                                onClick={() => setPage(p => p - 1)}
                                disabled={!pagination.previous}
                            >
                                <ChevronLeft size={16} /> Previous
                            </button>
                            <span className="pagination-info">Page {page}</span>
                            <button
                                className="btn btn-secondary btn-sm"
                                onClick={() => setPage(p => p + 1)}
                                disabled={!pagination.next}
                            >
                                Next <ChevronRight size={16} />
                            </button>
                        </div>
                    )}
                </>
            )}
        </div>
    );
}
