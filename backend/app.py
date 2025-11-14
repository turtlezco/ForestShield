from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np
from pathlib import Path

# --- Configuración de rutas base ---
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "outputs_forestshield" / "modelo_forestfire_final.pkl"
SCALER_PATH = BASE_DIR / "outputs_forestshield" / "scaler_forestfire_final.pkl"

# --- Cargar modelo y scaler ---
try:
    modelo = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
except Exception as e:
    raise RuntimeError(f"Error al cargar modelo o scaler: {e}")

# --- Inicializar aplicación FastAPI ---
app = FastAPI(
    title="API ForestShield",
    description="Predicción de riesgo de incendios forestales",
    version="1.0"
)

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # si quieres limitar: ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Modelo de entrada (solo las 8 variables usadas) ---
class DatosEntrada(BaseModel):
    DOY: int
    T2M: float
    ALLSKY_SFC_SW_DWN: float
    RH2M: float
    LATITUDE: float
    LONGITUDE: float
    HEAT_INDEX: float
    SOLAR_STRESS: float

# --- Endpoint de predicción ---
@app.post("/predecir")
def predecir(datos: DatosEntrada):
    try:
        X = np.array([[
            datos.DOY,
            datos.T2M,
            datos.ALLSKY_SFC_SW_DWN,
            datos.RH2M,
            datos.LATITUDE,
            datos.LONGITUDE,
            datos.HEAT_INDEX,
            datos.SOLAR_STRESS
        ]])

        X_scaled = scaler.transform(X)
        prob = modelo.predict_proba(X_scaled)[0][1]

        # umbral sensible ajustado
        riesgo = 1 if prob >= 0.35 else 0

        return {
            "riesgo_incendio": riesgo,
            "probabilidad": round(float(prob), 3)
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en predicción: {e}")

# --- Endpoint raíz ---
@app.get("/")
def raiz():
    return {
        "mensaje": "API ForestShield activa. Usa POST /predecir para evaluar el riesgo de incendio.",
        "ejemplo_json": {
            "DOY": 150,
            "T2M": 25.3,
            "ALLSKY_SFC_SW_DWN": 250.1,
            "RH2M": 60.5,
            "LATITUDE": 5.6,
            "LONGITUDE": -73.2,
            "HEAT_INDEX": 0.65,
            "SOLAR_STRESS": 0.45
        }
    }
