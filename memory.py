import json

def registrar_orden(user_id, n_orden):
    base_datos = "registro_pedidos.json"
    try:
        # Guardar en formato JSON para que sea fácil de leer después
        data = {"user_id": user_id, "orden": n_orden, "status": "completado"}
        with open(base_datos, "a") as f:
            f.write(json.dumps(data) + "\n")
        return True
    except Exception as e:
        print(f"Error en memoria: {e}")
        return False