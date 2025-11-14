// ForestShieldForm.jsx
// Componente formulario + tarjeta de resultados para ForestShield
// Estilo: Dashboard oscuro profesional con TailwindCSS

import { useState } from "react";
import axios from "axios";

export default function ForestShieldForm() {
  // Estado con los campos del formulario
  const [formData, setFormData] = useState({
    DOY: "",
    T2M: "",
    ALLSKY_SFC_SW_DWN: "",
    RH2M: "",
    LATITUDE: "",
    LONGITUDE: "",
    HEAT_INDEX: "",
    SOLAR_STRESS: ""
  });

  // Estado donde se almacenará la respuesta de FastAPI
  const [resultado, setResultado] = useState(null);

  // Manejar cambios en los inputs
  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  // Enviar datos a la API
  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post("http://localhost:8000/predecir", {
        ...formData,
        DOY: Number(formData.DOY),
        T2M: Number(formData.T2M),
        ALLSKY_SFC_SW_DWN: Number(formData.ALLSKY_SFC_SW_DWN),
        RH2M: Number(formData.RH2M),
        LATITUDE: Number(formData.LATITUDE),
        LONGITUDE: Number(formData.LONGITUDE),
        HEAT_INDEX: Number(formData.HEAT_INDEX),
        SOLAR_STRESS: Number(formData.SOLAR_STRESS)
      });

      setResultado(response.data);

    } catch (error) {
      console.error("Error al conectar con la API", error);
    }
  };

  // Componente para mostrar la tarjeta del riesgo
  const ResultadoCard = () => {
    if (!resultado) return null;

    // Colores dependiendo del riesgo
    const color = resultado.riesgo_incendio === 1
      ? "bg-red-600 border-red-400"
      : "bg-green-600 border-green-400";

    return (
      <div className={`w-full mt-6 p-4 border ${color} text-white rounded-xl shadow-lg`}>
        <h2 className="text-xl font-bold mb-2">
          Resultado de riesgo
        </h2>

        <p className="text-lg">
          Riesgo de incendio: 
          <span className="font-semibold ml-2">
            {resultado.riesgo_incendio === 1 ? "Alto" : "Bajo"}
          </span>
        </p>

        <p className="text-lg mt-1">
          Probabilidad: 
          <span className="font-semibold ml-2">
            {resultado.probabilidad}
          </span>
        </p>
      </div>
    );
  };

  return (
    <div className="w-full max-w-4xl mx-auto p-6 bg-gray-900 min-h-screen">
      
      {/* Título principal del dashboard */}
      <h1 className="text-3xl font-bold text-white text-center mb-8">
        ForestShield Dashboard
      </h1>

      {/* Contenedor del formulario */}
      <div className="bg-gray-800 border border-gray-700 p-6 rounded-xl shadow-xl">
        <h2 className="text-xl text-white font-semibold mb-4">
          Ingresar datos del sensor
        </h2>

        {/* Formulario de predicción */}
        <form className="grid grid-cols-2 gap-4" onSubmit={handleSubmit}>
          
          {/* Cada input es un campo del dataset */}
          {Object.keys(formData).map((campo) => (
            <div key={campo} className="flex flex-col">
              <label className="text-gray-300 mb-1 uppercase text-xs font-semibold">
                {campo.replace(/_/g, " ")}
              </label>
              <input
                type="number"
                step="any"
                name={campo}
                value={formData[campo]}
                onChange={handleChange}
                className="p-2 bg-gray-700 text-white rounded-lg border border-gray-600 focus:border-blue-400 focus:outline-none"
                required
              />
            </div>
          ))}

          {/* Botón enviar */}
          <div className="col-span-2 mt-4">
            <button
              type="submit"
              className="w-full bg-blue-600 hover:bg-blue-500 transition text-white py-2 rounded-lg font-semibold shadow-md"
            >
              Evaluar riesgo
            </button>
          </div>
        </form>
      </div>

      {/* Mostrar resultado solo si existe */}
      <ResultadoCard />
    </div>
  );
}
