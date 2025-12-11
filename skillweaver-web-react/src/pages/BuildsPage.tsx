import React, { useEffect, useState } from "react";
import { Layout } from "../components/layout/Layout";
import "./shared.css";
import { apiListBuilds } from "../api/client";
import type { BuildSummary } from "../api/client";

export const BuildsPage: React.FC = () => {
  const [builds, setBuilds] = useState<BuildSummary[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiListBuilds()
      .then((data) => setBuilds(data))
      .finally(() => setLoading(false));
  }, []);

  return (
    <Layout>
      <div className="sw-page">
        <header className="sw-page-header">
          <div className="sw-page-header-main">
            <p className="sw-page-kicker">Builds</p>
            <h1 className="sw-page-title">Talent Planner</h1>
            <p className="sw-page-subtitle">
              Manage your talent builds for different content profiles and send
              them to the SkillWeaver addon.
            </p>
          </div>
          <div className="sw-page-header-actions">
            <button className="sw-btn sw-btn-primary">New build</button>
            <button className="sw-btn sw-btn-ghost">Import from game</button>
          </div>
        </header>

        <div className="sw-grid">
          <section className="sw-card sw-card-wide">
            <h2 className="sw-card-title">Builds for this spec</h2>
            <p className="sw-card-subtitle">
              Once wired, these will match your current spec and character.
            </p>

            <div className="sw-card-placeholder" style={{ minHeight: 0 }}>
              {loading ? (
                <>Loading builds…</>
              ) : builds.length === 0 ? (
                <>No builds yet. Create your first build to get started.</>
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
                        Spec
                      </th>
                      <th style={{ textAlign: "left", padding: "4px 6px" }}>
                        Type
                      </th>
                      <th style={{ textAlign: "left", padding: "4px 6px" }}>
                        Updated
                      </th>
                      <th style={{ textAlign: "left", padding: "4px 6px" }}>
                        Recommended
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {builds.map((build) => (
                      <tr key={build.id}>
                        <td style={{ padding: "4px 6px" }}>{build.name}</td>
                        <td style={{ padding: "4px 6px" }}>{build.specName}</td>
                        <td style={{ padding: "4px 6px" }}>
                          {archetypeLabel(build.archetype)}
                        </td>
                        <td style={{ padding: "4px 6px" }}>
                          {new Date(build.lastUpdated).toLocaleString()}
                        </td>
                        <td style={{ padding: "4px 6px" }}>
                          {build.isRecommended ? "★" : "—"}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          </section>

          <section className="sw-card sw-card-wide">
            <h2 className="sw-card-title">Planner</h2>
            <p className="sw-card-subtitle">
              Later this will show a proper tree view for talents and a diff
              against your in-game build.
            </p>
            <div className="sw-card-placeholder">
              Talent tree / planner UI placeholder.
            </div>
          </section>
        </div>
      </div>
    </Layout>
  );
};

function archetypeLabel(a: BuildSummary["archetype"]): string {
  switch (a) {
    case "ST":
      return "Single Target";
    case "AOE":
      return "AoE";
    case "MYTHIC_PLUS":
      return "Mythic+";
    case "RAID":
      return "Raid";
    case "PVP":
      return "PvP";
    default:
      return a;
  }
}
