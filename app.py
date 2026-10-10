from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
import datetime

app = Flask(__name__)
CORS(app)


def load_tasks():
    if os.path.exists('tasks.json'):
        with open('tasks.json', 'r') as f:
            tasks = json.load(f)
            return tasks
    else:
        return []


def save_tasks(tasks):
    with open('tasks.json', 'w') as f:
        json.dump(tasks, f, indent=2)


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(load_tasks())


@app.route('/api/tasks', methods=['POST'])
def post_tasks():
    data = request.get_json()
    tasks = load_tasks()
    new_id = max([task['id'] for task in tasks], default=0) + 1
    new_task = {
        'id': new_id,
        'text': data['text'],
        'done': False,
        'created_at': datetime.datetime.now().isoformat(),
        'due_date': data.get('due_date', None)
        }
    tasks.append(new_task)
    save_tasks(tasks)
    return jsonify(new_task), 201


@app.route('/api/tasks/<int:id>', methods=['PUT'])
def change_task(id):
    tasks = load_tasks()
    data = request.get_json()
    for task in tasks:
        if task['id'] == id:
            if data and 'text' in data: task['text'] = data['text']
            elif data and 'due_date' in data: task['due_date'] = data['due_date']
            else: task['done'] = not task['done']
            save_tasks(tasks)
            return jsonify(task)
    return jsonify({'message': 'Task not found'}), 404


@app.route('/api/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task['id'] != id]
    save_tasks(tasks)
    return jsonify({'message': 'Task deleted'})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
