import React from "react";
import { NavLink } from "react-router-dom";
import "./layout.css";

interface LayoutProps {
  children: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="sw-app-shell">
      <aside className="sw-sidebar">
        <div className="sw-sidebar-header">
          <div className="sw-logo-mark">✦</div>
          <div className="sw-sidebar-title-block">
            <div className="sw-sidebar-title">SkillWeaver</div>
            <div className="sw-sidebar-subtitle">Midnight Combat</div>
          </div>
        </div>

        <nav className="sw-nav">
          <SidebarLink to="/" label="Dashboard" icon="📊" exact />
          <SidebarLink to="/builds" label="Builds" icon="🌌" />
          <SidebarLink to="/rotation" label="Rotation" icon="🔁" />
          <SidebarLink to="/macros" label="Macros" icon="⌨️" />
          <SidebarLink to="/encounters" label="Encounters" icon="⚔️" />
          <SidebarLink to="/analytics" label="Analytics" icon="📈" />
        </nav>

        <div className="sw-nav-section-label">System</div>
        <nav className="sw-nav sw-nav-secondary">
          <SidebarLink to="/settings" label="Settings" icon="⚙️" />
        </nav>

        <div className="sw-sidebar-footer">
          <span className="sw-sidebar-footnote">
            Integration: <strong>Addon Sync (GSE)</strong>
          </span>
        </div>
      </aside>

      <main className="sw-app-content">{children}</main>
    </div>
  );
};

interface SidebarLinkProps {
  to: string;
  label: string;
  icon?: string;
  exact?: boolean;
}

const SidebarLink: React.FC<SidebarLinkProps> = ({
  to,
  label,
  icon,
  exact,
}) => (
  <NavLink
    to={to}
    end={!!exact}
    className={({ isActive }) =>
      ["sw-nav-link", isActive ? "sw-nav-link-active" : ""]
        .filter(Boolean)
        .join(" ")
    }
  >
    {icon && <span className="sw-nav-link-icon">{icon}</span>}
    <span className="sw-nav-link-label">{label}</span>
  </NavLink>
);
