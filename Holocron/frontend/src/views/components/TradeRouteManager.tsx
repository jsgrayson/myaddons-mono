import React from 'react';

export const TradeRouteManager: React.FC = () => {
    // Mock State: The "Buffer" (Warbank)
    const warbankState = {
        TAB_1: { label: 'GEAR_TRANSFER', utilization: '80%' },
        TAB_2: { label: 'CONSUMABLES', utilization: '20%' },
        TAB_3: { label: 'AH_DUMP', utilization: '100% (FULL)' },
    };

    return (
        <div className="w-full bg-[#020617] border border-slate-800 p-4 mt-6">

            <div className="flex justify-between items-center mb-4">
                <h3 className="text-[10px] text-green-500 font-bold uppercase tracking-widest">
                    GOBLIN_TRADE_ROUTES <span className="text-slate-500">//</span> WARBANK_CONTROLLER
                </h3>
                <span className="text-[9px] text-slate-500">BANK_ACCESS: <span className="text-white">ONLINE</span></span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">

                {/* Route 1: Upgrade Pipeline (SkillWeaver) */}
                <div className="p-3 bg-slate-900/40 border-l-2 border-cyan-500">
                    <div className="text-[9px] text-cyan-500 mb-1">LOGISTICS_ROUTE_A</div>
                    <div className="text-xs font-bold text-white">GEAR_DISTRIBUTION</div>
                    <div className="mt-2 text-[9px] text-slate-400">
                        METHOD: <span className="text-white">WARBANK_TAB_1</span>
                        <br />
                        PENDING: 3 ITEMS
                    </div>
                </div>

                {/* Route 2: Liquidation Pipeline (Goblin) */}
                <div className="p-3 bg-slate-900/40 border-l-2 border-green-500">
                    <div className="text-[9px] text-green-500 mb-1">LOGISTICS_ROUTE_B</div>
                    <div className="text-xs font-bold text-white">AUCTION_LIQUIDATION</div>
                    <div className="mt-2 text-[9px] text-slate-400">
                        METHOD: <span className="text-white">WARBANK_TAB_3</span>
                        <br />
                        VALUE: 142,000g
                    </div>
                </div>

                {/* Warbank Capacity Viz */}
                <div className="p-3 bg-black border border-slate-800 flex flex-col justify-center">
                    <div className="flex justify-between text-[9px] text-slate-500 mb-1">
                        <span>WARBANK_CAPACITY</span>
                        <span className="text-red-500">TAB_3_FULL</span>
                    </div>
                    <div className="flex gap-1 h-2">
                        <div className="flex-1 bg-cyan-900/50 relative group">
                            <div className="absolute inset-0 bg-cyan-500 w-[80%]"></div>
                        </div>
                        <div className="flex-1 bg-green-900/50 relative">
                            <div className="absolute inset-0 bg-green-500 w-[100%] animate-pulse"></div>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    );
};
