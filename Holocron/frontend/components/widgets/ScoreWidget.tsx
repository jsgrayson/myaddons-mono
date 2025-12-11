import React from 'react';
import { Sparkles } from '../Icons';

interface ArcaneCardProps {
    icon: React.ComponentType<any>;
    value: string;
    label: string;
    sublabel?: string;
    accentColor?: 'cyan' | 'violet' | 'gold';
}

const ArcaneCard = ({ icon: Icon, value, label, sublabel, accentColor = 'cyan' }: ArcaneCardProps) => {
    const colors = {
        cyan: { border: 'border-cyan-500/30', glow: 'shadow-[0_0_30px_rgba(0,210,255,0.15)]', text: 'text-cyan-400', bg: 'from-cyan-500/10' },
        violet: { border: 'border-violet-500/30', glow: 'shadow-[0_0_30px_rgba(139,92,246,0.15)]', text: 'text-violet-400', bg: 'from-violet-500/10' },
        gold: { border: 'border-amber-500/30', glow: 'shadow-[0_0_30px_rgba(245,158,11,0.15)]', text: 'text-amber-400', bg: 'from-amber-500/10' },
    };
    const c = colors[accentColor];

    return (
        <div className={`relative overflow-hidden rounded-2xl p-6 bg-gradient-to-br ${c.bg} to-transparent backdrop-blur-xl border ${c.border} ${c.glow} transition-all duration-500 hover:scale-[1.02] group`}>
            <div className="absolute inset-0 bg-gradient-to-t from-black/40 via-transparent to-white/5 pointer-events-none" />
            <div className="relative z-10">
                <div className="flex items-center justify-between mb-4">
                    <div className={`w-12 h-12 rounded-xl bg-black/40 border ${c.border} flex items-center justify-center ${c.glow}`}>
                        <Icon className={`w-6 h-6 ${c.text}`} />
                    </div>
                    <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse shadow-[0_0_10px_rgba(34,197,94,0.5)]" />
                </div>
                <h3 className="text-4xl font-bold text-white mb-1 tracking-tight" style={{ textShadow: '0 0 20px rgba(139,92,246,0.3)' }}>{value}</h3>
                <p className="text-sm text-slate-400 uppercase tracking-widest font-medium">{label}</p>
                {sublabel && <p className="text-xs text-slate-500 mt-1">{sublabel}</p>}
            </div>
        </div>
    );
};

export const ScoreWidget = () => (
    <ArcaneCard icon={Sparkles} value="98" label="Performance" sublabel="Top 1% Region" accentColor="violet" />
);
