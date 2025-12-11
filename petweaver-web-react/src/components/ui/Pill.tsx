import React from 'react';

export const Pill: React.FC<{ children: React.ReactNode; className?: string }> = ({
  children,
  className = '',
}) => (
  <span
    className={
      'inline-flex items-center rounded-full border border-slate-600 bg-bg-panelSoft/70 px-3 py-1 text-[11px] uppercase tracking-wide text-slate-300 ' +
      className
    }
  >
    {children}
  </span>
);
