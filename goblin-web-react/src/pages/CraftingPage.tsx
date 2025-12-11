import React from "react";
import { Layout } from "../components/layout/Layout";
import "./shared.css";

export const CraftingPage: React.FC = () => {
  return (
    <Layout>
      <div className="gx-page">
        <header className="gx-page-header">
          <div className="gx-page-header-main">
            <p className="gx-page-kicker">Production</p>
            <h1 className="gx-page-title">Crafting</h1>
            <p className="gx-page-subtitle">
              Queue profitable crafts and simulate margins.
            </p>
          </div>
          <div className="gx-page-header-actions">
            <button className="gx-btn gx-btn-primary">New queue</button>
            <button className="gx-btn gx-btn-ghost">Import from TSM</button>
          </div>
        </header>

        <div className="gx-grid">
          <section className="gx-card gx-card-wide">
            <h2 className="gx-card-title">Crafting profit / queues</h2>
            <p className="gx-card-subtitle">List crafts with costs, profit, and reagents.</p>
            <div className="gx-card-placeholder">Crafting queue placeholder.</div>
          </section>

          <section className="gx-card">
            <h2 className="gx-card-title">Reagent optimizer</h2>
            <p className="gx-card-subtitle">Find cheapest sources and substitutions.</p>
            <div className="gx-card-placeholder">Reagent optimizer placeholder.</div>
          </section>

          <section className="gx-card">
            <h2 className="gx-card-title">Cooldowns</h2>
            <p className="gx-card-subtitle">Track profession cooldowns.</p>
            <div className="gx-card-placeholder">Cooldowns placeholder.</div>
          </section>
        </div>
      </div>
    </Layout>
  );
};
