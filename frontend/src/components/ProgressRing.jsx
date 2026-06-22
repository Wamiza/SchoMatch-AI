import React from 'react';

const ProgressRing = ({ score }) => {
  const radius = 24;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  let color = 'var(--success)'; // Green for 80+
  if (score < 60) color = 'var(--danger)';
  else if (score < 80) color = 'var(--warning)';

  return (
    <div style={{ position: 'relative', width: '60px', height: '60px' }}>
      <svg className="w-full h-full" viewBox="0 0 60 60">
        <circle
          cx="30" cy="30" r={radius}
          fill="none"
          stroke="var(--bg-tertiary)"
          strokeWidth="6"
        />
        <circle
          cx="30" cy="30" r={radius}
          fill="none"
          stroke={color}
          strokeWidth="6"
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          strokeLinecap="round"
          style={{ transition: 'stroke-dashoffset 1s ease-out', transform: 'rotate(-90deg)', transformOrigin: '50% 50%' }}
        />
      </svg>
      <div style={{ position: 'absolute', top: '0', left: '0', width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <span style={{ fontWeight: 'bold', fontSize: '0.875rem' }}>{score}%</span>
      </div>
    </div>
  );
};

export default ProgressRing;
