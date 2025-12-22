import React, { useState } from 'react';
import { TradeRouteManager } from './components/TradeRouteManager';
import { FieldLogistics } from './components/FieldLogistics';

// Types for the Order System
type Recommendation = { item: string; id: number; recipient: string; gain: string; icon: string };
type MailOrder = { recipient: string; items: string[] };

export const WarbandLogistics: React.FC = () => {
    const [analyzing, setAnalyzing] = useState(false);

    // Pending Recommendations (The "In-Box")
    const [recommendations, setRecommendations] = useState<Recommendation[]>([
        { id: 101, item: 'Void-Touched Claymore', icon: '⚔️', recipient: 'Alt_Warrior', gain: '+14.2%' },
        { id: 102, item: 'Cache of Storms', icon: '💎', recipient: 'Alt_Paladin', gain: '+8.5%' },
        { id: 103, item: 'Cloth of Unspoken Names', icon: '👘', recipient: 'Alt_Priest', gain: '+3.2%' },
    ]);

    // Approved Orders (The "Out-Box")
    const [manifest, setManifest] = useState<MailOrder[]>([]);

    // Move item from Recommendation -> Manifest
    const approveTransfer = (rec: Recommendation) => {
        setRecommendations(prev => prev.filter(r => r.id !== rec.id));

        setManifest(prev => {
            const existing = prev.find(o => o.recipient === rec.recipient);
            if (existing) {
                return prev.map(o => o.recipient === rec.recipient
                    ? { ...o, items: [...o.items, rec.item] }
                    : o
                );
            }
            return [...prev, { recipient: rec.recipient, items: [rec.item] }];
        });
    };

    // Generate the Lua String
    const generateManifestString = () => {
        // Format: "RECIPIENT:Item1,Item2;RECIPIENT2:Item3"
        const str = manifest.map(o => `${o.recipient}:${o.items.join(',')}`).join(';');
        return `HOLOCRON_MAIL::${btoa(str)}`;
    };

    return (
        <div className="w-full bg-[#020617] text-slate-200 font-mono p-6 border border-slate-800 flex flex-col gap-6 relative">

            {/* Header */}
            <header className="flex justify-between items-end border-b border-slate-800 pb-4">
                <div>
                    <h2 className="text-2xl font-bold text-white tracking-tighter">
                        WARBAND_LOGISTICS <span className="text-cyan-500 text-sm">FULFILLMENT_CENTER</span>
                    </h2>
                    <p className="text-[10px] text-slate-500 uppercase tracking-widest mt-1">
                        OPTIMIZATION_ENGINE: <span className="text-green-500">READY</span>
                    </p>
                </div>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">

                {/* LEFT: The Optimization Queue (Decisions) */}
                <section className="bg-slate-900/20 border border-slate-800 flex flex-col">
                    <div className="p-3 border-b border-slate-800 bg-slate-900/50 flex justify-between">
                        <span className="text-[10px] text-amber-500 font-bold uppercase">Pending_Transfers</span>
                        <span className="text-[10px] text-slate-500">{recommendations.length} ITEMS DETECTED</span>
                    </div>

                    <div className="flex-1 overflow-y-auto p-4 space-y-3">
                        {recommendations.map(rec => (
                            <div key={rec.id} className="flex justify-between items-center bg-black border border-slate-700 p-3 hover:border-amber-500/50 transition-colors group">
                                <div className="flex items-center gap-3">
                                    <div className="w-8 h-8 flex items-center justify-center bg-slate-800 text-lg grayscale group-hover:grayscale-0 transition-all">{rec.icon}</div>
                                    <div>
                                        <div className="text-xs font-bold text-white group-hover:text-amber-500 transition-colors">{rec.item}</div>
                                        <div className="text-[9px] text-slate-500">
                                            BETTER FOR: <span className="text-cyan-400 font-bold">{rec.recipient}</span> ({rec.gain})
                                        </div>
                                    </div>
                                </div>

                                <button
                                    onClick={() => approveTransfer(rec)}
                                    className="px-3 py-1 bg-amber-900/10 border border-amber-500 text-amber-500 text-[9px] font-bold uppercase hover:bg-amber-500 hover:text-black transition-all"
                                >
                                    CREATE_ORDER
                                </button>
                            </div>
                        ))}
                        {recommendations.length === 0 && (
                            <div className="text-center text-[10px] text-slate-600 mt-10">ALL_TRANSFERS_PROCESSED</div>
                        )}
                    </div>
                </section>

                {/* RIGHT: The Manifest (Execution) */}
                <section className="bg-black border border-slate-800 flex flex-col relative overflow-hidden">
                    {/* Background decoration */}
                    <div className="absolute top-0 right-0 p-4 pointer-events-none opacity-10">
                        <div className="text-6xl font-bold text-slate-700">MANIFEST</div>
                    </div>

                    <div className="p-3 border-b border-slate-800 bg-slate-900/80 flex justify-between">
                        <span className="text-[10px] text-cyan-500 font-bold uppercase">Logistics_Manifest (Outbox)</span>
                        <span className="text-[10px] text-slate-500">{manifest.length} PACKAGES</span>
                    </div>

                    <div className="flex-1 overflow-y-auto p-4 space-y-4">
                        {manifest.map((order, idx) => (
                            <div key={idx} className="relative pl-4 border-l-2 border-slate-700">
                                <div className="text-[10px] text-slate-400 mb-1">RECIPIENT: <span className="text-white font-bold">{order.recipient}</span></div>
                                <div className="space-y-1">
                                    {order.items.map((item, i) => (
                                        <div key={i} className="bg-slate-900/40 p-1 px-2 border border-slate-800 text-[10px] text-cyan-600 font-mono truncate">
                                            {item}
                                        </div>
                                    ))}
                                </div>
                            </div>
                        ))}
                    </div>

                    {/* Export Action Area */}
                    <div className="p-4 border-t border-slate-800 bg-slate-900/30">
                        <div className="text-[9px] text-slate-500 mb-2">ADDON_IMPORT_STRING:</div>

                        <div className="relative group">
                            <textarea
                                readOnly
                                value={manifest.length > 0 ? generateManifestString() : 'AWAITING_ORDERS...'}
                                className="w-full h-16 bg-black border border-slate-700 p-2 text-[9px] font-mono text-green-500 resize-none focus:outline-none"
                            />
                            {/* Copy Overlay */}
                            {manifest.length > 0 && (
                                <div className="absolute inset-0 bg-black/80 opacity-0 group-hover:opacity-100 flex items-center justify-center transition-opacity cursor-pointer">
                                    <span className="text-green-500 font-bold text-xs uppercase border border-green-500 px-4 py-2 hover:bg-green-500 hover:text-black transition-colors">
                                        COPY_MANIFEST_TO_CLIPBOARD
                                    </span>
                                </div>
                            )}
                        </div>

                        <div className="mt-2 flex justify-between items-center">
                            <span className="text-[9px] text-slate-600">INSTRUCTION: PASTE INTO HOLOCRON ADDON -&gt; TAB: "LOGISTICS"</span>
                        </div>
                    </div>

                </section>

            </div>

            {/* BOTTOM: Field Logistics & Trade Routes */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <TradeRouteManager />
                <FieldLogistics />
            </div>
        </div>
    );
};
