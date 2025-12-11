import { useParams, useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { PetFamilyBadge } from '../components/pets/PetFamilyBadge';
import type { PetDetails } from '../api/client';

export const PetDetailsPage: React.FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [pet, setPet] = useState<PetDetails | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    import('../api/client')
      .then((m) => m.apiGetPet(id as string))
      .then(setPet)
      .catch((err) => {
        console.error(err);
        setError(
          'apiGetPet is not implemented yet. Your AI coder should connect this to your backend in src/api/client.ts.'
        );
      });
  }, [id]);

  const familyKey = pet ? (pet.family as string).toLowerCase() : 'beast';
  const autoPortrait = `/assets/pets/${familyKey}_03.svg`;
  const portraitSrc = pet?.portraitUrl || autoPortrait;

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
        <div className="flex items-center gap-3">
          <Button variant="ghost" onClick={() => navigate(-1)}>
            ← Back
          </Button>
          <h1 className="text-xl font-semibold text-amber-50">
            {pet ? pet.name : `Pet #${id}`}
          </h1>
          {pet && <PetFamilyBadge family={pet.family} />}
        </div>

        <div className="grid md:grid-cols-[minmax(0,1.2fr)_minmax(0,1fr)] gap-4">
          <Card className="bg-bg-panel/85">
            <div className="flex gap-4">
              <div className="relative flex-shrink-0">
                <div className="h-32 w-32 rounded-full bg-gradient-to-tr from-ember-deep via-ember-light to-arcane-mid shadow-ember flex items-center justify-center overflow-hidden">
                  <img
                    src={portraitSrc}
                    alt={pet?.name ?? 'Pet portrait'}
                    className="h-full w-full object-cover"
                  />
                </div>
              </div>
              <div className="space-y-2 text-sm">
                {error && (
                  <div className="text-xs text-amber-200">{error}</div>
                )}
                {pet ? (
                  <>
                    <div className="text-slate-200">Level {pet.level}</div>
                    <div className="flex gap-4 text-xs text-slate-200">
                      <span>❤️ {pet.health}</span>
                      <span>💥 {pet.power}</span>
                      <span>⚡ {pet.speed}</span>
                    </div>
                    <p className="text-xs text-slate-300 max-w-md">
                      {pet.flavorText ??
                        'Flavor text will come from your backend once connected.'}
                    </p>
                  </>
                ) : !error ? (
                  <div className="text-xs text-slate-300">
                    Awaiting pet details from backend…
                  </div>
                ) : null}
              </div>
            </div>
          </Card>

          <Card className="bg-bg-panel/85">
            <div className="space-y-2 text-sm">
              <div className="text-xs text-slate-400 uppercase tracking-wide">
                Abilities
              </div>
              {pet && pet.abilities ? (
                <ul className="space-y-1">
                  {pet.abilities.map((a) => (
                    <li
                      key={a.id}
                      className="flex items-center gap-2 text-xs text-slate-100"
                    >
                      <span className="h-6 w-6 rounded-full bg-bg-panel flex items-center justify-center text-[13px]">
                        ✨
                      </span>
                      <span className="font-medium">{a.name}</span>
                      <span className="text-slate-400">• {a.cooldown || 0} CD</span>
                    </li>
                  ))}
                </ul>
              ) : (
                <div className="text-xs text-slate-400">
                  Ability data will appear once apiGetPet returns it from your engine.
                </div>
              )}
            </div>
          </Card>
        </div>
      </div>
    </section>
  );
};
