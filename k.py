from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = []


def generate_task_id():
    return len(tasks) + 1


@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    title = data.get('title')
    if title is None:
        return jsonify({'error': 'Title is required'}), 400

    task_id = generate_task_id()
    new_task = {'id': task_id, 'title': title, 'completed': False}
    tasks.append(new_task)
    return jsonify(new_task), 201


@app.route('/tasks', methods=['GET'])
def list_tasks():
    return jsonify({'tasks': tasks})


@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(task)


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t['id'] != task_id]
    return jsonify({'message': 'Task deleted successfully'})


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def edit_task(task_id):
    data = request.json
    title = data.get('title')
    completed = data.get('completed')

    task = next((t for t in tasks if t['id'] == task_id), None)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404

    if title is not None:
        task['title'] = title
    if completed is not None:
        task['completed'] = completed

    return jsonify(task)


# Extra Credit: Bulk add multiple tasks
@app.route('/tasks/bulk', methods=['POST'])
def bulk_add_tasks():
    data = request.json
    if not isinstance(data, list):
        return jsonify({'error': 'Invalid data format, expecting a list of tasks'}), 400

    new_tasks = []
    for task_data in data:
        title = task_data.get('title')
        if title is not None:
            task_id = generate_task_id()
            new_task = {'id': task_id, 'title': title, 'completed': False}
            new_tasks.append(new_task)

    tasks.extend(new_tasks)
    return jsonify({'tasks': new_tasks}), 201


# Extra Credit: Bulk delete multiple tasks
@app.route('/tasks/bulk', methods=['DELETE'])
def bulk_delete_tasks():
    data = request.json
    if not isinstance(data, list):
        return jsonify({'error': 'Invalid data format, expecting a list of task ids'}), 400

    global tasks
    tasks = [t for t in tasks if t['id'] not in data]
    return jsonify({'message': 'Tasks deleted successfully'})


if __name__ == '__main__':
    app.run(debug=True)
