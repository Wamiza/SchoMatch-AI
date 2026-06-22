import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Loader2 } from 'lucide-react';
import api from '../services/api';
import AgentPipeline from '../components/AgentPipeline';

const DiscoverPage = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    university: 'Stanford University',
    department: 'Computer Science',
    semester: 6,
    gpa: 3.8,
    degree_level: 'bachelor',
    skills: 'Python, Machine Learning, Data Analysis, Research',
    interests: 'Artificial Intelligence, Natural Language Processing',
    preferred_countries: 'United States, United Kingdom, Germany',
    opportunity_types: ['scholarship', 'internship', 'research']
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleCheckbox = (type) => {
    setFormData(prev => {
      const types = [...prev.opportunity_types];
      if (types.includes(type)) {
        return { ...prev, opportunity_types: types.filter(t => t !== type) };
      } else {
        return { ...prev, opportunity_types: [...types, type] };
      }
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      // Process comma-separated strings into arrays
      const payload = {
        ...formData,
        semester: parseInt(formData.semester),
        gpa: parseFloat(formData.gpa),
        skills: formData.skills.split(',').map(s => s.trim()).filter(Boolean),
        interests: formData.interests.split(',').map(s => s.trim()).filter(Boolean),
        preferred_countries: formData.preferred_countries.split(',').map(s => s.trim()).filter(Boolean),
      };

      console.log("Submitting:", payload);
      
      const response = await api.post('/discover', payload);
      
      // Store result in sessionStorage for the dashboard
      sessionStorage.setItem('lastDiscovery', JSON.stringify(response.data));
      
      navigate('/dashboard');
    } catch (error) {
      console.error('Discovery failed:', error);
      alert('An error occurred during discovery. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="flex flex-col items-center mb-8">
        <h1 className="text-center" style={{ fontSize: '2.5rem' }}>Discover <span className="gradient-text">Opportunities</span></h1>
        <p className="text-secondary text-center" style={{ maxWidth: '600px' }}>
          Tell us about your academic background and our specialized AI agents will find the perfect opportunities for you.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem', alignItems: 'start' }}>
        {/* Form Column */}
        <div className="card glass-panel">
          <form onSubmit={handleSubmit}>
            <h2 style={{ fontSize: '1.5rem', marginBottom: '1.5rem' }}>Academic Profile</h2>
            
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
              <div className="form-group">
                <label className="form-label">University</label>
                <input 
                  type="text" name="university" className="form-control" 
                  value={formData.university} onChange={handleChange} required 
                />
              </div>
              <div className="form-group">
                <label className="form-label">Department / Major</label>
                <input 
                  type="text" name="department" className="form-control" 
                  value={formData.department} onChange={handleChange} required 
                />
              </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '1rem' }}>
              <div className="form-group">
                <label className="form-label">Degree Level</label>
                <select name="degree_level" className="form-control form-select" value={formData.degree_level} onChange={handleChange}>
                  <option value="bachelor">Bachelor's</option>
                  <option value="master">Master's</option>
                  <option value="phd">PhD</option>
                </select>
              </div>
              <div className="form-group">
                <label className="form-label">Semester</label>
                <input 
                  type="number" name="semester" className="form-control" min="1" max="12"
                  value={formData.semester} onChange={handleChange} required 
                />
              </div>
              <div className="form-group">
                <label className="form-label">GPA (4.0 scale)</label>
                <input 
                  type="number" name="gpa" className="form-control" min="0" max="4.0" step="0.01"
                  value={formData.gpa} onChange={handleChange} required 
                />
              </div>
            </div>

            <div className="form-group">
              <label className="form-label">Skills (comma separated)</label>
              <input 
                type="text" name="skills" className="form-control" 
                value={formData.skills} onChange={handleChange} placeholder="Python, Data Analysis, Leadership..." 
              />
            </div>

            <div className="form-group">
              <label className="form-label">Interests (comma separated)</label>
              <input 
                type="text" name="interests" className="form-control" 
                value={formData.interests} onChange={handleChange} placeholder="AI, Renewable Energy, Public Policy..." 
              />
            </div>

            <div className="form-group">
              <label className="form-label">Preferred Countries (comma separated)</label>
              <input 
                type="text" name="preferred_countries" className="form-control" 
                value={formData.preferred_countries} onChange={handleChange} placeholder="United States, UK, Japan, Global..." 
              />
            </div>

            <div className="form-group">
              <label className="form-label">Opportunity Types</label>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.75rem', marginTop: '0.5rem' }}>
                {['scholarship', 'internship', 'research', 'fellowship', 'exchange', 'summer_school'].map(type => (
                  <label key={type} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer', background: 'rgba(255,255,255,0.05)', padding: '0.5rem 1rem', borderRadius: '2rem', border: `1px solid ${formData.opportunity_types.includes(type) ? 'var(--accent-primary)' : 'transparent'}` }}>
                    <input 
                      type="checkbox" 
                      checked={formData.opportunity_types.includes(type)}
                      onChange={() => handleCheckbox(type)}
                      style={{ accentColor: 'var(--accent-primary)' }}
                    />
                    <span style={{ textTransform: 'capitalize' }}>{type.replace('_', ' ')}</span>
                  </label>
                ))}
              </div>
            </div>

            <button 
              type="submit" 
              className="btn btn-primary w-full mt-4" 
              style={{ fontSize: '1.125rem' }}
              disabled={loading || formData.opportunity_types.length === 0}
            >
              {loading ? (
                <><Loader2 className="animate-spin" size={20} /> Running Agent Pipeline...</>
              ) : (
                <><Search size={20} /> Discover Opportunities</>
              )}
            </button>
          </form>
        </div>

        {/* Status Column */}
        <div style={{ position: 'sticky', top: '6rem' }}>
          <AgentPipeline isRunning={loading} />
        </div>
      </div>
    </div>
  );
};

export default DiscoverPage;
