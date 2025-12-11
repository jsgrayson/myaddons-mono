import React, { useEffect, useState } from "react";
import { Layout } from "../components/layout/Layout";
import "./shared.css";
import { apiGetRotationHealth } from "../api/client";
import type { RotationHealth } from "../api/client";

export const RotationPage: React.FC = () => {
  const [health, setHealth] = useState<RotationHealth | null>(null);

  useEffect(() => {
    apiGetRotationHealth().then(setHealth);
  }, []);

  return (
    <Layout>
      <div className="sw-page">
        <header className="sw-page-header">
          <div className="sw-page-header-main">
            <p className="sw-page-kicker">Logic</p>
            <h1 className="sw-page-title">Rotation Engine</h1>
            <p className="sw-page-subtitle">
              Define your priority list and cooldown rules. SkillWeaver will
              turn this into sequences and macro hints.
            </p>
          </div>
          <div className="sw-page-header-actions">
            <button className="sw-btn sw-btn-primary">New profile</button>
          </div>
        </header>

        <div className="sw-grid">
          <section className="sw-card">
            <h2 className="sw-card-title">Rotation health</h2>
            <p className="sw-card-subtitle">
              Once wired to logs, this will be based on real encounters.
            </p>
            <div className="sw-card-placeholder">
              {health ? (
                <div style={{ textAlign: "left" }}>
                  <div>Score: {health.score}/100</div>
                  <div>Missed procs: {health.missedProcs}</div>
                  <div>CD desyncs: {health.cdDesyncs}</div>
                  <div style={{ marginTop: 4 }}>{health.comment}</div>
                </div>
              ) : (
                <>No rotation data yet.</>
              )}
            </div>
          </section>

          <section className="sw-card sw-card-wide">
            <h2 className="sw-card-title">Priority list</h2>
            <p className="sw-card-subtitle">
              Later this will be a proper editor for ST / AoE / execute rules.
            </p>
            <div className="sw-card-placeholder">
              Priority editor placeholder.
            </div>
          </section>
        </div>
      </div>
    </Layout>
  );
};
