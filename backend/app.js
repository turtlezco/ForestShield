// backend/app.js
require('dotenv').config();

const express = require('express');
const mongoose = require('mongoose');

const app = express();

// Middleware
app.use(express.json());

// Rutas
const usuarioRoutes = require('./routes/usuario'); // 👈 asegúrate que el nombre coincida
app.use('/api/usuarios', usuarioRoutes); // 👈 con barra inicial

// Conexión a MongoDB Atlas
mongoose.connect(process.env.MONGO_URI)
  .then(() => console.log('✅ Conectado a MongoDB Atlas'))
  .catch(err => console.error('❌ Error al conectar a MongoDB:', err));

// Ruta de prueba
app.get('/', (req, res) => {
  res.send('Servidor ForestShield funcionando 🌳');
});

// Puerto
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`🚀 Servidor corriendo en el puerto ${PORT}`);
});
