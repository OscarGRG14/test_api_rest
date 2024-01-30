from flask import Flask, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

# Cargar datos iniciales desde el archivo data.json si existe
try:
    with open('data.json', 'r') as file:
        # Verifica si el archivo está vacío o no
        file_content = file.read()
        data = json.loads(file_content) if file_content else []
except FileNotFoundError:
    data = []
    with open('data.json', 'w') as file:
        json.dump(data, file)

# Función para generar un nuevo ID autoincrementado
def get_next_id():
    if data:
        return max(item['id'] for item in data) + 1
    else:
        return 1

# Ruta para obtener todos los nombres (GET)
@app.route('/names', methods=['GET'])
def get_names():
    return jsonify(data)

# Ruta para agregar un nuevo nombre (POST)
@app.route('/names', methods=['POST'])
def add_name():
    req_data = request.get_json()

    new_name = {
        'id': get_next_id(),
        'name': req_data['name'],
        'created_at': str(datetime.now()),
        'updated_at': str(datetime.now())
    }

    data.append(new_name)

    with open('data.json', 'w') as file:
        json.dump(data, file)

    return jsonify(new_name)

# Ruta para actualizar un nombre existente (PUT)
@app.route('/names/<int:name_id>', methods=['PUT'])
def update_name(name_id):
    req_data = request.get_json()

    for name in data:
        if name['id'] == name_id:
            name['name'] = req_data['name']
            name['updated_at'] = str(datetime.now())

            with open('data.json', 'w') as file:
                json.dump(data, file)

            return jsonify(name)

    return jsonify({'error': 'Name not found'}), 404

# Ruta para eliminar un nombre existente (DELETE)
@app.route('/names/<int:name_id>', methods=['DELETE'])
def delete_name(name_id):
    global data

    data = [name for name in data if name['id'] != name_id]

    with open('data.json', 'w') as file:
        json.dump(data, file)

    return jsonify({'result': 'Name deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
