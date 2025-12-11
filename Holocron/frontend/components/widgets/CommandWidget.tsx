import React from 'react';
import { Globe } from '../Icons';

export const CommandWidget = () => (
    <div className="relative flex flex-col items-center justify-center py-12">
        {/* Orbital rings */}
        <div className="absolute w-[300px] h-[300px] rounded-full border border-cyan-500/10 animate-spin" style={{ animationDuration: '60s' }} />
        <div className="absolute w-[240px] h-[240px] rounded-full border border-dashed border-violet-500/20 animate-spin" style={{ animationDuration: '45s', animationDirection: 'reverse' }} />
        <div className="absolute w-[180px] h-[180px] rounded-full border border-cyan-500/20" />

        {/* Central glow */}
        <div className="absolute w-[200px] h-[200px] bg-cyan-500/10 rounded-full blur-3xl" />
        <div className="absolute w-[100px] h-[100px] bg-violet-500/10 rounded-full blur-2xl" />

        {/* Globe icon */}
        <div className="relative z-10 w-24 h-24 rounded-full bg-black/60 backdrop-blur-md border border-cyan-500/30 flex items-center justify-center shadow-[0_0_40px_rgba(0,210,255,0.2)]">
            <Globe className="w-12 h-12 text-cyan-400 animate-pulse" style={{ animationDuration: '3s' }} />
        </div>

        {/* Title */}
        <h1 className="mt-8 text-5xl font-bold tracking-[0.3em] text-white uppercase" style={{ textShadow: '0 0 30px rgba(0,210,255,0.5), 0 0 60px rgba(139,92,246,0.3)' }}>
            HOLOCRON
        </h1>
        <p className="mt-2 text-sm text-cyan-400/80 tracking-[0.5em] uppercase">Command Center</p>

        {/* Status bar */}
        <div className="mt-6 flex items-center space-x-4 text-xs text-slate-400">
            <span className="flex items-center"><span className="w-2 h-2 rounded-full bg-green-500 mr-2 shadow-[0_0_8px_rgba(34,197,94,0.5)]" />System Online</span>
            <span className="text-slate-600">|</span>
            <span>Latency: 14ms</span>
            <span className="text-slate-600">|</span>
            <span>Region: US-East</span>
        </div>
    </div>
);
