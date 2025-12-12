// Types + stubbed API calls for SkillWeaver.
// Later you (or the addon/server) will replace the internals with real HTTP / sync logic.

const API_BASE = "/api";

export type WowClass =
  | "WARRIOR"
  | "PALADIN"
  | "HUNTER"
  | "ROGUE"
  | "PRIEST"
  | "DEATHKNIGHT"
  | "SHAMAN"
  | "MAGE"
  | "WARLOCK"
  | "MONK"
  | "DRUID"
  | "DEMONHUNTER"
  | "EVOKER";

export interface CharacterProfile {
  name: string;
  realm: string;
  classId: WowClass;
  specName: string;
  ilvl: number | null;
  lastSync: string | null;
}

export interface BuildSummary {
  id: string;
  name: string;
  specName: string;
  archetype: "ST" | "AOE" | "MYTHIC_PLUS" | "RAID" | "PVP";
  talentString: string;
  lastUpdated: string;
  isRecommended: boolean;
}

export interface MacroSummary {
  id: string;
  name: string;
  scope: "ST" | "AOE" | "UTILITY" | "DEFENSIVE";
  boundKey?: string;
  outOfDate?: boolean;
}

export interface EncounterSummary {
  id: string;
  name: string;
  context: "DUNGEON" | "RAID" | "WORLD";
  profileName: string;
  lastSeen?: string;
}

export interface RotationHealth {
  score: number; // 0–100
  missedProcs: number;
  cdDesyncs: number;
  comment: string;
}

// --------- Stubbed API calls ---------

export async function apiGetCurrentProfile(): Promise<CharacterProfile | null> {
  // TODO: replace with real backend call / addon sync
  return {
    name: "Examplemage",
    realm: "Illidan",
    classId: "MAGE",
    specName: "Frost",
    ilvl: 487,
    lastSync: "2025-12-10T05:00:00Z",
  };
}

export async function apiListBuilds(): Promise<BuildSummary[]> {
  return [
    {
      id: "frost-st-raid",
      name: "Frost ST Raid",
      specName: "Frost",
      archetype: "RAID",
      talentString: "BwQA....",
      lastUpdated: "2025-12-09T18:00:00Z",
      isRecommended: true,
    },
    {
      id: "frost-mplus",
      name: "Frost Mythic+",
      specName: "Frost",
      archetype: "MYTHIC_PLUS",
      talentString: "BwQA....",
      lastUpdated: "2025-12-08T21:30:00Z",
      isRecommended: false,
    },
  ];
}

export async function apiListMacros(): Promise<MacroSummary[]> {
  return [
    {
      id: "frost-st-main",
      name: "Frost ST Main",
      scope: "ST",
      boundKey: "1",
      outOfDate: false,
    },
    {
      id: "frost-aoe-main",
      name: "Frost AoE Main",
      scope: "AOE",
      boundKey: "2",
      outOfDate: true,
    },
  ];
}

export async function apiGetRotationHealth(): Promise<RotationHealth> {
  return {
    score: 82,
    missedProcs: 3,
    cdDesyncs: 1,
    comment: "Overall solid. Tighten up Brain Freeze usage and IV windows.",
  };
}

export async function apiListEncounters(): Promise<EncounterSummary[]> {
  return [
    {
      id: "midnight-raid-boss-1",
      name: "Midnight Boss 1",
      context: "RAID",
      profileName: "Frost ST Raid",
      lastSeen: "2025-12-09T23:12:00Z",
    },
    {
      id: "mplus-21-key",
      name: "+21 The War Within Dungeon",
      context: "DUNGEON",
      profileName: "Frost Mythic+",
      lastSeen: "2025-12-08T19:45:00Z",
    },
// Health check
export async function apiGetServerStatus(): Promise<{ status: string }> {
    const res = await fetch(`${API_BASE}/health`);
    if (!res.ok) throw new Error("Health check failed");
    return res.json();
  }
