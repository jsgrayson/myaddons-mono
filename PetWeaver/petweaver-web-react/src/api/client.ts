
export type PetFamily =
  | 'Beast'
  | 'Mechanical'
  | 'Dragonkin'
  | 'Magic'
  | 'Undead'
  | 'Aquatic'
  | 'Flying'
  | 'Humanoid'
  | 'Critter'
  | 'Elemental';

export interface PetSummary {
  /**
   * Stable per-instance unique identifier.
   * Maps directly to pets.pet_id (DB primary key).
   * MUST be used for React list keys.
   */
  instanceId: string;

  /**
   * Species / classification identifier.
   * NOT unique per owned pet.
   */
  id: string | number;

  // Optional raw passthrough fields
  pet_id?: number;
  species_id?: number;

  name: string;
  family: PetFamily;
  level: number;
  rarity: 'Common' | 'Uncommon' | 'Rare' | 'Epic';
  power: number;
  speed: number;
  health: number;
  portraitUrl?: string;
  icon?: string;
}

export interface PetDetails extends PetSummary {
  flavorText?: string;
  abilities?: { id: string | number; name: string; cooldown?: number; icon?: string; description?: string }[];
}

export interface SimulationResult {
  winner: string;
  turns: number;
  log: string[];
  message: string;
}

export interface ServerStatus {
  status: 'online' | 'degraded' | 'offline';
  uptimeSeconds: number;
  queueDepth: number;
  workers: number;
  stats?: any;
  dbStats?: {
    pets: number;
    unique: number;
    max_level: number;
    rare_or_better: number;
    avg_level: number;
  };
  combatStats?: {
    total_battles: number;
    wins: number;
    win_rate: number;
  };
}

// Data Mapping Helpers
const API_BASE = "";

function mapFamily(f: string | number): PetFamily {
  if (typeof f === 'number') {
    // Map ID to string if known, otherwise default
    const map: Record<number, PetFamily> = {
      1: 'Humanoid', 2: 'Dragonkin', 3: 'Flying', 4: 'Undead', 5: 'Critter',
      6: 'Magic', 7: 'Elemental', 8: 'Beast', 9: 'Aquatic', 10: 'Mechanical'
    };
    return map[f] || 'Beast';
  }
  // Capitalize first letter logic slightly robust against bad input
  if (!f) return 'Beast';
  const s = String(f).toLowerCase();
  return (s.charAt(0).toUpperCase() + s.slice(1)) as PetFamily;
}

function mapRarity(r: string | number): PetSummary['rarity'] {
  // Backend quality: 0=Poor, 1=Common, 2=Uncommon, 3=Rare, 4=Epic
  // Frontend Rarity: Common, Uncommon, Rare, Epic
  // We map Poor (0) -> Common to avoid missing assets

  if (typeof r === 'number') {
    const map: Record<number, PetSummary['rarity']> = {
      0: 'Common', 1: 'Common', 2: 'Uncommon', 3: 'Rare', 4: 'Epic'
    };
    return map[r] || 'Common';
  }

  const s = String(r).toLowerCase();
  const titleCase = s.charAt(0).toUpperCase() + s.slice(1);

  if (['Common', 'Uncommon', 'Rare', 'Epic'].includes(titleCase)) {
    return titleCase as PetSummary['rarity'];
  }
  return 'Common';
}

function assertUniqueInstanceIds(pets: Array<Pick<PetSummary, "instanceId">>) {
  if (!(import.meta as any).env?.DEV) return;

  const seen = new Set<string>();
  const duplicates: string[] = [];

  for (const p of pets) {
    if (seen.has(p.instanceId)) duplicates.push(p.instanceId);
    else seen.add(p.instanceId);
  }

  if (duplicates.length > 0) {
    console.error("[Petweaver] Duplicate instanceId(s) detected:", duplicates);
    // Don't throw, just warn, to prevent app crash if DB is weird
    console.warn(`[Petweaver] Duplicate instanceId(s): ${duplicates.slice(0, 10).join(", ")}`);
  }
}

export async function apiListPets(): Promise<PetSummary[]> {
  const res = await fetch(`${API_BASE}/api/collection/all`);
  if (!res.ok) throw new Error('Failed to fetch pets');
  const data = await res.json();

  // Determine if data is wrapped or direct list
  const list = Array.isArray(data) ? data : (data.pets || []);

  const mapped: PetSummary[] = list.map((p: any) => ({
    // TRUE per-instance identity (DB PK)
    instanceId: String(p.pet_id),

    // Species/classification id (duplicates allowed)
    id: p.species_id || p.id,

    // Optional passthrough
    pet_id: p.pet_id,
    species_id: p.species_id,

    name: p.name || p.petName || 'Unknown',
    family: mapFamily(p.family || p.family_id),
    level: p.level || 1,
    rarity: mapRarity(p.quality || p.rarity),
    power: p.power || 0,
    speed: p.speed || 0,
    health: p.health || p.max_hp || 0,
    portraitUrl: p.icon || undefined,
    icon: p.icon
  }));

  assertUniqueInstanceIds(mapped);
  return mapped;
}

export async function apiGetPet(id: string | number): Promise<PetDetails> {
  // Since we don't have a specific endpoint yet, we fetch all and find one
  // TODO: Add specific /api/pet/<id> endpoint for performance
  const pets = await apiListPets();
  const pet = pets.find((p) => String(p.id) === String(id));
  if (!pet) throw new Error(`Pet ${id} not found`);

  // Return structure with empty abilities for now if not present
  return {
    ...pet,
    abilities: [] // Pending backend support for detailed view
  };
}

export async function apiRunSimulation(payload: any): Promise<SimulationResult> {
  const res = await fetch(`${API_BASE}/api/simulate/wizard`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error('Simulation failed');
  return res.json();
}

export async function apiGetServerStatus(): Promise<ServerStatus> {
  try {
    const res = await fetch(`${API_BASE}/api/status`);
    if (!res.ok) throw new Error('Status check failed');
    const data = await res.json();
    return {
      status: data.status === 'RUNNING' || data.status === 'IDLE' ? 'online' : 'degraded',
      uptimeSeconds: 0, // Not provided by backend yet
      queueDepth: 0,
      workers: 1,
      stats: data.stats,
      dbStats: data.db_stats,
      combatStats: data.combat_stats
    };
  } catch (e) {
    return {
      status: 'offline',
      uptimeSeconds: 0,
      queueDepth: 0,
      workers: 0
    };
  }
}

export async function apiListEncounters(): Promise<any[]> {
  const res = await fetch(`${API_BASE}/api/encounters`);
  if (!res.ok) throw new Error('Failed to fetch encounters');
  return res.json();
}

export async function apiListLogs(): Promise<string[]> {
  const res = await fetch(`${API_BASE}/api/combat-logs/latest`);
  // Return format adjustment based on actual backend
  if (!res.ok) return [];

  // Check main list endpoint
  try {
    const listRes = await fetch(`${API_BASE}/api/combat-logs`);
    if (listRes.ok) {
      const list = await listRes.json();
      // Map to strings if they are objects
      return list.map((l: any) =>
        typeof l === 'string' ? l : `[${l.timestamp || '?'}] ${l.result || 'Result'} vs ${l.enemy || 'Unknown'}`
      );
    }
  } catch (e) { }

  return [];
}

export async function apiGetPetMedia(petId: number | string): Promise<{ url: string | null }> {
  try {
    const res = await fetch(`${API_BASE}/api/blizzard/pet/${petId}/media`);
    if (res.ok) {
      return res.json();
    }
  } catch (e) {
    console.error("Failed to fetch pet media", e);
  }
  return { url: null };
}

