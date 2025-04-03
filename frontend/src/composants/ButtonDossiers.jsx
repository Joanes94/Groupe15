import {useState} from 'react'

function ButtonDossiers() {
    const [activeButton, setActiveButton] = useState(null); // État pour le bouton actif
    
      const handleClick = (button) => {
        setActiveButton(button); // Met à jour le bouton actif
      };
  return (
    <div>
        <button 
            className={`border-2 rounded-3xl px-5 py-2  font-semibold text-sm lg:text-lg ${activeButton === 'dossiers' ? 'bg-[#269C26] text-white' : 'border-[#269C26] text-[#269C26]'}`} 
            onClick={() => handleClick('dossiers')}>
            Dossiers Patients
        </button>
    </div>
  )
}

export default ButtonDossiers