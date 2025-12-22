import React from 'react';

const MatrixArchitect: React.FC = () => {
    // Generate a 40x40 grid for visualization
    const gridNodes = Array.from({ length: 1600 }, (_, i) => {
        const row = Math.floor(i / 40);
        const col = i % 40;

        // Simulate some "Risk" data
        let riskClass = 'bg-slate-700'; // Default safe-ish
        if (Math.random() > 0.9) riskClass = 'bg-red-500 shadow-lg shadow-red-500/50'; // Crit
        else if (Math.random() > 0.8) riskClass = 'bg-amber-500'; // Warn
        else if (Math.random() > 0.7) riskClass = 'bg-emerald-500'; // Safe

        // Slot 40 (Wildcard) - strictly speaking index 39 or similar, 
        // but let's just make the last node the "Wildcard"
        if (i === 1599) riskClass = 'bg-violet-500 animate-pulse shadow-lg shadow-violet-500/50';

        return { id: i, riskClass };
    });

    return (
        <div className="flex gap-8 p-8 bg-[#020617] text-slate-200 font-sans border border-slate-800 rounded-xl h-full overflow-hidden">

            <div className="flex-1 flex flex-col gap-4">
                <header className="flex justify-between items-center border-b border-slate-800 pb-4">
                    <div>
                        <h2 className="text-xl font-bold tracking-widest text-cyan-400">SYSTEM STATUS: 40x40 MATRIX ACTIVE</h2>
                        <div className="text-xs text-violet-400 mt-1 font-mono animate-pulse">SLOT 40: DEVOURER PLACEHOLDER INITIALIZED</div>
                    </div>
                    <div className="px-3 py-1 bg-violet-900/30 border border-violet-500/30 rounded text-xs text-violet-200">
                        GHOST_SLOT_ACTIVE
                    </div>
                </header>

                <div className="flex-1 overflow-auto custom-scrollbar bg-white/5 p-4 rounded-lg border border-white/5 shadow-inner">
                    <div className="grid grid-cols-[repeat(40,minmax(8px,1fr))] gap-px aspect-square max-h-[80vh] mx-auto">
                        {gridNodes.map(node => (
                            <div
                                key={node.id}
                                className={`aspect-square rounded-[1px] transition-all duration-200 hover:scale-150 hover:z-10 ${node.riskClass}`}
                                title={`Node ${node.id}`}
                            />
                        ))}
                    </div>
                </div>
            </div>

            <div className="w-80 flex flex-col gap-6 border-l border-slate-800 pl-8">
                <div className="p-6 bg-slate-900/50 border border-violet-500/30 rounded-xl relative overflow-hidden group">
                    <div className="absolute inset-0 bg-violet-500/5 group-hover:bg-violet-500/10 transition-colors"></div>
                    <h3 className="text-2xl font-bold text-violet-200 mb-2 relative z-10">DEVOURER (257)</h3>
                    <p className="text-xs text-slate-400 mb-4 font-mono relative z-10">WILDCARD PROTOCOL</p>

                    <div className="space-y-4 relative z-10">
                        <div className="flex justify-between text-sm">
                            <span>THREAT LEVEL</span>
                            <span className="text-red-400 font-bold animate-pulse">EXTREME</span>
                        </div>
                        <div className="h-px bg-slate-700"></div>
                        <div className="text-xs font-mono text-cyan-500">
                            Calculating 40:40 parity... <span className="text-white">100%</span>
                        </div>
                    </div>
                </div>

                <div className="p-4 bg-slate-900/30 border border-slate-800 rounded-lg">
                    <h4 className="text-sm font-bold text-slate-300 mb-2">MATRIX LOG</h4>
                    <ul className="text-xs font-mono text-slate-500 space-y-1">
                        <li>[12:00:01] Initializing 40x40 Grid...</li>
                        <li>[12:00:02] Slot 40 (Devourer) Detected.</li>
                        <li>[12:00:02] Neural Handshake: <span className="text-emerald-500">STABLE</span></li>
                        <li>[12:00:03] Void Shift vectors calculated.</li>
                    </ul>
                </div>
            </div>

        </div>
    );
};

export default MatrixArchitect;
