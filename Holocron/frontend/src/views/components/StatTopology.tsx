import React from 'react';

export const StatTopology: React.FC = () => {
    // Mock Data: The Curve
    // Haste Value starts high (1.5), drops at Breakpoint 1 (30%), crashes at Hardware Cap (45%)
    const hasteCurve = [
        { rating: 0, weight: 1.5 },
        { rating: 2000, weight: 1.5 },
        { rating: 4000, weight: 1.4 },
        { rating: 5500, weight: 0.8 }, // Soft Cap
        { rating: 7000, weight: 0.2 }, // Hardware Cap
    ];

    return (
        <div className="w-full bg-black/60 border border-slate-800 p-6 relative overflow-hidden group">

            {/* Background Grid - "Topology" Vibe */}
            <div className="absolute inset-0 opacity-10"
                style={{ backgroundImage: 'linear-gradient(0deg, transparent 24%, #22d3ee 25%, #22d3ee 26%, transparent 27%, transparent 74%, #22d3ee 75%, #22d3ee 76%, transparent 77%, transparent), linear-gradient(90deg, transparent 24%, #22d3ee 25%, #22d3ee 26%, transparent 27%, transparent 74%, #22d3ee 75%, #22d3ee 76%, transparent 77%, transparent)', backgroundSize: '30px 30px' }}
            />

            <div className="relative z-10 flex justify-between items-start mb-6">
                <div>
                    <h3 className="text-sm text-cyan-500 font-bold uppercase tracking-widest">
                        Stat_Topology_Analysis <span className="text-white">v2.0</span>
                    </h3>
                    <p className="text-[10px] text-slate-500 font-mono mt-1">
                        HARDWARE_LATENCY_COMPENSATION: <span className="text-amber-500">ACTIVE (-24ms)</span>
                    </p>
                </div>

                {/* The Generated "Smart String" Status */}
                <div className="text-right">
                    <div className="text-[9px] text-slate-500 uppercase">NEXT_BREAKPOINT</div>
                    <div className="text-xl font-bold text-white font-mono">
                        +124 <span className="text-cyan-500 text-xs">HASTE</span>
                    </div>
                </div>
            </div>

            <div className="grid grid-cols-12 gap-8">

                {/* Left: The Curve Visualization */}
                <div className="col-span-8 h-48 bg-slate-900/40 border-l border-b border-slate-700 relative">
                    <div className="absolute top-2 left-2 text-[9px] text-slate-500">MARGINAL_UTILITY_CURVE</div>

                    {/* Rendering the Curve Line */}
                    <svg className="w-full h-full p-4 overflow-visible">
                        {/* The Curve */}
                        <path
                            d="M0,100 L100,100 L200,110 L300,160 L400,190"
                            fill="none"
                            stroke="#22d3ee"
                            strokeWidth="2"
                            className="drop-shadow-[0_0_10px_rgba(34,211,238,0.5)]"
                        />

                        {/* Current Player Position Marker */}
                        <line x1="240" y1="0" x2="240" y2="100%" stroke="#f59e0b" strokeWidth="1" strokeDasharray="4 4" />
                        <circle cx="240" cy="125" r="4" fill="#f59e0b" className="animate-pulse" />
                        <text x="250" y="125" fill="#f59e0b" fontSize="10" fontFamily="monospace">YOU_ARE_HERE</text>

                        {/* Hardware Cap Marker */}
                        <line x1="380" y1="0" x2="380" y2="100%" stroke="#ef4444" strokeWidth="1" />
                        <text x="385" y="20" fill="#ef4444" fontSize="10" fontFamily="monospace" style={{ writingMode: 'vertical-rl' }}>HW_CAP (USB_POLL)</text>
                    </svg>
                </div>

                {/* Right: The Breakpoint logic */}
                <div className="col-span-4 space-y-4">

                    {/* Analysis Card */}
                    <div className="bg-slate-900/80 p-3 border border-l-4 border-l-amber-500 border-t-0 border-r-0 border-b-0">
                        <h4 className="text-[10px] text-amber-500 font-bold uppercase mb-1">Recommendation</h4>
                        <p className="text-[10px] text-slate-300 leading-relaxed">
                            STOP stacking Haste. You are 124 rating away from the <span className="text-white font-bold">Hardware GCD Floor</span>. Any more Haste will be lost to USB latency.
                            <br /><br />
                            <span className="text-cyan-400">&gt;&gt; SWAP GEMS TO MASTERY.</span>
                        </p>
                    </div>

                    {/* Action Button */}
                    <button className="w-full py-3 bg-cyan-900/20 border border-cyan-500/50 hover:bg-cyan-500 hover:text-black hover:border-cyan-400 text-cyan-400 text-xs font-bold uppercase tracking-widest transition-all group-hover:shadow-[0_0_20px_rgba(34,211,238,0.15)]">
                        INJECT_OPTIMIZED_PROFILE
                    </button>
                    <div className="text-[8px] text-center text-slate-600 font-mono">
                        PUSHING TO: DESKTOP_MAIN, CLAW_01
                    </div>

                </div>
            </div>
        </div>
    );
};
