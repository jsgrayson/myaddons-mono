import React, { useEffect, useState } from "react";
import { Layout } from "../components/layout/Layout";
import "./shared.css";
import { apiListMacros } from "../api/client";
import type { MacroSummary } from "../api/client";

export const MacrosPage: React.FC = () => {
  const [macros, setMacros] = useState<MacroSummary[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiListMacros()
      .then((data) => setMacros(data))
      .finally(() => setLoading(false));
  }, []);

  return (
    <Layout>
      <div className="sw-page">
        <header className="sw-page-header">
          <div className="sw-page-header-main">
            <p className="sw-page-kicker">Sequences</p>
            <h1 className="sw-page-title">Macro Studio</h1>
            <p className="sw-page-subtitle">
              Design and manage GSE-style sequences and simple macros, then sync
              them to the SkillWeaver addon.
            </p>
          </div>
          <div className="sw-page-header-actions">
            <button className="sw-btn sw-btn-primary">New macro</button>
          </div>
        </header>

        <div className="sw-grid">
          <section className="sw-card sw-card-wide">
            <h2 className="sw-card-title">Macro editor</h2>
            <p className="sw-card-subtitle">
              Later this will be a full sequence editor with steps, reset
              conditions, and preview output.
            </p>
            <div className="sw-card-placeholder">
              Macro editor UI placeholder.
            </div>
          </section>

          <section className="sw-card sw-card-wide">
            <h2 className="sw-card-title">Saved macros</h2>
            <p className="sw-card-subtitle">
              These macros are the ones SkillWeaver will sync with the addon.
            </p>
            <div className="sw-card-placeholder" style={{ minHeight: 0 }}>
              {loading ? (
                <>Loading macros…</>
              ) : macros.length === 0 ? (
                <>No macros defined yet.</>
              ) : (
                <table
                  style={{
                    width: "100%",
                    borderCollapse: "collapse",
                    fontSize: "0.8rem",
                  }}
                >
                  <thead>
                    <tr>
                      <th style={{ textAlign: "left", padding: "4px 6px" }}>
                        Name
                      </th>
                      <th style={{ textAlign: "left", padding: "4px 6px" }}>
                        Scope
                      </th>
                      <th style={{ textAlign: "left", padding: "4px 6px" }}>
                        Keybind
                      </th>
                      <th style={{ textAlign: "left", padding: "4px 6px" }}>
                        Status
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {macros.map((m) => (
                      <tr key={m.id}>
                        <td style={{ padding: "4px 6px" }}>{m.name}</td>
                        <td style={{ padding: "4px 6px" }}>
                          {macroScopeLabel(m.scope)}
                        </td>
                        <td style={{ padding: "4px 6px" }}>
                          {m.boundKey ? m.boundKey : "—"}
                        </td>
                        <td style={{ padding: "4px 6px" }}>
                          {m.outOfDate ? (
                            <span className="sw-badge sw-badge-danger">
                              Out of date
                            </span>
                          ) : (
                            <span className="sw-badge">OK</span>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
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
