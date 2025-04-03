import React from 'react';

const ButtonDossiers = ({ isActive, onClick }) => {
  return (
    <button 
      className={`px-4 py-2 ${isActive ? 'bg-green-500' : 'bg-white'} border border-gray-300`} 
      onClick={onClick}
    >
      Dossiers
    </button>
  );
};

export default ButtonDossiers;