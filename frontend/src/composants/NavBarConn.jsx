import React, { useState } from 'react';
import { FaUser, FaSearch, FaFolder, FaBars } from 'react-icons/fa'; // Changement ici
import FormulaireDiagnostic from "../composants/FormulaireDiagnostic.jsx";
import Dossiers from './Dossiers.jsx';

const NavBarConn = () => {
  const sections = [
    { id: 'section1', content: <FormulaireDiagnostic /> },
    { id: 'section2', content: <Dossiers /> },
    { id: 'section3', content: "" },
  ];

  const [visibleSection, setVisibleSection] = useState('section1');
  const [isListVisible, setIsListVisible] = useState(false);

  const showSection = (sectionId) => {
    setVisibleSection(sectionId);
  };

  const toggleList = () => {
    setIsListVisible(!isListVisible);
  };
  
  return (
    <section className='inline lg:flex min-h-screen'>
      <nav className='bg-[#f6fbf6] text-[#269C26] w-full lg:w-80 flex flex-row lg:flex-col h-auto lg:min-h-screen'>
        <h1 className='roboto text-2xl lg:text-3xl 3xl:text-4xl font-extrabold text-start lg:text-center pt-5 pb-10'>KDiagnostics</h1>
        
        
        <button onClick={toggleList} className='bloc lg:hidden items-center mb-5 '>
          <FaBars size={20} color="#269C26" /> {/* Changement ici */}
        </button>

        {isListVisible && (
          <ul className='space-y-5 mx-2 '>
            <li>
              <button className='flex items-center gap-x-2' onClick={() => showSection('section1')}>
                <FaSearch size={20} color="#269C26" />
                <h1 className='text-2xl font-semibold'>Diagnostic</h1>
              </button>
            </li>
            <li>
              <button className='flex items-center gap-x-2' onClick={() => showSection('section2')}>
                <FaFolder size={20} color="#269C26" />
                <h1 className='text-2xl font-semibold'>Dossiers Patients</h1>
              </button>
            </li>
            <li>
              <button className='flex items-center gap-x-2' onClick={() => showSection('section3')}>
                <FaUser size={20} color="#269C26" />
                <h1 className='text-2xl font-semibold'>Profil</h1>
              </button>
            </li>
          </ul>
        )}
        <ul className='space-y-5 mx-2 hidden lg:block'>
            <li>
              <button className='flex items-center gap-x-2' onClick={() => showSection('section1')}>
                <FaSearch size={20} color="#269C26" />
                <h1 className='text-2xl font-semibold'>Diagnostic</h1>
              </button>
            </li>
            <li>
              <button className='flex items-center gap-x-2' onClick={() => showSection('section2')}>
                <FaFolder size={20} color="#269C26" />
                <h1 className='text-2xl font-semibold'>Dossiers Patients</h1>
              </button>
            </li>
            <li>
              <button className='flex items-center gap-x-2' onClick={() => showSection('section3')}>
                <FaUser size={20} color="#269C26" />
                <h1 className='text-2xl font-semibold'>Profil</h1>
              </button>
            </li>
          </ul>
      </nav>

      <div className='flex-grow'>
        {sections.find(section => section.id === visibleSection)?.content}
      </div>
    </section>
  );
};

export default NavBarConn;
