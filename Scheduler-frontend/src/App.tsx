import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import AuthInterface from './AuthInterface';
import Dashboard from './dashboard'; // Import your Dashboard component
import './globals.css';

function App() {
  return (
    <Router>
      <>
        <Routes>
          <Route path="/" element={<AuthInterface />} />
        </Routes>
        <Toaster />
      </>
    </Router>
  );
}
export default App;