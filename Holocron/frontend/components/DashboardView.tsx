import React, { useState, useEffect } from 'react';
import { WIDGET_REGISTRY, DEFAULT_LAYOUT, getWidget, getAvailableWidgets, WidgetConfig } from './widgets/WidgetRegistry';
import { Settings } from './Icons';

// ========================================
// STORAGE
// ========================================
const STORAGE_KEY = 'holocron-dashboard-layout';

const loadLayout = (): string[] => {
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      const parsed = JSON.parse(saved);
      if (Array.isArray(parsed) && parsed.every(id => WIDGET_REGISTRY[id])) {
        return parsed;
      }
    }
  } catch (e) {
    console.warn('Failed to load dashboard layout:', e);
  }
  return DEFAULT_LAYOUT;
};

const saveLayout = (layout: string[]) => {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(layout));
};

// ========================================
// WIDGET PICKER MODAL
// ========================================
const WidgetPicker = ({
  available,
  onSelect,
  onClose
}: {
  available: WidgetConfig[],
  onSelect: (id: string) => void,
  onClose: () => void
}) => (
  <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50" onClick={onClose}>
    <div className="bg-slate-900/90 border border-white/10 rounded-2xl p-6 max-w-md w-full mx-4 shadow-2xl" onClick={e => e.stopPropagation()}>
      <h3 className="text-xl font-bold text-white mb-4">Add Widget</h3>
      {available.length === 0 ? (
        <p className="text-slate-400 text-sm">All widgets are already on your dashboard.</p>
      ) : (
        <div className="space-y-2">
          {available.map(widget => {
            const Icon = widget.icon;
            return (
              <button
                key={widget.id}
                onClick={() => onSelect(widget.id)}
                className="w-full flex items-center space-x-4 p-4 rounded-xl bg-white/5 hover:bg-white/10 border border-white/5 hover:border-cyan-500/30 transition-all group"
              >
                <div className="w-10 h-10 rounded-lg bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center">
                  <Icon className="w-5 h-5 text-cyan-400" />
                </div>
                <div className="text-left flex-1">
                  <p className="text-white font-medium group-hover:text-cyan-400 transition-colors">{widget.name}</p>
                  <p className="text-xs text-slate-500">{widget.description}</p>
                </div>
              </button>
            );
          })}
        </div>
      )}
      <button onClick={onClose} className="mt-4 w-full py-2 text-sm text-slate-400 hover:text-white transition-colors">
        Cancel
      </button>
    </div>
  </div>
);

// ========================================
// WIDGET WRAPPER (with remove button)
// ========================================
const WidgetWrapper = ({
  widget,
  editMode,
  onRemove
}: {
  widget: WidgetConfig,
  editMode: boolean,
  onRemove: () => void
}) => {
  const Component = widget.component;
  const sizeClasses = {
    small: 'col-span-1',
    medium: 'col-span-2',
    large: 'col-span-3',
    full: 'col-span-full',
  };

  return (
    <div className={`relative ${sizeClasses[widget.defaultSize]} ${editMode ? 'ring-2 ring-cyan-500/30 ring-offset-2 ring-offset-transparent rounded-2xl' : ''}`}>
      {editMode && (
        <button
          onClick={onRemove}
          className="absolute -top-2 -right-2 z-20 w-6 h-6 rounded-full bg-red-500 text-white flex items-center justify-center text-xs font-bold shadow-lg hover:bg-red-400 transition-colors"
        >
          ×
        </button>
      )}
      <Component />
    </div>
  );
};

// ========================================
// MAIN DASHBOARD
// ========================================
export default function DashboardView() {
  const [layout, setLayout] = useState<string[]>(loadLayout);
  const [editMode, setEditMode] = useState(false);
  const [showPicker, setShowPicker] = useState(false);

  useEffect(() => {
    saveLayout(layout);
  }, [layout]);

  const handleAddWidget = (id: string) => {
    setLayout(prev => [...prev, id]);
    setShowPicker(false);
  };

  const handleRemoveWidget = (id: string) => {
    setLayout(prev => prev.filter(wid => wid !== id));
  };

  const availableWidgets = getAvailableWidgets(layout);

  return (
    <div className="h-full relative overflow-auto p-8">
      {/* Background effects */}
      <div className="fixed inset-0 bg-gradient-to-b from-violet-900/10 via-transparent to-cyan-900/10 pointer-events-none" />
      <div className="fixed top-0 left-1/2 -translate-x-1/2 w-[800px] h-[400px] bg-violet-500/5 rounded-full blur-[100px] pointer-events-none" />

      {/* Edit mode toggle */}
      <div className="relative z-10 flex justify-end mb-6">
        <button
          onClick={() => setEditMode(!editMode)}
          className={`flex items-center space-x-2 px-4 py-2 rounded-lg border transition-all ${editMode
              ? 'bg-cyan-500/20 border-cyan-500/50 text-cyan-400'
              : 'bg-white/5 border-white/10 text-slate-400 hover:text-white hover:border-white/20'
            }`}
        >
          <Settings className="w-4 h-4" />
          <span className="text-sm font-medium">{editMode ? 'Done Editing' : 'Edit Dashboard'}</span>
        </button>
      </div>

      {/* Widget grid */}
      <div className="relative z-10 grid grid-cols-1 md:grid-cols-3 gap-6">
        {layout.map(widgetId => {
          const widget = getWidget(widgetId);
          if (!widget) return null;
          return (
            <WidgetWrapper
              key={widgetId}
              widget={widget}
              editMode={editMode}
              onRemove={() => handleRemoveWidget(widgetId)}
            />
          );
        })}

        {/* Add widget button (visible in edit mode) */}
        {editMode && availableWidgets.length > 0 && (
          <button
            onClick={() => setShowPicker(true)}
            className="col-span-1 h-48 rounded-2xl border-2 border-dashed border-white/10 hover:border-cyan-500/30 flex flex-col items-center justify-center text-slate-500 hover:text-cyan-400 transition-all group"
          >
            <span className="text-4xl mb-2 group-hover:scale-110 transition-transform">+</span>
            <span className="text-sm font-medium">Add Widget</span>
          </button>
        )}
      </div>

      {/* Widget picker modal */}
      {showPicker && (
        <WidgetPicker
          available={availableWidgets}
          onSelect={handleAddWidget}
          onClose={() => setShowPicker(false)}
        />
      )}
    </div>
  );
}
