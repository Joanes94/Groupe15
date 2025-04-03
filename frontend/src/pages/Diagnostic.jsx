import React, { useState } from 'react';
import ButtonDiagnostic from '../composants/ButtonDiagnostic';
import ButtonDossiers from '../composants/ButtonDossiers';

function Diagnostic() {
  // État pour gérer quel bouton est actif
  const [activeButton, setActiveButton] = useState('diagnostic'); // 'diagnostic' par défaut

  // Fonction pour changer l'état actif
  const handleButtonClick = (button) => {
    setActiveButton(button);
  };

  return (
    <div className='pt-5 md:pt-8 lg:pt-10 xl:pt-16'>
      <div className='justify-between flex px-2 md:px-28 lg:px-56 xl:px-80'>
        <ButtonDiagnostic 
          isActive={activeButton === 'diagnostic'} 
          onClick={() => handleButtonClick('diagnostic')} 
        />
        <ButtonDossiers 
          isActive={activeButton === 'dossiers'} 
          onClick={() => handleButtonClick('dossiers')} 
        />
      </div>
      <form className="flex flex-col items-center py-6 mt-8 lg:mt-12 xl:mt-16" action="">
        <input className="border-[#269C26] border p-2 rounded-md w-72 lg:w-96 mb-2" type="text" name="nom" placeholder="Informations du patient" />
        <input className="border-[#269C26] border p-2 rounded-md w-72 lg:w-96 mb-2" type='text' name="creatinine" placeholder="Taux de créatinine" />
        <input className="border-[#269C26] border p-2 rounded-md w-72 lg:w-96 mb-2" type="text" name="albumine" placeholder="Présence d'albumine" />
        <input className="border-[#269C26] border p-2 rounded-md w-72 lg:w-96 mb-2" type="text" name="dfge" placeholder="DFGE" />
        <button className="bg-[#269C26] text-white font-bold px-4 py-2 rounded-lg mt-4" type="submit">
          Diagnostic
        </button>
      </form>
    </div>
  );
}

export default Diagnostic;
