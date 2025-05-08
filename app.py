from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app)

def get_connection():
    # Reutiliza la configuración de proxy.py para conectar
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='alquemy_robots'
        )
        return conn
    except Error as e:
        print("Error de conexión:", e)
        return None

@app.route('/api/robots', methods=['GET'])
def list_robots():
    """Lista todos los robots."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, model, active, created_at FROM robots")
    robots = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(robots), 200

@app.route('/api/robots', methods=['POST'])
def create_robot():
    """Crea un robot. JSON: {name, model}."""
    data = request.get_json()
    if not data or 'name' not in data or 'model' not in data:
        return jsonify({"error": "Faltan campos name/model"}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO robots (name, model) VALUES (%s, %s)",
        (data['name'], data['model'])
    )
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({"id": new_id}), 201

@app.route('/api/robots/<int:robot_id>', methods=['PUT'])
def update_robot(robot_id):
    """Actualiza un robot. JSON opcional: {name, model, active}."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON vacío"}), 400

    fields = []
    params = []
    for field in ('name', 'model', 'active'):
        if field in data:
            fields.append(f"{field} = %s")
            params.append(data[field])
    if not fields:
        return jsonify({"error": "Nada que actualizar"}), 400

    params.append(robot_id)
    query = f"UPDATE robots SET {', '.join(fields)} WHERE id = %s"

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, tuple(params))
    conn.commit()
    updated = cursor.rowcount
    cursor.close()
    conn.close()

    if updated == 0:
        return jsonify({"error": "Robot no encontrado"}), 404
    return jsonify({"message": "Actualizado"}), 200

@app.route('/api/robots/<int:robot_id>', methods=['DELETE'])
def delete_robot(robot_id):
    """Elimina un robot por ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM robots WHERE id = %s", (robot_id,))
    conn.commit()
    deleted = cursor.rowcount
    cursor.close()
    conn.close()

    if deleted == 0:
        return jsonify({"error": "Robot no encontrado"}), 404
    return jsonify({"message": "Eliminado"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)