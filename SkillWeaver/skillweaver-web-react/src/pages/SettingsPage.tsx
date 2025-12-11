import React from "react";
import { Layout } from "../components/layout/Layout";
import "./shared.css";

export const SettingsPage: React.FC = () => {
  return (
    <Layout>
      <div className="sw-page">
        <header className="sw-page-header">
          <div className="sw-page-header-main">
            <p className="sw-page-kicker">System</p>
            <h1 className="sw-page-title">Settings</h1>
            <p className="sw-page-subtitle">
              Control addon integration, export formats, and other SkillWeaver
              preferences.
            </p>
          </div>
        </header>

        <div className="sw-grid">
          <section className="sw-card">
            <h2 className="sw-card-title">Addon integration</h2>
            <p className="sw-card-subtitle">
              Later this will show which characters/specs are synced.
            </p>
            <div className="sw-card-placeholder">
              Addon sync settings placeholder.
            </div>
          </section>

          <section className="sw-card">
            <h2 className="sw-card-title">Export formats</h2>
            <p className="sw-card-subtitle">
              Choose between GSE, plain macros, and other output types.
            </p>
            <div className="sw-card-placeholder">
              Export preferences placeholder.
            </div>
          </section>
        </div>
      </div>
    </Layout>
  );
};
