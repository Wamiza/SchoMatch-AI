import React from 'react';
import { Routes, Route, Link, useLocation } from 'react-router-dom';
import { GraduationCap, Sparkles, LayoutDashboard } from 'lucide-react';

// Pages will be imported here
import HomePage from './pages/HomePage';
import DiscoverPage from './pages/DiscoverPage';
import DashboardPage from './pages/DashboardPage';

function App() {
  const location = useLocation();
  
  return (
    <>
      <div className="bg-blob blob-1"></div>
      <div className="bg-blob blob-2"></div>
      
      <nav className="navbar">
        <div className="container flex items-center justify-between w-full">
          <Link to="/" className="flex items-center gap-2" style={{ textDecoration: 'none', color: 'white' }}>
            <div style={{ background: 'linear-gradient(135deg, var(--accent-primary), var(--accent-tertiary))', padding: '0.5rem', borderRadius: '0.5rem' }}>
              <GraduationCap size={24} color="white" />
            </div>
            <span style={{ fontSize: '1.25rem', fontWeight: 'bold' }}>SchoMatch<span className="gradient-text">AI</span></span>
          </Link>
          
          <div className="flex items-center gap-6">
            <Link 
              to="/discover" 
              className="flex items-center gap-2" 
              style={{ 
                textDecoration: 'none', 
                color: location.pathname === '/discover' ? 'white' : 'var(--text-secondary)',
                fontWeight: location.pathname === '/discover' ? '600' : '500'
              }}
            >
              <Sparkles size={18} />
              <span>Discover</span>
            </Link>
            <Link 
              to="/dashboard" 
              className="flex items-center gap-2"
              style={{ 
                textDecoration: 'none', 
                color: location.pathname === '/dashboard' ? 'white' : 'var(--text-secondary)',
                fontWeight: location.pathname === '/dashboard' ? '600' : '500'
              }}
            >
              <LayoutDashboard size={18} />
              <span>Dashboard</span>
            </Link>
          </div>
        </div>
      </nav>

      <main className="main-content">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/discover" element={<DiscoverPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
        </Routes>
      </main>
    </>
  );
}

export default App;
