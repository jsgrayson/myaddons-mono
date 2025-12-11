import React from "react";
import { Layout } from "../components/layout/Layout";
import "./shared.css";

export const MarketsPage: React.FC = () => {
  return (
    <Layout>
      <div className="gx-page">
        <header className="gx-page-header">
          <div className="gx-page-header-main">
            <p className="gx-page-kicker">Price intelligence</p>
            <h1 className="gx-page-title">Markets</h1>
            <p className="gx-page-subtitle">
              Scan auction houses for deals and price trends.
            </p>
          </div>
          <div className="gx-page-header-actions">
            <button className="gx-btn gx-btn-primary">Scan markets</button>
            <button className="gx-btn gx-btn-ghost">View deals</button>
          </div>
        </header>

        <div className="gx-grid">
          <section className="gx-card gx-card-wide">
            <h2 className="gx-card-title">Price intelligence / Deals table</h2>
            <p className="gx-card-subtitle">Hook this up to AH scan results.</p>
            <div className="gx-card-placeholder">Deals table placeholder.</div>
          </section>

          <section className="gx-card">
            <h2 className="gx-card-title">Notable commodities</h2>
            <p className="gx-card-subtitle">Top gainers and losers.</p>
            <div className="gx-card-placeholder">Commodity list placeholder.</div>
          </section>

          <section className="gx-card">
            <h2 className="gx-card-title">Watchlist</h2>
            <p className="gx-card-subtitle">Items to alert on.</p>
            <div className="gx-card-placeholder">Watchlist placeholder.</div>
          </section>
        </div>
      </div>
    </Layout>
  );
};
