import React, { useState, useEffect } from 'react';
import { Sparkles, TrendingUp } from './Icons';

export default function NavigatorView() {
    const [activities, setActivities] = useState<any[]>([]);
    const [filteredActivities, setFilteredActivities] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [zoneFilter, setZoneFilter] = useState('All');
    const [sortBy, setSortBy] = useState<'points' | 'name'>('points');

    useEffect(() => {
        fetch('/api/navigator/activities')
            .then(res => res.json())
            .then(data => {
                const acts = data.activities || [];
                setActivities(acts);
                setFilteredActivities(acts);
                setLoading(false);
            })
            .catch(err => {
                console.error('Failed to fetch activities:', err);
                setLoading(false);
            });
    }, []);

    useEffect(() => {
        let result = [...activities];

        if (zoneFilter !== 'All') {
            result = result.filter(act => act.zone === zoneFilter);
        }

        result.sort((a, b) => {
            if (sortBy === 'points') return b.points - a.points;
            return a.name.localeCompare(b.name);
        });

        setFilteredActivities(result);
    }, [zoneFilter, sortBy, activities]);

    const zones = ['All', ...Array.from(new Set(activities.map(a => a.zone).filter(Boolean)))];

    if (loading) {
        return (
            <div className="flex items-center justify-center h-full">
                <div className="text-center">
                    <Sparkles className="w-16 h-16 text-rarity-epic animate-pulse mx-auto mb-4" />
                    <p className="text-slate-400 font-warcraft">Loading Activities...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            <div className="wow-panel p-6 rounded border border-rarity-epic/30 shadow-glow-purple bg-noise">
                <div className="flex justify-between items-start">
                    <div>
                        <h1 className="text-3xl font-bold text-white font-warcraft tracking-widest mb-2 text-shadow-glow">
                            NAVIGATOR
                        </h1>
                        <p className="text-slate-400">Priority Activities & Collections</p>
                    </div>
                    <div className="flex space-x-4">
                        <select
                            value={zoneFilter}
                            onChange={(e) => setZoneFilter(e.target.value)}
                            className="bg-black/40 border border-white/20 rounded px-3 py-2 text-white focus:border-rarity-epic outline-none"
                        >
                            {zones.map(z => <option key={z} value={z}>{z}</option>)}
                        </select>
                        <button
                            onClick={() => setSortBy(sortBy === 'points' ? 'name' : 'points')}
                            className="px-4 py-2 bg-rarity-epic/20 border border-rarity-epic text-white rounded hover:bg-rarity-epic/40 transition-all"
                        >
                            Sort by {sortBy === 'points' ? 'Name' : 'Points'}
                        </button>
                    </div>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {filteredActivities.map((activity, idx) => (
                    <div key={idx} className="wow-card p-4 rounded border border-white/10 hover:border-rarity-epic/50 transition-colors bg-noise group">
                        <div className="flex items-start justify-between mb-2">
                            <h3 className="text-lg font-warcraft text-white group-hover:text-rarity-epic transition-colors">{activity.name}</h3>
                            <span className="text-rarity-epic font-bold">{activity.points} pts</span>
                        </div>
                        <p className="text-sm text-slate-400 mb-2">{activity.zone}</p>
                        <div className="flex items-center justify-between text-xs">
                            <span className="text-slate-500">Type: {activity.type}</span>
                            {activity.owned ? (
                                <span className="text-rarity-uncommon">✓ Collected</span>
                            ) : (
                                <button className="px-2 py-1 bg-white/5 hover:bg-white/10 rounded text-slate-300 transition-colors">
                                    Track
                                </button>
                            )}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
