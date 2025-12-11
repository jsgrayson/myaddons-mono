import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { DashboardPage } from "./pages/DashboardPage";
import { BuildsPage } from "./pages/BuildsPage";
import { RotationPage } from "./pages/RotationPage";
import { MacrosPage } from "./pages/MacrosPage";
import { EncountersPage } from "./pages/EncountersPage";
import { AnalyticsPage } from "./pages/AnalyticsPage";
import { SettingsPage } from "./pages/SettingsPage";

const App: React.FC = () => {
  return (
    <Routes>
      <Route path="/" element={<DashboardPage />} />
      <Route path="/builds" element={<BuildsPage />} />
      <Route path="/rotation" element={<RotationPage />} />
      <Route path="/macros" element={<MacrosPage />} />
      <Route path="/encounters" element={<EncountersPage />} />
      <Route path="/analytics" element={<AnalyticsPage />} />
      <Route path="/settings" element={<SettingsPage />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
};

export default App;
