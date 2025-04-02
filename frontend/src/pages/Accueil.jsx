import React from 'react'
import { FaRulerCombined, FaThermometerHalf, FaStethoscope , FaFileAlt, FaPen } from 'react-icons/fa';

function Accueil() {
  return (
    <div className='flex flex-wrap justify-center gap-0 md:gap-x-20 xl:gap-x-44 items-center pt-8 lg:pt-14 xl:pt-24'>
        <div className='text-center md:text-start'>
            <h1 className='text-[#3aa33a] text-2xl lg:text-3xl xl:text-4xl w-[300px] lg:w-[500px] roboto'>Posez  rapidement et en toute sécurité un diagnostic de la maladie chronique rénale</h1>
            <h1 className='pt-5 pb-10 w-80  text-gray-700'>Bienvenue sur KDiagnostics, notre solution pour diagnostiquer le stade de la maladie chronique rénale. Inscrivez vous si vous n'avez pas encore de compte ou connectez vous si vous en avez déjà un afin de bénéficier de nos services.</h1>
            <div className='flex gap-x-5 text-white roboto ml-3 md:ml-0'>
                <button className='bg-[#269C26] px-6 py-3 text-lg font-semibold  rounded'> <link rel="stylesheet" href="#" /> S'inscrire </button>
                <button className='bg-[#269C26] px-6 py-3 text-lg font-semibold rounded'> <link rel="stylesheet" href="#" /> Se Connecter </button>
            </div>
        </div>
        <div className='hidden md:flex'>
            <div className='text-[#269C26] '><FaFileAlt size={200}/></div>  
            <div className='relative right-32 top-10 text-white'><FaPen size={40}/> </div>
        </div>
    </div>
  )
}

export default Accueil