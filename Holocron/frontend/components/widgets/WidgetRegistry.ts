import React from 'react';
import { DollarSign, Shield, Sparkles, Activity, Globe } from '../Icons';

// ========================================
// WIDGET REGISTRY
// ========================================

export type WidgetSize = 'small' | 'medium' | 'large' | 'full';

export interface WidgetConfig {
    id: string;
    name: string;
    description: string;
    icon: React.ComponentType<any>;
    defaultSize: WidgetSize;
    component: React.ComponentType<any>;
}

// Import widget components (will be created next)
import { GoldWidget } from './GoldWidget';
import { ScoreWidget } from './ScoreWidget';
import { RaidWidget } from './RaidWidget';
import { ActivityFeedWidget } from './ActivityFeedWidget';
import { CommandWidget } from './CommandWidget';

export const WIDGET_REGISTRY: Record<string, WidgetConfig> = {
    'stat-gold': {
        id: 'stat-gold',
        name: 'Gold Tracker',
        description: 'Track your character\'s gold and daily changes',
        icon: DollarSign,
        defaultSize: 'small',
        component: GoldWidget,
    },
    'stat-score': {
        id: 'stat-score',
        name: 'Performance Score',
        description: 'Your overall performance rating',
        icon: Sparkles,
        defaultSize: 'small',
        component: ScoreWidget,
    },
    'stat-raids': {
        id: 'stat-raids',
        name: 'Raid Progress',
        description: 'Current mythic raid progression',
        icon: Shield,
        defaultSize: 'small',
        component: RaidWidget,
    },
    'feed-activity': {
        id: 'feed-activity',
        name: 'Activity Feed',
        description: 'Live feed of recent events',
        icon: Activity,
        defaultSize: 'large',
        component: ActivityFeedWidget,
    },
    'command-center': {
        id: 'command-center',
        name: 'Command Display',
        description: 'Central holographic status display',
        icon: Globe,
        defaultSize: 'full',
        component: CommandWidget,
    },
};

export const DEFAULT_LAYOUT = ['command-center', 'stat-gold', 'stat-score', 'stat-raids', 'feed-activity'];

export const getWidget = (id: string): WidgetConfig | undefined => WIDGET_REGISTRY[id];

export const getAvailableWidgets = (currentLayout: string[]): WidgetConfig[] => {
    return Object.values(WIDGET_REGISTRY).filter(w => !currentLayout.includes(w.id));
};
