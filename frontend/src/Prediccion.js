import React, { useState } from "react";
import axios from "axios";

function Prediccion() {
  const [formData, setFormData] = useState({
    YEAR: "",
    DOY: "",
    T2M: "",
    ALLSKY_SFC_SW_DWN: "",
    RH2M: "",
    LATITUDE: "",
    LONGITUDE: "",
    PRECIP: "",
    WIND: "",
    ELEVATION: "",
    TEMP_HUMIDITY: "",
    SOLAR_STRESS: "",
  });

  const [resultado, setResultado] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post("http://127.0.0.1:8000/predecir", formData);
      setResultado(res.data);
    } catch (error) {
      console.error("Error al predecir:", error);
    }
  };

  return (
    <div className="min-h-screen bg-green-50 flex flex-col items-center justify-center p-6">
      <div className="bg-white rounded-2xl shadow-lg p-8 w-full max-w-3xl">
        <h1 className="text-3xl font-bold text-green-700 mb-6 text-center">
          🌲 ForestShield — Predicción de Incendios
        </h1>

        <form
          onSubmit={handleSubmit}
          className="grid grid-cols-2 gap-4 mb-6"
        >
          {Object.keys(formData).map((key) => (
            <div key={key}>
              <label className="block text-sm font-medium text-gray-700">
                {key}
              </label>
              <input
                type="number"
                step="any"
                name={key}
                value={formData[key]}
                onChange={handleChange}
                required
                className="mt-1 p-2 border border-gray-300 rounded-md w-full focus:ring-2 focus:ring-green-400 outline-none"
              />
            </div>
          ))}
          <button
            type="submit"
            className="col-span-2 bg-green-600 text-white py-2 rounded-lg hover:bg-green-700 transition"
          >
            Predecir Riesgo
          </button>
        </form>

        {resultado && (
          <div className="bg-green-100 p-4 rounded-lg text-center">
            <h2 className="text-lg font-semibold text-green-700">
              Resultado:
            </h2>
            <p>
              Riesgo de incendio:{" "}
              <span className="font-bold">
                {resultado.riesgo_incendio === 1 ? "ALTO 🔥" : "BAJO 🌿"}
              </span>
            </p>
            <p>Probabilidad: {resultado.probabilidad}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default Prediccion;
