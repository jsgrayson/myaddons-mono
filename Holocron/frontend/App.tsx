// App.tsx - The Restored Holocron OS Core
import React, { useState } from 'react';
import { GearOptimizer } from './components/GearOptimizer';
import { SequenceForge } from './components/SequenceForge';
import { HardwareMonitor } from './components/HardwareMonitor';

const THEME = {
    bg: '#050505',
    panel: '#121212',
    accent: '#2DD4BF',
    border: '#2A2A2A'
};

export default function HolocronOS() {
    const [activeTab, setActiveTab] = useState('GEAR');

    return (
        <div style={{ backgroundColor: THEME.bg, color: '#FFF', height: '100vh', display: 'flex', flexDirection: 'column', fontFamily: 'JetBrains Mono, monospace' }}>
            {/* Unified Telemetry HUD */}
            <header style={{ padding: '10px 20px', borderBottom: `1px solid ${THEME.border}`, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div style={{ color: THEME.accent, fontWeight: 'bold', letterSpacing: '2px' }}>MIDNIGHT_SYNC // V2.11</div>
                <div style={{ display: 'flex', gap: '20px', fontSize: '12px' }}>
                    <span>LATENCY: <span style={{ color: THEME.accent }}>14ms</span></span>
                    <span>HARDWARE: <span style={{ color: '#10B981' }}>CONNECTED (0xAA)</span></span>
                </div>
            </header>

            <div style={{ display: 'flex', flex: 1, overflow: 'hidden' }}>
                {/* Sidebar Navigation */}
                <nav style={{ width: '80px', borderRight: `1px solid ${THEME.border}`, display: 'flex', flexDirection: 'column', alignItems: 'center', paddingTop: '20px', gap: '30px' }}>
                    <NavIcon active={activeTab === 'GEAR'} onClick={() => setActiveTab('GEAR')} label="GEAR" />
                    <NavIcon active={activeTab === 'FORGE'} onClick={() => setActiveTab('FORGE')} label="FORGE" />
                    <NavIcon active={activeTab === 'HARDWARE'} onClick={() => setActiveTab('HARDWARE')} label="LINK" />
                </nav>

                {/* Main Viewport */}
                <main style={{ flex: 1, padding: '20px', position: 'relative' }}>
                    {activeTab === 'GEAR' && <GearOptimizer />}
                    {activeTab === 'FORGE' && <SequenceForge />}
                    {activeTab === 'HARDWARE' && <HardwareMonitor />}
                </main>
            </div>
        </div>
    );
}

function NavIcon({ active, onClick, label }: { active: boolean, onClick: () => void, label: string }) {
    return (
        <div onClick={onClick} style={{
            cursor: 'pointer',
            color: active ? '#2DD4BF' : '#444',
            fontSize: '10px',
            textAlign: 'center',
            transition: 'all 0.2s'
        }}>
            <div style={{ width: '40px', height: '40px', border: `1px solid ${active ? '#2DD4BF' : '#333'}`, borderRadius: '8px', marginBottom: '5px' }}></div>
            {label}
        </div>
    );
}
