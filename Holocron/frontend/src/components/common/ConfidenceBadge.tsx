import React, { useEffect, useState } from 'react';
import { Activity, AlertTriangle, CheckCircle, XCircle } from 'lucide-react';


interface Reason {
    code: string;
    message: string;
}

interface StatusEntry {
    status: 'OK' | 'WARN' | 'FAIL';
    reasons?: Reason[];
    timestamp?: string;
}

interface ExpandedStatus {
    overall: 'OK' | 'WARN' | 'FAIL';
    characters: Record<string, {
        overall: 'OK' | 'WARN' | 'FAIL',
        addons: Record<string, StatusEntry>
    }>;
}

export const ConfidenceBadge: React.FC = () => {
    const [data, setData] = useState<ExpandedStatus | null>(null);
    const [error, setError] = useState(false);

    useEffect(() => {
        const fetchStatus = () => {
            fetch('/api/v1/sanity/status')
                .then(res => res.json())
                .then((resp: ExpandedStatus) => {
                    setData(resp);
                    setError(false);
                })
                .catch(() => setError(true));
        };

        fetchStatus();
        const timer = setInterval(fetchStatus, 60000);
        return () => clearInterval(timer);
    }, []);

    let overallState: 'OK' | 'WARN' | 'FAIL' = data?.overall || 'OK';
    if (error) overallState = 'WARN';

    // Collect Issues
    const issues: string[] = [];
    if (data?.characters) {
        Object.entries(data.characters).forEach(([charName, charState]) => {
            Object.entries(charState.addons).forEach(([addon, report]) => {
                if (report.status !== 'OK') {
                    const icon = report.status === 'FAIL' ? '❌' : '⚠️';

                    // Handle structured reasons
                    if (report.reasons && report.reasons.length > 0) {
                        report.reasons.forEach(r => {
                            issues.push(`${icon} ${charName}/${addon} (${r.message})`);
                        });
                    } else {
                        // Fallback if no reasons but status is bad
                        issues.push(`${icon} ${charName}/${addon} (Unknown Issue)`);
                    }
                }
            });
        });
    }

    // Sort issues: FAIL first
    issues.sort((a, b) => (a.startsWith('❌') ? -1 : 1));

    const colors = {
        'OK': 'text-emerald-400 bg-emerald-400/10 border-emerald-400/20',
        'WARN': 'text-amber-400 bg-amber-400/10 border-amber-400/20',
        'FAIL': 'text-red-500 bg-red-500/10 border-red-500/20',
    };

    const label = overallState === 'OK' ? 'Verified' : overallState === 'FAIL' ? 'Data Error' : 'Warning';

    return (
        <div className={`flex items-center gap-2 px-3 py-1 rounded-full border ${colors[overallState]} transition-colors duration-300 group relative cursor-help`}>
            {overallState === 'OK' && <CheckCircle size={14} />}
            {overallState === 'WARN' && <AlertTriangle size={14} />}
            {overallState === 'FAIL' && <XCircle size={14} />}

            <span className="text-xs font-medium tracking-tight uppercase">{label}</span>

            {/* Tooltip */}
            {(issues.length > 0 || error) && (
                <div className="absolute top-full mt-2 right-0 w-64 p-3 rounded bg-gray-950 border border-white/10 shadow-xl opacity-0 group-hover:opacity-100 transition-opacity z-50 pointer-events-none">
                    <div className="text-[10px] text-gray-500 mb-2 uppercase tracking-wider font-semibold">Confidence Report</div>

                    {error && <div className="text-xs text-amber-500 mb-1">⚠️ API Connection Failed</div>}

                    {issues.map((issue, i) => (
                        <div key={i} className="text-xs text-white/90 mb-1.5 leading-snug break-words">
                            {issue}
                        </div>
                    ))}
                    <div className="mt-2 pt-2 border-t border-white/5 text-[10px] text-gray-600 italic">
                        Run /sanity in-game to update.
                    </div>
                </div>
            )}
        </div>
    );
};
