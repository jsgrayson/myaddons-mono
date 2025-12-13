import React, { useState, useEffect } from 'react';
import { Scroll, DollarSign } from './Icons';
import { InventoryItem, GroupedItem, groupItems, filterItems, calculateTotalValue, formatGold } from '../utils/inventory';

import { ViewState } from '../types';

interface DeepPocketsViewProps {
    onNavigate?: (view: ViewState, params?: Record<string, string>) => void;
}

export default function DeepPocketsView({ onNavigate }: DeepPocketsViewProps) {
    const [inventory, setInventory] = useState<GroupedItem[]>([]);
    const [filteredInventory, setFilteredInventory] = useState<GroupedItem[]>([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');
    const [qualityFilter, setQualityFilter] = useState('All');
    const [locationFilter, setLocationFilter] = useState('ALL');

    const handleItemClick = (item: GroupedItem) => {
        if (!onNavigate) return;

        // Navigate to Goblin view with item context
        onNavigate(ViewState.GOBLIN, {
            item_name: item.name,
            // item_id: item.id?.toString() // Pass ID if available?
        });
    };

    useEffect(() => {
        fetch('/api/deeppockets/inventory')
        // Fetch inventory using the Holocron Gateway endpoint
        const fetchInventory = async () => {
            try {
                setLoading(true);
                const response = await fetch('/api/v1/deeppockets/inventory');
                if (!response.ok) throw new Error('Failed to fetch inventory');
                const data = await response.json();

                const items: InventoryItem[] = data.items || [];
                // Transform and Group
                const grouped = groupItems(items);
                setInventory(grouped);
                setFilteredInventory(grouped);
            } catch (err) {
                console.error('Failed to fetch inventory:', err);
            } finally {
                setLoading(false);
            }
        };

        fetchInventory();
    }, []);

    useEffect(() => {
        const result = filterItems(inventory, locationFilter, qualityFilter, searchTerm);
        setFilteredInventory(result);
    }, [searchTerm, qualityFilter, inventory, locationFilter]);

    const totalValue = calculateTotalValue(filteredInventory);

    if (loading) {
        return (
            <div className="flex items-center justify-center h-full">
                <div className="text-center">
                    <Scroll className="w-16 h-16 text-rarity-rare animate-pulse mx-auto mb-4" />
                    <p className="text-slate-400 font-warcraft">Loading Inventory...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            <div className="wow-panel p-6 rounded border border-rarity-rare/30 shadow-glow-blue bg-noise">
                <div className="flex flex-col md:flex-row justify-between items-end gap-4">
                    <div>
                        <h1 className="text-3xl font-bold text-white font-warcraft tracking-widest mb-2 text-shadow-glow">
                            DEEP POCKETS
                        </h1>
                        <p className="text-slate-400">Inventory Management & Item Tracking</p>
                    </div>
                    <div className="flex gap-6 text-right">
                        <div>
                            <div className="text-2xl font-bold text-white">{filteredInventory.length}</div>
                            <div className="text-xs text-slate-500 uppercase tracking-wider">Unique Items</div>
                        </div>
                        <div>
                            <div className="text-2xl font-bold text-azeroth-gold font-mono tracking-tight">{formatGold(totalValue)}</div>
                            <div className="text-xs text-slate-500 uppercase tracking-wider">Total Value</div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Controls Bar */}
            <div className="wow-panel p-4 rounded border border-white/10 bg-noise flex flex-col md:flex-row gap-4">
                {/* Location Filter Tabs */}
                <div className="flex bg-black/40 rounded p-1 border border-white/10">
                    {['ALL', 'BAG', 'BANK', 'REAGENT_BANK'].map(loc => (
                        <button
                            key={loc}
                            onClick={() => setLocationFilter(loc)}
                            className={`px-4 py-1.5 rounded text-xs font-bold uppercase tracking-wide transition-colors ${locationFilter === loc
                                ? 'bg-slate-700 text-white shadow-sm'
                                : 'text-slate-500 hover:text-slate-300'
                                }`}
                        >
                            {loc.replace('_', ' ')}
                        </button>
                    ))}
                </div>

                <div className="flex-1">
                    <input
                        type="text"
                        placeholder="Search items..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="w-full bg-black/40 border border-white/20 rounded px-4 py-2 text-white focus:border-rarity-rare outline-none transition-colors"
                    />
                </div>

                <select
                    value={qualityFilter}
                    onChange={(e) => setQualityFilter(e.target.value)}
                    className="bg-black/40 border border-white/20 rounded px-4 py-2 text-white focus:border-rarity-rare outline-none cursor-pointer"
                >
                    <option value="All">All Qualities</option>
                    <option value="Epic">Epic</option>
                    <option value="Rare">Rare</option>
                    <option value="Uncommon">Uncommon</option>
                    <option value="Common">Common</option>
                </select>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {filteredInventory.map((item, idx) => (
                    <div
                        key={idx}
                        onClick={() => handleItemClick(item)}
                        className="wow-card p-3 rounded border border-white/10 hover:border-white/30 transition-all bg-noise flex items-center gap-3 group cursor-pointer hover:bg-white/5 active:scale-[0.98]"
                    >
                        <div className={`w-12 h-12 rounded border border-white/20 bg-black/50 flex items-center justify-center relative overflow-hidden group-hover:border-rarity-rare/50 transition-colors`}>
                            {item.quality === 'Epic' && <div className="absolute inset-0 bg-rarity-epic/20 animate-pulse-slow"></div>}
                            <Scroll className={`w-6 h-6 ${item.quality === 'Epic' ? 'text-rarity-epic' :
                                item.quality === 'Rare' ? 'text-rarity-rare' :
                                    item.quality === 'Uncommon' ? 'text-rarity-uncommon' : 'text-slate-500'
                                }`} />
                            {item.stacks > 1 && (
                                <div className="absolute bottom-0 right-0 bg-black/80 px-1 text-[9px] text-white border-tl border-white/20">
                                    {item.stacks} stacks
                                </div>
                            )}
                        </div>
                        <div className="flex-1 min-w-0">
                            <h4 className={`font-bold truncate ${item.quality === 'Epic' ? 'text-rarity-epic' :
                                item.quality === 'Rare' ? 'text-rarity-rare' :
                                    item.quality === 'Uncommon' ? 'text-rarity-uncommon' : 'text-white'
                                }`}>
                                {item.name}
                            </h4>
                            <div className="flex justify-between items-center text-xs mt-1">
                                <span className="text-slate-400">Qty: <span className="text-white font-mono">{item.totalQuantity}</span></span>
                                <span className="text-azeroth-gold font-mono">{formatGold(item.totalValue)}</span>
                            </div>
                            <div className="text-[10px] text-slate-500 mt-0.5 truncate uppercase tracking-wider group-hover:text-azeroth-gold transition-colors flex items-center gap-1">
                                {item.locations.join(' • ')}
                                <span className="opacity-0 group-hover:opacity-100 transition-opacity text-xs">↗</span>
                            </div>
                        </div>
                    </div>
                ))}
                {filteredInventory.length === 0 && (
                    <div className="col-span-full py-12 text-center border border-dashed border-white/10 rounded-lg">
                        <div className="inline-flex p-4 rounded-full bg-black/30 mb-3">
                            <DollarSign className="w-8 h-8 text-slate-600" />
                        </div>
                        <p className="text-slate-500 font-warcraft tracking-wide">No items found matching your filters.</p>
                    </div>
                )}
            </div>
        </div>
    );
}
