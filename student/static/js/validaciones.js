function obtenerCampo(formulario, nombreCampo) {
  return formulario.querySelector(`[name="${nombreCampo}"]`);
}

/**
 * Valida campo obligatorio
 */
function validarObligatorio(campo, nombreCampo, errores) {
  if (!campo || !campo.value.trim()) {
    errores.push(`${nombreCampo} es obligatorio.`);
    if (campo) campo.classList.add('is-invalid');
    return false;
  }
  if (campo) campo.classList.remove('is-invalid');
  return true;
}

/**
 * Valida que sea solo letras
 */
function validarSoloLetras(campo, nombreCampo, errores) {
  if (!campo || !campo.value.trim()) return true;
  
  if (!/^[a-zA-ZáéíóúÁÉÍÓÚ\s]+$/.test(campo.value)) {
    errores.push(`${nombreCampo} solo puede contener letras.`);
    campo.classList.add('is-invalid');
    return false;
  }
  campo.classList.remove('is-invalid');
  return true;
}

/**
 * Valida que sea solo números
 */
function validarSoloNumeros(campo, nombreCampo, errores) {
  if (!campo || !campo.value.trim()) return true;
  
  if (!/^\d+$/.test(campo.value)) {
    errores.push(`${nombreCampo} solo puede contener números.`);
    campo.classList.add('is-invalid');
    return false;
  }
  campo.classList.remove('is-invalid');
  return true;
}

/**
 * Valida cédula ecuatoriana
 */
function validarCedula(campo, nombreCampo, errores) {
  if (!campo || !campo.value.trim()) return true;
  
  const cedula = campo.value.trim();
  
  if (!/^\d{10}$/.test(cedula)) {
    errores.push(`${nombreCampo} debe tener exactamente 10 dígitos.`);
    campo.classList.add('is-invalid');
    return false;
  }
  
  const provincia = parseInt(cedula.substring(0, 2));
  if (provincia < 1 || provincia > 24) {
    errores.push(`${nombreCampo} debe comenzar con un código de provincia válido (01-24).`);
    campo.classList.add('is-invalid');
    return false;
  }
  
  campo.classList.remove('is-invalid');
  return true;
}

/**
 * Valida teléfono ecuatoriano
 */
function validarTelefono(campo, nombreCampo, errores) {
  if (!campo || !campo.value.trim()) return true;
  
  const telefono = campo.value.trim();
  
  if (!/^\d{10}$/.test(telefono)) {
    errores.push(`${nombreCampo} debe tener exactamente 10 dígitos.`);
    campo.classList.add('is-invalid');
    return false;
  }
  
  if (!telefono.startsWith('09')) {
    errores.push(`${nombreCampo} debe comenzar con 09.`);
    campo.classList.add('is-invalid');
    return false;
  }
  
  campo.classList.remove('is-invalid');
  return true;
}

/**
 * Valida correo electrónico
 */
function validarCorreo(campo, nombreCampo, errores) {
  if (!campo || !campo.value.trim()) {
    errores.push(`${nombreCampo} es obligatorio.`);
    if (campo) campo.classList.add('is-invalid');
    return false;
  }

  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!regex.test(campo.value)) {
    errores.push(`${nombreCampo} no tiene un formato válido.`);
    campo.classList.add('is-invalid');
    return false;
  }
  campo.classList.remove('is-invalid');
  return true;
}

/**
 * Valida contraseña
 */
function validarContraseña(campo, nombreCampo, errores) {
  if (!campo || !campo.value.trim()) return true;
  
  if (campo.value.length < 8) {
    errores.push(`${nombreCampo} debe tener al menos 8 caracteres.`);
    campo.classList.add('is-invalid');
    return false;
  }
  
  campo.classList.remove('is-invalid');
  return true;
}

/**
 * Muestra errores al usuario
 */
function mostrarErrores(errores) {
  const contenedor = document.getElementById('errorMessages');
  const lista = document.getElementById('errorList');

  if (!contenedor || !lista) return;

  if (errores.length === 0) {
    contenedor.classList.add('d-none');
    return;
  }

  lista.innerHTML = '';
  errores.forEach(error => {
    const li = document.createElement('li');
    li.textContent = error;
    lista.appendChild(li);
  });

  contenedor.classList.remove('d-none');
  contenedor.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Inicializa validaciones del formulario
 */
function inicializarValidaciones(formId) {
  const formulario = document.getElementById(formId);
  if (!formulario) return;

  formulario.addEventListener('submit', function(e) {
    const errores = [];

    // Obtener todos los campos
    const campos = formulario.querySelectorAll('input, textarea, select');
    
    campos.forEach(campo => {
      const nombre = campo.getAttribute('name');
      const tipo = campo.getAttribute('type') || campo.tagName.toLowerCase();
      const label = formulario.querySelector(`label[for="${campo.id}"]`)?.textContent || nombre;
      
      // Validar campo obligatorio
      if (campo.hasAttribute('required')) {
        if (!validarObligatorio(campo, label, errores)) return;
      }

      // Validar tipos específicos
      if (tipo === 'email') {
        validarCorreo(campo, label, errores);
      } else if (nombre === 'cedula') {
        validarCedula(campo, label, errores);
      } else if (nombre === 'telefono') {
        validarTelefono(campo, label, errores);
      } else if (nombre === 'first_name' || nombre === 'last_name' || nombre === 'nombre' || nombre === 'apellido') {
        validarSoloLetras(campo, label, errores);
      } else if (nombre === 'password1' || nombre === 'password2') {
        validarContraseña(campo, label, errores);
      }
    });

    if (errores.length > 0) {
      e.preventDefault();
      mostrarErrores(errores);
    }
  });

  // Limpiar error cuando el usuario escribe
  formulario.querySelectorAll('input, textarea, select').forEach(campo => {
    campo.addEventListener('input', function() {
      this.classList.remove('is-invalid');
    });
  });
}
