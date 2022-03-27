from flask import Flask, jsonify, abort, request

app = Flask(__name__)

tasks = [
    {
        "id": 1,
        "name": "Tomar la clase",
        "check": False,

    },
    {
        "id": 2,
        "name": "Hacer la tarea",
        "check": False,
    },
]

@app.route('/')
def hello_world():
    return '<h1>----- Bienvenido a mi API To-Do List -----</h1>'

#URI: /api/
#-------------------------------------------------------------
#Funcion con GET
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks, 'status': 'Todo OK'})

#-------------------------------------------------------------
#Funcion con GET
@app.route('/api/tasks/<int:id>', methods=['GET'])
def get_task(id):
    for task in tasks:
        if task['id'] == id:
            return jsonify({'task': task})
    return jsonify({'status': 'ID inexistente'})


#------------------- TASKS V1 ---------------------------------
#Funcion con GET
@app.route('/api/v1/tasks/<int:id>', methods=['GET'])
def get_task_v1(id):
    this_task = [task for task in tasks if task['id'] == id]
    if not this_task:
        abort(404)
    return jsonify({'task': this_task[0]})

#return jsonify({'task': this_task[0]}) if this_task else jsonify({"status": })      
#return jsonify({'tasks': [task for task in tasks if task ['id'] == id][0]})    
    

#------------------- TASKS V2 ---------------------------------
@app.route('/api/v2/tasks/<int:id>', methods=['GET'])
def get_task_v2(id):
    this_task = [task for task in tasks if task['id'] == id]
    return jsonify({'task': this_task[0]}) if this_task else jsonify({'status': 'ID inexistente'})
    
    

#--------------------------------------------------------------
#Funcion con POST
@app.route('/api/tasks', methods=['POST'])
def create_task():
    if not request.json:
        abort(404)
    task = {
        'id': len(tasks)+1,
        'name': request.json['name'],
        'check': False
    }
    tasks.append(task)
    return jsonify({'tasks': tasks}), 201       
#--------------------------------------------------------------
#Funcion con PUT
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    if not request.json:
        abort(400)
     
    this_task = [task for task in tasks if task['id'] == task_id]
    #print(request.json['name'])
    if not this_task:
        abort(404)

    if 'name' in request.json and type(request.json.get('name')) is not str:
        abort(400)

    if 'check' in request.json and type(request.json.get('check')) is not bool:
        abort(400)

    this_task[0]['check'] = request.json.get('check', this_task[0]['check'])
    this_task[0]['name'] = request.json.get('name', this_task[0]['name'])
    
    #this_task[0]['name'] = request.json['name'] if request.json['name'] else this_task[0]
    
    #try:
    #    this_task[0]['name'] = request.json['name'] if request.json['name'] else this_task[0]
    #except:
    #    print("name not found")    


    return jsonify({'task': this_task[0]}), 201
    
    #this_task[0]['check'] = request.json.get('check')
#--------------------------------------------------------------
#Funcion con Delete
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    this_task = [task for task in tasks if task['id'] == task_id]

    if not this_task:
        abort(404)

    tasks.remove(this_task[0])
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug = True)    

    



