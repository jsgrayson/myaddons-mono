import React, { useEffect, useMemo, useState } from 'react';
import { Layout } from '../components/layout/Layout';
import { apiListPets, PetSummary } from '../api/client';
import './codex.css';
import { getPetPortraitPath, resolvePetFamily } from '../utils/petAssets';

// Robust image component with fallback
function PetCodexCard({ pet }: { pet: PetSummary }) {
  const [imgError, setImgError] = useState(false);

  const familyKey = resolvePetFamily(pet.family);
  // Always prefer local assets; ignore remote portraitUrl to avoid 404s
  const portraitSrc = !imgError
    ? getPetPortraitPath(familyKey)
    : '/assets/pets/magic.png';

  return (
    <article className="codex-card">
      <div
        className={`codex-card-portrait rarity-${pet.rarity.toLowerCase()}`}
      >
        <img
          src={portraitSrc}
          alt={pet.name}
          loading="lazy"
          onError={() => setImgError(true)}
        />
      </div>
      <div className="codex-card-body">
        <h2 className="codex-card-name">{pet.name}</h2>
        <div className="codex-card-meta">
          <span className="codex-card-family">{pet.family}</span>
          <span
            className={`codex-card-rarity codex-rarity-${pet.rarity.toLowerCase()}`}
          >
            {pet.rarity}
          </span>
        </div>
      </div>
    </article>
  );
}

export const PetsPage: React.FC = () => {
  const [pets, setPets] = useState<PetSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [query, setQuery] = useState('');
  const totalPets = loading ? '...' : pets.length;

  useEffect(() => {
    apiListPets()
      .then((data) => {
        setPets(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message || 'Failed to load pets');
        setLoading(false);
      });
  }, []);

  // Simple client-side filtering by name or family
  const filteredPets = useMemo(() => {
    if (!query.trim()) return pets;
    const q = query.toLowerCase();
    return pets.filter((pet) => {
      return (
        pet.name.toLowerCase().includes(q) ||
        pet.family.toLowerCase().includes(q)
      );
    });
  }, [pets, query]);

  const showingCount = loading ? '...' : filteredPets.length;

  return (
    <Layout background="/assets/backgrounds/codex.png">
      <div className="codex-page">
        <div className="page-panel codex-panel">
          <div className="codex-vignette" />
          <div className="codex-inner">
            <header className="codex-header">
              <div className="codex-heading">
                <p className="codex-kicker">Midnight mode • Arcane Bestiary</p>
                <h1 className="codex-title">Pet Codex</h1>
                <p className="codex-subtitle">
                  Browse all discovered companions and their battle potential.
                </p>
                <div className="codex-pills">
                  <span className="codex-pill">
                    <span className="codex-pill-label">Total</span>
                    <span className="codex-pill-value">{totalPets}</span>
                  </span>
                  <span className="codex-pill codex-pill-ghost">
                    <span className="codex-pill-label">Skin</span>
                    <span className="codex-pill-value">Midnight</span>
                  </span>
                  <span className="codex-pill codex-pill-ghost">
                    <span className="codex-pill-label">Showing</span>
                    <span className="codex-pill-value">{showingCount}</span>
                  </span>
                </div>
              </div>
              <div className="codex-actions">
                <div className="codex-search-shell">
                  <input
                    type="search"
                    className="codex-search"
                    placeholder="Search by name or family..."
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                  />
                  <div className="codex-search-glow" />
                </div>
                <div className="codex-actions-note">Arcane archive</div>
              </div>
            </header>

            {loading && (
              <div className="codex-state codex-state-soft">
                Loading pets...
              </div>
            )}
            {error && (
              <div className="codex-state codex-state-error">{error}</div>
            )}

            {!loading && !error && filteredPets.length === 0 && (
              <div className="codex-state codex-state-soft">
                No pets match that query.
              </div>
            )}

            <section className="codex-grid">
              {filteredPets.map((pet, index) => (
                <PetCodexCard key={`${pet.id}-${index}`} pet={pet} />
              ))}
            </section>
          </div>
        </div>
      </div>
    </Layout>
  );
};
