import { NavLink } from 'react-router-dom';

const navLinkBase =
  'px-3 py-2 text-xs md:text-sm font-medium transition-colors relative rounded-md';
const activeEmber =
  'text-ember-light bg-bg-panel/70';

const links = [
  { to: '/dashboard', label: 'Dashboard' },
  { to: '/pets', label: 'Pet Codex' },
  { to: '/simulator', label: 'Simulator' },
  { to: '/genetic', label: 'Optimizer' },
  { to: '/encounters', label: 'Encounters' },
  { to: '/server', label: 'Server' },
  { to: '/logs', label: 'Logs' },
  { to: '/settings', label: 'Settings' },
];

export const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <div className="min-h-screen flex flex-col">
      <header className="border-b border-slate-800 bg-bg-base/95 backdrop-blur relative overflow-hidden">
        <div
          className="pointer-events-none absolute inset-0 opacity-35"
          style={{
            backgroundImage: "url('/assets/backgrounds/ember_bg_01.svg')",
            backgroundSize: 'cover',
            backgroundPosition: 'top center',
          }}
        />
        <div className="mx-auto max-w-6xl px-4 py-3 flex flex-col gap-3 relative z-10">
          <div className="flex items-center justify-between gap-6">
            <div className="flex items-center gap-3">
              <div className="h-9 w-9 rounded-full bg-gradient-to-tr from-ember-deep via-ember-light to-arcane-mid shadow-ember flex items-center justify-center">
                <span className="text-xl">🐾</span>
              </div>
              <div>
                <div className="font-title tracking-[0.15em] text-[10px] text-ember-light uppercase">
                  PetWeaver
                </div>
                <div className="text-xs text-slate-200">
                  Arcane Pet Battle Lab
                </div>
              </div>
            </div>
          </div>

          <nav className="flex flex-wrap items-center gap-2 text-sm">
            {links.map((link) => (
              <NavLink
                key={link.to}
                to={link.to}
                className={({ isActive }) =>
                  [
                    navLinkBase,
                    isActive
                      ? activeEmber
                      : 'text-slate-200 hover:text-ember-light hover:bg-bg-panel/60',
                  ].join(' ')
                }
              >
                {link.label}
              </NavLink>
            ))}
          </nav>
        </div>
      </header>

      <div className="h-[3px] bg-gradient-to-r from-ember-deep via-ember-light to-arcane-mid shadow-emberSoft" />

      <main className="flex-1">
        <div className="mx-auto max-w-6xl px-4 py-8">{children}</div>
      </main>

      <footer className="border-t border-slate-800 bg-bg-base/95 text-xs text-slate-500">
        <div className="mx-auto max-w-6xl px-4 py-3 flex justify-between gap-4">
          <span>PetWeaver • Arcane Pet Battle Intelligence</span>
          <span className="text-slate-600">
            Backend: <span className="text-amber-300">Not connected</span>
          </span>
        </div>
      </footer>
    </div>
  );
};
