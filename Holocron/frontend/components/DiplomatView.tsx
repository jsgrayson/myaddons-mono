import React, { useState, useEffect } from 'react';
import { Shield, Sparkles } from './Icons';

export default function DiplomatView() {
    const [opportunities, setOpportunities] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState<'all' | 'major' | 'minor'>('all');

    useEffect(() => {
        fetch('/api/diplomat/opportunities')
            .then(res => res.json())
            .then(data => {
                setOpportunities(data.opportunities || []);
                setLoading(false);
            })
            .catch(err => {
                console.error('Failed to fetch diplomat data:', err);
                setLoading(false);
            });
    }, []);

    const filteredOpps = opportunities.filter(opp => {
        if (filter === 'all') return true;
        return opp.type === filter;
    });

    if (loading) {
        return (
            <div className="flex items-center justify-center h-full">
                <div className="text-center">
                    <Shield className="w-16 h-16 text-rarity-rare animate-pulse mx-auto mb-4" />
                    <p className="text-slate-400 font-warcraft">Loading Diplomatic Relations...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            <div className="wow-panel p-6 rounded border border-rarity-rare/30 shadow-glow-blue bg-noise">
                <div className="flex justify-between items-center">
                    <div>
                        <h1 className="text-3xl font-bold text-white font-warcraft tracking-widest mb-2 text-shadow-glow">
                            THE DIPLOMAT
                        </h1>
                        <p className="text-slate-400">Reputation & Renown Tracking</p>
                    </div>
                    <div className="flex space-x-2">
                        <button
                            onClick={() => setFilter('all')}
                            className={`px-3 py-1 rounded border ${filter === 'all' ? 'bg-rarity-rare/20 border-rarity-rare text-white' : 'border-white/10 text-slate-400'}`}
                        >
                            All
                        </button>
                        <button
                            onClick={() => setFilter('major')}
                            className={`px-3 py-1 rounded border ${filter === 'major' ? 'bg-rarity-rare/20 border-rarity-rare text-white' : 'border-white/10 text-slate-400'}`}
                        >
                            Major Factions
                        </button>
                    </div>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {filteredOpps.map((opp, idx) => (
                    <div key={idx} className="wow-card p-4 rounded border border-white/10 hover:border-rarity-rare/50 transition-colors bg-noise">
                        <div className="flex justify-between items-start mb-2">
                            <h3 className="text-lg font-warcraft text-white">{opp.faction}</h3>
                            <span className="text-rarity-rare font-bold">{opp.standing}</span>
                        </div>
                        <div className="w-full h-2 bg-black/50 rounded-full overflow-hidden mb-2 border border-white/5">
                            <div
                                className="h-full bg-rarity-rare bar-gloss"
                                style={{ width: `${(opp.value / opp.max) * 100}%` }}
                            ></div>
                        </div>
                        <div className="flex justify-between text-xs text-slate-400">
                            <span>{opp.value} / {opp.max}</span>
                            <span>{Math.round((opp.value / opp.max) * 100)}%</span>
                        </div>
                        {opp.reward && (
                            <div className="mt-3 pt-2 border-t border-white/5 flex items-center text-sm">
                                <Sparkles className="w-4 h-4 text-azeroth-gold mr-2" />
                                <span className="text-slate-300">Next Reward: <span className="text-white">{opp.reward}</span></span>
                            </div>
                        )}
                    </div>
                ))}
                {filteredOpps.length === 0 && (
                    <div className="col-span-full text-center py-8 text-slate-500">
                        No reputation opportunities found matching filter.
                    </div>
                )}
            </div>
        </div>
    );
}
