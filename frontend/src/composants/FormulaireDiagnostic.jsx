import React from 'react'

function FormulaireDiagnostic() {
  return (
    <div>
        <form className="flex flex-col items-center py-6 mt-8 lg:mt-12 xl:mt-16" action="">
            <input className="border-[#269C26] border p-2 rounded-md w-72 lg:w-96 mb-2" type="text" name="nom" placeholder="Informations du patient" />
            <input className="border-[#269C26] border p-2 rounded-md w-72 lg:w-96 mb-2" type='text' name="creatinine" placeholder="Taux de créatinine" />
            <input className="border-[#269C26] border p-2 rounded-md w-72 lg:w-96 mb-2" type="text" name="albumine" placeholder="Présence d'albumine" />
            <input className="border-[#269C26] border p-2 rounded-md w-72 lg:w-96 mb-2" type="text" name="dfge" placeholder="DFGE" />
            <button className="bg-[#269C26] text-white font-bold px-4 py-2 rounded-lg mt-4" type="submit">
              Diagnostic
            </button>
        </form>
    </div>
  )
}

export default FormulaireDiagnostic