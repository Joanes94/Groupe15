import React from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation, Link } from 'react-router-dom';
import NavBar from './composants/NavBar.jsx';
import NavBarConn from './composants/NavBarConn.jsx';
import Accueil from './pages/Accueil.jsx';
import DeD from './pages/DeD.jsx';
import InscriptionMedecin from './pages/InscriptionMedecin.jsx';
import ConnexionMedecin from './pages/ConnexionMedecin.jsx';
import AjoutPatient from './pages/AjoutPatient.jsx';
import Dossiers from './composants/Dossiers.jsx';
import Infos from './pages/Infos.jsx';
function App() {
  return (
    <Router>
      <Main />
    </Router>
  );
}

function Main() {
  const location = useLocation();
  console.log(location.pathname);
  
  return (
    <div>
      {location.pathname !== '/' && <NavBarConn />}
      {location.pathname !== '/ded' && <NavBar />}
      
      <Routes>
        <Route path="/" element={<Accueil />} />
        <Route path="/inscriptionm" element={<InscriptionMedecin />} />
        <Route path="/connexionm" element={<ConnexionMedecin />} />
        <Route path="/ded" element={<DeD />} />
        <Route path="/ajoutp" element={<AjoutPatient />} />
        <Route path="/dossiers" element={<Dossiers />} />
        <Route path="/infos" element={<Infos />} />
      </Routes>
    </div>
  );
}

export default App;
