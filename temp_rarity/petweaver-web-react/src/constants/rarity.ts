export type Rarity = 'Common' | 'Uncommon' | 'Rare' | 'Epic';

export const rarityIcon: Record<Rarity, string> = {
  Common:   '/assets/rarity/common.svg',
  Uncommon: '/assets/rarity/uncommon.svg',
  Rare:     '/assets/rarity/rare.svg',
  Epic:     '/assets/rarity/epic.svg',
};

export const rarityColor: Record<Rarity, string> = {
  Common:   'text-slate-300',
  Uncommon: 'text-emerald-300',
  Rare:     'text-sky-300',
  Epic:     'text-fuchsia-300',
};

export const rarityGlow: Record<Rarity, string> = {
  Common:   'shadow-[0_0_12px_rgba(148,163,184,0.45)]',
  Uncommon: 'shadow-[0_0_14px_rgba(34,197,94,0.55)]',
  Rare:     'shadow-[0_0_14px_rgba(56,189,248,0.55)]',
  Epic:     'shadow-[0_0_16px_rgba(217,70,239,0.65)]',
};
