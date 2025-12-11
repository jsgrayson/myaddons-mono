import React from "react";
import { Layout } from "../components/layout/Layout";
import "./shared.css";

export const TradeSkillPage: React.FC = () => {
  return (
    <Layout>
      <div className="gx-page">
        <header className="gx-page-header">
          <div className="gx-page-header-main">
            <p className="gx-page-kicker">Leveling guide</p>
            <h1 className="gx-page-title">TradeSkill Guide</h1>
            <p className="gx-page-subtitle">
              Plan your leveling path with costs, mats, and skill jumps.
            </p>
          </div>
          <div className="gx-page-header-actions">
            <button className="gx-btn gx-btn-primary">New guide</button>
            <button className="gx-btn gx-btn-ghost">Import plan</button>
          </div>
        </header>

        <div className="gx-grid">
          <section className="gx-card gx-card-wide">
            <h2 className="gx-card-title">Tradeskill leveling guide</h2>
            <p className="gx-card-subtitle">Future: steps, mats, and vendor lists.</p>
            <div className="gx-card-placeholder">
              Tradeskill leveling guide placeholder.
            </div>
          </section>

          <section className="gx-card">
            <h2 className="gx-card-title">Materials</h2>
            <p className="gx-card-subtitle">Breakdown of required mats.</p>
            <div className="gx-card-placeholder">Materials placeholder.</div>
          </section>

          <section className="gx-card">
            <h2 className="gx-card-title">Cost estimate</h2>
            <p className="gx-card-subtitle">Projected cost to cap.</p>
            <div className="gx-card-placeholder">Cost placeholder.</div>
          </section>
        </div>
      </div>
    </Layout>
  );
};
