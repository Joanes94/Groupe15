import React from 'react'

function Infos() {
  return (
    <div className='justify-center flex flex-wrap gap-8 xl:gap-x-24 mt-8 lg:mt-12 '>
        <div className='justify-center flex flex-col border-2 rounded-lg border-[#269C26] p-4 bg-[#fdfffd]'>
          <div className='space-y-2 roboto'>
            <h1><strong>Nom:</strong>AMAGBEGNON</h1>
            <h1><strong>Prénoms:</strong>Rosmé</h1>
            <h1><strong>Date de naissance:</strong>03/09/2005</h1>
            <h1><strong>Sexe:</strong>F</h1>
            <h1><strong>GroupeSanguin:</strong></h1>
            <h1><strong>Electrophorèse:</strong></h1>
            <h1><strong>AntécédentsMédicaux:</strong></h1>
            <h1><strong>Traitements en cours:</strong></h1>
            <h1><strong>Prescriptions:</strong></h1>
          </div>
          <button className='roboto font-bold text-lg text-white bg-[#269C26] px-6 py-1 rounded-2xl mt-8'>
            Modifier
          </button>
        </div>
    </div>
  )
}

export default Infos