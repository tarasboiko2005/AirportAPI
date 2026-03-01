import { Outlet } from 'react-router-dom';
import Navbar from './Navbar';
import ChatWidget from './ChatWidget';
import { authService } from '../api/authService';

export default function Layout() {
    return (
        <>
            <Navbar />
            <main className="page">
                <div className="container">
                    <Outlet />
                </div>
            </main>
            {authService.isAuthenticated() && <ChatWidget />}
        </>
    );
}
