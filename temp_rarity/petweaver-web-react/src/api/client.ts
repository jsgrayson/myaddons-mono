export type PetFamily =
  | 'Beast'
  | 'Mechanical'
  | 'Dragonkin'
  | 'Magic'
  | 'Undead'
  | 'Aquatic'
  | 'Flying'
  | 'Humanoid'
  | 'Critter';

export interface PetSummary {
  id: string | number;
  name: string;
  family: PetFamily;
  level: number;
  rarity: 'Common' | 'Uncommon' | 'Rare' | 'Epic';
  power: number;
  speed: number;
  health: number;
  portraitUrl?: string;
}

export interface PetDetails extends PetSummary {
  flavorText?: string;
  abilities?: { id: string | number; name: string; cooldown?: number }[];
}

export interface SimulationResult {
  log: string[];
}

export interface ServerStatus {
  status: 'online' | 'degraded' | 'offline';
  uptimeSeconds: number;
  queueDepth: number;
  workers: number;
}

function notImplemented(name: string): never {
  throw new Error(
    `${name} is not implemented yet. Replace this stub in src/api/client.ts with real API calls to your backend.`
  );
}

export async function apiListPets(): Promise<PetSummary[]> {
  notImplemented('apiListPets');
}

export async function apiGetPet(id: string | number): Promise<PetDetails> {
  notImplemented('apiGetPet');
}

export async function apiRunSimulation(payload: any): Promise<SimulationResult> {
  notImplemented('apiRunSimulation');
}

export async function apiGetServerStatus(): Promise<ServerStatus> {
  notImplemented('apiGetServerStatus');
}

export async function apiListEncounters(): Promise<any[]> {
  notImplemented('apiListEncounters');
}

export async function apiListLogs(): Promise<string[]> {
  notImplemented('apiListLogs');
}
