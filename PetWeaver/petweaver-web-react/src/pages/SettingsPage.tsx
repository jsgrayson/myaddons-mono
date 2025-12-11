import React from 'react';
import { Layout } from '../components/layout/Layout';
import { Page } from '../theme/components/Page';
import { Panel } from '../theme/components/Panel';
import '../styles/tools.css';

export const SettingsPage: React.FC = () => {
  return (
    <Layout>
      <Page backgroundKey="settings">
        <div className="tools-page settings-page">
          <Panel className="tools-panel">
            <header className="page-header">
              <div className="page-header-main">
                <p className="page-kicker">Midnight mode • Control Panel</p>
                <h1 className="page-title">Settings</h1>
                <p className="page-subtitle">
                  Configure Petweaver behavior, skins, and integration settings.
                </p>
              </div>
            </header>

            <div className="tools-layout">
              <section className="tools-col card-midnight">
                <h2 className="card-title">General</h2>
                <div className="tools-card-body">
                  <div className="tools-placeholder">
                    Basic options (server URL, theme toggle, etc.).
                  </div>
                </div>
              </section>

              <section className="tools-col">
                <article className="card-midnight">
                  <h2 className="card-title">Integrations</h2>
                  <div className="tools-card-body">
                    <div className="tools-placeholder">
                      API keys, endpoints, and other hooks.
                    </div>
                  </div>
                </article>

                <article className="card-midnight">
                  <h2 className="card-title">Danger Zone</h2>
                  <div className="tools-card-body">
                    <div className="tools-placeholder">
                      Reset, clear caches, rebuild indices.
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
