import { Link } from 'react-router-dom';
import { CheckCircle, ShoppingCart } from 'lucide-react';

export default function PaymentSuccessPage() {
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
                background: 'rgba(16, 185, 129, 0.15)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                margin: '0 auto var(--space-6)'
            }}>
                <CheckCircle size={40} style={{ color: 'var(--color-success)' }} />
            </div>
            <h1 style={{
                fontSize: 'var(--font-size-3xl)',
                fontWeight: 800,
                marginBottom: 'var(--space-3)',
                color: 'var(--color-success)'
            }}>
                Payment Successful!
            </h1>
            <p style={{
                color: 'var(--color-text-secondary)',
                fontSize: 'var(--font-size-lg)',
                marginBottom: 'var(--space-8)'
            }}>
                Your booking has been confirmed. Thank you for choosing SkyPort!
            </p>
            <div style={{ display: 'flex', justifyContent: 'center', gap: 'var(--space-4)' }}>
                <Link to="/orders" className="btn btn-primary btn-lg">
                    <ShoppingCart size={18} />
                    View Orders
                </Link>
                <Link to="/flights" className="btn btn-secondary btn-lg">
                    Browse Flights
                </Link>
            </div>
        </div>
    );
}
