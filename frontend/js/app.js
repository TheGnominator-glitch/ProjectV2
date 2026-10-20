const API_URL = 'http://localhost:5000/api/v1/estudiantes';
let EDITA = false;

// Referencias al DOM
const form = document.getElementById('estudiante-form');
const formTitle = document.getElementById('form-title');
const submitBtn = document.getElementById('submit-btn');
const cancelBtn = document.getElementById('cancel-btn');
const tbody = document.getElementById('estudiantes-tbody');
const idInput = document.getElementById('estudiante-id');

// Cargar estudiantes al iniciar
document.addEventListener('DOMContentLoaded', () => {
    cargarEstudiantes();
});

// Evita que un nombre con etiquetas HTML se ejecute como código en la tabla
function escapeHtml(valor) {
    return String(valor)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

// Función para cargar todos los estudiantes (READ)
async function cargarEstudiantes() {
    try {
        const response = await fetch(API_URL);
        if (!response.ok) {
            throw new Error(`El servidor respondió con el código ${response.status}`);
        }
        const estudiantes = await response.json();

        tbody.innerHTML = '';

        if (estudiantes.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6">No hay estudiantes registrados</td></tr>';
            return;
        }

        estudiantes.forEach(estudiante => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${escapeHtml(estudiante.id)}</td>
                <td>${escapeHtml(estudiante.nombre)}</td>
                <td>${escapeHtml(estudiante.apellido)}</td>
                <td>${escapeHtml(estudiante.edad)}</td>
                <td>${escapeHtml(estudiante.carrera)}</td>
                <td>
                    <button class="btn-editar" onclick="editarEstudiante(${Number(estudiante.id)})">
                        Editar
                    </button>
                    <button class="btn-eliminar" onclick="eliminarEstudiante(${Number(estudiante.id)})">
                        Eliminar
                    </button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (error) {
        console.error('Error al cargar estudiantes:', error);
        alert('Error al cargar los datos del servidor');
    }
}

// Función para crear o actualizar estudiante (CREATE/UPDATE)
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const id = idInput.value.trim();
    const estudiante = {
        nombre: document.getElementById('nombre').value,
        apellido: document.getElementById('apellido').value,
        edad: parseInt(document.getElementById('edad').value),
        carrera: document.getElementById('carrera').value
    };

    // Al crear, el id es opcional: si se deja vacío lo asigna MySQL
    if (!EDITA && id !== '') {
        estudiante.id = parseInt(id);
    }

    const actualizando = EDITA;

    try {
        const response = await fetch(actualizando ? `${API_URL}/${id}` : API_URL, {
            method: actualizando ? 'PUT' : 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(estudiante)
        });

        if (response.ok) {
            alert(actualizando ? 'Estudiante actualizado exitosamente' : 'Estudiante creado exitosamente');
            limpiarFormulario();
            cargarEstudiantes();
        } else {
            // El backend explica qué falló (id repetido, campo faltante, etc.)
            const data = await response.json().catch(() => ({}));
            alert(data.error || 'Error al guardar el estudiante');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error de conexión con el servidor');
    }
});

// Función para editar estudiante
async function editarEstudiante(id) {
    try {
        const response = await fetch(`${API_URL}/${id}`);
        if (!response.ok) {
            alert('No se encontró el estudiante');
            return;
        }
        const estudiante = await response.json();

        idInput.value = estudiante.id;
        idInput.readOnly = true;   // el id identifica el registro, no se cambia al editar
        document.getElementById('nombre').value = estudiante.nombre;
        document.getElementById('apellido').value = estudiante.apellido;
        document.getElementById('edad').value = estudiante.edad;
        document.getElementById('carrera').value = estudiante.carrera;

        EDITA = true;
        formTitle.textContent = 'Editar Estudiante';
        submitBtn.textContent = 'Actualizar Estudiante';
        cancelBtn.style.display = 'block';

        // Scroll al formulario
        form.scrollIntoView({ behavior: 'smooth' });
    } catch (error) {
        console.error('Error al cargar estudiante:', error);
        alert('Error al cargar los datos del estudiante');
    }
}

// Función para eliminar estudiante (DELETE)
async function eliminarEstudiante(id) {
    if (!confirm('¿Estás seguro de eliminar este estudiante?')) {
        return;
    }

    try {
        const response = await fetch(`${API_URL}/${id}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            alert('Estudiante eliminado exitosamente');
            cargarEstudiantes();
        } else {
            alert('Error al eliminar el estudiante');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error de conexión con el servidor');
    }
}

// Función para limpiar el formulario (también sale del modo edición)
function limpiarFormulario() {
    form.reset();
    EDITA = false;
    idInput.value = '';
    idInput.readOnly = false;
    formTitle.textContent = 'Agregar Nuevo Estudiante';
    submitBtn.textContent = 'Agregar Estudiante';
    cancelBtn.style.display = 'none';
}

// Botón cancelar
cancelBtn.addEventListener('click', limpiarFormulario);
