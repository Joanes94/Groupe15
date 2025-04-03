import React from 'react'
import { FaUser } from 'react-icons/fa';
function NavBarConn() {
  return (
    <div>
        <nav className='bg-[#f6fbf6] text-[#269C26]  py-4 justify-between flex px-2 md:px-5 lg:px-16 xl:px-28 items-center'>
            <h1 className=' text-2xl lg:text-4xl 3xl:text-6xl font-bold text-center roboto'>KDiagnostics</h1>
            <div className='flex gap-x-0 lg:gap-x-2'>
                <FaUser size={30} color="#269C26" />
                <h2 className='text-lg lg:text-xl 3xl:text-2xl font-bold hidden lg:block'>Profil Utilisateur</h2>
            </div>
        </nav>
    </div>
  )
}

export default NavBarConn