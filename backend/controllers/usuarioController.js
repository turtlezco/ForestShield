const Usuario = require('../models/Usuario');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');

// 🔐 Iniciar sesión
exports.loginUsuario = async (req, res) => {
  const { correo, contraseña } = req.body;

  try {
    // 1️⃣ Buscar usuario por correo
    const usuario = await Usuario.findOne({ correo });
    if (!usuario) {
      return res.status(400).json({ error: 'Correo no registrado' });
    }

    // 2️⃣ Comparar contraseña ingresada con la encriptada
    const esValida = await bcrypt.compare(contraseña, usuario.contraseña);
    if (!esValida) {
      return res.status(400).json({ error: 'Contraseña incorrecta' });
    }

    // 3️⃣ Crear token JWT
    const token = jwt.sign(
      { id: usuario._id, rol: usuario.rol },
      process.env.JWT_SECRET,
      { expiresIn: '2h' }
    );

    res.json({
      mensaje: 'Inicio de sesión exitoso',
      usuario: {
        nombre: usuario.nombre,
        correo: usuario.correo,
        rol: usuario.rol
      },
      token
    });
  } catch (error) {
    res.status(500).json({ error: 'Error al iniciar sesión' });
  }
};
