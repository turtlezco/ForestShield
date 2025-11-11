const express = require('express');
const router = express.Router();
const Clima = require('../models/Clima');

// Registrar un nuevo dato climático
router.post('/', async (req, res) => {
  try {
    const nuevoClima = new Clima(req.body);
    await nuevoClima.save();
    res.status(201).json(nuevoClima);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// Obtener los registros climáticos
router.get('/', async (req, res) => {
  try {
    const registros = await Clima.find().sort({ fecha: -1 });
    res.json(registros);
  } catch (error) {
    res.status(500).json({ error: error.message }); // ✅ corregido
  }
});

module.exports = router;
