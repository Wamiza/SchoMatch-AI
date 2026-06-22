import React from 'react';
import { Link } from 'react-router-dom';
import { Sparkles, Globe, Target, Award, ArrowRight } from 'lucide-react';

const HomePage = () => {
  return (
    <div className="container" style={{ paddingBottom: '4rem' }}>
      {/* Hero Section */}
      <div className="flex flex-col items-center justify-center text-center mt-8 mb-8" style={{ minHeight: '60vh' }}>
        <div className="badge badge-primary mb-4 animate-fade-in" style={{ animationDelay: '0.1s' }}>
          Powered by Google Gemini 2.0
        </div>
        <h1 className="animate-fade-in" style={{ fontSize: '4rem', marginBottom: '1.5rem', animationDelay: '0.2s' }}>
          Find Your Perfect <br/>
          <span className="gradient-text">Academic Opportunity</span>
        </h1>
        <p className="animate-fade-in text-secondary" style={{ fontSize: '1.25rem', maxWidth: '600px', marginBottom: '2.5rem', animationDelay: '0.3s' }}>
          SchoMatch-AI analyzes your profile and matches you with scholarships, internships, and research programs worldwide.
        </p>
        
        <div className="flex gap-4 animate-fade-in" style={{ animationDelay: '0.4s' }}>
          <Link to="/discover" style={{ textDecoration: 'none' }}>
            <button className="btn btn-primary" style={{ padding: '1rem 2rem', fontSize: '1.125rem' }}>
              <Sparkles size={20} />
              Start Discovering
            </button>
          </Link>
        </div>
      </div>

      {/* Features Section */}
      <div className="mt-8">
        <h2 className="text-center mb-8" style={{ fontSize: '2.5rem' }}>How It Works</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '2rem' }}>
          
          <div className="card glass-panel flex flex-col items-center text-center">
            <div style={{ background: 'rgba(37, 99, 235, 0.2)', padding: '1rem', borderRadius: '50%', marginBottom: '1.5rem', color: 'var(--accent-secondary)' }}>
              <Target size={32} />
            </div>
            <h3 style={{ fontSize: '1.25rem' }}>1. Build Profile</h3>
            <p className="text-secondary" style={{ marginTop: '0.5rem' }}>
              Enter your academic details, skills, and interests into our secure system.
            </p>
          </div>
          
          <div className="card glass-panel flex flex-col items-center text-center">
            <div style={{ background: 'rgba(124, 58, 237, 0.2)', padding: '1rem', borderRadius: '50%', marginBottom: '1.5rem', color: 'var(--accent-primary)' }}>
              <Globe size={32} />
            </div>
            <h3 style={{ fontSize: '1.25rem' }}>2. AI Search</h3>
            <p className="text-secondary" style={{ marginTop: '0.5rem' }}>
              Our multi-agent system scours global databases to find your best matches.
            </p>
          </div>
          
          <div className="card glass-panel flex flex-col items-center text-center">
            <div style={{ background: 'rgba(16, 185, 129, 0.2)', padding: '1rem', borderRadius: '50%', marginBottom: '1.5rem', color: 'var(--success)' }}>
              <Award size={32} />
            </div>
            <h3 style={{ fontSize: '1.25rem' }}>3. Get Matched</h3>
            <p className="text-secondary" style={{ marginTop: '0.5rem' }}>
              Receive a curated list with match scores and personalized action plans.
            </p>
          </div>

        </div>
      </div>
    </div>
  );
};

export default HomePage;
