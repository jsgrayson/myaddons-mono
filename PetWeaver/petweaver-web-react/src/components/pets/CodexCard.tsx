import React, { useState } from 'react';
import type { PetSummary } from '../../api/client';
import { rarityIcon, rarityColor, rarityGlow } from '../../constants/rarity';

interface CodexCardProps {
    pet: PetSummary;
}

export const CodexCard: React.FC<CodexCardProps> = ({ pet }) => {
    const fam = pet.family.toLowerCase();
    // Map missing elemental to magic, otherwise use family name
    const assetName = fam === 'elemental' ? 'magic' : fam;

    const [imgSrc, setImgSrc] = useState<string>(
        pet.portraitUrl || `/assets/pets/${assetName}.png`
    );

    // Use a known existing file for fallback
    const fallbackSrc = '/assets/pets/beast.png';

    const handleError = () => {
        // Prevent loop if fallback itself fails (though beast.png should exist)
        if (imgSrc !== fallbackSrc) {
            setImgSrc(fallbackSrc);
        }
    };

    return (
        <article className="codex-card">
            <div className={`codex-card-portrait rarity-${pet.rarity.toLowerCase()}`}>
                <img
                    src={imgSrc}
                    alt={pet.name}
                    onError={handleError}
                    className="codex-card-image"
                />
            </div>
            <div className="codex-card-body">
                <h2 className="codex-card-name">{pet.name}</h2>
                <div className="codex-card-meta">
                    <span className="codex-card-family">{pet.family}</span>
                    <span className={`codex-card-rarity codex-rarity-${pet.rarity.toLowerCase()}`}>
                        {pet.rarity}
                    </span>
                </div>
            </div>
        </article>
    );
};
