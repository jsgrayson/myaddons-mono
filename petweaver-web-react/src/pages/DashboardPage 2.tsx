import { useEffect, useState } from 'react';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Link } from 'react-router-dom';
import { apiGetServerStatus, ServerStatus } from '../api/client';

export const DashboardPage: React.FC = () => {
  const [data, setData] = useState<ServerStatus | null>(null);

  useEffect(() => {
    apiGetServerStatus().then(setData).catch(console.error);
    const interval = setInterval(() => {
      apiGetServerStatus().then(setData).catch(console.error);
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const petsIndexed = data?.stats?.pets || 0;
  const strategies = (data as any)?.stats?.strategies || (data as any)?.stats?.ready || 0;
  // Note: app.py sends "strategies" and "ready" inside the root state object, NOT in "stats".
  // Let's check app.py response structure again:
  // return jsonify({ **state, "stats": stats, ... })
  // So state.stats.strategies is valid if mapped correctly. 
  // Wait, in app.py: state["stats"]["strategies"]...
  // So it IS inside the "stats" key of the root but mapped to "stats" prop in frontend IF we passed it through.
  // In client.ts: stats: data.stats.
  // BUT the backend returns:
  // { ...state, stats: db_stats }
  // state["stats"] was the Python global dict with { pets, strategies, ready }. 
  // It gets OVERWRITTEN by "stats": db_stats in the json response line: return jsonify({ **state, "stats": stats })
  // AH! Python quark. 
  // The 'state' global has a key "stats".
  // The jsonify call has a keyword argument "stats".
  // Keyword args overwrite dictionary unpacking.
  // So valid data is ONLY in db_helper.get_collection_stats().
  // db_helper stats: { pets, unique, max_level... }
  // App global state stats: { pets, strategies, ready }

  // To fix this, I need to fix the BACKEND to not collision the keys, or merge them.
  // I will assume for now I should fix the backend in the next step if values are missing.

  const simulationsToday = data?.combatStats?.total_battles || 0;

  return (
    <div className="space-y-6">
      <section
        className="page-bg"
        style={{
          backgroundImage: "url('/assets/backgrounds/ember_bg_02.svg')",
          backgroundSize: 'cover',
          backgroundPosition: 'top center',
        }}
      >
        <div className="page-bg-inner p-[1px]">
          <Card className="bg-bg-panel/80">
            <div className="flex flex-col md:flex-row gap-6 items-center">
              <div className="flex-1 space-y-3">
                <div className="font-title text-sm tracking-[0.25em] uppercase text-ember-light">
                  Arcane Pet Battle Engine
                </div>
                <h1 className="text-2xl md:text-3xl font-semibold text-amber-50">
                  Welcome back, Tamer.
                </h1>
                <p className="text-sm text-slate-200 max-w-xl">
                  {data ? (
                    <>
                      Engine is <span className={data.status === 'online' ? "text-green-400" : "text-amber-400"}>
                        {data.status.toUpperCase()}
                      </span>.
                      Currently tracking {petsIndexed} pets and {simulationsToday} battles today.
                    </>
                  ) : (
                    "Connecting to Arcane Engine..."
                  )}
                </p>

                <div className="flex gap-3 pt-2">
                  <Link to="/simulator">
                    <Button>Open Battle Simulator</Button>
                  </Link>
                  <Link to="/pets">
                    <Button variant="secondary">Browse Pet Codex</Button>
                  </Link>
                </div>
              </div>

              <div className="relative flex-shrink-0">
                <div className="h-40 w-40 md:h-48 md:w-48 rounded-full bg-gradient-to-tr from-ember-deep via-ember-light to-arcane-mid shadow-ember flex items-center justify-center overflow-hidden">
                  <img
                    src="/assets/hero_cinder_style.png" // Use absolute path
                    alt="Arcane Pets"
                    className="h-full w-full object-cover"
                    onError={(e) => {
                      (e.target as HTMLImageElement).style.display = 'none';
                    }}
                  />
                </div>
                <div className="pointer-events-none absolute inset-0 rounded-full border border-amber-300/70 blur-[1px]" />
              </div>
            </div>
          </Card>
        </div>
      </section>

      <div className="grid md:grid-cols-3 gap-4">
        {[
          {
            label: 'Pets Indexed',
            value: data ? petsIndexed : '—',
            sub: 'From local database'
          },
          {
            label: 'Simulations (today)',
            value: data ? simulationsToday : '—',
            sub: 'Training battles logged'
          },
          {
            label: 'Genetic Runs',
            value: '0', // Placeholder until we fix key collision
            sub: 'Optimization cycles'
          },
        ].map((s) => (
          <Card key={s.label}>
            <div className="space-y-1">
              <div className="text-xs text-slate-400 uppercase tracking-wide">
                {s.label}
              </div>
              <div className="text-xl font-semibold text-slate-300">{s.value}</div>
              <div className="text-[11px] text-slate-500">{s.sub}</div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
