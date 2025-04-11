import React from 'react';
import { useNavigate } from 'react-router-dom';

 function AjoutPatient() {
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault(); // Empêche le rechargement de la page
    // Ajoutez ici la logique d'ajout du patient (vérification des champs, enregistrement, etc.)
    navigate('/ded'); // Redirige vers la page de connexion après l'ajout
  };

  return (
    <div className='roboto justify-center'>
      <div className='flex items-center justify-center mt-10 lg:mt-16'>
        <form className="flex flex-col items-center px-2 md:px-4 py-3 xl:py-6" onSubmit={handleSubmit}>
          <input className="border-[#269C26] border-2 p-2 rounded-md w-72 lg:w-96 xl:w-[500px] mb-2" type="text" name="nom" placeholder="Nom" required />
          <input className="border-[#269C26] border-2 p-2 rounded-md w-72 lg:w-96 xl:w-[500px] mb-2" type='text' name="prenoms" placeholder="Prénoms" required />
          <input className="border-[#269C26] border-2 p-2 rounded-md w-72 lg:w-96 xl:w-[500px] mb-2" type="date" name="date" placeholder="Date de naissance" required />
          <input className="border-[#269C26] border-2 p-2 rounded-md w-72 lg:w-96 xl:w-[500px] mb-2" type="" name="sexe" placeholder="Sexe" required />
          <input className="border-[#269C26] border-2 p-2 rounded-md w-72 lg:w-96 xl:w-[500px] mb-2" type="text" name="contact" placeholder="Contact" required />
          <input className="border-[#269C26] border-2 p-2 rounded-md w-72 lg:w-96 xl:w-[500px] mb-2" type="text" name="adresse" placeholder="Adresse" required />
          <input className="border-[#269C26] border-2 p-2 rounded-md w-72 lg:w-96 xl:w-[500px] mb-2" type="text" name="antecedents" placeholder="Antécédents médicaux" required />
          <input className="border-[#269C26] border-2 p-2 rounded-md w-72 lg:w-96 xl:w-[500px] mb-2" type="text" name="traitement" placeholder="Traitement(s) en cours" required />
          <input className="border-[#269C26] border-2 p-2 rounded-md w-72 lg:w-96 xl:w-[500px] mb-2" type="text" name="prescriptions" placeholder="Prescriptions" required />
          <input className="border-[#269C26] border-2 p-2 rounded-md w-72 lg:w-96 xl:w-[500px] mb-2" type="text" name="ref" placeholder="Nom du médecin référent" required />
          <input className="border-[#269C26] border-2 p-2 rounded-md w-72 lg:w-96 xl:w-[500px] mb-2" type="text" name="contactref" placeholder="Contact du médecin référent" required />
          <button className="bg-[#269C26] text-white font-bold px-4 xl:px-10 py-2 rounded-lg mt-4" type="submit">
            Enregistrer
          </button>
        </form>
      </div>
    </div>
  );
}

export default AjoutPatient;
