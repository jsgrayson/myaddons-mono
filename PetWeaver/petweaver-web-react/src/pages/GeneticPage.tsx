import React from 'react';
import { Layout } from '../components/layout/Layout';
import { Page } from '../theme/components/Page';
import { Panel } from '../theme/components/Panel';
import '../styles/tools.css';

export const OptimizerPage: React.FC = () => {
  return (
    <Layout>
      <Page backgroundKey="optimizer">
        <div className="tools-page optimizer-page">
          <Panel className="tools-panel">
            <header className="page-header">
              <div className="page-header-main">
                <p className="page-kicker">Midnight mode • Team Builder</p>
                <h1 className="page-title">Optimizer</h1>
                <p className="page-subtitle">
                  Find the strongest pet teams for specific encounters and constraints.
                </p>
              </div>
              <div className="page-header-actions">
                <button className="btn-primary" type="button">
                  Run Optimization
                </button>
              </div>
            </header>

            <div className="tools-layout">
              <section className="tools-col card-midnight">
                <h2 className="card-title">Constraints</h2>
                <p className="card-subtitle">
                  Choose encounter, available pets, and filters.
                </p>
                <div className="tools-card-body">
                  <div className="tools-placeholder">
                    Encounter / filter form controls.
                  </div>
                </div>
              </section>

              <section className="tools-col">
                <article className="card-midnight">
                  <h2 className="card-title">Suggested Teams</h2>
                  <p className="card-subtitle">
                    Highest-performing comps based on your constraints.
                  </p>
                  <div className="tools-card-body">
                    <div className="tools-placeholder">
                      Team cards / rating rows.
                    </div>
                  </div>
                </article>

                <article className="card-midnight">
                  <h2 className="card-title">Notes</h2>
                  <div className="tools-card-body tools-log">
                    <div className="tools-log-empty">
                      Optimization notes and reasoning can appear here once the backend exposes them.
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

export const GeneticPage = OptimizerPage;
export default OptimizerPage;
