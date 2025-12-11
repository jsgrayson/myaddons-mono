import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Layout } from '../components/layout/Layout';
import { Page } from '../theme/components/Page';
import { Panel } from '../theme/components/Panel';
import { RarityPill, RarityKey } from '../theme/components/Rarity';
import { apiGetPet, PetDetails } from '../api/client';
import { getPetPortraitPath, resolvePetFamily } from '../utils/petAssets';
import '../styles/tools.css';
import './codex.css';

export const PetDetailsPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [pet, setPet] = useState<PetDetails | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (id) {
      apiGetPet(id)
        .then(setPet)
        .catch(console.error)
        .finally(() => setLoading(false));
    }
  }, [id]);

  const rarityKey = (pet?.rarity?.toLowerCase() as RarityKey) || 'common';
  const portrait = pet
    ? pet.portraitUrl ?? getPetPortraitPath(resolvePetFamily(pet.family))
    : '/assets/pets/magic.png';

  const loadingView = (
    <Panel className="tools-panel">
      <div className="state-banner">Loading pet data...</div>
    </Panel>
  );

  const notFoundView = (
    <Panel className="tools-panel">
      <div className="state-banner state-banner-error">Pet not found.</div>
    </Panel>
  );

  return (
    <Layout>
      <Page backgroundKey="petDetails">
        <div className="tools-page petdetails-page">
          {loading && loadingView}
          {!loading && !pet && notFoundView}
          {!loading && pet && (
            <Panel className="tools-panel">
              <header className="page-header">
                <div className="page-header-main">
                  <p className="page-kicker">Midnight mode • Pet Profile</p>
                  <h1 className="page-title">{pet.name}</h1>
                  <p className="page-subtitle">
                    Deep dive into a single companion’s stats, abilities, and performance history.
                  </p>
                </div>
                <div className="page-header-actions">
                  <RarityPill rarity={rarityKey} />
                </div>
              </header>

              <div className="tools-layout">
                <section className="tools-col card-midnight">
                  <h2 className="card-title">Overview</h2>
                  <p className="card-subtitle">
                    Portrait, family, rarity, and core stats.
                  </p>
                  <div className="tools-card-body">
                    <div className="flex items-start gap-4">
                      <div
                        className={`codex-card-portrait rarity-${pet.rarity.toLowerCase()}`}
                        style={{ width: 96, height: 96 }}
                      >
                        <img
                          src={portrait}
                          alt={pet.name}
                          loading="lazy"
                          onError={(e) => ((e.target as HTMLImageElement).src = '/assets/pets/magic.png')}
                        />
                      </div>
                      <div className="flex-1 space-y-2 text-sm text-slate-200">
                        <div className="flex justify-between border-b border-slate-800 pb-1">
                          <span className="text-slate-400">Family</span>
                          <span className="text-slate-100">{pet.family}</span>
                        </div>
                        <div className="flex justify-between border-b border-slate-800 pb-1">
                          <span className="text-slate-400">Health</span>
                          <span className="text-green-300">{pet.health}</span>
                        </div>
                        <div className="flex justify-between border-b border-slate-800 pb-1">
                          <span className="text-slate-400">Power</span>
                          <span className="text-amber-300">{pet.power}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-400">Speed</span>
                          <span className="text-blue-300">{pet.speed}</span>
                        </div>
                      </div>
                    </div>
                    <p className="mt-3 text-slate-400 text-sm">
                      {pet.flavorText ?? 'A mysterious creature with untapped potential.'}
                    </p>
                  </div>
                </section>

                <section className="tools-col">
                  <article className="card-midnight">
                    <h2 className="card-title">Abilities</h2>
                    <p className="card-subtitle">
                      Available abilities and their tuned values.
                    </p>
                    <div className="tools-card-body">
                      <div className="grid grid-cols-2 gap-2 mt-2 text-sm">
                        {(pet.abilities || []).map((ab) => (
                          <div
                            key={ab.id}
                            className="p-2 rounded border border-slate-700/60 bg-slate-900/60"
                          >
                            <div className="font-semibold text-slate-200">{ab.name}</div>
                            <div className="text-slate-500 mt-1">
                              {ab.description || 'No description'}
                            </div>
                          </div>
                        ))}
                        {(!pet.abilities || pet.abilities.length === 0) && (
                          <div className="tools-placeholder">No abilities discovered.</div>
                        )}
                      </div>
                    </div>
                  </article>

                  <article className="card-midnight">
                    <h2 className="card-title">History</h2>
                    <p className="card-subtitle">
                      Recent battles and win/loss performance for this pet.
                    </p>
                    <div className="tools-card-body tools-log">
                      <div className="tools-log-empty">
                        No history yet. Once wired, recent battles will appear here.
                      </div>
                    </div>
                  </article>
                </section>
              </div>
            </Panel>
          )}
        </div>
      </Page>
    </Layout>
  );
};
