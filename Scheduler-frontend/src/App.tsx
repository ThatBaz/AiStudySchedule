import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import AuthInterface from './AuthInterface'; //import auth interface component
import Dashboard from './dashboard'; // Import Dashboard component
import './globals.css';

function App() {
  return (
    <Router>
      {/* Main content container */}
        <Routes>
        <Route path="/">
          <ConditionalRoute>
            <AuthInterface /> {/* Render AuthInterface only if not authenticated */}
            </ConditionalRoute>
       </Route>
        <Route path="/dashboard">
          <ProtectedRoute>
            <Dashboard /> {/* Render Dashboard only if authenticated */}
          </ProtectedRoute>
        </Route>
        </Routes>

        <Toaster />
    </Router>
  );
}

function ConditionalRoute({ children }: { children: React.ReactNode }) {
  const token = localStorage.getItem('token');
  
  if (token) {
    return <Navigate to="/dashboard" replace />;
  }
  
  // If no token, render child components (AuthInterface)
  return children;
}

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const token = localStorage.getItem('token');
  
  if (!token) {
    return <Navigate to="/" replace />;
  }
  
  // If token exists, render child components (Dashboard)
  return children;
}

export default App;

