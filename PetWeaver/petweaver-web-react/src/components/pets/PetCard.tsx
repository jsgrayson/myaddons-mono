import { Link } from 'react-router-dom';
import type { PetSummary } from '../../api/client';
import { PetFamilyBadge } from './PetFamilyBadge';
import { rarityIcon, rarityColor, rarityGlow } from '../../constants/rarity';

function familyKey(family: PetSummary['family']): string {
  return family.toLowerCase();
}

export const PetCard: React.FC<{ pet: PetSummary }> = ({ pet }) => {
  const fam = familyKey(pet.family);
  // Unify elemental with magic if missing, or just use naming convention
  const assetName = fam === 'elemental' ? 'magic' : fam;
  const autoPortrait = `/assets/pets/${assetName}.png`;
  // Force local assets as external URLs are unreliable/broken
  const portraitSrc = autoPortrait;

  const rarityClass = rarityColor[pet.rarity];
  const auraClass = rarityGlow[pet.rarity];

  return (
    <Link to={`/pets/${pet.id}`}>
      <div className="group relative overflow-hidden rounded-xl bg-bg-panelSoft/90 border border-slate-800/80 shadow-xl shadow-black/50 hover:shadow-ember transition transform hover:-translate-y-0.5">
        <div className="pointer-events-none absolute inset-0 bg-gradient-to-t from-ember-deep/35 via-transparent to-transparent opacity-70 group-hover:opacity-100 transition" />
        <div className="relative z-10 p-4 flex gap-4">
          <div className="relative flex-shrink-0">
            <div className={`h-20 w-20 rounded-full bg-gradient-to-tr from-ember-deep via-ember-light to-arcane-mid flex items-center justify-center overflow-hidden ${auraClass}`}>
              <img
                src={portraitSrc}
                alt={pet.name}
                className="h-full w-full object-cover"
              />
            </div>
            <div className="pointer-events-none absolute -inset-1 rounded-full border border-amber-400/50 opacity-0 group-hover:opacity-100 transition" />
          </div>

          <div className="flex flex-col gap-1 min-w-0">
            <div className="flex items-center gap-2">
              <h3 className="text-sm font-semibold text-amber-50 truncate">
                {pet.name}
              </h3>
              <span className={`flex items-center gap-1 text-[11px] ${rarityClass}`}>
                <img
                  src={rarityIcon[pet.rarity]}
                  alt={pet.rarity}
                  className="h-3 w-3"
                />
                {pet.rarity}
              </span>
            </div>
            <PetFamilyBadge family={pet.family} />
            <div className="mt-1 flex gap-4 text-[11px] text-slate-300">
              <span>
                ❤️ <span className="text-amber-200">{pet.health}</span>
              </span>
              <span>
                💥 <span className="text-amber-200">{pet.power}</span>
              </span>
              <span>
                ⚡ <span className="text-amber-200">{pet.speed}</span>
              </span>
            </div>
          </div>
        </div>
      </div>
    </Link>
  );
};
