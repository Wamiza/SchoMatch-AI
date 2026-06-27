import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Loader2 } from 'lucide-react';
import api from '../services/api';
import AgentPipeline from '../components/AgentPipeline';

const UNIVERSITIES = [
  "NUST", "LUMS", "IBA Karachi", "FAST-NUCES", "UET Lahore", "UET Peshawar",
  "Quaid-i-Azam University", "University of Karachi", "COMSATS University",
  "Air University", "NED University", "Bahria University", "GIKI", "ITU Lahore",
  "UMT Lahore", "Superior University", "Punjab University", "Sindh University",
  "University of Peshawar", "Aga Khan University", "Dow University",
  "King Edward Medical University", "PIEAS", "NTTF", "Mehran University",
  "IObm", "Other"
];

const MAJORS = [
  "Computer Science", "Software Engineering", "Electrical Engineering",
  "Mechanical Engineering", "Civil Engineering", "Business Administration",
  "Economics", "Mathematics", "Physics", "Chemistry", "Biology", "Medicine",
  "Law", "Social Sciences", "Data Science", "Artificial Intelligence",
  "Cybersecurity", "Fintech", "Computer Engineering", "Other"
];

const DiscoverPage = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    university: '',
    department: '',
    semester: '',
    gpa: '',
    degree_level: '',
    skills: '',
    interests: '',
    preferred_countries: '',
    opportunity_types: [],
    country_filter: 'preferred'
  });
  const [otherUniversity, setOtherUniversity] = useState('');
  const [otherDepartment, setOtherDepartment] = useState('');
  const [errors, setErrors] = useState({});

  useEffect(() => {
    const saved = sessionStorage.getItem('discoveryForm');
    if (saved) {
      const parsed = JSON.parse(saved);
      setFormData(prev => ({
        ...prev,
        ...parsed,
        country_filter: parsed.country_filter || 'preferred'
      }));
    }
    const savedOtherUni = sessionStorage.getItem('discoveryOtherUniversity');
    if (savedOtherUni) setOtherUniversity(savedOtherUni);
    const savedOtherDept = sessionStorage.getItem('discoveryOtherDepartment');
    if (savedOtherDept) setOtherDepartment(savedOtherDept);
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => {
      const updated = { ...prev, [name]: value };
      sessionStorage.setItem('discoveryForm', JSON.stringify(updated));
      return updated;
    });
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const handleCheckbox = (type) => {
    setFormData(prev => {
      const types = [...prev.opportunity_types];
      const updatedTypes = types.includes(type)
        ? types.filter(t => t !== type)
        : [...types, type];
      const updated = { ...prev, opportunity_types: updatedTypes };
      sessionStorage.setItem('discoveryForm', JSON.stringify(updated));
      return updated;
    });
  };

  const handleOtherUniversityChange = (e) => {
    const val = e.target.value;
    setOtherUniversity(val);
    sessionStorage.setItem('discoveryOtherUniversity', val);
  };

  const handleOtherDepartmentChange = (e) => {
    const val = e.target.value;
    setOtherDepartment(val);
    sessionStorage.setItem('discoveryOtherDepartment', val);
  };

  const handleReset = () => {
    sessionStorage.removeItem('discoveryForm');
    sessionStorage.removeItem('discoveryOtherUniversity');
    sessionStorage.removeItem('discoveryOtherDepartment');
    setFormData({
      university: '',
      department: '',
      semester: '',
      gpa: '',
      degree_level: '',
      skills: '',
      interests: '',
      preferred_countries: '',
      opportunity_types: [],
      country_filter: 'preferred'
    });
    setOtherUniversity('');
    setOtherDepartment('');
    setErrors({});
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if ((formData.country_filter || 'preferred') !== 'global' && !formData.preferred_countries.trim()) {
      setErrors(prev => ({ ...prev, preferred_countries: 'Preferred countries is required' }));
      return;
    }

    setLoading(true);

    try {
      const hasInternshipOrResearch = formData.opportunity_types.includes('internship') || formData.opportunity_types.includes('research');

      // Process comma-separated strings into arrays
      const payload = {
        ...formData,
        university: formData.university === 'Other' ? otherUniversity : formData.university,
        department: formData.department === 'Other' ? otherDepartment : formData.department,
        semester: parseInt(formData.semester),
        gpa: parseFloat(formData.gpa),
        skills: hasInternshipOrResearch ? formData.skills.split(',').map(s => s.trim()).filter(Boolean) : [],
        interests: hasInternshipOrResearch ? formData.interests.split(',').map(s => s.trim()).filter(Boolean) : [],
        preferred_countries: (formData.country_filter || 'preferred') === 'global' ? [] : formData.preferred_countries.split(',').map(s => s.trim()).filter(Boolean),
      };

      console.log("Submitting:", payload);

      const response = await api.post('/discover', payload);

      // Store result in sessionStorage for the dashboard along with the selected filter scope
      sessionStorage.setItem('lastDiscovery', JSON.stringify({
        ...response.data,
        country_filter: formData.country_filter || 'preferred'
      }));

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
                <select
                  name="university"
                  className="form-control form-select"
                  value={formData.university}
                  onChange={handleChange}
                  required
                >
                  <option value="">Select University</option>
                  {UNIVERSITIES.map(uni => (
                    <option key={uni} value={uni}>{uni}</option>
                  ))}
                </select>
                {formData.university === 'Other' && (
                  <div style={{ marginTop: '0.5rem' }}>
                    <input
                      type="text"
                      placeholder="Specify University"
                      className="form-control"
                      value={otherUniversity}
                      onChange={handleOtherUniversityChange}
                      required
                    />
                  </div>
                )}
              </div>

              <div className="form-group">
                <label className="form-label">Department / Major</label>
                <select
                  name="department"
                  className="form-control form-select"
                  value={formData.department}
                  onChange={handleChange}
                  required
                >
                  <option value="">Select Major</option>
                  {MAJORS.map(major => (
                    <option key={major} value={major}>{major}</option>
                  ))}
                </select>
                {formData.department === 'Other' && (
                  <div style={{ marginTop: '0.5rem' }}>
                    <input
                      type="text"
                      placeholder="Specify Major"
                      className="form-control"
                      value={otherDepartment}
                      onChange={handleOtherDepartmentChange}
                      required
                    />
                  </div>
                )}
              </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '1rem' }}>
              <div className="form-group">
                <label className="form-label">Degree Level</label>
                <select
                  name="degree_level"
                  className="form-control form-select"
                  value={formData.degree_level}
                  onChange={handleChange}
                  required
                >
                  <option value="">Select Degree Level</option>
                  <option value="bachelor">Bachelor's</option>
                  <option value="master">Master's</option>
                  <option value="phd">PhD</option>
                </select>
              </div>
              <div className="form-group">
                <label className="form-label">Semester</label>
                <input
                  type="number" name="semester" className="form-control" min="1" max="8"
                  placeholder="Select Semester"
                  value={formData.semester} onChange={handleChange} required
                />
              </div>
              <div className="form-group">
                <label className="form-label">GPA (4.0 scale)</label>
                <input
                  type="number" name="gpa" className="form-control" min="0" max="4.0" step="0.01"
                  placeholder="e.g. 3.5"
                  value={formData.gpa} onChange={handleChange} required
                />
              </div>
            </div>

            {(formData.opportunity_types.includes('internship') || formData.opportunity_types.includes('research')) && (
              <div className="form-group">
                <label className="form-label">Skills (comma separated)</label>
                <input
                  type="text" name="skills" className="form-control"
                  value={formData.skills} onChange={handleChange} placeholder="e.g. Python, Data Analysis, Leadership"
                  required
                />
              </div>
            )}

            {(formData.opportunity_types.includes('internship') || formData.opportunity_types.includes('research')) && (
              <div className="form-group">
                <label className="form-label">Interests (comma separated)</label>
                <input
                  type="text" name="interests" className="form-control"
                  value={formData.interests} onChange={handleChange} placeholder="e.g. Artificial Intelligence, Robotics"
                  required
                />
              </div>
            )}

            <div className="form-group">
              <label className="form-label">Opportunity Scope</label>
              <div style={{ display: 'flex', gap: '0.75rem', marginTop: '0.5rem' }}>
                {[
                  { value: 'preferred', label: 'Preferred Countries Only' },
                  { value: 'global', label: 'Show All Countries (Global)' }
                ].map(option => (
                  <label key={option.value} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer', background: 'rgba(255,255,255,0.05)', padding: '0.5rem 1rem', borderRadius: '2rem', border: `1px solid ${(formData.country_filter || 'preferred') === option.value ? 'var(--accent-primary)' : 'transparent'}` }}>
                    <input
                      type="radio"
                      name="country_filter"
                      value={option.value}
                      checked={(formData.country_filter || 'preferred') === option.value}
                      onChange={handleChange}
                      style={{ accentColor: 'var(--accent-primary)' }}
                    />
                    <span>{option.label}</span>
                  </label>
                ))}
              </div>
            </div>

            {(formData.country_filter || 'preferred') !== 'global' && (
              <div className="form-group">
                <label className="form-label">Preferred Countries (comma separated)</label>
                <input
                  type="text" name="preferred_countries" className="form-control"
                  value={formData.preferred_countries} onChange={handleChange} placeholder="e.g. Germany, United Kingdom, Japan"
                  required
                />
                {errors.preferred_countries && (
                  <span style={{ color: 'var(--danger)', fontSize: '0.875rem', marginTop: '0.25rem', display: 'block' }}>
                    {errors.preferred_countries}
                  </span>
                )}
              </div>
            )}

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

            <button
              type="button"
              className="btn w-full mt-2"
              style={{
                background: 'transparent',
                border: '1px solid var(--border)',
                color: 'var(--text-secondary)',
                fontSize: '1rem',
                transition: 'var(--transition)'
              }}
              onClick={handleReset}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = 'rgba(255, 255, 255, 0.05)';
                e.currentTarget.style.color = 'var(--text-primary)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = 'transparent';
                e.currentTarget.style.color = 'var(--text-secondary)';
              }}
            >
              Reset Form
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
