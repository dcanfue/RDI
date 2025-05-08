import argparse
import requests

BASE_URL = "http://localhost:8000/api"  # Asegúrate de que este sea el puerto del proxy.py

def listar_robots():
    try:
        response = requests.get(f"{BASE_URL}/robots")
        response.raise_for_status()
        robots = response.json()
        if not robots:
            print("No hay robots registrados.")
        else:
            print("== Lista de Robots ==")
            for robot in robots:
                print(f"ID: {robot['id']} | Nombre: {robot['name']} | Modelo: {robot['model']} | Activo: {'Sí' if robot['active'] else 'No'}")
    except requests.exceptions.RequestException as e:
        print("Error al obtener robots:", e)

def agregar_robot(nombre, modelo):
    try:
        payload = {"name": nombre, "model": modelo}
        response = requests.post(f"{BASE_URL}/robots", json=payload)
        response.raise_for_status()
        print("✅ Robot agregado correctamente.")
    except requests.exceptions.RequestException as e:
        print("Error al agregar robot:", e)

def actualizar_robot(robot_id, nombre=None, modelo=None, activo=None):
    try:
        payload = {}
        if nombre: payload["name"] = nombre
        if modelo: payload["model"] = modelo
        if activo is not None: payload["active"] = activo
        response = requests.put(f"{BASE_URL}/robots/{robot_id}", json=payload)
        response.raise_for_status()
        print("✅ Robot actualizado correctamente.")
    except requests.exceptions.RequestException as e:
        print("Error al actualizar robot:", e)

def eliminar_robot(robot_id):
    try:
        response = requests.delete(f"{BASE_URL}/robots/{robot_id}")
        response.raise_for_status()
        print("🗑️ Robot eliminado correctamente.")
    except requests.exceptions.RequestException as e:
        print("Error al eliminar robot:", e)

def main():
    parser = argparse.ArgumentParser(description="CLI para controlar robots vía proxy.py")
    subparsers = parser.add_subparsers(dest="comando")

    # listar
    subparsers.add_parser("listar", help="Lista todos los robots")

    # agregar
    p_agregar = subparsers.add_parser("agregar", help="Agrega un robot")
    p_agregar.add_argument("--nombre", required=True)
    p_agregar.add_argument("--modelo", required=True)

    # actualizar
    p_actualizar = subparsers.add_parser("actualizar", help="Actualiza un robot")
    p_actualizar.add_argument("--id", required=True, type=int)
    p_actualizar.add_argument("--nombre")
    p_actualizar.add_argument("--modelo")
    p_actualizar.add_argument("--activo", choices=["si", "no"])

    # eliminar
    p_eliminar = subparsers.add_parser("eliminar", help="Elimina un robot")
    p_eliminar.add_argument("--id", required=True, type=int)

    args = parser.parse_args()

    if args.comando == "listar":
        listar_robots()
    elif args.comando == "agregar":
        agregar_robot(args.nombre, args.modelo)
    elif args.comando == "actualizar":
        activo = {"si": True, "no": False}.get(args.activo, None)
        actualizar_robot(args.id, args.nombre, args.modelo, activo)
    elif args.comando == "eliminar":
        eliminar_robot(args.id)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
