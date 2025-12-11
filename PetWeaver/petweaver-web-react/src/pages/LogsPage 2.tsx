import { useEffect, useState } from 'react';
import { Card } from '../components/ui/Card';

export const LogsPage: React.FC = () => {
  const [lines, setLines] = useState<string[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    import('../api/client')
      .then((m) => m.apiListLogs())
      .then(setLines)
      .catch((e) => {
        console.error(e);
        setError(
          'apiListLogs is not implemented yet. Your AI coder should connect this to your server logs in src/api/client.ts.'
        );
      });
  }, []);

  return (
    <section
      className="space-y-4 page-bg"
      style={{
        backgroundImage: "url('/assets/backgrounds/ember_bg_04.svg')",
        backgroundSize: 'cover',
        backgroundPosition: 'top center',
      }}
    >
      <div className="page-bg-inner space-y-4">
        <h1 className="text-xl font-semibold text-amber-50">Logs</h1>
        <Card className="bg-bg-panel/85">
          {error && <div className="text-xs text-amber-200 mb-2">{error}</div>}
          {!error && !lines && (
            <div className="text-sm text-slate-300">
              Waiting for log stream endpoint…
            </div>
          )}
          {lines && (
            <div className="max-h-80 overflow-y-auto text-xs font-mono text-slate-100 space-y-0.5">
              {lines.map((l, i) => (
                <div key={i}>{l}</div>
              ))}
            </div>
          )}
        </Card>
      </div>
    </section>
  );
};
