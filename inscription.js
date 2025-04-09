import React, { useState } from 'react';
import './inscription.css';
const Inscription = ({ onSubmit }) => {
  const [formData, setFormData] = useState({
    nom: '',
    prenom: '',
    nomUtilisateur: '',
    email: '',
    motDePasse: '',
    confirmotDePasse: '',
  });

  const [error, setError] = useState('');

  // A propos de la saisie dans le formulaire
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  // A propos de l'envoi du formulaire
  const handleSubmit = (e) => {
    e.preventDefault();
    const { nom, prenom, nomUtilisateur, email, motDePasse,confirmotDePasse } = formData;

    //  vérifier que les champs sont remplis
    if (!nom || !prenom || !nomUtilisateur || !email || !motDePasse || !confirmotDePasse) {
      setError('Tous les champs sont obligatoires.');
      return;
    }

    setError('');
    
    onSubmit(formData);
  };

  return (
    <div className="container">
      <h2>Inscription Médecin</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="nom">Nom</label>
          <input
            type="text"
            id="nom"
            name="nom"
            value={formData.nom}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="prenom">Prénom</label>
          <input
            type="text"
            id="prenom"
            name="prenom"
            value={formData.prenom}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="motDePasse">Mot de passe</label>
          <input
            type="password"
            id="motDePasse"
            name="motDePasse"
            value={formData.motDePasse}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="confirmotDePasse"> Confirmation du Mot de passe</label>
          <input
            type="password"
            id="confirmotDePasse"
            name="confirmotDePasse"
            value={formData.confirmotDePasse}
            onChange={handleChange}
            required
          />
        </div>

        {error && <p className="error-message">{error}</p>}

        <button type="submit">S'inscrire</button>
      </form>
      <div>
          <a href="./connexion.js">Deja Inscris?</a>
        </div>
    </div>
  );
};

export default Inscription;