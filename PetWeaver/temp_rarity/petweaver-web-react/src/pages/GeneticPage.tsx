import { Card } from '../components/ui/Card';

export const GeneticPage: React.FC = () => {
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
        <h1 className="text-xl font-semibold text-amber-50">Genetic Optimizer</h1>
        <Card className="bg-bg-panel/85">
          <p className="text-sm text-slate-200 mb-2">
            This page is ready for your genetic algorithm integration.
          </p>
          <ul className="text-xs text-slate-300 space-y-1 list-disc ml-5">
            <li>
              Implement an API in <code className="font-mono">api/client.ts</code> to start an
              optimization run.
            </li>
            <li>Return progress, fitness scores and best teams.</li>
            <li>Map the results to cards, charts or tables here.</li>
          </ul>
        </Card>
      </div>
    </section>
  );
};
