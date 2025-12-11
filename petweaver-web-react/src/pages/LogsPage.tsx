import React, { useEffect, useState } from 'react';
import { Layout } from '../components/layout/Layout';
import { Page } from '../theme/components/Page';
import { Panel } from '../theme/components/Panel';
import { apiListLogs } from '../api/client';
import '../styles/tools.css';

export const LogsPage: React.FC = () => {
  const [logs, setLogs] = useState<string[]>([]);

  useEffect(() => {
    const fetchLogs = () => {
      apiListLogs().then(setLogs).catch(console.error);
    };
    fetchLogs();
    const interval = setInterval(fetchLogs, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <Layout>
      <Page backgroundKey="logs">
        <div className="tools-page logs-page">
          <Panel className="tools-panel">
            <header className="page-header">
              <div className="page-header-main">
                <p className="page-kicker">Midnight mode • Event Stream</p>
                <h1 className="page-title">Logs</h1>
                <p className="page-subtitle">
                  Inspect server and simulation logs for debugging and tuning.
                </p>
              </div>
              <div className="page-header-actions">
                <button className="btn-ghost" type="button">
                  Download
                </button>
              </div>
            </header>

            <div className="tools-layout">
              <section className="tools-col card-midnight">
                <h2 className="card-title">Filters</h2>
                <div className="tools-card-body">
                  <div className="tools-placeholder">
                    Level / category / search filters.
                  </div>
                </div>
              </section>

              <section className="tools-col">
                <article className="card-midnight">
                  <h2 className="card-title">Log Stream</h2>
                  <div className="tools-card-body tools-log">
                    {logs.length === 0 ? (
                      <div className="tools-log-empty">
                        Live or recent logs will show here once the backend is streaming them.
                      </div>
                    ) : (
                      <pre className="whitespace-pre-wrap font-mono text-xs text-slate-200">
                        {logs.join('\n')}
                      </pre>
                    )}
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
