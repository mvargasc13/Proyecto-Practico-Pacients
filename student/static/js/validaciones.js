function obtenerCampo(formulario, nombreCampo) {
  return formulario.querySelector(`[name="${nombreCampo}"]`);
}

/**
 * Valida campo obligatorio
 */
function validarObligatorio(campo, nombreCampo, errores) {
  if (!campo || !campo.value.trim()) {
    errores.push(`${nombreCampo} es obligatorio.`);
    if (campo) campo.classList.add('is-invalid');p
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
