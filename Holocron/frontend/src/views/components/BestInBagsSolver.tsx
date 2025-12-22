import React, { useState } from 'react';

type Spec = 'DEVASTATION' | 'PRESERVATION' | 'AUGMENTATION';

export const BestInBagsSolver: React.FC = () => {
    const [activeSpec, setActiveSpec] = useState<Spec>('DEVASTATION');
    const [solving, setSolving] = useState(false);
    const [progress, setProgress] = useState(0);

    // The "AMR Killer" Constraints
    const [constraints, setConstraints] = useState({
        allowGems: true,
        allowEnchants: true,
        forceTierSet: true, // 4-piece check
        optimizeTrinkets: true,
    });

    // Mock Result Data
    const solution = {
        dpsGain: activeSpec === 'AUGMENTATION' ? '+4,102 (Support)' : '+1,420 (3.2%)',
        changes: [
            { slot: 'NECK', action: 'SWAP', from: 'Lariat of Bling', to: 'Torc of Twilight', reason: 'Hit Haste Breakpoint' },
            { slot: 'RING_1', action: 'ENCHANT', from: 'Haste', to: 'Mastery', reason: 'Avoid DR Cap' },
        ]
    };

    const handleSolve = () => {
        setSolving(true);
        let p = 0;
        const interval = setInterval(() => {
            p += 2; // Slower progress to look like "Thinking"
            setProgress(p);
            if (p >= 100) {
                clearInterval(interval);
                setSolving(false);
            }
        }, 50);
    };

    const toggleConstraint = (key: keyof typeof constraints) => {
        setConstraints(prev => ({ ...prev, [key]: !prev[key] }));
    };

    return (
        <div className="w-full bg-[#020617] border border-slate-800 flex flex-col relative group overflow-hidden">

            {/* Background Tech Mesh */}
            <div className="absolute inset-0 opacity-5 pointer-events-none"
                style={{ backgroundImage: 'radial-gradient(circle, #22d3ee 1px, transparent 1px)', backgroundSize: '24px 24px' }}
            />

            {/* 1. TOP BAR: SPEC SELECTOR */}
            <div className="flex border-b border-slate-800">
                {['DEVASTATION', 'PRESERVATION', 'AUGMENTATION'].map((spec) => (
                    <button
                        key={spec}
                        onClick={() => setActiveSpec(spec as Spec)}
                        className={`flex-1 py-3 text-[10px] font-bold uppercase tracking-widest transition-all ${activeSpec === spec
                                ? 'bg-cyan-900/20 text-cyan-400 border-b-2 border-cyan-500'
                                : 'bg-black text-slate-600 hover:text-slate-400 border-b-2 border-transparent'
                            }`}
                    >
                        {spec}
                    </button>
                ))}
            </div>

            <div className="p-6 flex flex-col gap-6 relative z-10">

                {/* Header */}
                <div className="flex justify-between items-start">
                    <div>
                        <h2 className="text-xl font-bold text-white tracking-tighter">
                            COMBINATORIAL_SOLVER <span className="text-slate-600">//</span> {activeSpec}
                        </h2>
                        <p className="text-[10px] text-slate-500 uppercase tracking-widest mt-1">
                            ENGINE: <span className="text-amber-500">SIMC_NATIVE_V2</span> // PERMUTATIONS: ~45,000
                        </p>
                    </div>
                </div>

                {/* 2. THE CONSTRAINTS MATRIX (AMR Features) */}
                <div className="grid grid-cols-2 gap-4 bg-slate-900/30 border border-slate-800 p-4">
                    <div className="col-span-2 text-[9px] text-slate-500 uppercase border-b border-white/5 pb-2 mb-2">
                        Solver_Constraints (Exclusion_Logic)
                    </div>

                    {/* Constraint Toggles */}
                    <div
                        onClick={() => toggleConstraint('allowGems')}
                        className={`cursor-pointer flex items-center justify-between p-2 border ${constraints.allowGems ? 'border-green-500/30 bg-green-900/10' : 'border-red-900/30 bg-red-900/5'}`}
                    >
                        <span className={`text-[10px] ${constraints.allowGems ? 'text-green-400' : 'text-slate-500 line-through'}`}>INCLUDE_GEMS</span>
                        <div className={`w-2 h-2 rounded-sm ${constraints.allowGems ? 'bg-green-500' : 'bg-slate-700'}`} />
                    </div>

                    <div
                        onClick={() => toggleConstraint('allowEnchants')}
                        className={`cursor-pointer flex items-center justify-between p-2 border ${constraints.allowEnchants ? 'border-green-500/30 bg-green-900/10' : 'border-red-900/30 bg-red-900/5'}`}
                    >
                        <span className={`text-[10px] ${constraints.allowEnchants ? 'text-green-400' : 'text-slate-500 line-through'}`}>INCLUDE_ENCHANTS</span>
                        <div className={`w-2 h-2 rounded-sm ${constraints.allowEnchants ? 'bg-green-500' : 'bg-slate-700'}`} />
                    </div>

                    <div
                        onClick={() => toggleConstraint('forceTierSet')}
                        className={`cursor-pointer flex items-center justify-between p-2 border ${constraints.forceTierSet ? 'border-amber-500/30 bg-amber-900/10' : 'border-slate-800'}`}
                    >
                        <span className={`text-[10px] ${constraints.forceTierSet ? 'text-amber-500' : 'text-slate-500'}`}>MAINTAIN_4PC_TIER</span>
                        <div className={`w-2 h-2 rounded-sm ${constraints.forceTierSet ? 'bg-amber-500' : 'bg-slate-700'}`} />
                    </div>

                    <div className="flex items-center justify-center p-2 border border-slate-800 bg-black opacity-50 cursor-not-allowed">
                        <span className="text-[10px] text-slate-600">SLOT_LOCKING (COMING_SOON)</span>
                    </div>
                </div>

                {/* 3. EXECUTION PANEL */}
                <div className="flex gap-4 items-center">
                    <button
                        onClick={handleSolve}
                        disabled={solving}
                        className={`flex-1 py-4 font-bold text-sm uppercase tracking-widest transition-all clip-path-slant ${solving
                                ? 'bg-slate-800 text-slate-500 cursor-wait'
                                : 'bg-cyan-500 text-black hover:bg-cyan-400 hover:shadow-[0_0_20px_rgba(34,211,238,0.4)]'
                            }`}
                    >
                        {solving ? 'RUNNING_SIMULATION...' : 'SOLVE_LOADOUT'}
                    </button>

                    <div className="w-1/3 bg-black border border-slate-800 p-2 flex flex-col justify-center">
                        <div className="flex justify-between text-[8px] text-slate-500 mb-1">
                            <span>EST_TIME</span>
                            <span>12.4s</span>
                        </div>
                        <div className="h-1 bg-slate-800 w-full overflow-hidden">
                            {solving && <div className="h-full bg-cyan-500 animate-progress" style={{ width: `${progress}%` }}></div>}
                        </div>
                    </div>
                </div>

                {/* 4. RESULTS (Context Aware) */}
                {!solving && progress === 100 && (
                    <div className="animate-in fade-in slide-in-from-bottom-2 duration-300">
                        <div className="bg-slate-900/50 border-l-2 border-cyan-500 p-4">
                            <div className="flex justify-between items-end mb-2">
                                <span className="text-[10px] text-cyan-500 font-bold uppercase">Optimized_Delta</span>
                                <span className="text-xl text-white font-mono font-bold">{solution.dpsGain}</span>
                            </div>

                            {/* Pawn String Auto-Generator */}
                            <div className="mt-4 pt-4 border-t border-white/5">
                                <div className="text-[9px] text-slate-500 mb-2">GENERATED_PAWN_STRING ({activeSpec}):</div>
                                <code className="block bg-black p-2 text-[9px] text-green-500 font-mono break-all border border-slate-800">
                                    ( Pawn: v1: "Holocron_{activeSpec}": Class=Evoker, Haste=1.42, Crit=0.9... )
                                </code>
                            </div>
                        </div>
                    </div>
                )}

            </div>
        </div>
    );
};
