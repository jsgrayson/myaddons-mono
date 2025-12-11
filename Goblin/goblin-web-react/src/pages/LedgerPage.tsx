import React from "react";
import { Layout } from "../components/layout/Layout";
import "./shared.css";

export const LedgerPage: React.FC = () => {
  return (
    <Layout>
      <div className="gx-page">
        <header className="gx-page-header">
          <div className="gx-page-header-main">
            <p className="gx-page-kicker">Accounting</p>
            <h1 className="gx-page-title">Ledger</h1>
            <p className="gx-page-subtitle">
              Sales, purchases, and expenses across characters.
            </p>
          </div>
          <div className="gx-page-header-actions">
            <button className="gx-btn gx-btn-primary">Export CSV</button>
            <button className="gx-btn gx-btn-ghost">Filter</button>
          </div>
        </header>

        <div className="gx-grid">
          <section className="gx-card gx-card-wide">
            <h2 className="gx-card-title">Sales & purchases</h2>
            <p className="gx-card-subtitle">Transaction history and summaries.</p>
            <div className="gx-card-placeholder">Ledger table placeholder.</div>
          </section>

          <section className="gx-card">
            <h2 className="gx-card-title">Top buyers</h2>
            <p className="gx-card-subtitle">Who buys from you most.</p>
            <div className="gx-card-placeholder">Top buyers placeholder.</div>
          </section>

          <section className="gx-card">
            <h2 className="gx-card-title">Top sellers</h2>
            <p className="gx-card-subtitle">Most profitable items.</p>
            <div className="gx-card-placeholder">Top sellers placeholder.</div>
          </section>
        </div>
      </div>
    </Layout>
  );
};
