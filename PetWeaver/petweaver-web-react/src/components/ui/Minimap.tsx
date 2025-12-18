import React from 'react';
import './minimap.css';

interface MinimapProps {
    zoneName?: string;
}

export const Minimap: React.FC<MinimapProps> = ({ zoneName = "Midnight Shard" }) => {
    return (
        <div className="minimap-outer-wrapper">
            <div className="minimap-zone-label">{zoneName}</div>
            <div className="minimap-container">
                {/* The actual map content */}
                <div className="minimap-content" style={{ backgroundImage: `url('https://placehold.co/400x400/020617/1e293b?text=Zone+Map')` }}></div>

                {/* The gold border overlay for the main map */}
                <div className="minimap-main-border"></div>

                {/* The circular button sitting on the rim */}
                <button className="minimap-button" aria-label="Open Management">
                    <div className="button-icon" style={{ backgroundImage: `url('https://placehold.co/64x64/331144/cc88ff?text=PW')` }}></div>
                    <div className="button-border"></div>
                </button>
            </div>
        </div>
    );
};
