import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import AuthInterface from './AuthInterface'; //import auth interface component
import Dashboard from './dashboard'; // Import Dashboard component
import './globals.css';

function App() {
  return (
    <Router>
      <>
        <Routes>
          <Route path="/" element={
            <ConditionalRoute>
              <AuthInterface />
            </ConditionalRoute>
          } />
          <Route 
            path="/dashboard" 
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            } 
          />
        </Routes>
        <Toaster />
      </>
    </Router>
  );
}

function ConditionalRoute({ children }: { children: React.ReactNode }) {
  const token = localStorage.getItem('token');
  if (token) {
    return <Navigate to="/dashboard" replace />;
  }
  return children;
}

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const token = localStorage.getItem('token');
  if (!token) {
    return <Navigate to="/" replace />;
  }
  return children;
}

export default App;

