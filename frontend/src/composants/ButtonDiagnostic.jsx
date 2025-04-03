import React from 'react';

const ButtonDiagnostic = ({ isActive, onClick }) => {
  return (
    <button 
      className={`px-4 py-2 ${isActive ? 'bg-green-500' : 'bg-white'} border border-gray-300`} 
      onClick={onClick}
    >
      Diagnostic
    </button>
  );
};

export default ButtonDiagnostic;