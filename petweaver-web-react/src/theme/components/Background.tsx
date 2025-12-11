import React from 'react';
import { Midnight } from '../midnight';
import { layers } from '../layers';

interface BackgroundProps {
  backgroundKey: keyof typeof Midnight.backgrounds;
  className?: string;
}

/**
 * Full-viewport background for a given Midnight background key.
 * Usually you won't need this if you use <Page>, but it's here if you want it.
 */
export const Background: React.FC<BackgroundProps> = ({
  backgroundKey,
  className,
}) => {
  const bgDef = Midnight.backgrounds[backgroundKey];

  const style: React.CSSProperties = {
    backgroundImage: [
      bgDef.vignette ?? '',
      bgDef.overlay ?? '',
      `url("${bgDef.image}")`,
    ]
      .filter(Boolean)
      .join(', '),
    backgroundSize: 'cover',
    backgroundPosition: 'center top',
    backgroundRepeat: 'no-repeat',
    zIndex: layers.background,
  };

  return <div className={`midnight-bg ${className ?? ''}`.trim()} style={style} />;
};
