import React from 'react';
import { useNavigate } from 'react-router-dom';

function InscriptionMedecin() {
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault(); // Empêche le rechargement de la page
    // Ajoutez ici la logique d'inscription (vérification des champs, enregistrement, etc.)
    navigate('/connexionm'); // Redirige vers la page de connexion après l'inscription
  };

  return (
    <div className='roboto justify-center'>
      <div className='flex items-center justify-center mt-10 lg:mt-16'>
        <form className="flex flex-col items-center px-2 md:px-4 py-3 xl:py-6" onSubmit={handleSubmit}>
          <input className="border-[#269C26] border-2 p-2 rounded-md w-72 lg:w-96 xl:w-[500px] mb-2" type="text" name="nom" placeholder="Nom" required />
          <input className="border-[#269C26] border-2 p-2 rounded-md w-72 lg:w-96 xl:w-[500px] mb-2" type='text' name="prenoms" placeholder="Prénoms" required />
          <input className="border-[#269C26] border-2 p-2 rounded-md w-72 lg:w-96 xl:w-[500px] mb-2" type="email" name="email" placeholder="Email" required />
          <input className="border-[#269C26] border-2 p-2 rounded-md w-72 lg:w-96 xl:w-[500px] mb-2" type="password" name="pass" placeholder="Mot de passe" required />
          <input className="border-[#269C26] border-2 p-2 rounded-md w-72 lg:w-96 xl:w-[500px] mb-2" type="password" name="passconfirm" placeholder="Confirmez le mot de passe" required />
          <button className="bg-[#269C26] text-white font-bold px-4 xl:px-10 py-2 rounded-lg mt-4" type="submit">
            S'inscrire
          </button>
        </form>
      </div>
    </div>
  );
}

export default InscriptionMedecin;
