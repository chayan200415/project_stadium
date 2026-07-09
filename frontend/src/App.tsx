import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Layout } from './components/Layout';
import Dashboard from './pages/Dashboard';
import Chat from './pages/Chat';
import Navigation from './pages/Navigation';
import Crowd from './pages/Crowd';
import Operations from './pages/Operations';
import Transport from './pages/Transport';
import Sustainability from './pages/Sustainability';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="chat" element={<Chat />} />
          <Route path="navigation" element={<Navigation />} />
          <Route path="crowd" element={<Crowd />} />
          <Route path="operations" element={<Operations />} />
          <Route path="transport" element={<Transport />} />
          <Route path="sustainability" element={<Sustainability />} />
          <Route path="settings" element={<div className="p-6">Settings Page</div>} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
