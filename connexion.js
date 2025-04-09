import React, { useState } from 'react';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // Validation de base
    if (!email || !password) {
      setError('Tous les champs doivent être remplis.');
      return;
    }

    if (!validateEmail(email)) {
      setError('L\'email est invalide.');
      return;
    }

    // Appel à l'API de connexion ou toute autre logique
    setError(''); // Réinitialiser l'erreur
    console.log('Connexion réussie', { email, password });
    // Rediriger ou autre action après une connexion réussie
  };

  // Fonction de validation de l'email
  const validateEmail = (email) => {
    const re = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    return re.test(email);
  };

  return (
    <div style={styles.pageContainer}>
      <div style={styles.container}>
        <h2>Veillez vous connectez</h2>
        <form onSubmit={handleSubmit} style={styles.form}>
          <div style={styles.inputGroup}>
            <label htmlFor="email">Email :</label>
            <input
              type="email"
              id="email"
              name="email"
              value={email}
              onChange={handleEmailChange}
              placeholder="Entrez votre email"
              style={styles.input}
            />
          </div>
          <div style={styles.inputGroup}>
            <label htmlFor="password">Mot de passe :</label>
            <input
              type="password"
              id="password"
              name="password"
              value={password}
              onChange={handlePasswordChange}
              placeholder="Entrez votre mot de passe"
              style={styles.input}
            />
          </div>
          {error && <p style={styles.error}>{error}</p>}
          <button type="submit" style={styles.button}>Se connecter</button>
        

        </form>
        <div style={styles.footer}>
          <a href="./inscription.js" style={styles.link}>S'inscrire</a>
          <a href="/forgot-password" style={styles.link}>Mot de passe oublié ?</a>
        </div>
      </div>
    </div>
  );
};

// Styles modifiés
const styles = {
  pageContainer: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    minHeight: '100vh', // Pour centrer verticalement
    backgroundColor: '#f4f4f4', // Une couleur de fond légère pour mieux voir le formulaire
  },
  container: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    padding: '30px',
    borderRadius: '8px',
    border: '1px solid #ccc',
    backgroundColor: '#fff',
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
    width: '650px',
    maxWidth: '650px', // Une largeur maximale pour le formulaire
    margin: '30px', // Marges autour du formulaire
    height: '60vh',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    width: '100%',
  },
  inputGroup: {
    marginBottom: '15px',
  },
  input: {
    width: '90%',
    padding: '20px',
    borderRadius: '4px',
    border: '1px solid #ccc',
    fontSize: '16px',
    margin : '5px 5px 5px 5px',
  },
  button: {
    backgroundColor: '#4CAF50',
    color: '#fff',
    padding: '20px',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '16px',
    marginTop: '10px',
    width: '98%',
  },
  error: {
    color: 'red',
    fontSize: '14px',
    marginBottom: '15px',
  },
  
  footer: {
    display: 'flex',
    justifyContent: 'center',
    width: '100%',
    marginTop: '30px',
  },
  link: {
    color: '#007BFF',
    textDecoration: 'none',
    fontSize: '18px',
    
    marginLeft:'10px',
    marginRight: '50px',
  },
  linkHover: {
    textDecoration: 'underline',
  }

};

export default LoginPage;
