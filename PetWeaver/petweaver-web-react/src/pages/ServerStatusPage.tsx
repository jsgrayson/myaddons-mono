import React, { useEffect, useState } from 'react';
import { Layout } from '../components/layout/Layout';
import { Page } from '../theme/components/Page';
import { Panel } from '../theme/components/Panel';
import { apiGetServerStatus, ServerStatus } from '../api/client';
import '../styles/tools.css';

export const ServerStatusPage: React.FC = () => {
  const [status, setStatus] = useState<ServerStatus | null>(null);

  useEffect(() => {
    apiGetServerStatus().then(setStatus).catch(console.error);
  }, []);

  const s: ServerStatus = status || {
    status: 'offline',
    uptimeSeconds: 0,
    queueDepth: 0,
    workers: 0,
    combatStats: { wins: 0, total_battles: 0, win_rate: 0 },
    dbStats: { pets: 0, unique: 0, max_level: 0, rare_or_better: 0, avg_level: 0 },
  };

  const uptime = s.uptimeSeconds
    ? `${Math.floor(s.uptimeSeconds / 3600)}h ${Math.floor((s.uptimeSeconds % 3600) / 60)}m`
    : '—';

  return (
    <Layout>
      <Page backgroundKey="serverStatus">
        <div className="tools-page server-page">
          <Panel className="tools-panel">
            <header className="page-header">
              <div className="page-header-main">
                <p className="page-kicker">Midnight mode • Shard Health</p>
                <h1 className="page-title">Server Status</h1>
                <p className="page-subtitle">
                  Monitor uptime, latency, and current shard health for your Petweaver backend.
                </p>
              </div>
              <div className="page-header-actions">
                <button className="btn-primary" type="button">
                  Ping
                </button>
              </div>
            </header>

            <div className="tools-layout">
              <section className="tools-col card-midnight">
                <h2 className="card-title">Overview</h2>
                <div className="tools-card-body">
                  <div className="space-y-2 text-sm text-slate-200">
                    <div className="flex justify-between border-b border-slate-800 pb-1">
                      <span className="text-slate-400">Status</span>
                      <span className={s.status === 'online' ? 'text-green-300' : 'text-red-300'}>
                        {s.status === 'online' ? 'Online' : 'Offline'}
                      </span>
                    </div>
                    <div className="flex justify-between border-b border-slate-800 pb-1">
                      <span className="text-slate-400">Uptime</span>
                      <span>{uptime}</span>
                    </div>
                    <div className="flex justify-between border-b border-slate-800 pb-1">
                      <span className="text-slate-400">Queue depth</span>
                      <span>{s.queueDepth}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">Active battles</span>
                      <span>{s.combatStats?.total_battles || 0}</span>
                    </div>
                  </div>
                </div>
              </section>

              <section className="tools-col">
                <article className="card-midnight">
                  <h2 className="card-title">Metrics</h2>
                  <div className="tools-card-body">
                    <div className="tools-placeholder">
                      Latency / uptime graphs or metrics.
                    </div>
                  </div>
                </article>

                <article className="card-midnight">
                  <h2 className="card-title">Health Check Log</h2>
                  <div className="tools-card-body tools-log">
                    <div className="tools-log-empty">
                      Health check events will appear here when wired.
                    </div>
                  </div>
                </article>
              </section>
            </div>
          </Panel>
        </div>
      </Page>
    </Layout>
  );
};
