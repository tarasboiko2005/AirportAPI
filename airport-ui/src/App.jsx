import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import ProtectedRoute from './components/ProtectedRoute';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import FlightsPage from './pages/FlightsPage';
import FlightDetailPage from './pages/FlightDetailPage';
import AirportsPage from './pages/AirportsPage';
import TicketsPage from './pages/TicketsPage';
import OrdersPage from './pages/OrdersPage';
import PaymentsPage from './pages/PaymentsPage';
import ProfilePage from './pages/ProfilePage';
import PaymentSuccessPage from './pages/PaymentSuccessPage';
import PaymentCancelPage from './pages/PaymentCancelPage';

export default function App() {
    return (
        <Routes>
            <Route element={<Layout />}>
                <Route path="/" element={<HomePage />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />
                <Route path="/flights" element={<FlightsPage />} />
                <Route path="/flights/:id" element={<FlightDetailPage />} />
                <Route path="/airports" element={<AirportsPage />} />
                <Route path="/tickets" element={<TicketsPage />} />
                <Route
                    path="/orders"
                    element={<ProtectedRoute><OrdersPage /></ProtectedRoute>}
                />
                <Route
                    path="/payments"
                    element={<ProtectedRoute><PaymentsPage /></ProtectedRoute>}
                />
                <Route
                    path="/profile"
                    element={<ProtectedRoute><ProfilePage /></ProtectedRoute>}
                />
                <Route path="/payment/success" element={<PaymentSuccessPage />} />
                <Route path="/payment/cancel" element={<PaymentCancelPage />} />
            </Route>
        </Routes>
    );
}
