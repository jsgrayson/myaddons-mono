import React from 'react';

export function GearOptimizer() {
    return (
        <>
            <style>
                {`
          :root {
            --midnight-bg: #0A0A0B;
            --teal-accent: #2DD4BF;
            --border-dim: #2A2A2A;
            --glass-panel: rgba(15, 15, 18, 0.85);
          }

          .stat-topology-container {
              display: grid;
              grid-template-columns: 1fr 350px;
              gap: 20px;
              background: var(--midnight-bg);
              color: #FFF;
              font-family: 'JetBrains Mono', monospace;
              padding: 20px;
              height: 100vh;
              overflow: hidden;
          }

          .module-card {
              background: var(--glass-panel);
              border: 1px solid var(--border-dim);
              border-radius: 4px;
              position: relative;
              overflow: hidden;
          }

          .module-card::before {
              content: "";
              position: absolute;
              top: 0; left: 0;
              width: 100%; height: 2px;
              background: var(--teal-accent);
          }

          .stat-radar {
              width: 100%;
              height: 400px;
              background: url('placeholder-radar-asset.png') center no-repeat;
              background-size: contain;
          }

          .solver-list {
              list-style: none;
              padding: 0;
              font-size: 12px;
          }

          .solver-item {
              padding: 10px;
              border-bottom: 1px solid var(--border-dim);
              display: flex;
              justify-content: space-between;
          }
        `}
            </style>

            <div className="stat-topology-container">
                <div className="module-card" id="topology-lab">
                    <header style={{ padding: '15px' }}>
                        <span style={{ color: 'var(--teal-accent)' }}>[01]</span> STAT_TOPOLOGY_LAB
                    </header>
                    <div className="stat-radar"></div>
                </div>

                <div className="module-card" id="best-in-bags">
                    <header style={{ padding: '15px' }}>
                        <span style={{ color: 'var(--teal-accent)' }}>[02]</span> BEST_IN_BAGS_SOLVER
                    </header>
                    <div className="solver-list">
                        <div className="solver-item"><span>PRIMARY_SPEC</span> <span style={{ color: 'var(--teal-accent)' }}>RET_PALADIN</span></div>
                        <div className="solver-item"><span>CURRENT_ILVL</span> <span>639.2</span></div>
                        <div className="solver-item"><span>OPTIMIZATION</span> <span style={{ color: '#FBBF24' }}>BURST_WINDOW</span></div>
                    </div>
                </div>
            </div>
        </>
    );
}
