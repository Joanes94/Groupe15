import React from 'react'
import ButtonRecherche from './ButtonRecherche';
import { FaPlus } from 'react-icons/fa';
function Dossiers() {
  return (
    <div>
        <div className='justify-center flex flex-wrap items-center gap-5 md:gap-x-10 lg:gap-x-24 mt-8'>
            <div className='flex items-center gap-x-2 lg:gap-x-4 '>
                <h1>Ajouter un patient</h1>
                <FaPlus color='#269C26' size={20} />
            </div>
            <ButtonRecherche/>
        </div>
        <div className='justify-center flex flex-xrap gap-8 mt-8 lg:mt-12 xl:mt-16'>
            <div className='border-2 rounded-lg border-[#269C26] p-4  '>
                <div className='space-y-2 '>
                    <h1> <strong>Nom:</strong> </h1>
                    <h1> <strong>Prénoms:</strong> </h1>
                    <h1> <strong>Age:</strong> </h1>
                    <h1> <strong>Sexe:</strong> </h1>
                </div>
                <button className='roboto  font-bold text-lg text-white bg-[#269C26] px-6 py-1 rounded-2xl mt-8'>Voir Plus</button>
            </div>
        </div>
    </div>
    
  )
}

export default Dossiers