import React from 'react'
import { FaSearch } from 'react-icons/fa';
function ButtonRecherche() {
  return (
    <div className='flex gap-x-2 rounded-3xl py-2 border-2 border-[#269C26] items-center w-56 pl-2'>
        <FaSearch color='#269C26'  />
        <input type="text" placeholder='Rechercher'/>
    </div>
  )
}

export default ButtonRecherche