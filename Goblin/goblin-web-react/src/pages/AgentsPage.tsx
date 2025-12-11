import React from "react";
import { Layout } from "../components/layout/Layout";
import "./shared.css";

export const AgentsPage: React.FC = () => {
  return (
    <Layout>
      <div className="gx-page">
        <header className="gx-page-header">
          <div className="gx-page-header-main">
            <p className="gx-page-kicker">Automation</p>
            <h1 className="gx-page-title">Agents</h1>
            <p className="gx-page-subtitle">
              Manage Goblin agents like TSM Brain and Warden.
            </p>
          </div>
          <div className="gx-page-header-actions">
            <button className="gx-btn gx-btn-primary">Dispatch agent</button>
            <button className="gx-btn gx-btn-ghost">View logs</button>
          </div>
        </header>

        <div className="gx-grid">
          <section className="gx-card gx-card-wide">
            <h2 className="gx-card-title">Agents & automation</h2>
            <p className="gx-card-subtitle">Queue actions, monitor runs, and status.</p>
            <div className="gx-card-placeholder">Agents overview placeholder.</div>
          </section>

          <section className="gx-card">
            <h2 className="gx-card-title">TSM Brain</h2>
            <p className="gx-card-subtitle">Insights and controls.</p>
            <div className="gx-card-placeholder">TSM Brain placeholder.</div>
          </section>

          <section className="gx-card">
            <h2 className="gx-card-title">Warden</h2>
            <p className="gx-card-subtitle">Automation guardrails.</p>
            <div className="gx-card-placeholder">Warden placeholder.</div>
          </section>
        </div>
      </div>
    </Layout>
  );
};
