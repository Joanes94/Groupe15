import React from 'react';

const ButtonDossiers = ({ isActive, onClick }) => {
  return (
    <button 
      className={`px-4 lg:px-8 py-2 rounded-3xl font-bold text-lg ${isActive ? 'bg-[#269C26] text-white' : 'bg-white text-[#269C26]'} border-2 border-[#269C26]`} 
      onClick={onClick}
    >
      Dossiers
    </button>
  );
};

export default ButtonDossiers;