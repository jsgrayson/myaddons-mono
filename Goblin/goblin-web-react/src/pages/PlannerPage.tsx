import React from "react";
import { Layout } from "../components/layout/Layout";
import "./shared.css";

export const PlannerPage: React.FC = () => {
  return (
    <Layout>
      <div className="gx-page">
        <header className="gx-page-header">
          <div className="gx-page-header-main">
            <p className="gx-page-kicker">Spec planner</p>
            <h1 className="gx-page-title">Planner</h1>
            <p className="gx-page-subtitle">
              Distribute skill points and specializations for your trade.
            </p>
          </div>
          <div className="gx-page-header-actions">
            <button className="gx-btn gx-btn-primary">Save plan</button>
            <button className="gx-btn gx-btn-ghost">Export</button>
          </div>
        </header>

        <div className="gx-grid">
          <section className="gx-card gx-card-wide">
            <h2 className="gx-card-title">Spec planner</h2>
            <p className="gx-card-subtitle">Tree layout and point allocation.</p>
            <div className="gx-card-placeholder">Spec planner placeholder.</div>
          </section>

          <section className="gx-card">
            <h2 className="gx-card-title">Bonuses</h2>
            <p className="gx-card-subtitle">Show perks unlocked per spec.</p>
            <div className="gx-card-placeholder">Bonuses placeholder.</div>
          </section>

          <section className="gx-card">
            <h2 className="gx-card-title">Materials focus</h2>
            <p className="gx-card-subtitle">Material targets and notes.</p>
            <div className="gx-card-placeholder">Materials focus placeholder.</div>
          </section>
        </div>
      </div>
    </Layout>
  );
};
