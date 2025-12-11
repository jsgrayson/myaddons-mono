import React, { useState, useEffect } from 'react';
import { Bell } from './Icons';

export default function ScoutView() {
    const [alerts, setAlerts] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch('/api/scout/alerts')
            .then(res => res.json())
            .then(data => {
                setAlerts(data.alerts || []);
                setLoading(false);
            })
            .catch(err => {
                console.error('Failed to fetch alerts:', err);
                setLoading(false);
            });
    }, []);

    if (loading) {
        return (
            <div className="flex items-center justify-center h-full">
                <div className="text-center">
                    <Bell className="w-16 h-16 text-rarity-legendary animate-pulse mx-auto mb-4" />
                    <p className="text-slate-400 font-warcraft">Loading Alerts...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            <div className="wow-panel p-6 rounded border border-rarity-legendary/30 shadow-glow-gold bg-noise">
                <h1 className="text-3xl font-bold text-white font-warcraft tracking-widest mb-2 text-shadow-glow">
                    SCOUT ALERTS
                </h1>
                <p className="text-slate-400">Time-Sensitive Notifications & Opportunities</p>
            </div>

            <div className="space-y-4">
                {alerts.length > 0 ? (
                    alerts.map((alert, idx) => (
                        <div key={idx} className="wow-card p-4 rounded border border-rarity-legendary/20 bg-noise">
                            <h3 className="font-warcraft text-white mb-2">{alert.title}</h3>
                            <p className="text-sm text-slate-400">{alert.message}</p>
                        </div>
                    ))
                ) : (
                    <div className="wow-card p-6 rounded border border-white/10 bg-noise text-center">
                        <Bell className="w-16 h-16 mx-auto mb-3 text-slate-600" />
                        <p className="text-slate-500">No active alerts</p>
                    </div>
                )}
            </div>
        </div>
    );
}
