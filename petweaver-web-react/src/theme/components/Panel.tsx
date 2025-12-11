import React from 'react';
import { layers } from '../layers';

interface PanelProps {
  className?: string;
  children: React.ReactNode;
}

/**
 * Generic Midnight panel – maps to .page-panel styles.
 */
export const Panel: React.FC<PanelProps> = ({ className, children }) => {
  return (
    <section
      className={`page-panel ${className ?? ''}`.trim()}
      style={{ position: 'relative', zIndex: layers.panel }}
    >
      {children}
    </section>
  );
};
