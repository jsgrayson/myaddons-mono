import React from "react";
import { Layout } from "../components/layout/Layout";
import "./shared.css";

export const DashboardPage: React.FC = () => {
  return (
    <Layout>
      <div className="gx-page">
        <header className="gx-page-header">
          <div className="gx-page-header-main">
            <p className="gx-page-kicker">Cartel overview</p>
            <h1 className="gx-page-title">Dashboard</h1>
            <p className="gx-page-subtitle">
              Track your gold, profit, and Goblin agents in one place.
            </p>
          </div>
          <div className="gx-page-header-actions">
            <button className="gx-btn gx-btn-primary">Sync data</button>
            <button className="gx-btn gx-btn-ghost">Open ledger</button>
          </div>
        </header>

        <div className="gx-grid">
          <section className="gx-card">
            <h2 className="gx-card-title">Total gold</h2>
            <p className="gx-card-subtitle">
              Across all realms, factions, and characters.
            </p>
            <div className="gx-card-placeholder">Gold metric goes here.</div>
          </section>

          <section className="gx-card">
            <h2 className="gx-card-title">24h profit</h2>
            <p className="gx-card-subtitle">Net after purchases and fees.</p>
            <div className="gx-card-placeholder">Profit metric goes here.</div>
          </section>

          <section className="gx-card">
            <h2 className="gx-card-title">Active opportunities</h2>
            <p className="gx-card-subtitle">Items under predicted value.</p>
            <div className="gx-card-placeholder">Deals count goes here.</div>
          </section>

          <section className="gx-card gx-card-wide">
            <h2 className="gx-card-title">Gold over time</h2>
            <p className="gx-card-subtitle">
              Once connected, this will chart your net worth.
            </p>
            <div className="gx-card-placeholder">
              Gold graph placeholder (per day / week).
            </div>
          </section>
        </div>
      </div>
    </Layout>
  );
};
