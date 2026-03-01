import { useState, useEffect } from 'react';
import { CreditCard, ChevronLeft, ChevronRight, DollarSign } from 'lucide-react';
import { paymentService } from '../api/paymentService';

const formatDate = (dt) => {
    if (!dt) return '—';
    return new Date(dt).toLocaleDateString('en-GB', {
        day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit'
    });
};

export default function PaymentsPage() {
    const [payments, setPayments] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [page, setPage] = useState(1);
    const [pagination, setPagination] = useState({ next: null, previous: null, count: 0 });

    useEffect(() => {
        const fetchPayments = async () => {
            setLoading(true);
            try {
                const { data } = await paymentService.getPayments({ page });
                setPayments(data.results || []);
                setPagination({ next: data.next, previous: data.previous, count: data.count || 0 });
            } catch (err) {
                setError('Failed to load payments.');
            } finally {
                setLoading(false);
            }
        };
        fetchPayments();
    }, [page]);

    if (loading) {
        return (
            <div className="loading-container">
                <div className="spinner" />
                <p style={{ color: 'var(--color-text-secondary)' }}>Loading payments...</p>
            </div>
        );
    }

    return (
        <div>
            <div className="page-header">
                <h1 className="page-title">Payment History</h1>
                <p className="page-subtitle">Track all your payment transactions</p>
            </div>

            {error && <div className="alert alert-error">{error}</div>}

            {payments.length === 0 ? (
                <div className="empty-state">
                    <div className="empty-state-icon">💳</div>
                    <div className="empty-state-title">No payments yet</div>
                    <p style={{ color: 'var(--color-text-secondary)' }}>
                        Your payment history will appear here
                    </p>
                </div>
            ) : (
                <div className="table-container">
                    <table className="table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Order</th>
                                <th>Amount</th>
                                <th>Currency</th>
                                <th>Status</th>
                                <th>Date</th>
                            </tr>
                        </thead>
                        <tbody>
                            {payments.map((payment) => (
                                <tr key={payment.id}>
                                    <td style={{ fontWeight: 600 }}>
                                        <CreditCard size={14} style={{
                                            marginRight: 6,
                                            verticalAlign: 'middle',
                                            color: 'var(--color-accent)'
                                        }} />
                                        #{payment.id}
                                    </td>
                                    <td>Order #{payment.order || '—'}</td>
                                    <td style={{ fontWeight: 700, color: 'var(--color-success)' }}>
                                        <DollarSign size={14} style={{ verticalAlign: 'middle' }} />
                                        {payment.amount}
                                    </td>
                                    <td>{(payment.currency || '').toUpperCase()}</td>
                                    <td>
                                        <span className={`badge badge-${payment.status}`}>
                                            {payment.status}
                                        </span>
                                    </td>
                                    <td style={{ color: 'var(--color-text-secondary)' }}>
                                        {formatDate(payment.created_at)}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
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
        </div>
    );
}
