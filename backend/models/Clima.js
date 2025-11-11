// backend/models/Clima.js
const mongoose = require('mongoose');

const ClimaSchema = new mongoose.Schema({
  zona: { type: String, required: true },
  temperatura: { type: Number, required: true },
  humedad: { type: Number, required: true },
  lluvia: { type: String, required: true },   // <-- ahora String
  viento: { type: String, required: true },   // <-- ahora String
  fecha: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Clima', ClimaSchema);
