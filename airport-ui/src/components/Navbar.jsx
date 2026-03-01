import { Link, useLocation, useNavigate } from 'react-router-dom';
import { authService } from '../api/authService';
import {
    Plane, MapPin, ShoppingCart, CreditCard, LogOut, LogIn, UserPlus,
    Ticket, User
} from 'lucide-react';

export default function Navbar() {
    const location = useLocation();
    const navigate = useNavigate();
    const isAuth = authService.isAuthenticated();
    const username = authService.getUsername();

    const isActive = (path) => location.pathname === path ? 'navbar-link active' : 'navbar-link';

    const handleLogout = () => {
        authService.clearTokens();
        navigate('/login');
    };

    return (
        <nav className="navbar">
            <div className="navbar-inner">
                <Link to="/" className="navbar-brand">
                    <span className="navbar-brand-icon">✈️</span>
                    <span className="navbar-brand-gradient">SkyPort</span>
                </Link>

                <div className="navbar-links">
                    <Link to="/flights" className={isActive('/flights')}>
                        <Plane size={18} />
                        <span>Flights</span>
                    </Link>
                    <Link to="/airports" className={isActive('/airports')}>
                        <MapPin size={18} />
                        <span>Airports</span>
                    </Link>
                    <Link to="/tickets" className={isActive('/tickets')}>
                        <Ticket size={18} />
                        <span>Tickets</span>
                    </Link>
                    {isAuth && (
                        <>
                            <Link to="/orders" className={isActive('/orders')}>
                                <ShoppingCart size={18} />
                                <span>Orders</span>
                            </Link>
                            <Link to="/payments" className={isActive('/payments')}>
                                <CreditCard size={18} />
                                <span>Payments</span>
                            </Link>
                            <Link to="/profile" className={isActive('/profile')}>
                                <User size={18} />
                                <span>My Cabinet</span>
                            </Link>
                        </>
                    )}
                </div>

                <div className="navbar-actions">
                    {isAuth ? (
                        <>
                            <div className="navbar-user">
                                <div className="navbar-avatar">
                                    {(username || 'U')[0].toUpperCase()}
                                </div>
                                <span>{username}</span>
                            </div>
                            <button className="btn btn-secondary btn-sm" onClick={handleLogout}>
                                <LogOut size={16} />
                                <span>Logout</span>
                            </button>
                        </>
                    ) : (
                        <>
                            <Link to="/login" className="btn btn-secondary btn-sm">
                                <LogIn size={16} />
                                <span>Login</span>
                            </Link>
                            <Link to="/register" className="btn btn-primary btn-sm">
                                <UserPlus size={16} />
                                <span>Register</span>
                            </Link>
                        </>
                    )}
                </div>
            </div>
        </nav>
    );
}
