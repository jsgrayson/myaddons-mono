import React from "react";
import { NavLink } from "react-router-dom";
import "./layout.css";

interface LayoutProps {
  children: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="gx-app-shell">
      <aside className="gx-sidebar">
        <div className="gx-sidebar-header">
          <div className="gx-logo-mark">☣</div>
          <div className="gx-sidebar-title-block">
            <div className="gx-sidebar-title">Goblin Exchange</div>
            <div className="gx-sidebar-subtitle">Midnight Cartel</div>
          </div>
        </div>

        <nav className="gx-nav">
          <SidebarLink to="/" label="Dashboard" icon="📊" exact />
          <SidebarLink to="/markets" label="Markets" icon="🏷" />
          <SidebarLink to="/tradeskill" label="TradeSkill Guide" icon="📜" />
          <SidebarLink to="/planner" label="Spec Planner" icon="🧬" />
          <SidebarLink to="/inventory" label="Inventory" icon="📦" />
          <SidebarLink to="/crafting" label="Crafting" icon="🛠" />
          <SidebarLink to="/ledger" label="Ledger" icon="📒" />
        </nav>

        <div className="gx-nav-section-label">System</div>
        <nav className="gx-nav gx-nav-secondary">
          <SidebarLink to="/agents" label="Agents" icon="🤖" />
          <SidebarLink to="/settings" label="Settings" icon="⚙️" />
        </nav>

        <div className="gx-sidebar-footer">
          <span className="gx-sidebar-footnote">
            Skin: <strong>Midnight Cartel</strong>
          </span>
        </div>
      </aside>

      <main className="gx-app-content">{children}</main>
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
      ["gx-nav-link", isActive ? "gx-nav-link-active" : ""]
        .filter(Boolean)
        .join(" ")
    }
  >
    {icon && <span className="gx-nav-link-icon">{icon}</span>}
    <span className="gx-nav-link-label">{label}</span>
  </NavLink>
);
