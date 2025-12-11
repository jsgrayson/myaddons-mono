import React from 'react';
import { Activity } from '../Icons';

const mockActivities = [
    { time: 'Now', text: 'Scanning local auction data...' },
    { time: '2m', text: 'Sniper Alert: Draconium Ore x400 @ 12g (MV: 45g)' },
    { time: '5m', text: 'Crafting queue completed: Enchant Weapon - Sophic' },
    { time: '12m', text: 'Navigator: New rare spawn detected in Zaralek' },
];

export const ActivityFeedWidget = () => (
    <div className="rounded-2xl bg-black/40 backdrop-blur-xl border border-white/5 overflow-hidden h-full">
        <div className="px-6 py-4 border-b border-white/5 flex items-center justify-between">
            <div className="flex items-center space-x-3">
                <Activity className="w-4 h-4 text-cyan-400" />
                <span className="text-sm font-medium text-white uppercase tracking-widest">Live Feed</span>
            </div>
            <span className="text-xs bg-green-500/10 text-green-400 px-3 py-1 rounded-full border border-green-500/20 animate-pulse">
                STREAMING
            </span>
        </div>
        <div className="p-4 space-y-2 max-h-48 overflow-y-auto">
            {mockActivities.map((act, i) => (
                <div key={i} className="flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-white/5 transition-colors group">
                    <div className="w-1.5 h-1.5 rounded-full bg-cyan-400 shadow-[0_0_6px_rgba(0,210,255,0.5)]" />
                    <span className="text-xs text-cyan-400 font-mono w-12">[{act.time}]</span>
                    <span className="text-sm text-slate-300 group-hover:text-white transition-colors flex-1">{act.text}</span>
                </div>
            ))}
        </div>
    </div>
);
