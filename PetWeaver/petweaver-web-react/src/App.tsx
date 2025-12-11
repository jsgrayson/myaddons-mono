import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';

import { DashboardPage } from './pages/DashboardPage';
import { PetsPage } from './pages/PetsPage';
import { PetDetailsPage } from './pages/PetDetailsPage';
import { SimulatorPage } from './pages/SimulatorPage';
import { OptimizerPage } from './pages/OptimizerPage';
import { EncountersPage } from './pages/EncountersPage';
import { ServerStatusPage } from './pages/ServerStatusPage';
import { LogsPage } from './pages/LogsPage';
import { SettingsPage } from './pages/SettingsPage';

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<DashboardPage />} />
      <Route path="/pets" element={<PetsPage />} />
      <Route path="/pets/:petId" element={<PetDetailsPage />} />
      <Route path="/simulator" element={<SimulatorPage />} />
      <Route path="/optimizer" element={<OptimizerPage />} />
      <Route path="/encounters" element={<EncountersPage />} />
      <Route path="/server" element={<ServerStatusPage />} />
      <Route path="/logs" element={<LogsPage />} />
      <Route path="/settings" element={<SettingsPage />} />
      {/* Legacy alias for optimizer */}
      <Route path="/genetic" element={<OptimizerPage />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
