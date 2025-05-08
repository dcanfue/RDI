import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Función para crear la base de datos si no existe y retornar la conexión final
def conectar():
    try:
        # Conexión inicial sin especificar base de datos para crearla
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root'
        )
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS alquemy_robots")
            conn.commit()
            cursor.close()
            conn.close()
    except Error as e:
        print("Error al crear la base de datos:", e)
    
    try:
        # Conexión definitiva a la base de datos alquemy_robots
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='alquemy_robots'
        )
        return conn
    except Error as e:
        print("Error al conectar a la base de datos alquemy_robots:", e)
        return None

# Función para crear la tabla robots si no existe
def crear_tabla_robots(conn):
    try:
        cursor = conn.cursor()
        query = """
        CREATE TABLE IF NOT EXISTS robots (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            model VARCHAR(50) NOT NULL,
            active BOOLEAN DEFAULT TRUE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(query)
        conn.commit()
        cursor.close()
    except Error as e:
        print("Error al crear la tabla robots:", e)

# Función para listar todos los robots
def list_robots(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, model, active, created_at FROM robots")
        robots = cursor.fetchall()
        if not robots:
            print("No hay robots registrados.")
        else:
            print("\n== Lista de Robots ==")
            for (rid, name, model, active, created_at) in robots:
                estado = "Activo" if active else "Inactivo"
                print(f"ID: {rid} | Nombre: {name} | Modelo: {model} | Estado: {estado} | Creado: {created_at}")
        cursor.close()
    except Error as e:
        print("Error al listar robots:", e)

# Función para agregar un robot
def add_robot(conn):
    name = input("Ingresa el nombre del robot: ")
    model = input("Ingresa el modelo del robot: ")
    try:
        cursor = conn.cursor()
        query = "INSERT INTO robots (name, model) VALUES (%s, %s)"
        cursor.execute(query, (name, model))
        conn.commit()
        print("Robot agregado correctamente.")
        cursor.close()
    except Error as e:
        print("Error al agregar el robot:", e)

# Función para actualizar un robot
def update_robot(conn):
    try:
        robot_id = int(input("Ingresa el ID del robot a actualizar: "))
    except ValueError:
        print("El ID debe ser un número entero.")
        return

    try:
        cursor = conn.cursor()
        # Verificar si el robot existe
        cursor.execute("SELECT name, model, active FROM robots WHERE id = %s", (robot_id,))
        robot = cursor.fetchone()
        if not robot:
            print(f"No se encontró ningún robot con ID {robot_id}.")
            cursor.close()
            return

        current_name, current_model, current_active = robot

        new_name = input(f"Nuevo nombre (actual: {current_name}) [presiona Enter para mantener]: ")
        new_model = input(f"Nuevo modelo (actual: {current_model}) [presiona Enter para mantener]: ")
        new_status = input(f"¿Activo? (actual: {'sí' if current_active else 'no'}, escribe 'sí' o 'no' o Enter para mantener): ").strip().lower()

        # Si el usuario no ingresa nada, se mantiene el valor actual.
        updated_name = new_name if new_name else current_name
        updated_model = new_model if new_model else current_model

        if new_status == "":
            updated_active = current_active
        elif new_status in ["sí", "si"]:
            updated_active = True
        elif new_status == "no":
            updated_active = False
        else:
            updated_active = current_active

        query = "UPDATE robots SET name = %s, model = %s, active = %s WHERE id = %s"
        cursor.execute(query, (updated_name, updated_model, updated_active, robot_id))
        conn.commit()
        print("Robot actualizado correctamente.")
        cursor.close()
    except Error as e:
        print("Error al actualizar el robot:", e)

# Función para eliminar un robot
def delete_robot(conn):
    try:
        robot_id = int(input("Ingresa el ID del robot a eliminar: "))
    except ValueError:
        print("El ID debe ser un número entero.")
        return

    try:
        cursor = conn.cursor()
        # Verificar si el robot existe
        cursor.execute("SELECT id FROM robots WHERE id = %s", (robot_id,))
        robot = cursor.fetchone()
        if not robot:
            print(f"No se encontró ningún robot con ID {robot_id}.")
            cursor.close()
            return
        
        query = "DELETE FROM robots WHERE id = %s"
        cursor.execute(query, (robot_id,))
        conn.commit()
        print("Robot eliminado correctamente.")
        cursor.close()
    except Error as e:
        print("Error al eliminar el robot:", e)

# Menú principal
def main():
    conn = conectar()
    if conn is None:
        return
    crear_tabla_robots(conn)
    
    while True:
        print("\n=== Menú de Robots ===")
        print("1. Listar Robots")
        print("2. Agregar Robot")
        print("3. Actualizar Robot")
        print("4. Eliminar Robot")
        print("5. Salir")
        opcion = input("Elige una opción (1-5): ").strip()
        
        if opcion == "1":
            list_robots(conn)
        elif opcion == "2":
            add_robot(conn)
        elif opcion == "3":
            update_robot(conn)
        elif opcion == "4":
            delete_robot(conn)
        elif opcion == "5":
            print("Saliendo...")
            break
        else:
            print("Opción inválida. Intenta de nuevo.")
    
    conn.close()

if __name__ == "__main__":
    main()