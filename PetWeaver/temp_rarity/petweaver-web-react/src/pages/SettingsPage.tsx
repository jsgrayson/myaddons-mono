import { Card } from '../components/ui/Card';

export const SettingsPage: React.FC = () => {
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
        <h1 className="text-xl font-semibold text-amber-50">Settings</h1>
        <Card className="bg-bg-panel/85">
          <p className="text-sm text-slate-200 mb-2">
            This is a placeholder for your PetWeaver control panel.
          </p>
          <p className="text-xs text-slate-300">
            Add toggles & inputs that map to your backend config: difficulty, battle
            rules, queue parameters, logging verbosity, etc.
          </p>
        </Card>
      </div>
    </section>
  );
};
