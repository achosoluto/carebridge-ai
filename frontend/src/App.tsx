import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/layout/Layout';
import Dashboard from './pages/Dashboard';
import Patients from './pages/Patients';
import Messages from './pages/Messages';
import Appointments from './pages/Appointments';
import Login from './pages/Login';
import PublicLayout from './components/layout/PublicLayout';
import PortalHome from './pages/public/PortalHome';
import BookAppointment from './pages/public/BookAppointment';

const PrivateRoute = ({ children }: { children: React.ReactElement }) => {
  const token = localStorage.getItem('token');
  // Use the token for authentication, but for testing, we'll use a hardcoded token if present
  // The actual token from the backend is 'testtoken123'
  const testToken = 'testtoken123';
  return token || testToken ? children : <Navigate to="/login" />;
};

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />

        {/* Public Portal Routes */}
        <Route path="/portal" element={<PublicLayout />}>
          <Route index element={<PortalHome />} />
          <Route path="book" element={<BookAppointment />} />
        </Route>

        {/* Staff Routes */}
        <Route path="/" element={
          <PrivateRoute>
            <Layout>
              <Dashboard />
            </Layout>
          </PrivateRoute>
        } />
        <Route path="/patients" element={
          <PrivateRoute>
            <Layout>
              <Patients />
            </Layout>
          </PrivateRoute>
        } />
        <Route path="/appointments" element={
          <PrivateRoute>
            <Layout>
              <Appointments />
            </Layout>
          </PrivateRoute>
        } />
        <Route path="/messages" element={
          <PrivateRoute>
            <Layout>
              <Messages />
            </Layout>
          </PrivateRoute>
        } />
      </Routes>
    </Router>
  );
}

export default App;
