import { useState, useEffect } from 'react';

export interface SyncStatus {
    last_synced_at: string | null;
    is_stale: boolean;
    age_seconds?: number;
    stale_after_seconds?: number;
    source?: string;
    loading: boolean;
    error: string | null;
}

export const useSyncStatus = () => {
    const [status, setStatus] = useState<SyncStatus>({
        last_synced_at: null,
        is_stale: false,
        loading: true,
        error: null
    });

    const fetchStatus = async () => {
        try {
            const response = await fetch('/api/v1/system/sync_status');
            if (!response.ok) {
                throw new Error('Failed to fetch sync status');
            }
            const data = await response.json();
            setStatus({
                ...data,
                loading: false,
                error: null
            });
        } catch (err) {
            console.error(err);
            setStatus(prev => ({
                ...prev,
                loading: false,
                error: 'Unable to check data freshness'
            }));
        }
    };

    useEffect(() => {
        // Initial fetch
        fetchStatus();

        // Poll every 60 seconds
        const interval = setInterval(fetchStatus, 60000);

        // Refetch on tab focus
        const handleFocus = () => fetchStatus();
        window.addEventListener('focus', handleFocus);

        return () => {
            clearInterval(interval);
            window.removeEventListener('focus', handleFocus);
        };
    }, []);

    return status;
};
