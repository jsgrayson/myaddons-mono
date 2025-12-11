import { useEffect, useState } from 'react';
import { Card } from '../components/ui/Card';
import { PetCard } from '../components/pets/PetCard';
import type { PetSummary } from '../api/client';
import { Button } from '../components/ui/Button';

export const PetsPage: React.FC = () => {
  const [pets, setPets] = useState<PetSummary[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // This will throw until your API coder wires apiListPets
    import('../api/client')
      .then((m) => m.apiListPets())
      .then(setPets)
      .catch((err) => {
        console.error(err);
        setError(
          'apiListPets is not implemented yet. Your AI coder should connect this to your backend in src/api/client.ts.'
        );
      });
  }, []);

  return (
    <section
      className="space-y-4 page-bg"
      style={{
        backgroundImage: "url('/assets/backgrounds/ember_bg_03.svg')",
        backgroundSize: 'cover',
        backgroundPosition: 'top center',
      }}
    >
      <div className="page-bg-inner space-y-4">
        <div className="flex items-end justify-between gap-4">
          <div>
            <h1 className="text-xl font-semibold text-amber-50">Pet Codex</h1>
            <p className="text-xs text-slate-200">
              This will list every pet your engine knows about once the backend is
              connected.
            </p>
          </div>
        </div>

        <Card className="bg-bg-panel/85">
          {error && (
            <div className="mb-3 rounded-md border border-amber-500/60 bg-bg-panelSoft/80 px-3 py-2 text-[11px] text-amber-100">
              {error}
            </div>
          )}
          {!error && pets === null && (
            <div className="text-sm text-slate-300">
              Contacting the codex… (waiting for backend hook-up)
            </div>
          )}
          {pets && pets.length === 0 && (
            <div className="text-sm text-slate-300">
              The codex is connected but returned no pets yet.
            </div>
          )}
          {pets && pets.length > 0 && (
            <div className="grid sm:grid-cols-2 md:grid-cols-3 gap-4">
              {pets.map((p) => (
                <PetCard key={p.id} pet={p} />
              ))}
            </div>
          )}
          <div className="mt-4">
            <Button
              variant="ghost"
              onClick={() => {
                window.alert(
                  'Your AI coder should implement apiListPets in src/api/client.ts to fetch from your backend.'
                );
              }}
            >
              Integration hint
            </Button>
          </div>
        </Card>
      </div>
    </section>
  );
};
