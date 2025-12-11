import React, { useEffect, useState } from "react";
import { Layout } from "../components/layout/Layout";
import "./shared.css";
import {
  apiGetCurrentProfile,
  apiGetRotationHealth,
  apiListMacros,
} from "../api/client";
import type {
  CharacterProfile,
  RotationHealth,
  MacroSummary,
} from "../api/client";

export const DashboardPage: React.FC = () => {
  const [profile, setProfile] = useState<CharacterProfile | null>(null);
  const [rotationHealth, setRotationHealth] = useState<RotationHealth | null>(
    null
  );
  const [macros, setMacros] = useState<MacroSummary[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;

    async function load() {
      try {
        const [p, h, m] = await Promise.all([
          apiGetCurrentProfile(),
          apiGetRotationHealth(),
          apiListMacros(),
        ]);
        if (cancelled) return;
        setProfile(p);
        setRotationHealth(h);
        setMacros(m);
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    load();
    return () => {
      cancelled = true;
    };
  }, []);

  const outOfDateCount = macros.filter((m) => m.outOfDate).length;

  return (
    <Layout>
      <div className="sw-page">
        <header className="sw-page-header">
          <div className="sw-page-header-main">
            <p className="sw-page-kicker">Overview</p>
            <h1 className="sw-page-title">Combat Dashboard</h1>
            <p className="sw-page-subtitle">
              See your current spec, rotation health, and macro status at a
              glance. All data is mock right now, ready to be wired to the
              addon later.
            </p>
          </div>
          <div className="sw-page-header-actions">
            <button className="sw-btn sw-btn-primary">Sync with addon</button>
            <button className="sw-btn sw-btn-ghost">Open macros</button>
          </div>
        </header>

        <div className="sw-grid">
          {/* Character / spec card */}
          <section className="sw-card">
            <h2 className="sw-card-title">Active character</h2>
            <p className="sw-card-subtitle">
              Spec and build currently synced from the SkillWeaver addon.
            </p>
            <div className="sw-card-placeholder">
              {loading ? (
                <>Loading profile…</>
              ) : profile ? (
                <div style={{ textAlign: "left", width: "100%" }}>
                  <div style={{ fontSize: "0.9rem", marginBottom: 4 }}>
                    <strong>
                      {profile.name}-{profile.realm}
                    </strong>
                  </div>
                  <div style={{ fontSize: "0.8rem", marginBottom: 4 }}>
                    {profile.classId} – {profile.specName}
                  </div>
                  <div style={{ fontSize: "0.8rem" }}>
                    Item level:{" "}
                    {profile.ilvl ? `${profile.ilvl}` : "Unknown (not synced)"}
                  </div>
                  <div style={{ fontSize: "0.75rem", marginTop: 6 }}>
                    Last sync:{" "}
                    {profile.lastSync
                      ? new Date(profile.lastSync).toLocaleString()
                      : "No sync yet"}
                  </div>
                </div>
              ) : (
                <>No character data yet. Sync with the addon to begin.</>
              )}
            </div>
          </section>

          {/* Rotation health */}
          <section className="sw-card">
            <h2 className="sw-card-title">Rotation health</h2>
            <p className="sw-card-subtitle">
              Once wired to logs, this will be derived from real pulls. For now
              it’s a stubbed score.
            </p>
            <div className="sw-card-placeholder">
              {rotationHealth ? (
                <div style={{ textAlign: "left", width: "100%" }}>
                  <div style={{ marginBottom: 4 }}>
                    <span className="sw-badge">
                      Score: {rotationHealth.score}/100
                    </span>
                  </div>
                  <div style={{ fontSize: "0.8rem" }}>
                    Missed procs: {rotationHealth.missedProcs}
                    <br />
                    Cooldown desyncs: {rotationHealth.cdDesyncs}
                  </div>
                  <div style={{ fontSize: "0.8rem", marginTop: 6 }}>
                    {rotationHealth.comment}
                  </div>
                </div>
              ) : (
                <>No rotation profile loaded yet.</>
              )}
            </div>
          </section>

          {/* Macro status */}
          <section className="sw-card">
            <h2 className="sw-card-title">Macro status</h2>
            <p className="sw-card-subtitle">
              GSE-style sequences and simple macros for this spec.
            </p>
            <div className="sw-card-placeholder">
              {loading ? (
                <>Loading macros…</>
              ) : macros.length === 0 ? (
                <>No macros defined yet.</>
              ) : (
                <div style={{ textAlign: "left", width: "100%" }}>
                  <div style={{ marginBottom: 6, fontSize: "0.8rem" }}>
                    Total macros: {macros.length}
                  </div>
                  {outOfDateCount > 0 && (
                    <div
                      style={{
                        marginBottom: 8,
                        fontSize: "0.8rem",
                      }}
                    >
                      <span className="sw-badge sw-badge-danger">
                        {outOfDateCount} out of date
                      </span>
                    </div>
                  )}
                  <ul
                    style={{
                      listStyle: "none",
                      padding: 0,
                      margin: 0,
                      fontSize: "0.8rem",
                    }}
                  >
                    {macros.map((m) => (
                      <li
                        key={m.id}
                        style={{
                          display: "flex",
                          justifyContent: "space-between",
                          gap: 8,
                          marginBottom: 4,
                        }}
                      >
                        <span>
                          {m.name}{" "}
                          <span style={{ opacity: 0.7 }}>
                            ({macroScopeLabel(m.scope)})
                          </span>
                        </span>
                        <span style={{ whiteSpace: "nowrap" }}>
                          {m.boundKey && (
                            <span className="sw-badge">
                              Key: {m.boundKey}
                            </span>
                          )}
                          {m.outOfDate && (
                            <span className="sw-badge sw-badge-danger">
                              Out of date
                            </span>
                          )}
                        </span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </section>

          {/* Encounters / recent pulls placeholder */}
          <section className="sw-card sw-card-wide">
            <h2 className="sw-card-title">Recent encounters</h2>
            <p className="sw-card-subtitle">
              When you connect logs, recent pulls and their assigned profiles
              will appear here.
            </p>
            <div className="sw-card-placeholder">
              Encounter list / performance summary placeholder.
            </div>
          </section>
        </div>
      </div>
    </Layout>
  );
};

function macroScopeLabel(scope: MacroSummary["scope"]): string {
  switch (scope) {
    case "ST":
      return "Single Target";
    case "AOE":
      return "AoE";
    case "UTILITY":
      return "Utility";
    case "DEFENSIVE":
      return "Defensive";
    default:
      return scope;
  }
}
