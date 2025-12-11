
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
  | 'Elemental'; // Added Elemental

export interface PetSummary {
  id: string | number;
  name: string;
  family: PetFamily;
  level: number;
  rarity: 'Common' | 'Uncommon' | 'Rare' | 'Epic' | 'Poster' | 'Poor';
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
  combatStats?: {
    total_battles: number;
    wins: number;
    win_rate: number;
  };
}

// Data Mapping Helpers
function mapFamily(f: string | number): PetFamily {
  if (typeof f === 'number') {
    // Map ID to string if known, otherwise default
    const map: Record<number, PetFamily> = {
      1: 'Humanoid', 2: 'Dragonkin', 3: 'Flying', 4: 'Undead', 5: 'Critter',
      6: 'Magic', 7: 'Elemental', 8: 'Beast', 9: 'Aquatic', 10: 'Mechanical'
    };
    return map[f] || 'Beast';
  }
  // Capitalize first letter
  const s = String(f).toLowerCase();
  return (s.charAt(0).toUpperCase() + s.slice(1)) as PetFamily;
}

function mapRarity(r: string | number): any {
  if (typeof r === 'number') {
    const map: Record<number, string> = {
      0: 'Poor', 1: 'Common', 2: 'Uncommon', 3: 'Rare', 4: 'Epic'
    };
    return map[r] || 'Common';
  }
  const s = String(r).toLowerCase();
  return (s.charAt(0).toUpperCase() + s.slice(1));
}

export async function apiListPets(): Promise<PetSummary[]> {
  const res = await fetch('/api/collection/all');
  if (!res.ok) throw new Error('Failed to fetch pets');
  const data = await res.json();

  // Determine if data is wrapped or direct list
  const list = Array.isArray(data) ? data : (data.pets || []);

  return list.map((p: any) => ({
    id: p.species_id || p.id,
    name: p.name || p.petName || 'Unknown',
    family: mapFamily(p.family || p.family_id),
    level: p.level || 1,
    rarity: mapRarity(p.quality || p.rarity || 'Rare'),
    power: p.power || 0,
    speed: p.speed || 0,
    health: p.health || p.max_hp || 0,
    portraitUrl: p.icon || undefined,
    icon: p.icon
  }));
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
  const res = await fetch('/api/simulate/wizard', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error('Simulation failed');
  return res.json();
}

export async function apiGetServerStatus(): Promise<ServerStatus> {
  try {
    const res = await fetch('/api/status');
    if (!res.ok) throw new Error('Status check failed');
    const data = await res.json();
    return {
      status: data.status === 'RUNNING' || data.status === 'IDLE' ? 'online' : 'degraded',
      uptimeSeconds: 0, // Not provided by backend yet
      queueDepth: 0,
      workers: 1,
      stats: data.stats,
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
  const res = await fetch('/api/encounters');
  if (!res.ok) throw new Error('Failed to fetch encounters');
  return res.json();
}

export async function apiListLogs(): Promise<string[]> {
  const res = await fetch('/api/combat-logs/latest');
  // Return format adjustment based on actual backend
  // Backend returns single object or list?
  // client.ts expected string[], backend /latest returns object
  // We should fallback to /api/combat-logs if we want a list
  if (!res.ok) return [];

  // Check main list endpoint
  try {
    const listRes = await fetch('/api/combat-logs');
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
