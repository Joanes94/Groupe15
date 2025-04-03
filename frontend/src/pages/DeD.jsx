import React, { useState } from 'react';
import ButtonDiagnostic from '../composants/ButtonDiagnostic';
import ButtonDossiers from '../composants/ButtonDossiers';
import FormulaireDiagnostic from '../composants/FormulaireDiagnostic';

function DeD() {
  // État pour suivre le bouton actif
  const [activeButton, setActiveButton] = useState('diagnostic'); // 'diagnostic' actif par défaut

  const handleButtonClick = (button) => {
    setActiveButton(button);
  };

  return (
    <div className=' pt-5 md:pt-8 lg:pt-10 xl:pt-16'>
        <div className='justify-between flex  px-2 md:px-28 lg:px-56 xl:px-80'>
            <ButtonDiagnostic 
                isActive={activeButton === 'diagnostic'} 
                onClick={() => handleButtonClick('diagnostic')} 
            />
            <ButtonDossiers 
                isActive={activeButton === 'dossiers'}  
                onClick={() => handleButtonClick('dossiers')} 
            />
        </div>
      
      
      {/* Rendu conditionnel de la div */}
      {activeButton === 'diagnostic' && (
        <div className='mt-4'>
          {/* Contenu à afficher lorsque ButtonDiagnostic est actif */}
          <FormulaireDiagnostic/>
        </div>
      )}
    </div>
  );
}

export default DeD;
