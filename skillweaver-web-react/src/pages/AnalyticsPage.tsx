import React from "react";
import { Layout } from "../components/layout/Layout";
import "./shared.css";

export const AnalyticsPage: React.FC = () => {
  return (
    <Layout>
      <div className="sw-page">
        <header className="sw-page-header">
          <div className="sw-page-header-main">
            <p className="sw-page-kicker">Stats</p>
            <h1 className="sw-page-title">Analytics</h1>
            <p className="sw-page-subtitle">
              Later this will pull from logs to show performance metrics,
              cooldown usage, and missed opportunities.
            </p>
          </div>
        </header>

        <div className="sw-grid">
          <section className="sw-card sw-card-wide">
            <h2 className="sw-card-title">Performance overview</h2>
            <p className="sw-card-subtitle">
              Once wired, charts and breakdowns per encounter will appear here.
            </p>
            <div className="sw-card-placeholder">
              Analytics charts placeholder.
            </div>
          </section>
        </div>
      </div>
    </Layout>
  );
};
