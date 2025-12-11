import React from 'react';
import { Midnight } from '../midnight';
import { layers } from '../layers';

interface PageProps {
  /** Key into Midnight.backgrounds, e.g. "codex", "simulator", "dashboard" */
  backgroundKey?: keyof typeof Midnight.backgrounds;
  /** Optional explicit background image override */
  backgroundImage?: string;
  className?: string;
  children: React.ReactNode;
}

/**
  * Midnight Page wrapper – handles background image + basic stacking.
  * You can use this inside Layout or as the top-level wrapper for a route.
  */
export const Page: React.FC<PageProps> = ({
  backgroundKey,
  backgroundImage,
  className,
  children,
}) => {
  const bgDef = backgroundKey ? Midnight.backgrounds[backgroundKey] : undefined;

  const finalBgImage = backgroundImage ?? bgDef?.image;

  const style: React.CSSProperties = finalBgImage
    ? {
        backgroundImage: `url("${finalBgImage}")`,
        backgroundSize: 'cover',
        backgroundPosition: 'center top',
        backgroundRepeat: 'no-repeat',
      }
    : {};

  return (
    <div
      className={`midnight-page-root ${className ?? ''}`.trim()}
      style={style}
    >
      {/* Optional vignette / overlay */}
      {bgDef && (bgDef.vignette || bgDef.overlay) && (
        <div
          className="midnight-page-vignette"
          style={{
            zIndex: layers.vignette,
            backgroundImage: [bgDef.vignette ?? '', bgDef.overlay ?? '']
              .filter(Boolean)
              .join(', '),
          }}
        />
      )}

      <div className="midnight-page-inner" style={{ zIndex: layers.page }}>
        {children}
      </div>
    </div>
  );
};
