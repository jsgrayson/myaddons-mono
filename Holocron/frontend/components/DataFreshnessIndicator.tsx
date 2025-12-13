import React from 'react';
import { useSyncStatus } from '../services/sync';
import { Sparkles, AlertTriangle, RefreshCw } from '../components/Icons';

export const DataFreshnessIndicator = () => {
    const { last_synced_at, is_stale, age_seconds, error, loading } = useSyncStatus();
    const [copied, setCopied] = React.useState(false);

    if (loading) return null;
    if (error) return null;

    const formatTimeAgo = (seconds: number) => {
        if (seconds < 60) return 'just now';
        if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
        if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
        return `${Math.floor(seconds / 86400)}d ago`;
    };

    const handleCopyCommand = () => {
        navigator.clipboard.writeText('python3 Holocron/sync_addon_data.py');
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    if (is_stale) {
        return (
            <button
                onClick={handleCopyCommand}
                className="flex items-center space-x-2 px-3 py-1 bg-yellow-500/20 border border-yellow-500/50 rounded text-xs text-yellow-200 hover:bg-yellow-500/30 transition-colors animate-pulse cursor-pointer group"
                title="Click to copy sync command"
            >
                <AlertTriangle className="w-3 h-3 text-yellow-500" />
                <span className="font-mono uppercase tracking-wide">Data Stale</span>
                <span className="hidden md:inline text-yellow-500/50">|</span>
                <span className="hidden md:inline font-mono">
                    {copied ? 'Command Copied!' : 'Click to Copy Sync Command'}
                </span>
            </button>
        );
    }

    // Normal State
    return (
        <div className="flex items-center space-x-2 px-3 py-1 bg-black/40 border border-white/10 rounded text-xs text-slate-400 group hover:border-azeroth-gold/50 transition-colors cursor-help" title={`Last Synced: ${last_synced_at}`}>
            <div className={`w-2 h-2 rounded-full ${age_seconds && age_seconds < 300 ? 'bg-resource-health animate-pulse' : 'bg-slate-600'}`}></div>
            <span className="font-mono">Synced: {age_seconds ? formatTimeAgo(age_seconds) : 'Unknown'}</span>
            <RefreshCw className="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity text-azeroth-gold" />
        </div>
    );
};
