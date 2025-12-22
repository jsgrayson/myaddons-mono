import React from 'react';

export const FieldLogistics: React.FC = () => {
    // Mock Data: Syncs with Addon to know real cooldowns
    const assets = [
        { name: 'MOLL-E', type: 'MAILBOX_TOY', status: 'READY', cooldown: 0 },
        { name: 'Katy Stampwhistle', type: 'MAILBOX_TOY', status: 'ON_COOLDOWN', cooldown: 6400 }, // seconds
        { name: 'Ohn\'ir Windsage', type: 'MAILBOX_TOY', status: 'READY', cooldown: 0 },
        { name: 'Grand Expedition Yak', type: 'VENDOR_MOUNT', status: 'READY', cooldown: 0 },
        { name: 'Warband Bank Distance', type: 'SPELL', status: 'READY', cooldown: 0 }, // The new Warband spell
    ];

    return (
        <div className="w-full bg-[#020617] border border-slate-800 p-4 mt-4">

            <div className="flex justify-between items-center mb-3">
                <h3 className="text-[10px] text-purple-400 font-bold uppercase tracking-widest">
                    Field_Asset_Availability
                </h3>
                <span className="text-[9px] text-slate-500">MOBILE_NODES: <span className="text-white">ACTIVE</span></span>
            </div>

            <div className="grid grid-cols-5 gap-2">
                {assets.map((asset, idx) => (
                    <div
                        key={idx}
                        className={`p-2 border flex flex-col justify-between h-16 ${asset.status === 'READY'
                                ? 'bg-purple-900/10 border-purple-500/50'
                                : 'bg-slate-900/50 border-slate-700 opacity-60'
                            }`}
                    >
                        <div className="flex justify-between items-start">
                            <span className={`text-[9px] font-bold ${asset.status === 'READY' ? 'text-white' : 'text-slate-500'}`}>
                                {asset.name}
                            </span>
                            {asset.type === 'MAILBOX_TOY' && <span className="text-[8px] text-purple-400">📬</span>}
                            {asset.type === 'VENDOR_MOUNT' && <span className="text-[8px] text-amber-400">🛒</span>}
                        </div>

                        <div className="text-[9px] font-mono text-right">
                            {asset.status === 'READY' ? (
                                <span className="text-green-400">DEPLOY_READY</span>
                            ) : (
                                <span className="text-red-400">CD: {Math.floor(asset.cooldown / 60)}m</span>
                            )}
                        </div>
                    </div>
                ))}
            </div>

            {/* Dynamic Instruction Overlay */}
            <div className="mt-3 bg-black border border-slate-800 p-2 flex items-center justify-between">
                <div className="text-[9px] text-slate-400">
                    OPTIMAL_EXECUTION_PATH:
                </div>
                <div className="text-[10px] font-bold text-cyan-400 font-mono">
                    {`>> CAST_WARBAND_BANK (SPELL) >> DEPOSIT_ALL`}
                </div>
            </div>

        </div>
    );
};
