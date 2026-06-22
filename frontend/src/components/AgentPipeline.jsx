import React, { useEffect, useState } from 'react';
import { Activity, CheckCircle2, Circle, Clock, Loader2, AlertCircle } from 'lucide-react';

const AgentPipeline = ({ isRunning }) => {
  const [steps, setSteps] = useState([
    { id: 'profile', name: 'Profile Analysis', status: 'pending', desc: 'Extracting skills and attributes' },
    { id: 'discovery', name: 'Opportunity Discovery', status: 'pending', desc: 'Searching global databases' },
    { id: 'eligibility', name: 'Eligibility Matching', status: 'pending', desc: 'Calculating match scores' },
    { id: 'career', name: 'Career Advisor', status: 'pending', desc: 'Generating action plans' },
    { id: 'deadline', name: 'Deadline Tracker', status: 'pending', desc: 'Organizing application schedule' }
  ]);

  // Simulate pipeline progress for demo if real SSE isn't implemented yet
  useEffect(() => {
    if (isRunning) {
      let currentStep = 0;
      
      // Reset all to pending
      setSteps(prev => prev.map(s => ({ ...s, status: 'pending' })));
      
      const interval = setInterval(() => {
        if (currentStep < steps.length) {
          setSteps(prev => prev.map((step, idx) => {
            if (idx === currentStep) return { ...step, status: 'running' };
            if (idx < currentStep) return { ...step, status: 'completed' };
            return step;
          }));
          
          currentStep++;
        } else {
          setSteps(prev => prev.map(step => ({ ...step, status: 'completed' })));
          clearInterval(interval);
        }
      }, 2000); // 2s per agent step simulation
      
      return () => clearInterval(interval);
    } else {
      // If not running, keep them as they are or reset to pending
      // If just finished, they will all be 'completed'
    }
  }, [isRunning]);

  return (
    <div className="card glass-panel h-full">
      <div className="flex items-center gap-2 mb-6">
        <Activity className={isRunning ? "animate-pulse" : ""} color="var(--accent-primary)" />
        <h2 style={{ fontSize: '1.25rem', margin: 0 }}>Agent Pipeline Status</h2>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', position: 'relative' }}>
        {/* Connecting Line */}
        <div style={{ position: 'absolute', left: '11px', top: '24px', bottom: '24px', width: '2px', background: 'var(--border)', zIndex: 0 }}></div>

        {steps.map((step, idx) => (
          <div key={step.id} className="flex gap-4" style={{ position: 'relative', zIndex: 1 }}>
            <div style={{ background: 'var(--bg-secondary)', borderRadius: '50%', padding: '2px' }}>
              {step.status === 'completed' ? (
                <CheckCircle2 color="var(--success)" fill="rgba(16, 185, 129, 0.2)" />
              ) : step.status === 'running' ? (
                <Loader2 className="animate-spin" color="var(--accent-secondary)" />
              ) : step.status === 'error' ? (
                <AlertCircle color="var(--danger)" />
              ) : (
                <Circle color="var(--text-muted)" />
              )}
            </div>
            
            <div style={{ flex: 1, opacity: step.status === 'pending' ? 0.5 : 1 }}>
              <div className="flex justify-between items-center mb-1">
                <h4 style={{ margin: 0, fontSize: '1rem', color: step.status === 'running' ? 'var(--text-primary)' : 'inherit' }}>
                  {step.name}
                </h4>
                {step.status === 'running' && <span className="badge badge-primary animate-pulse">Running</span>}
                {step.status === 'completed' && <span className="badge badge-success">Done</span>}
              </div>
              <p className="text-secondary" style={{ fontSize: '0.875rem', margin: 0 }}>
                {step.desc}
              </p>
            </div>
          </div>
        ))}
      </div>
      
      {!isRunning && steps[0].status === 'completed' && (
        <div className="mt-6 p-3 rounded" style={{ background: 'rgba(16, 185, 129, 0.1)', border: '1px solid rgba(16, 185, 129, 0.2)' }}>
          <p className="text-center" style={{ color: 'var(--success)', margin: 0, fontSize: '0.875rem' }}>
            Pipeline executed successfully. Total time: 10.4s
          </p>
        </div>
      )}
    </div>
  );
};

export default AgentPipeline;
