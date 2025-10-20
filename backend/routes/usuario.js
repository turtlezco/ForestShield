// routes/usuarios.js
const express = require('express');
const router = express.Router();
const bcrypt = require('bcryptjs');
const Usuario = require('../models/Usuario');

// Obtener todos los usuarios
router.get('/', async (req, res) => {
  try {
    const usuarios = await Usuario.find();
    res.json(usuarios);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Crear un nuevo usuario
router.post('/', async (req, res) => {
  try {
    const { nombre, correo, contraseña, rol } = req.body;

    const nuevoUsuario = new Usuario({
      nombre,
      correo,
      contraseña, // se encripta automáticamente en el modelo
      rol,
    });

    await nuevoUsuario.save();
    res.status(201).json({ mensaje: 'Usuario creado correctamente', usuario: nuevoUsuario });
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});


// Login de usuario
router.post('/login', async (req, res) => {
  try {
    const { correo, contraseña } = req.body;

    // Buscar usuario por correo
    const usuario = await Usuario.findOne({ correo });
    if (!usuario) {
      return res.status(404).json({ error: 'Usuario no encontrado' });
    }

    // Comparar contraseñas
    const esValida = await bcrypt.compare(contraseña, usuario.contraseña);
    if (!esValida) {
      return res.status(400).json({ error: 'Contraseña incorrecta' });
    }

    res.json({ mensaje: 'Inicio de sesión exitoso', usuario });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;
