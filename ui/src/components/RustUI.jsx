import React, { useState } from 'react';

const RustUI = () => {
    const [tickerItems] = useState([
        { name: "DRACONIUM", price: "45g", change: -2.3 },
        { name: "KHAZ'GORITE", price: "120g", change: 5.1 },
        { name: "AWAKENED AIR", price: "850g", change: 12.4 },
        { name: "SEREVITE", "price": "15g", change: -0.5 },
    ]);

    return (
        <div className="goblin-panel pointer-events-auto">

            {/* [LEFT SCRREBN] Status Modules */}
            <div className="goblin-screen flex flex-col gap-6">
                <div className="border border-green-900/50 p-2">
                    <h3 className="text-[#eeb211] mb-2 font-bold border-b border-[#eeb211]/30 pb-1">MODULE_STATUS</h3>
                    <ul className="space-y-3 font-bold text-sm">
                        <li className="flex justify-between items-center">
                            <span>AUCTION</span>
                            <span className="text-[#39ff14] bg-[#39ff14]/10 px-2 rounded">OK</span>
                        </li>
                        <li className="flex justify-between items-center">
                            <span>UNDERMINE</span>
                            <span className="text-[#39ff14] bg-[#39ff14]/10 px-2 rounded">OK</span>
                        </li>
                        <li className="flex justify-between items-center">
                            <span>TSM_SYNC</span>
                            <span className="text-[#eeb211] bg-[#eeb211]/10 px-2 rounded animate-pulse">SYNC</span>
                        </li>
                    </ul>
                </div>

                <div className="mt-auto">
                    <h2 className="text-[#eeb211] text-sm mb-1">REVENUE</h2>
                    <div className="text-4xl text-[#39ff14] drop-shadow-[0_0_5px_rgba(57,255,20,0.8)]">
                        452,980g
                    </div>
                    <div className="text-right text-xs text-[#eeb211] mt-1">+12.5%</div>
                </div>
            </div>

            {/* [CENTER SCREEN] Transaction Log */}
            <div className="goblin-screen flex flex-col">
                <div className="text-[#eeb211] text-center text-xl mb-4 font-bold border-b border-[#eeb211]/30 pb-2">
                    &lt; LIVE_FEED &gt;
                </div>
                <div className="flex-1 overflow-y-auto custom-scrollbar">
                    <table className="w-full text-left">
                        <thead className="text-[#eeb211] sticky top-0 bg-[#050505] z-10">
                            <tr>
                                <th className="p-2">TIME</th>
                                <th className="p-2">ITEM</th>
                                <th className="p-2 text-right">VAL</th>
                            </tr>
                        </thead>
                        <tbody className="text-[#39ff14]">
                            {[...Array(20)].map((_, i) => (
                                <tr key={i} className="hover:bg-[#39ff14]/10 border-b border-[#39ff14]/10">
                                    <td className="p-2 opacity-70">14:2{i}:05</td>
                                    <td className="p-2">Draconium Ore [Q3]</td>
                                    <td className="p-2 text-right text-[#eeb211] font-bold">+45g</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>

            {/* [RIGHT SCREEN] Ticker */}
            <div className="goblin-screen flex flex-col">
                <div className="text-right border-b border-[#eeb211]/30 pb-2 mb-4">
                    <h2 className="text-xl text-[#eeb211] font-bold">MARKET</h2>
                    <div className="text-xs opacity-70">US-NA // GADGETZAN</div>
                </div>

                <div className="flex-1 overflow-hidden relative">
                    <div className="animate-ticker-vertical flex flex-col gap-2">
                        {[...tickerItems, ...tickerItems, ...tickerItems].map((item, i) => (
                            <div key={i} className="p-2 border border-[#39ff14]/20 hover:bg-[#39ff14]/10">
                                <div className="font-bold">{item.name}</div>
                                <div className="flex justify-between items-center text-sm mt-1">
                                    <span className="text-[#eeb211]">{item.price}</span>
                                    <span className={item.change > 0 ? "text-[#39ff14]" : "text-red-500"}>
                                        {item.change}%
                                    </span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

        </div>
    );
};

export default RustUI;
