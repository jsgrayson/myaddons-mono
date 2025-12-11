import React from "react";
import { Layout } from "../components/layout/Layout";
import "./shared.css";

export const InventoryPage: React.FC = () => {
  return (
    <Layout>
      <div className="gx-page">
        <header className="gx-page-header">
          <div className="gx-page-header-main">
            <p className="gx-page-kicker">Storage</p>
            <h1 className="gx-page-title">Inventory & Banks</h1>
            <p className="gx-page-subtitle">
              Consolidate bags, banks, and alts into one view.
            </p>
          </div>
          <div className="gx-page-header-actions">
            <button className="gx-btn gx-btn-primary">Sync banks</button>
            <button className="gx-btn gx-btn-ghost">Filter</button>
          </div>
        </header>

        <div className="gx-grid">
          <section className="gx-card gx-card-wide">
            <h2 className="gx-card-title">Inventory & banks</h2>
            <p className="gx-card-subtitle">Search and sort items across characters.</p>
            <div className="gx-card-placeholder">Inventory placeholder.</div>
          </section>

          <section className="gx-card">
            <h2 className="gx-card-title">Reagents</h2>
            <p className="gx-card-subtitle">Track crafting mats on hand.</p>
            <div className="gx-card-placeholder">Reagent list placeholder.</div>
          </section>

          <section className="gx-card">
            <h2 className="gx-card-title">Mail & storage</h2>
            <p className="gx-card-subtitle">Mailbox and guild bank summaries.</p>
            <div className="gx-card-placeholder">Mail summary placeholder.</div>
          </section>
        </div>
      </div>
    </Layout>
  );
};
