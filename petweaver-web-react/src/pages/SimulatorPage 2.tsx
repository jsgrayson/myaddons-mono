import { useState } from 'react';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';

export const SimulatorPage: React.FC = () => {
  const [log, setLog] = useState<string[]>([]);
  const [error, setError] = useState<string | null>(null);

  async function runSimulation() {
    setError(null);
    setLog((prev) => [...prev, 'Casting simulation spell…']);
    try {
      const m = await import('../api/client');
      const result = await m.apiRunSimulation({});
      setLog(result.log);
    } catch (e: any) {
      console.error(e);
      setError(
        'apiRunSimulation is not implemented yet. Your AI coder should connect this to your simulator backend in src/api/client.ts.'
      );
    }
  }

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
        <div className="flex items-center justify-between gap-4">
          <div>
            <h1 className="text-xl font-semibold text-amber-50">Battle Simulator</h1>
            <p className="text-xs text-slate-200">
              UI is ready. Wire <code className="font-mono text-[11px]">
                apiRunSimulation
              </code>{' '}
              to your engine to stream real combat logs.
            </p>
          </div>
          <Button onClick={runSimulation}>Run Simulation</Button>
        </div>

        <div className="grid md:grid-cols-[minmax(0,1.2fr)_minmax(0,1fr)] gap-4">
          <Card className="bg-bg-panel/85">
            <div className="text-sm text-slate-200">
              Team builder UI goes here — your coder can either:
              <ul className="list-disc ml-5 mt-1 text-xs text-slate-300 space-y-1">
                <li>Expose server-side presets</li>
                <li>Or build a drag-and-drop grid that maps to your engine payload</li>
              </ul>
            </div>
          </Card>

          <Card className="bg-bg-panel/85">
            <div className="text-xs font-mono text-slate-100 space-y-1 max-h-72 overflow-y-auto">
              {error && (
                <div className="text-amber-200 mb-2">
                  {error}
                </div>
              )}
              {log.length === 0 && !error && (
                <div className="text-slate-400">
                  No simulations yet. Hit <span className="text-ember-light">Run</span>{' '}
                  once your backend is connected.
                </div>
              )}
              {log.map((line, idx) => (
                <div key={idx}>{line}</div>
              ))}
            </div>
          </Card>
        </div>
      </div>
    </section>
  );
};
