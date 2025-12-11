/**
 * Pet family asset resolver — single source of truth for portrait icons.
 * Normalizes backend-provided family strings into a known asset key and
 * warns when input is unrecognized.
 */
export const FAMILY_ALIASES: Record<string, string> = {
  beast: 'beast',
  beasts: 'beast',

  critter: 'critter',
  critters: 'critter',

  flying: 'flying',
  flyer: 'flying',
  fly: 'flying',

  aquatic: 'aquatic',
  water: 'aquatic',

  humanoid: 'humanoid',
  human: 'humanoid',

  undead: 'undead',
  ghost: 'undead',

  mechanical: 'mechanical',
  mech: 'mechanical',
  robot: 'mechanical',

  dragonkin: 'dragonkin',
  dragon: 'dragonkin',

  magic: 'magic',
  arcane: 'magic',
  spell: 'magic',

  elemental: 'elemental',
  element: 'elemental',
};

/**
 * Normalize backend family strings into one valid family key.
 */
export function resolvePetFamily(input: string | null | undefined): string {
  if (!input) return 'magic';

  const normalized = input.toLowerCase().trim().replace(/[^a-z]/g, '');

  if (FAMILY_ALIASES[normalized]) {
    return FAMILY_ALIASES[normalized];
  }

  // Substring match as a last resort
  const hit = Object.keys(FAMILY_ALIASES).find((key) =>
    normalized.includes(key)
  );
  if (hit) return FAMILY_ALIASES[hit];

  // Warn in dev so we can tighten aliases
  if (import.meta.env.DEV) {
    console.warn('[PetAssets] Unrecognized family string:', input);
  }
  return 'magic';
}

/**
 * Resolve portrait path for any pet.
 */
export function getPetPortraitPath(family: string): string {
  const fam = resolvePetFamily(family);
  return `/assets/pets/${fam}.png`;
}

// During development: verify that all expected assets exist
if (import.meta.env.DEV) {
  const expected = new Set(Object.values(FAMILY_ALIASES));
  expected.forEach((fam) => {
    const url = `/assets/pets/${fam}.png`;
    const img = new Image();
    img.src = url;
    img.onerror = () =>
      console.warn('[PetAssets] Missing asset:', url);
  });
}
