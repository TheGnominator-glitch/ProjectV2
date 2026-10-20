from flask import Blueprint, jsonify, request
from mysql.connector import Error

from models import Estudiante, ErrorBaseDatos, IdDuplicadoError

estudiantes_bp = Blueprint('estudiantes', __name__)

CAMPOS_REQUERIDOS = ('nombre', 'apellido', 'edad', 'carrera')


# ---------- Manejo de errores (las rutas ya no abren conexiones) ----------
@estudiantes_bp.errorhandler(ErrorBaseDatos)
def error_conexion(e):
    return jsonify({'error': 'Error de conexión con la base de datos'}), 500


@estudiantes_bp.errorhandler(Error)
def error_mysql(e):
    print(f"Error de MySQL: {e}")
    return jsonify({'error': 'Error en la base de datos'}), 500


# ---------- Validación del JSON recibido ----------
def validar_datos(data):
    """Devuelve (datos_limpios, mensaje_de_error). Uno de los dos es None."""
    if not isinstance(data, dict):
        return None, 'Se esperaba un cuerpo JSON'

    faltantes = [c for c in CAMPOS_REQUERIDOS if data.get(c) in (None, '')]
    if faltantes:
        return None, f"Faltan campos: {', '.join(faltantes)}"

    try:
        edad = int(data['edad'])
    except (TypeError, ValueError):
        return None, 'La edad debe ser un número entero'

    limpios = {
        'nombre': str(data['nombre']).strip(),
        'apellido': str(data['apellido']).strip(),
        'edad': edad,
        'carrera': str(data['carrera']).strip(),
    }
    if not limpios['nombre'] or not limpios['apellido'] or not limpios['carrera']:
        return None, 'Nombre, apellido y carrera no pueden estar vacíos'
    return limpios, None


# ---------- Rutas CRUD para la entidad "estudiantes" ----------
# CREATE - Crear estudiante (POST - INSERT)
@estudiantes_bp.route('/api/v1/estudiantes', methods=['POST'])
def crear_estudiante():
    data = request.get_json(silent=True)
    datos, error = validar_datos(data)
    if error:
        return jsonify({'error': error}), 400

    # El id es opcional: si no viene, MySQL lo genera (AUTO_INCREMENT)
    id_estudiante = None
    if data.get('id') not in (None, ''):
        try:
            id_estudiante = int(data['id'])
        except (TypeError, ValueError):
            return jsonify({'error': 'El id debe ser un número entero'}), 400

    estudiante = Estudiante(id=id_estudiante, **datos)
    try:
        estudiante.guardar()
    except IdDuplicadoError as e:
        return jsonify({'error': str(e)}), 409

    return jsonify({'mensaje': 'Estudiante creado exitosamente', 'id': estudiante.id}), 201


# READ - Obtener todos los estudiantes (GET - SELECT)
@estudiantes_bp.route('/api/v1/estudiantes', methods=['GET'])
def obtener_estudiantes():
    return jsonify(Estudiante.obtener_todos()), 200


# READ - Obtener un estudiante por ID (GET - SELECT)
@estudiantes_bp.route('/api/v1/estudiantes/<int:id>', methods=['GET'])
def obtener_estudiante(id):
    estudiante = Estudiante.obtener_por_id(id)
    if estudiante:
        return jsonify(estudiante), 200
    return jsonify({'error': 'Estudiante no encontrado'}), 404


# UPDATE - Actualizar estudiante por ID (PUT - UPDATE)
@estudiantes_bp.route('/api/v1/estudiantes/<int:id>', methods=['PUT'])
def actualizar_estudiante(id):
    datos, error = validar_datos(request.get_json(silent=True))
    if error:
        return jsonify({'error': error}), 400

    if Estudiante(id=id, **datos).actualizar():
        return jsonify({'mensaje': 'Estudiante actualizado exitosamente'}), 200
    return jsonify({'error': 'Estudiante no encontrado'}), 404


# DELETE - Eliminar estudiante por ID (DELETE - DELETE)
@estudiantes_bp.route('/api/v1/estudiantes/<int:id>', methods=['DELETE'])
def eliminar_estudiante(id):
    if Estudiante(id=id).eliminar():
        return jsonify({'mensaje': 'Estudiante eliminado exitosamente'}), 200
    return jsonify({'error': 'Estudiante no encontrado'}), 404
