import { Navigate } from 'react-router-dom';
import { authService } from '../api/authService';

export default function ProtectedRoute({ children }) {
    if (!authService.isAuthenticated()) {
        return <Navigate to="/login" replace />;
    }
    return children;
}
