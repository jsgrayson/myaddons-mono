import React, { useState, useEffect } from 'react';
import { Shield } from './Icons';

export default function CodexView() {
    const [raidData, setRaidData] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch('/api/dashboard/summary')
            .then(res => res.json())
            .then(data => {
                setRaidData(data.modules?.codex || {});
                setLoading(false);
            })
            .catch(err => {
                console.error('Failed to fetch raid data:', err);
                setLoading(false);
            });
    }, []);

    if (loading) {
        return (
            <div className="flex items-center justify-center h-full">
                <div className="text-center">
                    <Shield className="w-16 h-16 text-rarity-death animate-pulse mx-auto mb-4" />
                    <p className="text-slate-400 font-warcraft">Loading Raid Data...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            <div className="wow-panel p-6 rounded border border-rarity-death/30 shadow-glow-purple bg-noise">
                <h1 className="text-3xl font-bold text-white font-warcraft tracking-widest mb-2 text-shadow-glow">
                    THE CODEX
                </h1>
                <p className="text-slate-400">Raid Progress & Boss Encounters</p>
            </div>

            <div className="wow-card p-6 rounded border border-white/10 bg-noise">
                <h2 className="text-2xl font-warcraft text-white mb-4">{raidData.current_raid || 'No Active Raid'}</h2>
                <div className="space-y-4">
                    <div>
                        <span className="text-slate-400">Bosses Defeated:</span>
                        <span className="text-rarity-epic font-bold ml-3">{raidData.bosses || 0}</span>
                    </div>
                    <div className="text-sm text-slate-500 italic">
                        Quest tracking and boss encounter data will appear here as you progress through content.
                    </div>
                </div>
            </div>
        </div>
    );
}
