from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app_pais = Flask(__name__)
CORS(app_pais)

tasks_pais = [
    {"id": 1, "task": "Belajar Python", "completed": False},
    {"id": 2, "task": "Mengerjakan tugas kuliah", "completed": False},
    {"id": 3, "task": "Membuat aplikasi sederhana", "completed": False},
]

backup_file_path = 'backup.json'

if os.path.exists(backup_file_path) and os.path.getsize(backup_file_path) > 0:
    with open(backup_file_path, 'r') as json_file:
        tasks_pais = json.load(json_file)

@app_pais.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks_pais)

@app_pais.route('/tasks', methods=['POST'])
def add_task():
    new_task_pais = request.json
    new_task_pais['id'] = max(task['id'] for task in tasks_pais) + 1 if tasks_pais else 1
    new_task_pais['completed'] = False
    tasks_pais.append(new_task_pais)
    return jsonify(new_task_pais), 201

@app_pais.route('/tasks/<int:task_id_pais>', methods=['PUT'])
def update_task(task_id_pais):
    for task_pais in tasks_pais:
        if task_pais['id'] == task_id_pais:
            task_pais['completed'] = not task_pais['completed']
            return jsonify(task_pais)
    return jsonify({"error": "Task not found"}), 404

@app_pais.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks_pais
    tasks_pais = [task_pais for task_pais in tasks_pais if task_pais['id'] != task_id]
    return jsonify({"message": "Task deleted"})

@app_pais.route('/tasks/backup', methods=['GET'])
def backup_tasks():
    with open('backup.txt', 'w') as f:
        for task_pais in tasks_pais:
            f.write(f"{task_pais['id']}: {task_pais['task']} ({'completed' if task_pais['completed'] else 'not completed'})\n")

    with open('backup.json', 'w') as json_file:
        json.dump(tasks_pais, json_file)

    return jsonify({"message": "Backup created"})
    

if __name__ == '__main__':
    app_pais.run(debug=True)