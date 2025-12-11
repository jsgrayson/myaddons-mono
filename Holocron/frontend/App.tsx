import React, { useState } from 'react';
import { LayoutDashboard, BarChart3, Bot, Settings, Bell, Shield, Sword, Scroll, Gem, DollarSign, Sparkles } from './components/Icons';
import DashboardView from './components/DashboardView';
import AiAssistantView from './components/AiAssistantView';
import GoblinView from './components/GoblinView';
import NavigatorView from './components/NavigatorView';
import CodexView from './components/CodexView';
import DeepPocketsView from './components/DeepPocketsView';
import ScoutView from './components/ScoutView';
import DiplomatView from './components/DiplomatView';
import { ViewState, NavItem } from './types';

export default function App() {
    const [currentView, setCurrentView] = useState<ViewState>(ViewState.DASHBOARD);

    const navItems: NavItem[] = [
        { id: ViewState.DASHBOARD, label: 'Dashboard', icon: LayoutDashboard },
        { id: ViewState.GOBLIN, label: 'Goblin Markets', icon: DollarSign },
        { id: ViewState.NAVIGATOR, label: 'Navigator', icon: Sparkles },
        { id: ViewState.CODEX, label: 'Codex', icon: Shield },
        { id: ViewState.DEEPPOCKETS, label: 'Deep Pockets', icon: Scroll },
        { id: ViewState.SCOUT, label: 'Scout', icon: Bell },
        { id: ViewState.DIPLOMAT, label: 'Diplomat', icon: Shield },
        { id: ViewState.AI_ASSISTANT, label: 'Oracle', icon: Gem },
        { id: ViewState.SETTINGS, label: 'Settings', icon: Settings },
    ];

    const renderContent = () => {
        switch (currentView) {
            case ViewState.DASHBOARD:
                return <DashboardView />;
            case ViewState.GOBLIN:
                return <GoblinView />;
            case ViewState.NAVIGATOR:
                return <NavigatorView />;
            case ViewState.CODEX:
                return <CodexView />;
            case ViewState.DEEPPOCKETS:
                return <DeepPocketsView />;
            case ViewState.SCOUT:
                return <ScoutView />;
            case ViewState.DIPLOMAT:
                return <DiplomatView />;
            case ViewState.AI_ASSISTANT:
                return <AiAssistantView />;
            case ViewState.ANALYTICS:
                return (
                    <div className="h-full flex flex-col items-center justify-center text-slate-500 bg-noise">
                        <Sword className="w-32 h-32 mb-6 opacity-10 text-rarity-epic animate-pulse" />
                        <p className="font-warcraft text-3xl tracking-widest text-slate-400 text-shadow">COMBAT LOG OFFLINE</p>
                        <div className="h-px w-32 bg-gradient-to-r from-transparent via-rarity-epic to-transparent my-4"></div>
                        <p className="font-sans text-sm opacity-50 uppercase tracking-widest text-azeroth-gold">Module requires Level 80</p>
                    </div>
                );
            case ViewState.SETTINGS:
                return (
                    <div className="h-full flex flex-col items-center justify-center text-slate-500 bg-noise">
                        <Settings className="w-32 h-32 mb-6 opacity-10 text-azeroth-gold animate-spin" style={{ animationDuration: '10s' }} />
                        <p className="font-warcraft text-3xl tracking-widest text-slate-400 text-shadow">INTERFACE MENU</p>
                        <div className="h-px w-32 bg-gradient-to-r from-transparent via-azeroth-gold to-transparent my-4"></div>
                        <p className="font-sans text-sm opacity-50 uppercase tracking-widest">Configuration Locked</p>
                    </div>
                );
            default:
                return <DashboardView />;
        }
    };

    const getTheme = (view: ViewState): string => {
        switch (view) {
            case ViewState.GOBLIN:
                return 'theme-cyber';
            case ViewState.DEEPPOCKETS:
                return 'theme-industrial';
            case ViewState.SCOUT:
                return 'theme-druid'; // Mapping Scout to Druid theme for now
            default:
                return 'theme-arcane';
        }
    };

    return (
        <div className={`flex h-screen overflow-hidden text-slate-200 selection:bg-rarity-epic/30 font-sans bg-noise ${getTheme(currentView)} transition-colors duration-500`}>
            {/* Sidebar - "Character Sheet" Style */}
            <aside className="w-80 wow-panel border-r border-black flex flex-col z-30 relative shadow-2xl">
                {/* Unit Frame Profile Header */}
                <div className="p-6 pb-2">
                    <div className="bg-black/40 border border-white/10 rounded-lg p-3 flex items-center space-x-3 shadow-inset relative overflow-hidden group">
                        <div className="relative">
                            {/* Portrait */}
                            <div className="w-14 h-14 rounded-full bg-slate-800 border-2 border-azeroth-gold overflow-hidden relative z-10 box-shadow-glow-gold">
                                <div className="w-full h-full bg-gradient-to-br from-cyan-900 to-blue-900 flex items-center justify-center">
                                    <Bot className="text-white w-8 h-8" />
                                </div>
                            </div>
                            {/* Level Badge */}
                            <div className="absolute -bottom-1 -right-1 z-20 w-6 h-6 bg-black rounded-full border border-azeroth-gold text-azeroth-gold font-bold text-xs flex items-center justify-center">
                                80
                            </div>
                        </div>

                        {/* Stats Bars */}
                        <div className="flex-1 space-y-1">
                            <div className="flex justify-between items-end">
                                <span className="text-sm font-bold font-warcraft tracking-wide text-white text-shadow group-hover:text-azeroth-gold transition-colors">Commander</span>
                                <span className="text-[10px] text-slate-400">100%</span>
                            </div>
                            {/* Health Bar */}
                            <div className="h-3 w-full bg-black/50 rounded-sm border border-white/10 relative overflow-hidden">
                                <div className="absolute inset-0 bg-resource-health w-full bar-gloss"></div>
                            </div>
                            {/* Mana Bar */}
                            <div className="h-3 w-full bg-black/50 rounded-sm border border-white/10 relative overflow-hidden">
                                <div className="absolute inset-0 bg-resource-mana w-[85%] bar-gloss"></div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Decorative Divider */}
                <div className="px-6 py-2">
                    <div className="h-px w-full bg-gradient-to-r from-transparent via-azeroth-gold/50 to-transparent"></div>
                </div>

                {/* Spellbook Navigation */}
                <nav className="flex-1 px-4 space-y-1 overflow-y-auto custom-scrollbar">
                    <p className="px-4 py-2 text-[10px] font-warcraft uppercase tracking-[0.2em] text-slate-500">Grimoire</p>
                    {navItems.map((item) => {
                        const Icon = item.icon;
                        const isActive = currentView === item.id;
                        return (
                            <button
                                key={item.id}
                                onClick={() => setCurrentView(item.id as ViewState)}
                                className={`w-full flex items-center space-x-3 px-3 py-3 rounded border transition-all duration-200 group relative overflow-hidden ${isActive
                                    ? 'bg-gradient-to-r from-azeroth-gold/20 to-transparent border-azeroth-gold/30 text-white'
                                    : 'bg-transparent border-transparent text-slate-400 hover:text-white hover:bg-white/5 hover:border-white/10'
                                    }`}
                            >
                                <div className={`p-1.5 rounded bg-black/50 border ${isActive ? 'border-azeroth-gold text-azeroth-gold shadow-glow-gold' : 'border-slate-700 text-slate-500 group-hover:border-slate-500'}`}>
                                    <Icon className="w-5 h-5" />
                                </div>

                                <span className={`font-medium font-warcraft tracking-wide uppercase text-sm flex-1 text-left ${isActive ? 'text-azeroth-gold text-shadow' : ''}`}>
                                    {item.label}
                                </span>

                                {/* Selection Arrow */}
                                {isActive && <div className="w-2 h-2 bg-azeroth-gold rotate-45 transform translate-x-1"></div>}
                            </button>
                        );
                    })}
                </nav>

                {/* Bottom Panel Status */}
                <div className="p-4 bg-black/40 border-t border-white/10">
                    <div className="flex justify-between items-center text-xs text-slate-500 font-mono">
                        <span>Durability</span>
                        <div className="flex space-x-1">
                            <Shield className="w-4 h-4 text-white" />
                            <span>100%</span>
                        </div>
                    </div>
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 flex flex-col min-w-0 relative">
                {/* Header - "Titan Bar" */}
                <header className="h-16 wow-panel border-b border-black flex items-center justify-between px-6 z-20 backdrop-blur-md relative shadow-lg">
                    <div className="absolute bottom-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-white/10 to-transparent"></div>

                    {/* Breadcrumb / Location Info */}
                    <div className="flex flex-col">
                        <h2 className="text-xl font-bold text-white font-warcraft tracking-[0.1em] uppercase text-shadow-glow">
                            {currentView === ViewState.DASHBOARD ? 'Command Center' :
                                currentView === ViewState.AI_ASSISTANT ? 'Arcane Oracle' :
                                    (currentView as string).replace(/_/g, ' ')}
                        </h2>
                        <div className="flex items-center space-x-2 text-[10px] text-slate-400 font-sans tracking-wide uppercase">
                            <span className="text-azeroth-gold">Khaz Algar</span>
                            <span className="opacity-30">/</span>
                            <span className="text-rarity-epic font-bold">The Coreway</span>
                        </div>
                    </div>

                    <div className="flex items-center space-x-4">
                        <div className="hidden md:flex items-center space-x-2 px-3 py-1 rounded bg-black/40 border border-white/10 shadow-inner">
                            <div className="w-2 h-2 rounded-full bg-resource-health animate-pulse"></div>
                            <span className="text-[10px] font-warcraft tracking-widest text-slate-300">14ms</span>
                        </div>
                        <button className="relative text-slate-400 hover:text-white transition-colors p-2 hover:bg-white/5 rounded group">
                            <Bell className="w-5 h-5 group-hover:animate-swing text-azeroth-gold" />
                            <span className="absolute top-1 right-1 w-2 h-2 bg-rarity-legendary rounded-full shadow-[0_0_5px_#ff8000] animate-pulse"></span>
                        </button>
                    </div>
                </header>

                {/* Scrollable View Area */}
                <div className="flex-1 overflow-auto relative custom-scrollbar p-6">
                    {/* Ambient Background Effects */}
                    <div className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-rarity-epic/5 blur-[100px] pointer-events-none rounded-full animate-pulse-slow" />

                    <div className="relative z-10 max-w-7xl mx-auto pb-10">
                        {renderContent()}
                    </div>
                </div>
            </main>
        </div>
    );
}
