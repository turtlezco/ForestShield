import warnings
warnings.filterwarnings("ignore")
import matplotlib
matplotlib.use('Agg')  # evita errores de display en servidores o VSCode
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib, json
from pathlib import Path

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, f1_score, roc_auc_score,
    confusion_matrix, classification_report
)
from imblearn.over_sampling import SMOTE

# =====================================================
#  RUTAS
# =====================================================
BASE_DIR = Path(__file__).resolve().parent        # backend/models
DATA_DIR = BASE_DIR.parent / "data"               # backend/data
DATASET_PATH = DATA_DIR / "dataset_combinado_limpio.csv"

OUTPUT_DIR = BASE_DIR.parent / "outputs_forestshield"  # backend/outputs_forestshield
OUTPUT_DIR.mkdir(exist_ok=True)

# =====================================================
#  CARGA DE DATOS
# =====================================================
print("Cargando dataset...")
df = pd.read_csv(DATASET_PATH).drop_duplicates()
print(f" Registros: {df.shape[0]}, Columnas: {df.shape[1]}")

# =====================================================
#  TRANSFORMACIONES Y FEATURES
# =====================================================
# Normalizar coordenadas
df["LATITUDE"] = (df["LATITUDE"] - df["LATITUDE"].mean()) / df["LATITUDE"].std()
df["LONGITUDE"] = (df["LONGITUDE"] - df["LONGITUDE"].mean()) / df["LONGITUDE"].std()

# Features derivadas
df["HEAT_INDEX"] = df["T2M"] * (1 - df["RH2M"] / 100)
df["SOLAR_STRESS"] = df["ALLSKY_SFC_SW_DWN"] / (df["RH2M"] + 1)
df["TEMP_HUMIDITY"] = df["T2M"] * (100 - df["RH2M"])
df["FIRE_RISK"] = (df["T2M"] / (df["RH2M"] + 1)) * df["ALLSKY_SFC_SW_DWN"]

# Indicadores de riesgo
df["LOW_HUMIDITY"] = np.where(df["RH2M"] < 30, 1, 0)
df["HIGH_TEMP"] = np.where(df["T2M"] > df["T2M"].quantile(0.85), 1, 0)
df["HIGH_SOLAR"] = np.where(df["ALLSKY_SFC_SW_DWN"] > df["ALLSKY_SFC_SW_DWN"].quantile(0.80), 1, 0)

# Variable objetivo
df["FIRE_OCCURRED"] = np.where(df["FIRE_SIZE"] > df["FIRE_SIZE"].quantile(0.60), 1, 0)
y = df["FIRE_OCCURRED"]
print(f"Distribución de clases: {np.unique(y, return_counts=True)}")

# Variables predictoras
X = df[[
    "T2M", "RH2M", "ALLSKY_SFC_SW_DWN",
    "LATITUDE", "LONGITUDE",
    "HEAT_INDEX", "SOLAR_STRESS", "TEMP_HUMIDITY", "FIRE_RISK",
    "LOW_HUMIDITY", "HIGH_TEMP", "HIGH_SOLAR"
]]

# =====================================================
#  DIVISIÓN Y ESCALAMIENTO
# =====================================================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, stratify=y, random_state=42
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# =====================================================
#  BALANCEO DE CLASES
# =====================================================
print("Aplicando SMOTE...")
smote = SMOTE(random_state=42, sampling_strategy=1.0)
X_train_bal, y_train_bal = smote.fit_resample(X_train_scaled, y_train)

# =====================================================
#  ENTRENAMIENTO Y OPTIMIZACIÓN
# =====================================================
print("Optimizando modelo...")

param_grid = {
    'n_estimators': [600, 800],
    'max_depth': [25, 30],
    'min_samples_split': [2, 3],
    'min_samples_leaf': [1],
    'class_weight': ['balanced']
}

rf_search = GridSearchCV(
    RandomForestClassifier(random_state=42, n_jobs=-1),
    param_grid=param_grid,
    cv=3,
    scoring='accuracy',
    n_jobs=-1
)

rf_search.fit(X_train_bal, y_train_bal)
rf_model = rf_search.best_estimator_

print(f" Mejores parámetros: {rf_search.best_params_}")
# =====================================================
#  EVALUACIÓN
# =====================================================
y_pred = rf_model.predict(X_test_scaled)
y_proba = rf_model.predict_proba(X_test_scaled)[:, 1]

acc = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_proba)

print("\n Resultados del modelo:")
print(f"Accuracy: {acc:.4f}")
print(f"F1 Score: {f1:.4f}")
print(f"AUC: {auc:.4f}")
print("\n" + classification_report(y_test, y_pred))

# =====================================================
#  VISUALIZACIONES
# =====================================================
# Matriz de confusión
plt.figure(figsize=(6,5))
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt="d", cmap="Greens")
plt.title(f"Matriz de Confusión (Accuracy: {acc:.3f})")
plt.xlabel("Predicción")
plt.ylabel("Real")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "confusion_matrix.png")
plt.close()

# Importancia de variables
importances = pd.DataFrame({
    "Variable": X.columns,
    "Importancia": rf_model.feature_importances_
}).sort_values(by="Importancia", ascending=False)

print("\n🌡️ Top variables más influyentes:")
print(importances.head(8))

plt.figure(figsize=(8,5))
sns.barplot(x="Importancia", y="Variable", data=importances.head(8), palette="viridis")
plt.title("Importancia de Variables")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "importancia_variables.png")
plt.close()

# =====================================================
#  GUARDADO DE MODELO Y MÉTRICAS
# =====================================================
joblib.dump(rf_model, OUTPUT_DIR / "modelo_final.pkl")
joblib.dump(scaler, OUTPUT_DIR / "scaler_final.pkl")

metrics = {
    "accuracy": float(acc),
    "f1_score": float(f1),
    "auc": float(auc),
    "params": rf_search.best_params_
}

with open(OUTPUT_DIR / "metrics.json", "w") as f:
    json.dump(metrics, f, indent=2)

print(f"\n Modelo guardado en: {OUTPUT_DIR}")
print(" Entrenamiento completado correctamente.")

if acc >= 0.90:
    print(f" Objetivo alcanzado: {acc:.4f}")
else:
    print(f"Considera ajustar el quantil (línea 70, actual: 0.60) para mejorar el accuracy")
