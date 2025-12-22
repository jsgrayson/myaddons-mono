import React from 'react';

export interface NavItem {
    id: string;
    label: string;
    icon: React.ComponentType<any>;
}

export interface ChartData {
    name: string;
    value: number;
    uv: number;
}

export interface Message {
    id: string;
    role: 'user' | 'model';
    text: string;
    timestamp: Date;
}

export enum ViewState {
    DASHBOARD = 'DASHBOARD',
    GOBLIN = 'GOBLIN',
    NAVIGATOR = 'NAVIGATOR',
    PATHFINDER = 'PATHFINDER',
    CODEX = 'CODEX',
    DEEPPOCKETS = 'DEEPPOCKETS',
    SCOUT = 'SCOUT',
    DIPLOMAT = 'DIPLOMAT',
    AI_ASSISTANT = 'AI_ASSISTANT',
    ANALYTICS = 'ANALYTICS',
    GEAR_OPTIMIZER = 'GEAR_OPTIMIZER',
    WARBAND_LOGISTICS = 'WARBAND_LOGISTICS',
    SEQUENCE_FORGE = 'SEQUENCE_FORGE',
    HARDWARE_MONITOR = 'HARDWARE_MONITOR',
    SETTINGS = 'SETTINGS'
}

export interface KPI {
    label: string;
    value: string;
    change: string;
    trend: 'up' | 'down' | 'neutral';
}
