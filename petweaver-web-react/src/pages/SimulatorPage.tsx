import React from 'react';
import { Layout } from '../components/layout/Layout';
import { Page } from '../theme/components/Page';
import { Panel } from '../theme/components/Panel';
import '../styles/simulator.css';

export const SimulatorPage: React.FC = () => {
  return (
    <Layout>
      <Page backgroundKey="simulator">
        <div className="simulator-page">
          <Panel className="simulator-panel">
            <header className="page-header">
              <div className="page-header-main">
                <p className="page-kicker">Midnight mode • Battle Sandbox</p>
                <h1 className="page-title">Simulator</h1>
                <p className="page-subtitle">
                  Model encounters, test pet teams, and iterate on comps before you step into the real fight.
                </p>
              </div>
              <div className="page-header-actions">
                <button className="btn-primary" type="button">
                  New Simulation
                </button>
                <button className="btn-ghost" type="button">
                  Clear Results
                </button>
              </div>
            </header>

            <div className="simulator-layout">
              <section className="simulator-col simulator-config card-midnight">
                <h2 className="card-title">Setup</h2>
                <p className="card-subtitle">
                  Choose pets, abilities, and enemy scripts to simulate.
                </p>
                <div className="simulator-placeholder">
                  Simulation controls go here.
                </div>
              </section>

              <section className="simulator-col simulator-results">
                <article className="card-midnight simulator-results-card">
                  <h2 className="card-title">Results</h2>
                  <p className="card-subtitle">
                    Charts, logs, and outcome distributions appear here once you run a simulation.
                  </p>
                  <div className="simulator-placeholder">
                    Results / graph area.
                  </div>
                </article>

                <article className="card-midnight simulator-log-card">
                  <h2 className="card-title">Combat Log</h2>
                  <div className="simulator-log">
                    <div className="simulator-log-empty">
                      No simulations yet. Run one to see the combat log.
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
