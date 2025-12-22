import React, { useState } from 'react';
import { Settings, Zap, Shield, Sparkles, X } from './Icons';

interface LODrawerProps {
    isOpen: boolean;
    onClose: () => void;
}

export const LODrawer: React.FC<LODrawerProps> = ({ isOpen, onClose }) => {
    const [stability, setStability] = useState(0.95);
    const [maxDepth, setMaxDepth] = useState(12);
    const [preferExisting, setPreferExisting] = useState(true);

    return (
        <>
            {/* Backdrop */}
            <div
                className={`fixed inset-0 bg-black/60 backdrop-blur-sm z-[100] transition-opacity duration-300 ${isOpen ? 'opacity-100' : 'opacity-0 pointer-events-none'}`}
                onClick={onClose}
            />

            {/* Drawer */}
            <div className={`fixed top-0 right-0 h-full w-80 bg-slate-950 border-l border-cyan-500/20 z-[101] transition-transform duration-500 shadow-[-20px_0_50px_rgba(0,0,0,0.5)] ${isOpen ? 'translate-x-0' : 'translate-x-full'}`}>
                <div className="absolute inset-0 opacity-5 pointer-events-none" style={{ backgroundImage: 'radial-gradient(circle at 2px 2px, #22d3ee 1px, transparent 0)', backgroundSize: '24px 24px' }}></div>

                <div className="relative h-full flex flex-col p-6">
                    <header className="flex justify-between items-center mb-10">
                        <div>
                            <h2 className="text-xs font-mono font-bold text-cyan-500 uppercase tracking-[0.3em]">System_Overrides</h2>
                            <h3 className="text-xl font-light text-white uppercase tracking-tighter">Logic<span className="text-cyan-500 font-bold">LO</span></h3>
                        </div>
                        <button onClick={onClose} className="p-2 text-slate-500 hover:text-white transition-colors">
                            <X className="w-5 h-5" />
                        </button>
                    </header>

                    <div className="flex-1 space-y-8">
                        {/* Stability Requirement */}
                        <div className="space-y-3">
                            <div className="flex justify-between items-center">
                                <label className="text-[10px] font-mono text-slate-400 uppercase tracking-widest flex items-center gap-2">
                                    <Shield className="w-3 h-3 text-cyan-500" />
                                    Verify_Stability
                                </label>
                                <span className="text-xs font-mono text-cyan-400">{(stability * 100).toFixed(0)}%</span>
                            </div>
                            <input
                                type="range"
                                min="0.5"
                                max="1.0"
                                step="0.01"
                                value={stability}
                                onChange={(e) => setStability(parseFloat(e.target.value))}
                                className="w-full h-1 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-cyan-500"
                            />
                            <p className="text-[8px] text-slate-600 italic">Minimum confidence threshold before archiving skills.</p>
                        </div>

                        {/* Max DOM Depth */}
                        <div className="space-y-3">
                            <div className="flex justify-between items-center">
                                <label className="text-[10px] font-mono text-slate-400 uppercase tracking-widest flex items-center gap-2">
                                    <Zap className="w-3 h-3 text-pink-500" />
                                    Max_DOM_Depth
                                </label>
                                <span className="text-xs font-mono text-white">{maxDepth}</span>
                            </div>
                            <input
                                type="number"
                                value={maxDepth}
                                onChange={(e) => setMaxDepth(parseInt(e.target.value))}
                                className="w-full bg-slate-900 border border-slate-800 p-2 text-sm text-cyan-400 font-mono focus:outline-none focus:border-cyan-500/50"
                            />
                            <p className="text-[8px] text-slate-600 italic">Recursion limit for agent node exploration.</p>
                        </div>

                        {/* Prefer Existing API */}
                        <div className="space-y-3">
                            <div className="flex justify-between items-center p-3 bg-slate-900/50 border border-white/5 rounded-sm">
                                <label className="text-[10px] font-mono text-slate-400 uppercase tracking-widest flex items-center gap-2">
                                    <Sparkles className="w-3 h-3 text-purple-500" />
                                    Prefer_Existing
                                </label>
                                <button
                                    onClick={() => setPreferExisting(!preferExisting)}
                                    className={`w-10 h-5 rounded-full relative transition-colors ${preferExisting ? 'bg-cyan-600' : 'bg-slate-800'}`}
                                >
                                    <div className={`absolute top-1 w-3 h-3 bg-white rounded-full transition-all ${preferExisting ? 'left-6' : 'left-1'}`} />
                                </button>
                            </div>
                            <p className="text-[8px] text-slate-600 italic">Global preference for library reuse over new synthesis.</p>
                        </div>
                    </div>

                    <footer className="mt-auto pt-6 border-t border-white/5">
                        <button className="w-full py-3 bg-cyan-600 hover:bg-cyan-500 text-black font-mono font-bold text-[10px] uppercase tracking-widest transition-all shadow-[0_0_20px_rgba(6,182,212,0.2)]">
                            Apply_Overrides
                        </button>
                        <div className="mt-4 text-center">
                            <span className="text-[8px] font-mono text-slate-700 italic">LAST_SYNC: 18:46:12_UTC</span>
                        </div>
                    </footer>
                </div>
            </div>
        </>
    );
};
