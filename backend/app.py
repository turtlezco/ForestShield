from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # 👈 IMPORTANTE
from pydantic import BaseModel
import joblib
import numpy as np
from pathlib import Path

# --- Cargar modelo y scaler ---
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "outputs_forestshield" / "modelo_final.pkl"
SCALER_PATH = BASE_DIR / "outputs_forestshield" / "scaler_final.pkl"

modelo = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# --- Configurar FastAPI ---
app = FastAPI(title="🌲 ForestShield API", version="1.0")

# --- CORS ---
origins = [
    "http://localhost:3000",  # frontend React
    "http://127.0.0.1:3000",  # a veces React usa 127.0.0.1
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 👈 lista explícita
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Datos Entrada ---
class DatosEntrada(BaseModel):
    YEAR: int
    DOY: int
    T2M: float
    ALLSKY_SFC_SW_DWN: float
    RH2M: float
    LATITUDE: float
    LONGITUDE: float
    PRECIP: float
    WIND: float
    ELEVATION: float
    TEMP_HUMIDITY: float
    SOLAR_STRESS: float


@app.get("/")
def home():
    return {"mensaje": "API de ForestShield activa ✅"}


@app.post("/predecir")
def predecir(datos: DatosEntrada):
    X = np.array([[
        datos.YEAR,
        datos.DOY,
        datos.T2M,
        datos.ALLSKY_SFC_SW_DWN,
        datos.RH2M,
        datos.LATITUDE,
        datos.LONGITUDE,
        datos.PRECIP,
        datos.WIND,
        datos.ELEVATION,
        datos.TEMP_HUMIDITY,
        datos.SOLAR_STRESS
    ]])

    X_scaled = scaler.transform(X)
    pred = modelo.predict(X_scaled)
    prob = modelo.predict_proba(X_scaled)[0][1]

    return {
        "riesgo_incendio": int(pred[0]),
        "probabilidad": round(float(prob), 3)
    }
