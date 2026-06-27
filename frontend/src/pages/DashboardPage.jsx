import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Bookmark, ExternalLink, Calendar, MapPin, GraduationCap, ChevronDown, ChevronUp } from 'lucide-react';
import ProgressRing from '../components/ProgressRing';

const DashboardPage = () => {
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [expandedId, setExpandedId] = useState(null);
  const [countryFilter, setCountryFilter] = useState('preferred');

  useEffect(() => {
    let scope = 'preferred';
    const savedData = sessionStorage.getItem('lastDiscovery');
    if (savedData) {
      const parsedData = JSON.parse(savedData);
      setData(parsedData);
      if (parsedData.country_filter) {
        scope = parsedData.country_filter;
      }
    }

    // Fallback to discoveryForm if not found in lastDiscovery
    const savedForm = sessionStorage.getItem('discoveryForm');
    if (savedForm) {
      const parsed = JSON.parse(savedForm);
      if (parsed.country_filter) {
        scope = parsed.country_filter;
      }
    }

    setCountryFilter(scope);
  }, [navigate]);

  if (!data) {
    return (
      <div className="container flex items-center justify-center" style={{ minHeight: '60vh' }}>
        <div className="text-center">
          <h2>No Results Found</h2>
          <p className="text-secondary mb-4">You haven't run a discovery scan yet.</p>
          <button className="btn btn-primary" onClick={() => navigate('/discover')}>Run Discovery</button>
        </div>
      </div>
    );
  }

  return (
    <div className="container" style={{ paddingBottom: '4rem' }}>
      <div className="flex justify-between items-center mb-8">
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', flexWrap: 'wrap' }}>
            <h1 style={{ margin: 0 }}>Your <span className="gradient-text">Matches</span></h1>
            {countryFilter === 'preferred' ? (
              <span className="badge" style={{ background: 'rgba(37, 99, 235, 0.2)', color: 'var(--accent-secondary)' }}>
                Preferred Countries Only
              </span>
            ) : (
              <span className="badge" style={{ background: 'rgba(124, 58, 237, 0.2)', color: 'var(--accent-primary)' }}>
                Global Search
              </span>
            )}
          </div>
          <p className="text-secondary" style={{ marginTop: '0.5rem', marginBottom: 0 }}>Found {data.total_matches} opportunities tailored to your profile.</p>
        </div>
        <button className="btn btn-secondary" onClick={() => navigate('/discover')}>
          Back to Discovery
        </button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 3fr', gap: '2rem', alignItems: 'start' }}>
        {/* Sidebar / Advice */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <div className="card glass-panel" style={{ background: 'linear-gradient(180deg, rgba(30,41,59,0.7) 0%, rgba(15,23,42,0.8) 100%)', borderTop: '2px solid var(--accent-primary)' }}>
            <h3 style={{ fontSize: '1.25rem', marginBottom: '1rem' }}>Career Advisor Notes</h3>
            <p className="text-secondary" style={{ fontSize: '0.9rem', marginBottom: '1.5rem' }}>
              {data.career_advice}
            </p>

            <h4 style={{ fontSize: '1rem', marginBottom: '0.75rem' }}>Action Plan</h4>
            <ul style={{ listStyleType: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              {data.overall_action_plan.map((item, idx) => (
                <li key={idx} className="flex gap-2 items-start" style={{ fontSize: '0.875rem' }}>
                  <div style={{ background: 'rgba(124, 58, 237, 0.2)', color: 'var(--accent-primary)', width: '20px', height: '20px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0, fontSize: '0.75rem', fontWeight: 'bold' }}>
                    {idx + 1}
                  </div>
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>

          <div className="card glass-panel">
            <h3 style={{ fontSize: '1.125rem', marginBottom: '1rem' }}>Profile Summary</h3>
            <div className="flex flex-col gap-2 text-sm">
              <div className="flex justify-between"><span className="text-secondary">GPA:</span> <span>{data.profile_summary.gpa}</span></div>
              <div className="flex justify-between"><span className="text-secondary">Degree:</span> <span style={{ textTransform: 'capitalize' }}>{data.profile_summary.degree_level}</span></div>
              <div className="flex justify-between"><span className="text-secondary">Major:</span> <span>{data.profile_summary.department}</span></div>
            </div>
          </div>
        </div>

        {/* Results List */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          {data.opportunities.map((opp, idx) => (
            <div key={idx} className="card glass-panel" style={{ padding: '0' }}>
              <div className="flex justify-between items-start" style={{ padding: '1.5rem' }}>
                <div style={{ flex: 1 }}>
                  <div className="flex items-center gap-2 mb-2">
                    <span className="badge badge-primary">{opp.opportunity_type.replace('_', ' ')}</span>
                    <span className="badge badge-neutral">{opp.funding_status}</span>
                    {opp.tags.map(t => <span key={t} className="badge badge-neutral" style={{ background: 'rgba(255,255,255,0.05)' }}>{t}</span>)}
                  </div>
                  <h2 style={{ fontSize: '1.5rem', marginBottom: '0.25rem' }}>{opp.name}</h2>
                  <p className="text-secondary" style={{ fontSize: '1rem', marginBottom: '1rem' }}>{opp.organization}</p>

                  <div className="flex gap-6 mb-4">
                    <div className="flex items-center gap-2 text-sm text-secondary">
                      <MapPin size={16} /> <span>{opp.country}</span>
                    </div>
                    <div className="flex items-center gap-2 text-sm text-secondary">
                      <Calendar size={16} /> <span>{opp.deadline || 'Rolling'}</span>
                    </div>
                  </div>

                  <p style={{ fontSize: '0.9rem', marginBottom: '0' }}>
                    <strong>Why it matches:</strong> {opp.recommendation_reason}
                  </p>
                </div>

                <div className="flex flex-col items-center gap-4 ml-4" style={{ minWidth: '80px' }}>
                  <ProgressRing score={opp.match_score} />
                  <a href={opp.application_link} target="_blank" rel="noreferrer" className="btn btn-primary" style={{ padding: '0.5rem 1rem', width: '100%' }}>
                    Apply <ExternalLink size={16} />
                  </a>
                </div>
              </div>

              <div
                style={{ borderTop: '1px solid var(--border)', padding: '0.75rem 1.5rem', background: 'rgba(0,0,0,0.2)', cursor: 'pointer', display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '0.5rem' }}
                onClick={() => setExpandedId(expandedId === idx ? null : idx)}
              >
                <span style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                  {expandedId === idx ? 'Hide Details' : 'View Action Plan & Eligibility'}
                </span>
                {expandedId === idx ? <ChevronUp size={16} className="text-secondary" /> : <ChevronDown size={16} className="text-secondary" />}
              </div>

              {expandedId === idx && (
                <div style={{ padding: '1.5rem', borderTop: '1px solid var(--border)', background: 'rgba(15,23,42,0.4)', borderBottomLeftRadius: 'var(--radius-md)', borderBottomRightRadius: 'var(--radius-md)' }}>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem' }}>
                    <div>
                      <h4 className="mb-2">Eligibility Summary</h4>
                      <p className="text-secondary text-sm mb-4">{opp.eligibility_summary}</p>

                      {opp.missing_requirements.length > 0 && (
                        <>
                          <h4 className="mb-2 text-warning flex items-center gap-2"><AlertCircle size={16} /> Missing Requirements</h4>
                          <ul className="text-sm text-secondary pl-5">
                            {opp.missing_requirements.map((req, i) => <li key={i}>{req}</li>)}
                          </ul>
                        </>
                      )}
                    </div>
                    <div>
                      <h4 className="mb-2">Your Action Plan</h4>
                      <ul className="text-sm pl-5" style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                        {opp.action_plan.map((step, i) => (
                          <li key={i}>{step}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

// Assuming AlertCircle is needed in the expansion panel
import { AlertCircle } from 'lucide-react';

export default DashboardPage;
