from flask import Flask
from flask_cors import CORS

from models import Estudiante, ErrorBaseDatos
from routes.estudiantes import estudiantes_bp

app = Flask(__name__)
CORS(app)  # Permite peticiones desde el frontend (otro origen/puerto)

# Registrar blueprints (rutas)
app.register_blueprint(estudiantes_bp)


@app.route('/')
def index():
    return {'mensaje': 'API de Estudiantes - Universidad Libre'}, 200


if __name__ == '__main__':
    # Crear la tabla al iniciar (si MySQL no responde, avisamos pero el servidor arranca)
    try:
        Estudiante.crear_tabla()
    except ErrorBaseDatos:
        print("No se pudo crear la tabla: revisa que MySQL esté iniciado en XAMPP "
              "y que el puerto en config.py (o .env) sea el correcto.")
    print("\n── Universidad Libre — Servidor iniciado en http://localhost:5000")
    app.run(debug=True, port=5000)
