export interface InventoryItem {
    name: string;
    quantity: number;
    quality: string;
    type: string;
    location?: string; // 'Bag', 'Bank', 'Reagent Bank'
    icon?: string;
    price?: number; // Single unit price
    id?: number;
}

export interface GroupedItem extends InventoryItem {
    totalQuantity: number;
    totalValue: number;
    locations: string[]; // List of where this item is found
    stacks: number; // How many stacks combined
}

// Group items by Name (and ID if available)
export const groupItems = (items: InventoryItem[]): GroupedItem[] => {
    const groups: { [key: string]: GroupedItem } = {};

    items.forEach(item => {
        // Create a unique key (prefer ID if available, else Name)
        const key = item.id ? `id-${item.id}` : `name-${item.name}`;

        if (!groups[key]) {
            groups[key] = {
                ...item,
                totalQuantity: 0,
                totalValue: 0,
                locations: [],
                stacks: 0,
            };
        }

        const group = groups[key];
        group.totalQuantity += item.quantity;
        group.stacks += 1;

        // Accumulate Value (mock price if missing? handled in UI mostly, but let's try)
        // Assuming price is per unit. Validate inputs.
        const unitPrice = item.price || 0;
        group.totalValue += (unitPrice * item.quantity);

        // Track locations
        const loc = item.location || 'Unknown';
        if (!group.locations.includes(loc)) {
            group.locations.push(loc);
        }
    });

    return Object.values(groups).sort((a, b) => b.totalValue - a.totalValue); // Default sort by value
};

export const filterItems = (items: GroupedItem[], locationFilter: string, qualityFilter: string, search: string): GroupedItem[] => {
    return items.filter(item => {
        // Search Filter
        if (search && !item.name.toLowerCase().includes(search.toLowerCase())) return false;

        // Quality Filter
        if (qualityFilter !== 'All' && item.quality !== qualityFilter) return false;

        // Location Filter
        if (locationFilter !== 'ALL') {
            // Because items are grouped, we check if *any* stack is in this location
            // actually, user might want to see "Only items in Bank".
            // If I have Cloth in Bag AND Bank, showing the Group implies showing the total.
            // Strict filtering might mean "Show me only the stacks in Bank".
            // But we are committed to "Grouped View". 
            // So: If I filter "Bank", I should probably still show the item if it exists in Bank, 
            // but maybe adjusted quantity? 
            // FOR MVP: If the Group has presence in the location, show the Group.
            if (!item.locations.some(loc => loc.toLowerCase().includes(locationFilter.toLowerCase().replace('_', ' ')))) {
                return false;
            }
        }

        return true;
    });
};

export const calculateTotalValue = (items: GroupedItem[]): number => {
    return items.reduce((sum, item) => sum + item.totalValue, 0);
};

export const formatGold = (copper: number): string => {
    if (copper === 0) return '0g';
    const gold = Math.floor(copper / 10000);
    const silver = Math.floor((copper % 10000) / 100);
    const cop = copper % 100;

    let parts = [];
    if (gold > 0) parts.push(`${gold}g`);
    if (silver > 0) parts.push(`${silver}s`);
    // if (cop > 0) parts.push(`${cop}c`); // Too noisy/granular often
    return parts.join(' ');
};
