import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Link } from 'react-router-dom';

export const DashboardPage: React.FC = () => {
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
                  This is the front-end of your PetWeaver lab. Your AI coder just
                  needs to wire the API calls in <code className="font-mono text-xs">
                    src/api/client.ts
                  </code>{' '}
                  to your backend.
                </p>
                <p className="text-xs text-slate-400">
                  Until then, the UI renders with no mock data — just a beautiful shell
                  waiting for real battles.
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
                    src="/assets/hero_cinder_style.png"
                    alt="Arcane Pets"
                    className="h-full w-full object-cover"
                    onError={(e) => {
                      (e.target as HTMLImageElement).style.display = 'none';
                    }}
                  />
                  <span className="text-5xl" style={{ display: 'none' }}>
                    🔥
                  </span>
                </div>
                <div className="pointer-events-none absolute inset-0 rounded-full border border-amber-300/70 blur-[1px]" />
              </div>
            </div>
          </Card>
        </div>
      </section>

      <div className="grid md:grid-cols-3 gap-4">
        {[
          { label: 'Pets Indexed', value: '—', sub: 'Connect backend to populate' },
          { label: 'Simulations (today)', value: '—', sub: 'Waiting for engine' },
          { label: 'Genetic Runs', value: '—', sub: 'Wire optimizer endpoint' },
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
