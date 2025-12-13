import { useState, useEffect } from 'react';
import { DollarSign, TrendingUp, Sparkles } from './Icons';

export default function GoblinView() {
    const [opportunities, setOpportunities] = useState<any[]>([]);
    const [filteredOpps, setFilteredOpps] = useState<any[]>([]);
    const [summary, setSummary] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');
    const [sortBy, setSortBy] = useState<'profit' | 'margin' | 'score'>('profit');
    const [minProfit, setMinProfit] = useState(0);

    useEffect(() => {
        // Fetch Data
        fetch('/api/goblin')
            .then(res => res.json())
            .then(data => {
                const opps = data.opportunities || [];
                setOpportunities(opps);
                // Initial Filter from URL if present
                const params = new URLSearchParams(window.location.search);
                const itemName = params.get('item_name');
                if (itemName) {
                    setSearchTerm(decodeURIComponent(itemName));
                    // If filtering by specific item, maybe clear min profit by default?
                    // setMinProfit(0); // Optional UX choice
                }
                setSummary(data);
                setLoading(false);
            })
            .catch(err => {
                console.error('Failed to fetch goblin data:', err);
                setLoading(false);
            });
    }, []);

    useEffect(() => {
        let filtered = opportunities.filter(opp =>
            opp.recipe_name.toLowerCase().includes(searchTerm.toLowerCase()) &&
            opp.profit >= minProfit
        );

        filtered.sort((a, b) => {
            if (sortBy === 'profit') return b.profit - a.profit;
            if (sortBy === 'margin') return b.profit_margin - a.profit_margin;
            return b.score - a.score;
        });

        setFilteredOpps(filtered);
    }, [searchTerm, minProfit, sortBy, opportunities]);

    if (loading) {
        return (
            <div className="flex items-center justify-center h-full">
                <div className="text-center">
                    <DollarSign className="w-16 h-16 text-azeroth-gold animate-pulse mx-auto mb-4" />
                    <p className="text-slate-400 font-warcraft">Loading Market Data...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            {/* Header with Stats */}
            <div className="wow-panel p-6 rounded border border-azeroth-gold/30 shadow-glow-gold bg-noise">
                <div className="flex justify-between items-start mb-4">
                    <div>
                        <h1 className="text-3xl font-bold text-white font-warcraft tracking-widest mb-2 text-shadow-glow">
                            GOBLIN MARKETS
                        </h1>
                        <p className="text-slate-400">
                            Total Profit: <span className="text-azeroth-gold font-bold">{summary?.total_potential_profit || 0}g</span>
                            <span className="text-slate-500 mx-2">•</span>
                            Opportunities: <span className="text-white font-bold">{filteredOpps.length}</span>
                        </p>
                    </div>
                    <button
                        onClick={() => window.location.reload()}
                        className="px-4 py-2 bg-azeroth-gold/20 border border-azeroth-gold text-azeroth-gold rounded hover:bg-azeroth-gold hover:text-black transition-all font-warcraft text-sm tracking-wider"
                    >
                        Refresh Prices
                    </button>
                </div>
            </div>

            {/* Interactive Filters */}
            <div className="wow-panel p-4 rounded border border-white/10 bg-noise">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {/* Search */}
                    <div>
                        <label className="text-xs text-slate-400 font-warcraft uppercase mb-1 block">Search Recipe</label>
                        <input
                            type="text"
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                            placeholder="Type to filter..."
                            className="w-full bg-black/40 border border-white/20 rounded px-3 py-2 text-white placeholder-slate-600 focus:border-azeroth-gold focus:outline-none"
                        />
                    </div>

                    {/* Min Profit Filter */}
                    <div>
                        <label className="text-xs text-slate-400 font-warcraft uppercase mb-1 block">Min Profit: {minProfit}g</label>
                        <input
                            type="range"
                            min="0"
                            max="500"
                            step="10"
                            value={minProfit}
                            onChange={(e) => setMinProfit(Number(e.target.value))}
                            className="w-full"
                        />
                    </div>

                    {/* Sort */}
                    <div>
                        <label className="text-xs text-slate-400 font-warcraft uppercase mb-1 block">Sort By</label>
                        <select
                            value={sortBy}
                            onChange={(e) => setSortBy(e.target.value as any)}
                            className="w-full bg-black/40 border border-white/20 rounded px-3 py-2 text-white focus:border-azeroth-gold focus:outline-none"
                        >
                            <option value="profit">Profit (High to Low)</option>
                            <option value="margin">Margin %</option>
                            <option value="score">Score</option>
                        </select>
                    </div>
                </div>
            </div>

            {/* Opportunities Grid */}
            <div className="grid grid-cols-1 gap-4">
                {filteredOpps.length > 0 ? (
                    filteredOpps.map((opp, idx) => (
                        <div key={idx} className="wow-card p-4 rounded border border-white/10 hover:border-azeroth-gold/50 transition-all bg-noise group">
                            <div className="flex justify-between items-start">
                                <div className="flex-1">
                                    <h3 className="text-lg font-bold text-white font-warcraft mb-1 group-hover:text-azeroth-gold transition-colors">
                                        {opp.recipe_name}
                                    </h3>
                                    <p className="text-sm text-slate-400">{opp.recommendation}</p>
                                </div>
                                <div className="text-right">
                                    <div className="text-2xl font-bold text-azeroth-gold">{opp.profit}g</div>
                                    <div className="text-xs text-rarity-uncommon">+{opp.profit_margin}%</div>
                                </div>
                            </div>
                            <div className="mt-3 flex items-center justify-between">
                                <div className="grid grid-cols-3 gap-3 text-sm flex-1">
                                    <div>
                                        <span className="text-slate-500">Cost:</span>
                                        <span className="text-white ml-2">{opp.crafting_cost}g</span>
                                    </div>
                                    <div>
                                        <span className="text-slate-500">Value:</span>
                                        <span className="text-white ml-2">{opp.market_value}g</span>
                                    </div>
                                    <div>
                                        <span className="text-slate-500">Score:</span>
                                        <span className="text-rarity-epic ml-2">{opp.score}</span>
                                    </div>
                                </div>
                                <button className="px-4 py-2 bg-rarity-epic/20 border border-rarity-epic text-rarity-epic rounded hover:bg-rarity-epic hover:text-white transition-all text-sm font-warcraft tracking-wide">
                                    Queue Craft
                                </button>
                            </div>
                        </div>
                    ))
                ) : (
                    <div className="wow-card p-8 rounded border border-white/10 bg-noise text-center">
                        <p className="text-slate-500">No opportunities match your filters</p>
                        <button
                            onClick={() => {
                                setSearchTerm('');
                                setMinProfit(0);
                                // Clear URL params too
                                const url = new URL(window.location.href);
                                url.searchParams.delete('item_name');
                                window.history.pushState({}, '', url.toString());
                            }}
                            className="mt-4 text-azeroth-gold hover:underline text-sm"
                        >
                            Clear Filters
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
}
