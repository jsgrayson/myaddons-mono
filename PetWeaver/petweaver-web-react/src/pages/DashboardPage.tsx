import React from 'react';
import { Layout } from '../components/layout/Layout';
import { Page } from '../theme/components/Page';
import { Panel } from '../theme/components/Panel';
import '../styles/dashboard.css';

export const DashboardPage: React.FC = () => {
  return (
    <Layout>
      <Page backgroundKey="dashboard">
        <div className="dashboard-page">
          <Panel className="dashboard-panel">
            <header className="page-header">
              <div className="page-header-main">
                <p className="page-kicker">Midnight mode • Control Nexus</p>
                <h1 className="page-title">Petweaver Dashboard</h1>
                <p className="page-subtitle">
                  A high-level view of your pet battler server — activity, encounters, and health at a glance.
                </p>
              </div>
              <div className="page-header-actions">
                <button className="btn-primary" type="button">
                  Refresh
                </button>
                <button className="btn-ghost" type="button">
                  View Logs
                </button>
              </div>
            </header>

            <div className="dashboard-grid">
              <section className="card-midnight dashboard-card">
                <h2 className="card-title">Server Status</h2>
                <p className="card-subtitle">
                  Current uptime, active sessions, and queue state.
                </p>
                <div className="dashboard-card-body">
                  <div className="dashboard-metric-row">
                    <span className="dashboard-metric-label">Uptime</span>
                    <span className="dashboard-metric-value">–</span>
                  </div>
                  <div className="dashboard-metric-row">
                    <span className="dashboard-metric-label">Active pet battles</span>
                    <span className="dashboard-metric-value">–</span>
                  </div>
                  <div className="dashboard-metric-row">
                    <span className="dashboard-metric-label">Queue length</span>
                    <span className="dashboard-metric-value">–</span>
                  </div>
                </div>
              </section>

              <section className="card-midnight dashboard-card">
                <h2 className="card-title">Recent Activity</h2>
                <p className="card-subtitle">
                  A quick look at the latest runs and Codex entries.
                </p>
                <div className="dashboard-card-body dashboard-activity-list">
                  <div className="dashboard-activity-empty">
                    No recent activity yet. Once the backend is wired, the latest events will appear here.
                  </div>
                </div>
              </section>

              <section className="card-midnight dashboard-card dashboard-wide">
                <h2 className="card-title">Midnight Overview</h2>
                <p className="card-subtitle">
                  Aggregate stats across your pet teams, encounters, and simulations.
                </p>
                <div className="dashboard-card-body dashboard-summary-grid">
                  <div className="dashboard-summary-item">
                    <div className="dashboard-summary-label">Total pets</div>
                    <div className="dashboard-summary-value">–</div>
                  </div>
                  <div className="dashboard-summary-item">
                    <div className="dashboard-summary-label">Teams configured</div>
                    <div className="dashboard-summary-value">–</div>
                  </div>
                  <div className="dashboard-summary-item">
                    <div className="dashboard-summary-label">Simulations run</div>
                    <div className="dashboard-summary-value">–</div>
                  </div>
                  <div className="dashboard-summary-item">
                    <div className="dashboard-summary-label">Win rate (last 24h)</div>
                    <div className="dashboard-summary-value">–</div>
                  </div>
                </div>
              </section>
            </div>
          </Panel>
        </div>
      </Page>
    </Layout>
  );
};
