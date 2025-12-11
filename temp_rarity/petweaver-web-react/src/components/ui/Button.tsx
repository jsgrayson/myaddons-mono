import React from 'react';

type Props = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: 'primary' | 'secondary' | 'ghost';
};

export const Button: React.FC<Props> = ({ variant = 'primary', className = '', ...rest }) => {
  const base =
    'inline-flex items-center justify-center rounded-md px-4 py-2 text-sm font-semibold transition shadow-sm focus:outline-none focus-visible:ring-2 focus-visible:ring-ember-light focus-visible:ring-offset-2 focus-visible:ring-offset-bg-base disabled:opacity-60 disabled:cursor-not-allowed';
  const styles: Record<string, string> = {
    primary:
      'bg-gradient-to-r from-ember-deep via-ember-light to-arcane-mid text-slate-900 shadow-ember hover:brightness-110',
    secondary:
      'border border-amber-500/60 bg-bg-panel text-amber-100 hover:border-amber-300 hover:text-amber-50',
    ghost: 'bg-transparent text-slate-200 hover:bg-slate-800/60',
  };

  return <button className={`${base} ${styles[variant]} ${className}`} {...rest} />;
};
