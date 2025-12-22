import React, { useState } from 'react';

// Placeholder for the timeline asset
const ASSETS = {
    timelineRuler: "url('/assets/timeline-ruler-technical.png')",
};

export const SequenceForge: React.FC = () => {
    const [latencyOffset, setLatencyOffset] = useState(25); // ms
    const [sequenceData] = useState([
        { id: 1, action: 'OPENER_MACRO', duration: 1500, type: 'GCD' },
        { id: 2, action: 'TRINKET_1', duration: 0, type: 'OFF_GCD' },
        { id: 3, action: 'BIG_DAM_SPELL', duration: 1200, type: 'CAST' },
        { id: 4, action: 'LATE_KICK_WINDOW', duration: 300, type: 'WINDOW' },
    ]);

    return (
        <div className="min-h-screen bg-[#020617] text-slate-200 font-mono p-8 selection:bg-amber-500/30">

            {/* Header */}
            <header className="flex justify-between items-end border-b border-slate-800 pb-4 mb-8">
                <div>
                    <h1 className="text-3xl font-bold tracking-tighter text-white">
                        SEQUENCE_FORGE <span className="text-amber-500 text-sm align-top">SERIAL_BRIDGE</span>
                    </h1>
                    <p className="text-[10px] text-slate-500 uppercase tracking-widest mt-1">
                        HARDWARE_TARGET: <span className="text-cyan-400">PRO_MICRO_V3</span> // BAUD: 9600
                    </p>
                </div>

                <div className="flex gap-2">
                    <button className="px-6 py-2 border border-cyan-500 bg-cyan-950/30 text-cyan-400 text-xs font-bold hover:bg-cyan-500 hover:text-black transition-colors uppercase">
                        COMPILE_TO_HEX
                    </button>
                    <button className="px-6 py-2 border border-slate-700 bg-slate-900 text-slate-400 text-xs font-bold hover:border-amber-500 hover:text-amber-500 transition-colors uppercase">
                        TEST_PULSE
                    </button>
                </div>
            </header>

            {/* Main Workspace */}
            <main className="grid grid-cols-1 lg:grid-cols-4 gap-8 h-[calc(100vh-200px)]">

                {/* Left: Logic Parameters */}
                <div className="col-span-1 border-r border-slate-800 pr-6 space-y-8">

                    {/* Latency Tuner */}
                    <div className="bg-slate-900/40 p-4 border border-slate-800">
                        <label className="flex justify-between text-[10px] uppercase text-slate-400 mb-4">
                            Hardware_Latency_Offset
                            <span className="text-amber-500 font-bold">{latencyOffset}ms</span>
                        </label>
                        <input
                            type="range"
                            min="0" max="100"
                            value={latencyOffset}
                            onChange={(e) => setLatencyOffset(Number(e.target.value))}
                            className="w-full h-1 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-amber-500"
                        />
                        <div className="flex justify-between text-[9px] text-slate-600 mt-2 font-mono">
                            <span>0ms (VIRTUAL)</span>
                            <span>100ms (LAG)</span>
                        </div>
                    </div>

                    {/* Logic Override List */}
                    <div>
                        <h3 className="text-[10px] uppercase text-cyan-500 mb-4 border-b border-cyan-900/50 pb-2">
                            Logic_Overrides (LO)
                        </h3>
                        <div className="space-y-2">
                            {['PRIORITIZE_INTERRUPT', 'HOLD_BURST_FOR_BOSS', 'SYNC_TRINKETS'].map((opt) => (
                                <div key={opt} className="flex items-center gap-3 p-2 border border-white/5 hover:bg-white/5 cursor-pointer">
                                    <div className="w-3 h-3 border border-slate-500 rounded-sm" />
                                    <span className="text-[10px] text-slate-300">{opt}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

                {/* Center: The Timeline Editor */}
                <div className="col-span-3 flex flex-col relative bg-black/50 border border-slate-800">

                    {/* Timeline Header (Ruler) */}
                    <div
                        className="h-8 border-b border-slate-700 w-full opacity-50"
                        style={{ backgroundImage: ASSETS.timelineRuler, backgroundRepeat: 'repeat-x' }}
                    />

                    {/* The Tracks */}
                    <div className="flex-1 p-4 space-y-4 overflow-y-auto">

                        {/* Track 1: Global Cooldowns */}
                        <div className="relative h-16 bg-slate-900/30 border border-dashed border-slate-800 flex items-center px-2">
                            <span className="absolute left-2 top-1 text-[8px] text-slate-600">GCD_TRACK</span>

                            {/* Render Blocks */}
                            {sequenceData.filter(d => d.type === 'GCD').map((block, idx) => (
                                <div
                                    key={block.id}
                                    className="h-10 bg-cyan-900/40 border border-cyan-500/50 flex items-center justify-center text-[10px] text-cyan-200 mx-1"
                                    style={{ width: `${block.duration / 10}px` }}
                                >
                                    {block.action}
                                </div>
                            ))}
                        </div>

                        {/* Track 2: Off-GCD / Hardware Pulses */}
                        <div className="relative h-16 bg-slate-900/30 border border-dashed border-slate-800 flex items-center px-2">
                            <span className="absolute left-2 top-1 text-[8px] text-slate-600">HARDWARE_PULSE_TRACK</span>
                            {sequenceData.filter(d => d.type === 'OFF_GCD').map((block, idx) => (
                                <div
                                    key={block.id}
                                    className="h-8 w-8 rounded-full bg-amber-900/40 border border-amber-500 flex items-center justify-center text-[8px] text-amber-500 mx-8"
                                >
                                    TRIG
                                </div>
                            ))}
                        </div>

                    </div>

                    {/* Pulse Monitor (Bottom Overlay) */}
                    <div className="h-32 border-t border-slate-700 bg-black/80 relative overflow-hidden">
                        <div className="absolute top-2 left-2 text-[10px] text-cyan-500">SERIAL_OUT_PREVIEW</div>
                        {/* Abstract representation of the waveform */}
                        <div className="flex items-end h-full gap-1 px-4 pb-0 opacity-60">
                            {Array.from({ length: 100 }).map((_, i) => (
                                <div
                                    key={i}
                                    className="w-1 bg-cyan-500"
                                    style={{ height: `${Math.random() * 80 + 10}%`, opacity: Math.random() }}
                                />
                            ))}
                        </div>
                    </div>

                </div>

            </main>
        </div>
    );
};
