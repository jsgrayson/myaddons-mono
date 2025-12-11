import React, { useEffect, useState } from "react";
import { Layout } from "../components/layout/Layout";
import "./shared.css";
import { apiListEncounters } from "../api/client";
import type { EncounterSummary } from "../api/client";

export const EncountersPage: React.FC = () => {
  const [encounters, setEncounters] = useState<EncounterSummary[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiListEncounters()
      .then((data) => setEncounters(data))
      .finally(() => setLoading(false));
  }, []);

  return (
    <Layout>
      <div className="sw-page">
        <header className="sw-page-header">
          <div className="sw-page-header-main">
            <p className="sw-page-kicker">Profiles</p>
            <h1 className="sw-page-title">Encounters</h1>
            <p className="sw-page-subtitle">
              Associate builds, rotations, and macros with specific bosses and
              keys.
            </p>
          </div>
          <div className="sw-page-header-actions">
            <button className="sw-btn sw-btn-primary">New encounter profile</button>
          </div>
        </header>

        <div className="sw-grid">
          <section className="sw-card sw-card-wide">
            <h2 className="sw-card-title">Encounter profiles</h2>
            <p className="sw-card-subtitle">
              This table will be backed by your logs and manual profiles later.
            </p>
            <div className="sw-card-placeholder" style={{ minHeight: 0 }}>
              {loading ? (
                <>Loading encounters…</>
              ) : encounters.length === 0 ? (
                <>No encounters yet. They will appear here after you sync.</>
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
                        Context
                      </th>
                      <th style={{ textAlign: "left", padding: "4px 6px" }}>
                        Profile
                      </th>
                      <th style={{ textAlign: "left", padding: "4px 6px" }}>
                        Last seen
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {encounters.map((e) => (
                      <tr key={e.id}>
                        <td style={{ padding: "4px 6px" }}>{e.name}</td>
                        <td style={{ padding: "4px 6px" }}>
                          {encounterContextLabel(e.context)}
                        </td>
                        <td style={{ padding: "4px 6px" }}>{e.profileName}</td>
                        <td style={{ padding: "4px 6px" }}>
                          {e.lastSeen
                            ? new Date(e.lastSeen).toLocaleString()
                            : "—"}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          </section>

          <section className="sw-card sw-card-wide">
            <h2 className="sw-card-title">Timeline / plan</h2>
            <p className="sw-card-subtitle">
              Eventually this will let you plan cooldowns and phases visually.
            </p>
            <div className="sw-card-placeholder">
              Encounter timeline placeholder.
            </div>
          </section>
        </div>
      </div>
    </Layout>
  );
};

function encounterContextLabel(
  c: EncounterSummary["context"]
): string {
  switch (c) {
    case "DUNGEON":
      return "Dungeon";
    case "RAID":
      return "Raid";
    case "WORLD":
      return "World";
    default:
      return c;
  }
}
