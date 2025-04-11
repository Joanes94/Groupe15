import React from 'react';
import ButtonRecherche from './ButtonRecherche';
import { FaPlus } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom';
function Dossiers() {
  const navigate = useNavigate();

  const handleAddPatient = () => {
    navigate('/ajoutp'); // Redirige vers la page d'ajout d'un patient
  };

  return (
    <div className='justify-center mx-10 flex flex-col'>
      <div className='justify-between flex flex-wrap space-y-4 items-center mx-5 mt-8'>
        <div className='flex items-center gap-x-2 lg:gap-x-4'>
          <h1>Ajouter un patient</h1>
          <button onClick={handleAddPatient}>
            <FaPlus color='#269C26' size={20} />
          </button>
        </div>
        <ButtonRecherche />
      </div>
      <div className='justify-center flex flex-wrap gap-8 xl:gap-x-24 mt-8 lg:mt-12 xl:mt-16'>
        <div className='justify-center flex flex-col border-2 rounded-lg border-[#269C26] p-4 bg-[#fdfffd]'>
          <div className='space-y-2 roboto'>
            <h1><strong>Nom:</strong>AMAGBEGNON</h1>
            <h1><strong>Prénoms:</strong>Rosmé</h1>
            <h1><strong>Date de naissance:</strong>03/09/2005</h1>
            <h1><strong>Sexe:</strong>F</h1>
          </div>
          <button className='roboto font-bold text-lg text-white bg-[#269C26] px-6 py-1 rounded-2xl mt-8'>
            <Link to="/infos">VoirPlus</Link>
          </button>
        </div>
      </div>
    </div>
  );
}

export default Dossiers;
