import React from 'react'

function Infos() {
  return (
    <div className='px-4 py-2 rounded border-2 border-[#269C26] roboto'>
        <div className='space-y-2'>
            <div className='text-center space-y-1'>
                <h1 className='text-[#269C26]'>Nom Prénoms</h1>
                <h1>Age:</h1>
                <h1>Sexe:</h1>
            </div>
            <div>
                <h1>Groupe sanguin:</h1>
                <h1>Allergies:</h1>
                <h1>Antécédents:</h1>
                <h1>Poids:</h1>
                <h1>Taille:</h1>
            </div>
            <button className='roboto  font-bold text-lg text-white bg-[#269C26] px-6 py-1 rounded-2xl mt-8'>Modifier</button>
        </div>
    </div>
  )
}

export default Infos