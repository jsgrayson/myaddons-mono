import React, { useState } from 'react';

// Assets
const ASSETS = {
    networkMap: "url('/assets/network-topology-grid.png')",
};

export const HardwareMonitor: React.FC = () => {
    const [selectedClient, setSelectedClient] = useState<'DESKTOP' | 'CLAW'>('DESKTOP');

    // Mock State of the Fleet
    const clients = {
        DESKTOP: { status: 'ONLINE', ip: '192.168.1.50', syncState: 'SYNCED', latency: 4 },
        CLAW: { status: 'ONLINE', ip: '192.168.1.55', syncState: 'OUTDATED', latency: 24 }
    };

    return (
        <div
            className="min-h-screen bg-[#020617] text-slate-200 font-mono p-8 relative overflow-hidden"
            style={{ backgroundImage: ASSETS.networkMap, backgroundSize: 'cover', backgroundBlendMode: 'overlay' }}
        >

            {/* Header */}
            <header className="flex justify-between items-end border-b border-slate-800 pb-6 mb-8 backdrop-blur-sm relative z-10">
                <div>
                    <h1 className="text-3xl font-bold tracking-tighter text-white">
                        NETWORK_UPLINK <span className="text-cyan-500 text-sm align-top">FLEET_MANAGER</span>
                    </h1>
                    <p className="text-[10px] text-slate-500 uppercase tracking-widest mt-1">
                        DATA_PASSING_PROTOCOL: <span className="text-cyan-400">WEBSOCKET_SECURE</span>
                    </p>
                </div>

                {/* Master Sync Button */}
                <button className="px-6 py-2 bg-cyan-900/20 border border-cyan-500 text-cyan-400 text-xs font-bold hover:bg-cyan-500 hover:text-black transition-all uppercase">
                    FORCE_GLOBAL_SYNC
                </button>
            </header>

            <main className="grid grid-cols-12 gap-8 relative z-10">

                {/* Left: Device Selector (The "Hub") */}
                <section className="col-span-3 space-y-4">
                    <label className="text-[10px] text-slate-500 uppercase tracking-widest">Select_Target_Node</label>

                    {/* Desktop Card */}
                    <div
                        onClick={() => setSelectedClient('DESKTOP')}
                        className={`p-4 border cursor-pointer transition-all ${selectedClient === 'DESKTOP' ? 'bg-cyan-950/30 border-cyan-500' : 'bg-slate-900/30 border-slate-700 hover:border-cyan-500/50'}`}
                    >
                        <div className="flex justify-between items-center mb-2">
                            <span className="font-bold text-white">DESKTOP_PC_MAIN</span>
                            <div className="w-2 h-2 rounded-full bg-green-500 shadow-[0_0_8px_#22c55e]" />
                        </div>
                        <div className="text-[10px] text-slate-400 font-mono space-y-1">
                            <div className="flex justify-between"><span>IP:</span> <span className="text-cyan-400">192.168.1.50</span></div>
                            <div className="flex justify-between"><span>LATEST_PUSH:</span> <span className="text-white">SEQ_V1.2.7</span></div>
                        </div>
                    </div>

                    {/* Claw Card */}
                    <div
                        onClick={() => setSelectedClient('CLAW')}
                        className={`p-4 border cursor-pointer transition-all ${selectedClient === 'CLAW' ? 'bg-cyan-950/30 border-cyan-500' : 'bg-slate-900/30 border-slate-700 hover:border-cyan-500/50'}`}
                    >
                        <div className="flex justify-between items-center mb-2">
                            <span className="font-bold text-white">MSI_CLAW_MOBILE</span>
                            <div className="w-2 h-2 rounded-full bg-amber-500 animate-pulse" />
                        </div>
                        <div className="text-[10px] text-slate-400 font-mono space-y-1">
                            <div className="flex justify-between"><span>IP:</span> <span className="text-cyan-400">192.168.1.55</span></div>
                            <div className="flex justify-between"><span>LATEST_PUSH:</span> <span className="text-red-400">SEQ_V1.2.6 (OUTDATED)</span></div>
                        </div>
                    </div>
                </section>

                {/* Center: Data Loop Visualization */}
                <section className="col-span-9 bg-black/80 border border-slate-800 relative p-6 backdrop-blur-md">
                    <div className="absolute top-4 left-4 text-[10px] text-cyan-500 uppercase tracking-widest">
                        Data_Pipeline_Status // {selectedClient}
                    </div>

                    {/* Visualizing the "Up" and "Down" Stream */}
                    <div className="grid grid-cols-3 gap-4 mt-12 text-center font-mono text-[10px]">

                        {/* Step 1: Ingest */}
                        <div className="p-4 border border-dashed border-slate-700 rounded bg-slate-900/20">
                            <div className="text-slate-400 mb-2">UPSTREAM (FROM CLIENT)</div>
                            <div className="text-xl font-bold text-white mb-1">ADDON_DATA</div>
                            <div className="text-green-500">RECEIVED: 2s AGO</div>
                        </div>

                        {/* Arrow */}
                        <div className="flex items-center justify-center">
                            <div className="h-1 w-full bg-slate-800 relative">
                                <div className="absolute right-0 top-1/2 -translate-y-1/2 w-2 h-2 bg-slate-500 rotate-45" />
                            </div>
                        </div>

                        {/* Step 2: Deploy */}
                        <div className="p-4 border border-dashed border-slate-700 rounded bg-slate-900/20">
                            <div className="text-slate-400 mb-2">DOWNSTREAM (TO CLIENT)</div>

                            <div className="flex justify-between items-center mb-1">
                                <div className="text-xs font-bold text-white">SEQ_HEX_FILE</div>
                                {selectedClient === 'CLAW' ? (
                                    <div className="text-[9px] text-amber-500 animate-pulse">PENDING</div>
                                ) : (
                                    <div className="text-[9px] text-green-500">SYNCED</div>
                                )}
                            </div>

                            <div className="flex justify-between items-center border-t border-slate-800 pt-1 mt-1">
                                <div className="text-xs font-bold text-white">PAWN_STRING</div>
                                <div className="text-[9px] text-green-500">SYNCED (V1.2)</div>
                            </div>
                        </div>

                    </div>

                    {/* Remote Hardware Telemetry (The Pass-Through) */}
                    <div className="mt-12 pt-8 border-t border-slate-800">
                        <h3 className="text-[10px] text-slate-500 uppercase tracking-widest mb-4">Remote_Hardware_Telemetry (Relayed)</h3>
                        <div className="grid grid-cols-4 gap-4">
                            <div className="bg-slate-900/50 p-2 border-l-2 border-cyan-500">
                                <div className="text-[9px] text-slate-500">PRO_MICRO_STATUS</div>
                                <div className="text-sm text-white">CONNECTED (COM4)</div>
                            </div>
                            <div className="bg-slate-900/50 p-2 border-l-2 border-green-500">
                                <div className="text-[9px] text-slate-500">AVG_GCD_DELTA</div>
                                <div className="text-sm text-white">0.02ms</div>
                            </div>
                            <div className="bg-slate-900/50 p-2 border-l-2 border-slate-500">
                                <div className="text-[9px] text-slate-500">KEY_MATRIX_TEMP</div>
                                <div className="text-sm text-white">34°C</div>
                            </div>
                        </div>
                    </div>

                </section>
            </main>
        </div>
    );
};
