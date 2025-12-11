import type { PetFamily } from '../../api/client';

const familyColor: Record<PetFamily, string> = {
  Beast: 'bg-pet-beast/30 text-pet-beast border-pet-beast/70',
  Mechanical: 'bg-pet-mechanical/25 text-pet-mechanical border-pet-mechanical/70',
  Dragonkin: 'bg-pet-dragonkin/25 text-pet-dragonkin border-pet-dragonkin/70',
  Magic: 'bg-pet-magic/25 text-pet-magic border-pet-magic/70',
  Undead: 'bg-pet-undead/25 text-pet-undead border-pet-undead/70',
  Aquatic: 'bg-pet-aquatic/25 text-pet-aquatic border-pet-aquatic/70',
  Flying: 'bg-pet-flying/25 text-pet-flying border-pet-flying/70',
  Humanoid: 'bg-pet-humanoid/25 text-pet-humanoid border-pet-humanoid/70',
  Critter: 'bg-pet-critter/25 text-pet-critter border-pet-critter/70',
};

export const PetFamilyBadge: React.FC<{ family: PetFamily }> = ({ family }) => (
  <span
    className={`inline-flex items-center gap-1 rounded-full border px-2 py-0.5 text-[11px] uppercase tracking-wide ${familyColor[family]}`}
  >
    <span className="text-xs">●</span>
    {family}
  </span>
);
