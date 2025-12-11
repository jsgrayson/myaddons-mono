import React from "react";
import { Layout } from "../components/layout/Layout";
import "./shared.css";

export const SettingsPage: React.FC = () => {
  return (
    <Layout>
      <div className="gx-page">
        <header className="gx-page-header">
          <div className="gx-page-header-main">
            <p className="gx-page-kicker">Configuration</p>
            <h1 className="gx-page-title">Settings</h1>
            <p className="gx-page-subtitle">
              Realms, integrations, and data sources for Goblin.
            </p>
          </div>
          <div className="gx-page-header-actions">
            <button className="gx-btn gx-btn-primary">Save changes</button>
            <button className="gx-btn gx-btn-ghost">Reset</button>
          </div>
        </header>

        <div className="gx-grid">
          <section className="gx-card gx-card-wide">
            <h2 className="gx-card-title">Settings & realms</h2>
            <p className="gx-card-subtitle">Configure realms, API keys, and preferences.</p>
            <div className="gx-card-placeholder">Settings placeholder.</div>
          </section>

          <section className="gx-card">
            <h2 className="gx-card-title">Integrations</h2>
            <p className="gx-card-subtitle">TSM, WCL, custom APIs.</p>
            <div className="gx-card-placeholder">Integrations placeholder.</div>
          </section>

          <section className="gx-card">
            <h2 className="gx-card-title">Security</h2>
            <p className="gx-card-subtitle">Tokens and permissions.</p>
            <div className="gx-card-placeholder">Security placeholder.</div>
          </section>
        </div>
      </div>
    </Layout>
  );
};
