import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import NavBar from './composants/NavBar.jsx';
import Accueil from './pages/Accueil.jsx';

function App() {
  return (
    <Router>
      <div>
        <NavBar />
        <Routes>
          <Route path="/" element={<Accueil />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;