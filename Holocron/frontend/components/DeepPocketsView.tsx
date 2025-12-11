import React, { useState, useEffect } from 'react';
import { Scroll } from './Icons';

export default function DeepPocketsView() {
    const [inventory, setInventory] = useState<any[]>([]);
    const [filteredInventory, setFilteredInventory] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');
    const [qualityFilter, setQualityFilter] = useState('All');

    useEffect(() => {
        fetch('/api/deeppockets/inventory')
            .then(res => res.json())
            .then(data => {
                const items = data.items || [];
                setInventory(items);
                setFilteredInventory(items);
                setLoading(false);
            })
            .catch(err => {
                console.error('Failed to fetch inventory:', err);
                setLoading(false);
            });
    }, []);

    useEffect(() => {
        let result = inventory.filter(item =>
            item.name.toLowerCase().includes(searchTerm.toLowerCase())
        );

        if (qualityFilter !== 'All') {
            result = result.filter(item => item.quality === qualityFilter);
        }

        setFilteredInventory(result);
    }, [searchTerm, qualityFilter, inventory]);

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
                <div className="flex justify-between items-end">
                    <div>
                        <h1 className="text-3xl font-bold text-white font-warcraft tracking-widest mb-2 text-shadow-glow">
                            DEEP POCKETS
                        </h1>
                        <p className="text-slate-400">Inventory Management & Item Tracking</p>
                    </div>
                    <div className="text-right">
                        <div className="text-2xl font-bold text-white">{inventory.length}</div>
                        <div className="text-xs text-slate-500 uppercase tracking-wider">Total Items</div>
                    </div>
                </div>
            </div>

            <div className="wow-panel p-4 rounded border border-white/10 bg-noise flex gap-4">
                <div className="flex-1">
                    <input
                        type="text"
                        placeholder="Search items..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="w-full bg-black/40 border border-white/20 rounded px-4 py-2 text-white focus:border-rarity-rare outline-none"
                    />
                </div>
                <select
                    value={qualityFilter}
                    onChange={(e) => setQualityFilter(e.target.value)}
                    className="bg-black/40 border border-white/20 rounded px-4 py-2 text-white focus:border-rarity-rare outline-none"
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
                    <div key={idx} className="wow-card p-3 rounded border border-white/10 hover:border-white/30 transition-colors bg-noise flex items-center gap-3">
                        <div className={`w-10 h-10 rounded border border-white/20 bg-black/50 flex items-center justify-center`}>
                            {/* Placeholder icon if no image */}
                            <Scroll className="w-5 h-5 text-slate-500" />
                        </div>
                        <div className="flex-1 min-w-0">
                            <h4 className={`font-bold truncate ${item.quality === 'Epic' ? 'text-rarity-epic' :
                                    item.quality === 'Rare' ? 'text-rarity-rare' :
                                        item.quality === 'Uncommon' ? 'text-rarity-uncommon' : 'text-white'
                                }`}>
                                {item.name}
                            </h4>
                            <p className="text-xs text-slate-400">Qty: {item.quantity} • {item.type}</p>
                        </div>
                    </div>
                ))}
                {filteredInventory.length === 0 && (
                    <div className="col-span-full text-center py-8 text-slate-500">
                        No items found matching your search.
                    </div>
                )}
            </div>
        </div>
    );
}
