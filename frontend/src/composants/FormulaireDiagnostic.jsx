import React from 'react'
function FormulaireDiagnostic() {
  return (
    <div className='roboto justify-center'>
      <h1 className='text-center text-2xl lg:text-3xl pt-10 font-bold text-[#269C26]'>Renseignez les résultats de l'analyse demandés ci-dessous</h1>
      <div className='flex items-center justify-center mt-10 lg:mt-16  '>
        <form className="flex flex-col items-center px-2 md:px-4  py-3 xl:py-6 " action="">
            <input className="border-[#269C26] border-2 p-2 rounded-md w-72 lg:w-96 xl:w-[500px] mb-2" type="text" name="nom" placeholder="Informations du patient" />
            <input className="border-[#269C26] border-2 p-2 rounded-md w-72 lg:w-96 xl:w-[500px]  mb-2" type='text' name="creatinine" placeholder="Taux de créatinine" />
            <input className="border-[#269C26] border-2 p-2 rounded-md w-72 lg:w-96 xl:w-[500px]  mb-2" type="text" name="albumine" placeholder="Présence d'albumine" />
            <input className="border-[#269C26] border-2 p-2 rounded-md w-72 lg:w-96 xl:w-[500px]  mb-2" type="text" name="dfge" placeholder="DFGE" />
            <button className="bg-[#269C26] text-white font-bold px-4 xl:px-10 py-2 rounded-lg mt-4" type="submit">
              Diagnostic
            </button>
        </form>
      </div>
    </div>
    
  )
}

export default FormulaireDiagnostic