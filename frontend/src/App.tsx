import { Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Messages from './pages/Messages'
import Appointments from './pages/Appointments'
import Monitoring from './pages/Monitoring'
import PatientDetails from './pages/PatientDetails'
import PatientMessages from './pages/PatientMessages'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/staff/dashboard" replace />} />

      {/* Staff Routes with Layout */}
      <Route path="/staff/*" element={<Layout><StaffRoutes /></Layout>} />

      {/* Patient Routes (No Layout) */}
      <Route path="/patient/messages" element={<PatientMessages />} />

      <Route path="*" element={<Navigate to="/staff/dashboard" replace />} />
    </Routes>
  )
}

function StaffRoutes() {
  return (
    <Routes>
      <Route path="dashboard" element={<Dashboard />} />
      <Route path="messages" element={<Messages />} />
      <Route path="messages/:patientId" element={<PatientDetails />} />
      <Route path="appointments" element={<Appointments />} />
      <Route path="monitoring" element={<Monitoring />} />
    </Routes>
  )
}

export default App