# TC2008B - Modeling of Multi-Agent Systems with Computer Graphics
# Python Flask server to interact with Unity. 

# Based on Octavio Navarro's sample
# https://github.com/octavio-navarro/TC2008B/blob/main/AgentsVisualization/Server/server.py 

# Last Update: 19/Nov/2023
# Joaquín Badillo

from flask import Flask, request, jsonify, abort, make_response

# Global Variables
types = {
    "car": type(None),
    "obstacle": type(None),
    "road": type(None),
    "stoplight": type(None),
}

model_params = {
    "num_agents": 5,
    "width": 50,
    "height": 50
}

model = None
currentStep = 0

app = Flask(__name__)

@app.route('/init', methods=['POST'])
def initModel():
    global model_params, model, currentStep

    if request.method == 'POST':
        for key in model_params:
            model_params[key] = int(request.form.get(key, model_params[key]))

        # TODO - Initialize model (Requires a model lol)
        model = None

        currentStep = 0
        return jsonify({"message": "Model Initialized"})

@app.route('/agents/<agentType>', methods=['GET'])
def getAgents(agentType):
    global model
    agentType == request.view_args['agentType']

    if request.method == 'GET':
        if model is None:
            abort(make_response(jsonify(message="Model not initialized"), 400))

        if agentType not in types:
            abort(make_response(jsonify(message="Invalid Agent Type"), 400))

        agentPositions = [
            {"id": str(a.unique_id), "x": x, "y":1, "z":z} for a, (x, z)
            in model.grid.coord_iter() if isinstance(a, agentType)
        ]

        return jsonify({'positions':agentPositions})

@app.route('/stats', methods=['GET'])
def getStats():
    if request.method == 'GET':
        stats = {
            "total_cars": 0,
            "concurrent_cars": 0,
            "num_arrivals": 0,
            "num_steps": 0,
        }

        return jsonify({'stats':stats})

@app.route('/update', methods=['GET'])
def updateModel():
    global currentStep, model
    if request.method == 'GET':
        model.step()
        currentStep += 1
        return jsonify({
            'message': 'Model updated.', 
            'currentStep':currentStep
        })

if __name__ == '__main__':
    app.run(port="8080", debug=True)