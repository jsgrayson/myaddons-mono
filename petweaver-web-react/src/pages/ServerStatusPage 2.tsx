import { useEffect, useState } from 'react';
import { Card } from '../components/ui/Card';
import type { ServerStatus } from '../api/client';

export const ServerStatusPage: React.FC = () => {
  const [status, setStatus] = useState<ServerStatus | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    import('../api/client')
      .then((m) => m.apiGetServerStatus())
      .then(setStatus)
      .catch((e) => {
        console.error(e);
        setError(
          'apiGetServerStatus is not implemented yet. Your AI coder should connect this to your worker / queue stats in src/api/client.ts.'
        );
      });
  }, []);

  return (
    <section
      className="space-y-4 page-bg"
      style={{
        backgroundImage: "url('/assets/backgrounds/ember_bg_05.svg')",
        backgroundSize: 'cover',
        backgroundPosition: 'top center',
      }}
    >
      <div className="page-bg-inner space-y-4">
        <h1 className="text-xl font-semibold text-amber-50">Server Status</h1>
        <Card className="bg-bg-panel/85">
          {error && <div className="text-xs text-amber-200 mb-2">{error}</div>}
          {!status && !error && (
            <div className="text-sm text-slate-300">
              Waiting for backend status endpoint…
            </div>
          )}
          {status && (
            <div className="text-sm text-slate-200 space-y-1">
              <div>
                Status:{' '}
                <span className="font-mono text-amber-200">{status.status}</span>
              </div>
              <div>Uptime: {Math.round(status.uptimeSeconds / 3600)}h</div>
              <div>Queue depth: {status.queueDepth}</div>
              <div>Workers: {status.workers}</div>
            </div>
          )}
        </Card>
      </div>
    </section>
  );
};
