import { useState, useEffect } from 'react';

export interface ServiceStatus {
    ok: boolean;
    latency_ms?: number;
    error?: string;
    status_code?: number;
}

export interface SystemStatus {
    ok: boolean;
    services: Record<string, ServiceStatus>;
}

export const useSystemStatus = () => {
    const [status, setStatus] = useState<SystemStatus>({ ok: true, services: {} });
    const [loading, setLoading] = useState(true);
    const [lastChecked, setLastChecked] = useState<Date | null>(null);

    const checkSystem = async () => {
        try {
            const response = await fetch('/readyz');
            const data = await response.json();
            setStatus(data);
        } catch (err) {
            console.error('System check failed:', err);
            setStatus({ ok: false, services: {} });
        } finally {
            setLoading(false);
            setLastChecked(new Date());
        }
    };

    useEffect(() => {
        checkSystem();
        const interval = setInterval(checkSystem, 30000); // 30s poll

        const handleFocus = () => checkSystem();
        window.addEventListener('focus', handleFocus);

        return () => {
            clearInterval(interval);
            window.removeEventListener('focus', handleFocus);
        };
    }, []);

    return { status, loading, lastChecked };
};
