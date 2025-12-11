import React, { useEffect, useState } from 'react';
import { Layout } from '../components/layout/Layout';
import { Page } from '../theme/components/Page';
import { Panel } from '../theme/components/Panel';
import { apiListEncounters } from '../api/client';
import '../styles/tools.css';

export const EncountersPage: React.FC = () => {
  const [encounters, setEncounters] = useState<any[]>([]);

  useEffect(() => {
    apiListEncounters().then(setEncounters).catch(console.error);
  }, []);

  return (
    <Layout>
      <Page backgroundKey="encounters">
        <div className="tools-page encounters-page">
          <Panel className="tools-panel">
            <header className="page-header">
              <div className="page-header-main">
                <p className="page-kicker">Midnight mode • Encounter Library</p>
                <h1 className="page-title">Encounters</h1>
                <p className="page-subtitle">
                  Browse and manage scripted encounters for the simulator and optimizer.
                </p>
              </div>
              <div className="page-header-actions">
                <button className="btn-primary" type="button">
                  New Encounter
                </button>
              </div>
            </header>

            <div className="tools-layout">
              <section className="tools-col card-midnight">
                <h2 className="card-title">Encounter List</h2>
                <p className="card-subtitle">
                  All registered encounters with difficulty and tags.
                </p>
                <div className="tools-card-body">
                  <div className="tools-placeholder" style={{ minHeight: 0 }}>
                    <div className="w-full">
                      {encounters.length === 0 ? (
                        <div className="text-center text-sm text-slate-400">No encounters loaded.</div>
                      ) : (
                        <ul className="space-y-2 max-h-72 overflow-y-auto text-sm">
                          {encounters.map((enc, i) => (
                            <li
                              key={i}
                              className="p-2 rounded border border-slate-700/60 bg-slate-900/60"
                            >
                              {enc.name || `Encounter #${i + 1}`}
                            </li>
                          ))}
                        </ul>
                      )}
                    </div>
                  </div>
                </div>
              </section>

              <section className="tools-col">
                <article className="card-midnight">
                  <h2 className="card-title">Details</h2>
                  <p className="card-subtitle">
                    Selected encounter’s composition and script summary.
                  </p>
                  <div className="tools-card-body">
                    <div className="tools-placeholder">
                      Encounter details panel.
                    </div>
                  </div>
                </article>

                <article className="card-midnight">
                  <h2 className="card-title">Script Preview</h2>
                  <div className="tools-card-body tools-log">
                    <div className="tools-log-empty">
                      Encounter script preview will appear here.
                    </div>
                  </div>
                </article>
              </section>
            </div>
          </Panel>
        </div>
      </Page>
    </Layout>
  );
};
