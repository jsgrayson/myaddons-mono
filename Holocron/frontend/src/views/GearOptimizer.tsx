import React, { useState } from 'react';
import { StatTopology } from './components/StatTopology';
import { BestInBagsSolver } from './components/BestInBagsSolver';

// Placeholder styles for the generated assets
const ASSETS = {
    bgGrid: "url('/assets/bg-blueprint-grid.png')",
    gearFrame: "url('/assets/cad-gear-frame.png')",
    radarChart: "url('/assets/stat-radar-vector.png')"
};

export const GearOptimizer: React.FC = () => {
    const [importString, setImportString] = useState('');
    const [simStatus, setSimStatus] = useState<'IDLE' | 'ANALYZING' | 'OPTIMIZED'>('IDLE');

    return (
        <div
            className="min-h-screen bg-[#020617] text-slate-200 font-mono p-8 relative overflow-hidden"
            style={{ backgroundImage: ASSETS.bgGrid, backgroundSize: '64px 64px' }}
        >
            {/* Header: Technical Readout */}
            <header className="flex justify-between items-end border-b border-cyan-500/30 pb-4 mb-10 backdrop-blur-sm">
                <div>
                    <h1 className="text-3xl font-bold tracking-tighter text-white">
                        GEAR_OPTIMIZER <span className="text-cyan-400 text-sm align-top">v1.2.7</span>
                    </h1>
                    <div className="flex gap-4 mt-2 text-[10px] uppercase tracking-widest text-slate-500">
                        <span>Target_Patch: <span className="text-cyan-400">MIDNIGHT</span></span>
                        <span>Sim_Engine: <span className="text-amber-500">LOCAL_HOST</span></span>
                    </div>
                </div>

                {/* Sim Status Indicator */}
                <div className="flex items-center gap-3 border border-slate-800 bg-black/40 px-4 py-2">
                    <div className={`w-2 h-2 rounded-full ${simStatus === 'ANALYZING' ? 'bg-amber-500 animate-pulse' : 'bg-cyan-500'}`} />
                    <span className="text-xs text-cyan-500 font-bold">
                        {simStatus === 'IDLE' ? 'SYSTEM_READY' : 'CALCULATING_WEIGHTS...'}
                    </span>
                </div>
            </header>

            <main className="grid grid-cols-12 gap-8">

                {/* Left Col: The Loadout Grid (Your "Paper Doll") */}
                <section className="col-span-5 relative">
                    <div className="absolute -top-6 left-0 text-[10px] text-cyan-600 uppercase tracking-widest">Current_Loadout_State</div>

                    {/* Visual Representation of Gear Slots */}
                    <div className="grid grid-cols-2 gap-4 max-w-md mx-auto relative z-10">
                        {['HEAD', 'NECK', 'SHOULDER', 'BACK', 'CHEST', 'WRIST'].map((slot) => (
                            <div
                                key={slot}
                                className="group relative h-20 bg-slate-900/50 border border-slate-800 hover:border-cyan-400 transition-colors flex items-center justify-between px-4"
                            >
                                {/* CAD Frame Overlay */}
                                <div className="absolute inset-0 opacity-20 pointer-events-none" style={{ backgroundImage: ASSETS.gearFrame, backgroundSize: 'cover' }} />

                                <span className="text-[10px] text-slate-500">{slot}</span>
                                <div className="h-12 w-12 border border-dashed border-slate-700 group-hover:border-cyan-500/50 flex items-center justify-center">
                                    <span className="text-[10px] text-slate-600">+</span>
                                </div>
                            </div>
                        ))}
                    </div>

                    {/* Sim Data Visualization Layer */}

                </section>

                {/* Center Col: The Stat Weight Radar */}
                <section className="col-span-4 flex flex-col items-center justify-center relative border-x border-slate-800/50 bg-black/20">
                    <div className="absolute top-0 w-full text-center py-2 border-b border-white/5">
                        <h3 className="text-xs text-amber-500 uppercase tracking-widest">Stat_Priority_Matrix</h3>
                    </div>

                    <div className="w-64 h-64 opacity-90 relative">
                        {/* The Radar Chart Asset */}
                        <img src="/assets/stat-radar-vector.png" alt="Stat Weights" className="w-full h-full object-contain drop-shadow-[0_0_8px_rgba(245,158,11,0.2)]" />

                        {/* Live Data Overlays */}
                        <div className="absolute top-0 left-1/2 -translate-x-1/2 text-[10px] text-cyan-400 font-mono">HASTE [32%]</div>
                        <div className="absolute bottom-10 right-0 text-[10px] text-slate-400 font-mono">MASTERY [12%]</div>
                        <div className="absolute bottom-10 left-0 text-[10px] text-amber-500 font-mono font-bold">VERS [8%] (LOW)</div>
                    </div>

                    {/* REPLACEMENT: Stat Topology Lab */}
                    <div className="w-full mt-4">
                        <StatTopology />
                    </div>

                    <div className="mt-8 w-full px-8">
                        <div className="flex justify-between text-[10px] text-slate-500 mb-1">
                            <span>SIM_ACCURACY</span>
                            <span>1,000,000 ITERATIONS</span>
                        </div>
                        <div className="h-1 w-full bg-slate-800 rounded-full overflow-hidden">
                            <div className="h-full bg-cyan-500 w-[85%]"></div>
                        </div>
                    </div>
                </section>

                {/* Right Col: Solver Matrix */}
                <section className="col-span-3">
                    <BestInBagsSolver />
                </section>
            </main>
        </div>
    );
};
