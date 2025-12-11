import { Routes, Route, Navigate } from 'react-router-dom';
import { Layout } from './components/layout/Layout';
import { DashboardPage } from './pages/DashboardPage';
import { PetsPage } from './pages/PetsPage';
import { PetDetailsPage } from './pages/PetDetailsPage';
import { SimulatorPage } from './pages/SimulatorPage';
import { GeneticPage } from './pages/GeneticPage';
import { EncountersPage } from './pages/EncountersPage';
import { ServerStatusPage } from './pages/ServerStatusPage';
import { LogsPage } from './pages/LogsPage';
import { SettingsPage } from './pages/SettingsPage';

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/pets" element={<PetsPage />} />
        <Route path="/pets/:id" element={<PetDetailsPage />} />
        <Route path="/simulator" element={<SimulatorPage />} />
        <Route path="/genetic" element={<GeneticPage />} />
        <Route path="/encounters" element={<EncountersPage />} />
        <Route path="/server" element={<ServerStatusPage />} />
        <Route path="/logs" element={<LogsPage />} />
        <Route path="/settings" element={<SettingsPage />} />
      </Routes>
    </Layout>
  );
}
