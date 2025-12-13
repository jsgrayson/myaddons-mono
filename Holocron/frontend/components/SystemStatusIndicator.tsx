import React, { useState } from 'react';
import { useSystemStatus } from '../services/system';
import { Activity, Zap, Hexagon, Globe } from './Icons';

export const SystemStatusIndicator = () => {
    const { status, loading } = useSystemStatus();
    const [isOpen, setIsOpen] = useState(false);

    if (loading) return null;

    // Determine overall color
    // Green = All OK
    // Red = Overall NOT OK
    // (Could add Yellow for mixed, but requirements say Green/Red/Yellow logic)
    // Req: "Green dot: all ok", "Yellow: some degraded" (latency?), "Red: one or more down"

    let colorClass = 'bg-resource-health'; // Green
    let pulseClass = '';

    // Count issues
    const services = Object.values(status.services || {});
    const downServices = services.filter(s => !s.ok).length;

    if (!status.ok) {
        if (downServices === services.length && services.length > 0) {
            colorClass = 'bg-red-500'; // All down
            pulseClass = 'animate-pulse';
        } else {
            colorClass = 'bg-yellow-500'; // Some down
        }
    }

    return (
        <div className="relative">
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="flex items-center space-x-2 px-3 py-1.5 rounded bg-black/40 border border-white/10 hover:border-white/30 transition-all group"
            >
                <div className={`w-2 h-2 rounded-full ${colorClass} ${pulseClass}`}></div>
                <span className="text-[10px] font-warcraft tracking-widest text-slate-400 group-hover:text-white transition-colors">
                    SYSTEM
                </span>
            </button>

            {/* Popover */}
            {isOpen && (
                <>
                    <div className="fixed inset-0 z-40" onClick={() => setIsOpen(false)}></div>
                    <div className="absolute right-0 top-full mt-2 w-64 bg-slate-900 border border-white/10 rounded shadow-xl z-50 p-3 animate-in fade-in slide-in-from-top-2">
                        <div className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2 pb-2 border-b border-white/5 flex justify-between">
                            <span>Service Status</span>
                            <Activity className="w-3 h-3" />
                        </div>
                        <div className="space-y-2">
                            {Object.entries(status.services || {}).map(([name, svc]) => (
                                <div key={name} className="flex justify-between items-center text-xs">
                                    <div className="flex items-center space-x-2">
                                        <div className={`w-1.5 h-1.5 rounded-full ${svc.ok ? 'bg-resource-health' : 'bg-red-500'}`}></div>
                                        <span className="capitalize text-slate-300">{name}</span>
                                    </div>
                                    <div className="text-right">
                                        {svc.ok ? (
                                            <span className="font-mono text-slate-500">{svc.latency_ms}ms</span>
                                        ) : (
                                            <span className="text-red-400 text-[10px] max-w-[80px] truncate" title={svc.error || 'Down'}>
                                                {svc.status_code ? `Err ${svc.status_code}` : 'Down'}
                                            </span>
                                        )}
                                    </div>
                                </div>
                            ))}
                            {Object.keys(status.services || {}).length === 0 && (
                                <div className="text-center text-slate-500 text-xs py-2">No services detected</div>
                            )}
                        </div>
                    </div>
                </>
            )}
        </div>
    );
};
