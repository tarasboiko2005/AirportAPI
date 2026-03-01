import { Link } from 'react-router-dom';
import { XCircle, ShoppingCart, Plane } from 'lucide-react';

export default function PaymentCancelPage() {
    return (
        <div style={{
            textAlign: 'center',
            padding: 'var(--space-16) 0',
            maxWidth: '500px',
            margin: '0 auto'
        }}>
            <div style={{
                width: 80,
                height: 80,
                borderRadius: 'var(--radius-full)',
                background: 'rgba(239, 68, 68, 0.15)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                margin: '0 auto var(--space-6)'
            }}>
                <XCircle size={40} style={{ color: 'var(--color-error)' }} />
            </div>
            <h1 style={{
                fontSize: 'var(--font-size-3xl)',
                fontWeight: 800,
                marginBottom: 'var(--space-3)',
                color: 'var(--color-error)'
            }}>
                Payment Cancelled
            </h1>
            <p style={{
                color: 'var(--color-text-secondary)',
                fontSize: 'var(--font-size-lg)',
                marginBottom: 'var(--space-8)'
            }}>
                Your payment was not completed. You can try again from your orders page.
            </p>
            <div style={{ display: 'flex', justifyContent: 'center', gap: 'var(--space-4)' }}>
                <Link to="/orders" className="btn btn-primary btn-lg">
                    <ShoppingCart size={18} />
                    View Orders
                </Link>
                <Link to="/flights" className="btn btn-secondary btn-lg">
                    <Plane size={18} />
                    Browse Flights
                </Link>
            </div>
        </div>
    );
}
