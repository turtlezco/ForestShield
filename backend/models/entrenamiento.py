import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, classification_report
from imblearn.over_sampling import SMOTE
import joblib
from scipy.stats import randint, uniform

# ================================
# 1️⃣ Cargar datos
# ================================
df = pd.read_csv("/home/luis-perez/Documentos/Universidad/ForestShield/backend/data/dataset_combinado_limpio.csv")

print(f"Registros: {df.shape[0]}, Columnas: {df.shape[1]}")
print(df.head())

# ================================
# 2️⃣ Selección correcta de variables
# ================================
y = df["FIRE_OCCURRED"]

# 🔥 Variables válidas para predicción (sin FIRE_SIZE)
FEATURES = [
    "DOY", "T2M", "ALLSKY_SFC_SW_DWN", "RH2M",
    "LATITUDE", "LONGITUDE",
    "HEAT_INDEX", "SOLAR_STRESS"
]

X = df[FEATURES].fillna(df.mean())

print("\nVariables usadas en el modelo:")
print(FEATURES)

# ================================
# 3️⃣ Train/Test split (ANTES de SMOTE)
# ================================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ================================
# 4️⃣ Balanceo solo en train
# ================================
smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

# ================================
# 5️⃣ Escalado correcto
# ================================
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_resampled)
X_test_scaled = scaler.transform(X_test)

# ================================
# 6️⃣ Random Forest optimizado con RandomSearch
# ================================
param_dist = {
    "n_estimators": randint(300, 800),
    "max_depth": randint(8, 30),
    "min_samples_split": randint(2, 10),
    "min_samples_leaf": randint(1, 5),
    "max_features": ["sqrt", "log2"],
    "class_weight": ["balanced"]
}

rf = RandomForestClassifier(random_state=42)

search = RandomizedSearchCV(
    rf, param_distributions=param_dist,
    n_iter=20, cv=4, scoring="f1",
    n_jobs=-1, random_state=42
)

search.fit(X_train_scaled, y_train_resampled)
best_model = search.best_estimator_

print("\n✨ Mejores parámetros obtenidos:")
print(search.best_params_)

# ================================
# 7️⃣ Evaluación del modelo
# ================================
y_pred = best_model.predict(X_test_scaled)
y_prob = best_model.predict_proba(X_test_scaled)[:, 1]

print("\n📊 Rendimiento del modelo:")
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print(f"F1 Score: {f1_score(y_test, y_pred):.4f}")
print(f"AUC: {roc_auc_score(y_test, y_prob):.4f}")
print("\n", classification_report(y_test, y_pred))

# ================================
# 8️⃣ Guardar modelo y scaler
# ================================
joblib.dump(best_model, "modelo_forestfire_final.pkl")
joblib.dump(scaler, "scaler_forestfire_final.pkl")

print("\n✅ Modelo y scaler guardados correctamente.")

# ================================
# 9️⃣ Prueba rápida (SIN FIRE_SIZE)
# ================================
ejemplo = np.array([[
    150,        # DOY
    34.5,       # T2M
    25.8,       # ALLSKY_SFC_SW_DWN
    22.0,       # RH2M
    4.711,      # LATITUDE
    -74.072,    # LONGITUDE
    2.5,        # HEAT_INDEX
    1.17        # SOLAR_STRESS
]])

ejemplo_scaled = scaler.transform(ejemplo)
prob = best_model.predict_proba(ejemplo_scaled)[0][1]
pred = int(prob > 0.5)

print(f"\n🧪 Ejemplo -> Probabilidad: {prob:.3f}, Predicción: {pred}")
