import React from 'react';

export const Card: React.FC<{ className?: string; children: React.ReactNode }> = ({
  className = '',
  children,
}) => (
  <div
    className={`relative overflow-hidden rounded-xl bg-bg-panel/40 backdrop-blur-md border border-white/5 shadow-lg shadow-black/50 ${className}`}
  >
    <div className="pointer-events-none absolute inset-0 bg-ember-vignette opacity-10" />
    <div className="relative z-10 p-4">{children}</div>
  </div>
);
