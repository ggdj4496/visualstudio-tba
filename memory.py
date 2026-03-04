import json
import os

MEMORY_FILE = "order_history.json"

def save_order(user_id, order_number):
    # Cargar base de datos local
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r') as f:
            data = json.load(f)
    else:
        data = {}

    # Vincular usuario con su número de orden
    data[str(user_id)] = {
        "last_order": order_number,
        "status": "assimilated"
    }

    with open(MEMORY_FILE, 'w') as f:
        json.dump(data, f, indent=4)
    
    return f"Orden {order_number} registrada para el usuario {user_id}"