import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";

import { DashboardPage } from "./pages/DashboardPage";
import { MarketsPage } from "./pages/MarketsPage";
import { TradeSkillPage } from "./pages/TradeSkillPage";
import { PlannerPage } from "./pages/PlannerPage";
import { InventoryPage } from "./pages/InventoryPage";
import { CraftingPage } from "./pages/CraftingPage";
import { LedgerPage } from "./pages/LedgerPage";
import { AgentsPage } from "./pages/AgentsPage";
import { SettingsPage } from "./pages/SettingsPage";

const App: React.FC = () => {
  return (
    <Routes>
      <Route path="/" element={<DashboardPage />} />
      <Route path="/markets" element={<MarketsPage />} />
      <Route path="/tradeskill" element={<TradeSkillPage />} />
      <Route path="/planner" element={<PlannerPage />} />
      <Route path="/inventory" element={<InventoryPage />} />
      <Route path="/crafting" element={<CraftingPage />} />
      <Route path="/ledger" element={<LedgerPage />} />
      <Route path="/agents" element={<AgentsPage />} />
      <Route path="/settings" element={<SettingsPage />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
};

export default App;
