# 🌳 ForestShield API

API RESTful para la gestión de usuarios y datos del proyecto **ForestShield**, una iniciativa educativa y tecnológica para promover la protección ambiental mediante soluciones digitales.

---

## 📘 Descripción

La **ForestShield API** permite registrar usuarios, iniciar sesión y gestionar datos del sistema. 
Está desarrollada con **Node.js**, **Express** y **MongoDB**, e incluye autenticación segura mediante **bcrypt** y **JWT**.

Este proyecto forma parte de una colaboración para desarrollar herramientas que fomenten la conciencia ambiental y la enseñanza de programación aplicada a causas reales. 🌱

---

## ⚙️ Tecnologías utilizadas

- **Node.js** – entorno de ejecución para JavaScript en el servidor. 
- **Express.js** – framework minimalista para construir la API. 
- **MongoDB + Mongoose** – base de datos NoSQL y modelado de datos. 
- **bcryptjs** – cifrado de contraseñas. 
- **dotenv** – manejo de variables de entorno.
- **JWT (JSON Web Token)** – autenticación segura. 

---

## 🧰 Instalación

Sigue estos pasos para ejecutar el proyecto localmente:

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/TU_USUARIO/ForestShield-API.git
   ```

2. **Entrar al directorio del proyecto:**
   ```bash
   cd ForestShield-API
   ```

3. **Instalar las dependencias:**
   ```bash
   npm install
   ```

4. **Crear un archivo `.env`** en la raíz del proyecto con el siguiente contenido:
   ```bash
   PORT=3000
   MONGO_URI=tu_cadena_de_conexion_a_mongodb
   JWT_SECRET=tu_clave_secreta
   ```

5. **Ejecutar el servidor:**
   ```bash
   npm start
   ```

6. Abre tu navegador o Postman y accede a:
   ```
   http://localhost:3000
   ```

---

## 🔗 Endpoints principales

### 🧍 Usuarios

| Método | Endpoint | Descripción |
|--------|-----------|-------------|
| **POST** | `/api/usuarios` | Crea un nuevo usuario |
| **POST** | `/api/usuarios/login` | Inicia sesión |
| **GET** | `/api/usuarios` | Lista todos los usuarios (solo admin) |

---

## 📤 Ejemplo de petición

**Petición:**
```json
POST /api/usuarios/login
{
  "correo": "laura2@example.com",
  "contraseña": "laura123"
}
```

**Respuesta:**
```json
{
  "mensaje": "Inicio de sesión exitoso",
  "usuario": {
    "nombre": "Laura Nicols",
    "correo": "laura2@example.com",
    "rol": "admin"
  }
}
```

---

## 📂 Estructura del proyecto

```
ForestShield-API/
│
├── controllers/      # Lógica de negocio
├── models/           # Modelos de datos (Mongoose)
├── routes/           # Rutas de la API
├── middlewares/      # (opcional) Middleware de autenticación
├── server.js         # Punto de entrada principal
├── package.json
└── README.md
```

---

## 🤝 Colaboradores

👤 **Luis Pérez** – Desarrollador principal 


---

## 🪪 Licencia

Este proyecto está bajo la licencia **MIT**. 
Puedes usarlo, modificarlo y distribuirlo libremente mencionando al autor original.

---

## 💡 Consejos para colaboradores

1. Antes de comenzar una nueva funcionalidad, crea una **rama (branch)**:
   ```bash
   git checkout -b nombre-de-tu-rama
   ```

2. Cuando termines, haz un **commit** claro y descriptivo:
   ```bash
   git commit -m "Agrega autenticación JWT"
   ```

3. Luego **sube tus cambios** y crea un **pull request**:
   ```bash
   git push origin nombre-de-tu-rama
   ```

4. No olvides probar los endpoints antes de enviar tus cambios.

---

✨ **ForestShield API — Proyecto en desarrollo activo.**