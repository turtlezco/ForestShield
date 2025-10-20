const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');

const usuarioSchema = new mongoose.Schema({
  nombre: {
    type: String,
    required: true,
    trim: true
  },
  correo: {
    type: String,
    required: true,
    unique: true,
    trim: true
  },
  contraseña: {
    type: String,
    required: true,
    trim: true
  },
  rol: {
    type: String,
    enum: ['admin', 'usuario'],
    default: 'usuario'
  },
}, {
  timestamps: true
});

// 🔒 Encriptar contraseña antes de guardar
usuarioSchema.pre('save', async function(next) {
  if (!this.isModified('contraseña')) return next();
  const salt = await bcrypt.genSalt(10);
  this.contraseña = await bcrypt.hash(this.contraseña, salt);
  next();
});

// 🚫 Ocultar contraseña cuando se convierte a JSON
usuarioSchema.methods.toJSON = function() {
  const usuario = this.toObject();
  delete usuario.contraseña;
  return usuario;
};

module.exports = mongoose.model('Usuario', usuarioSchema);
