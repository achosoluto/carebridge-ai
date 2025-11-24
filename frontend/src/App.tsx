import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Messages from './pages/Messages'
import Appointments from './pages/Appointments'
import Monitoring from './pages/Monitoring'
import PatientDetails from './pages/PatientDetails'

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Navigate to="/staff/dashboard" replace />} />
        <Route path="/staff/dashboard" element={<Dashboard />} />
        <Route path="/staff/messages" element={<Messages />} />
        <Route path="/staff/messages/:patientId" element={<PatientDetails />} />
        <Route path="/staff/appointments" element={<Appointments />} />
        <Route path="/staff/monitoring" element={<Monitoring />} />
      </Routes>
    </Layout>
  );
}

export default App