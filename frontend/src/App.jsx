import React from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import NavBar from './composants/NavBar.jsx';
import NavBarConn from './composants/NavBarConn.jsx';
import Accueil from './pages/Accueil.jsx';
import DeD from './pages/DeD.jsx';

function App() {
  return (
    <Router>
      <Main />
    </Router>
  );
}

function Main() {
  const location = useLocation();
  
  return (
    <div>
      {location.pathname !== '/' && <NavBarConn />}
      {location.pathname !== '/ded' && <NavBar />}
      <Routes>
        <Route path="/" element={<Accueil />} />
        <Route path="/ded" element={<DeD />} />
      </Routes>
    </div>
  );
}

export default App;
