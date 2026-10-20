from mysql.connector import IntegrityError

from config import DatabaseConfig


class ErrorBaseDatos(Exception):
    """No se pudo abrir la conexión con MySQL."""


class IdDuplicadoError(Exception):
    """Ya existe un estudiante con ese id."""


class Estudiante:
    def __init__(self, id=None, nombre=None, apellido=None, edad=None, carrera=None):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.carrera = carrera

    # ---------- Conexión (único lugar donde se abre) ----------
    @staticmethod
    def _conectar():
        connection = DatabaseConfig.get_connection()
        if connection is None:
            raise ErrorBaseDatos("No se pudo conectar a la base de datos")
        return connection

    # ---------- Tabla ----------
    @staticmethod
    def crear_tabla():
        """Crea la tabla de estudiantes si no existe."""
        connection = Estudiante._conectar()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS estudiantes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    apellido VARCHAR(100) NOT NULL,
                    edad INT NOT NULL,
                    carrera VARCHAR(150) NOT NULL,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            connection.commit()
            cursor.close()
        finally:
            connection.close()

    # ---------- READ ----------
    @staticmethod
    def obtener_todos():
        """Lista de diccionarios con todos los estudiantes."""
        connection = Estudiante._conectar()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM estudiantes ORDER BY id")
            resultados = cursor.fetchall()
            cursor.close()
            return resultados
        finally:
            connection.close()

    @staticmethod
    def obtener_por_id(estudiante_id):
        """Diccionario del estudiante, o None si no existe."""
        connection = Estudiante._conectar()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM estudiantes WHERE id = %s", (estudiante_id,))
            resultado = cursor.fetchone()
            cursor.close()
            return resultado
        finally:
            connection.close()

    # ---------- CREATE ----------
    def guardar(self):
        """INSERT. Si self.id es None, MySQL asigna el id automáticamente."""
        connection = Estudiante._conectar()
        try:
            cursor = connection.cursor()
            if self.id is None:
                cursor.execute(
                    "INSERT INTO estudiantes (nombre, apellido, edad, carrera) "
                    "VALUES (%s, %s, %s, %s)",
                    (self.nombre, self.apellido, self.edad, self.carrera)
                )
                self.id = cursor.lastrowid
            else:
                cursor.execute(
                    "INSERT INTO estudiantes (id, nombre, apellido, edad, carrera) "
                    "VALUES (%s, %s, %s, %s, %s)",
                    (self.id, self.nombre, self.apellido, self.edad, self.carrera)
                )
            connection.commit()
            cursor.close()
        except IntegrityError as e:
            raise IdDuplicadoError(f"Ya existe un estudiante con id {self.id}") from e
        finally:
            connection.close()

    # ---------- UPDATE ----------
    def actualizar(self):
        """UPDATE. Devuelve True si el estudiante existe, False si no."""
        connection = Estudiante._conectar()
        try:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE estudiantes SET nombre=%s, apellido=%s, edad=%s, carrera=%s "
                "WHERE id=%s",
                (self.nombre, self.apellido, self.edad, self.carrera, self.id)
            )
            connection.commit()
            filas_afectadas = cursor.rowcount
            cursor.close()
            return filas_afectadas > 0
        finally:
            connection.close()

    # ---------- DELETE ----------
    def eliminar(self):
        """DELETE. Devuelve True si se eliminó, False si no existía."""
        connection = Estudiante._conectar()
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM estudiantes WHERE id = %s", (self.id,))
            connection.commit()
            filas_afectadas = cursor.rowcount
            cursor.close()
            return filas_afectadas > 0
        finally:
            connection.close()
