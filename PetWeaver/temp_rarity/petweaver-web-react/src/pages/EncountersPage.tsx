import { useEffect, useState } from 'react';
import { Card } from '../components/ui/Card';

export const EncountersPage: React.FC = () => {
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    import('../api/client')
      .then((m) => m.apiListEncounters())
      .then(() => {})
      .catch((e) => {
        console.error(e);
        setError(
          'apiListEncounters is not implemented yet. Your AI coder should connect this to your encounter data in src/api/client.ts.'
        );
      });
  }, []);

  return (
    <section
      className="space-y-4 page-bg"
      style={{
        backgroundImage: "url('/assets/backgrounds/ember_bg_02.svg')",
        backgroundSize: 'cover',
        backgroundPosition: 'top center',
      }}
    >
      <div className="page-bg-inner space-y-4">
        <h1 className="text-xl font-semibold text-amber-50">Encounters</h1>
        <Card className="bg-bg-panel/85">
          {error ? (
            <div className="text-xs text-amber-200">{error}</div>
          ) : (
            <div className="text-sm text-slate-200">
              Once wired, this will list trainers, world quests and boss encounters
              powered by your scraped data.
            </div>
          )}
        </Card>
      </div>
    </section>
  );
};
