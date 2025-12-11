import React from 'react';
import { layers } from '../layers';

interface CardProps {
  className?: string;
  as?: keyof JSX.IntrinsicElements;
  children: React.ReactNode;
}

/**
 * Generic Midnight card – maps to .card-midnight styles.
 */
export const Card: React.FC<CardProps> = ({
  className,
  as: Tag = 'article',
  children,
}) => {
  return (
    <Tag
      className={`card-midnight ${className ?? ''}`.trim()}
      style={{ position: 'relative', zIndex: layers.card }}
    >
      {children}
    </Tag>
  );
};
