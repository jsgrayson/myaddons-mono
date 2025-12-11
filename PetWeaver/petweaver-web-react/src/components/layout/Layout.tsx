import React from 'react';
import { NavLink } from 'react-router-dom';
import './layout.css';

const navLinks = [
  { to: '/', label: 'Dashboard', icon: '🏠', exact: true },
  { to: '/pets', label: 'Pet Codex', icon: '📚' },
  { to: '/simulator', label: 'Simulator', icon: '🧪' },
  { to: '/optimizer', label: 'Optimizer', icon: '🧬' },
  { to: '/encounters', label: 'Encounters', icon: '⚔️' },
];

const navLinksServer = [
  { to: '/server', label: 'Server Status', icon: '🛰' },
  { to: '/logs', label: 'Logs', icon: '📜' },
  { to: '/settings', label: 'Settings', icon: '⚙️' },
];

const SidebarLink: React.FC<{ to: string; label: string; icon?: string; exact?: boolean }> = ({
  to,
  label,
  icon,
  exact,
}) => (
  <NavLink
    to={to}
    end={exact}
    className={({ isActive }) =>
      ['app-nav-link', isActive ? 'app-nav-link-active' : ''].filter(Boolean).join(' ')
    }
  >
    {icon && <span className="app-nav-link-icon">{icon}</span>}
    <span className="app-nav-link-label">{label}</span>
  </NavLink>
);

export const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <div className="app-shell">
      <aside className="app-sidebar">
        <div className="app-sidebar-header">
          <div className="app-sidebar-title">PetWeaver</div>
          <div className="app-sidebar-subtitle">Midnight shard</div>
        </div>

        <nav className="app-nav">
          {navLinks.map((link) => (
            <SidebarLink key={link.to} {...link} />
          ))}
        </nav>

        <div className="app-nav-section-label">Server</div>
        <nav className="app-nav app-nav-secondary">
          {navLinksServer.map((link) => (
            <SidebarLink key={link.to} {...link} />
          ))}
        </nav>

        <div className="app-sidebar-footer">
          <span className="app-sidebar-footnote">
            Skin: <strong>Midnight</strong>
          </span>
        </div>
      </aside>

      <main className="app-content">{children}</main>
    </div>
  );
};
