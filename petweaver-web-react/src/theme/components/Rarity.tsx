import React from 'react';
import { Midnight } from '../midnight';

export type RarityKey = keyof typeof Midnight.rarity;

interface RarityPillProps {
  rarity: RarityKey;
  className?: string;
}

/**
 * Small rarity pill (e.g. "Rare", "Epic") with color + glow from the theme.
 */
export const RarityPill: React.FC<RarityPillProps> = ({
  rarity,
  className,
}) => {
  const def = Midnight.rarity[rarity];

  const style: React.CSSProperties = {
    borderColor: def.border,
    color: def.text,
    boxShadow: def.glow,
  };

  return (
    <span
      className={`midnight-rarity-pill ${className ?? ''}`.trim()}
      style={style}
    >
      {rarity[0].toUpperCase() + rarity.slice(1)}
    </span>
  );
};
