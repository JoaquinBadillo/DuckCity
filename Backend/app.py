# TC2008B - Modeling of Multi-Agent Systems with Computer Graphics
# Python Flask server to interact with Unity. 

# Based on Octavio Navarro's sample
# https://github.com/octavio-navarro/TC2008B/blob/main/AgentsVisualization/Server/server.py 

# Last Update: 19/Nov/2023
# Joaquín Badillo

from flask import Flask, request, jsonify, abort
from TrafficSimulation.agents import Car, Stoplight
from TrafficSimulation.model import TrafficModel

# Global Variables

# Maps each agent str type to a dictionary
# Its cool this way, because we can dynamically add agents and data to serve
agents = {
    "car": {
        "type": Car,
        "collection": None,
        "reducer": lambda agent: {
            "id": agent.unique_id, 
            "x": agent.pos[0],
            "y": 0,
            "z": agent.pos[1],
        }
    },
    "stoplight": {
        "type": Stoplight,
        "collection": None,
        "reducer": lambda agent: {
            "id": agent.unique_id,
            "color": agent.state.name.lower()
        }
    }
}

model = None

app = Flask("app")

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"message": "Resource not found"}), 404

@app.errorhandler(400)
def bad_request(e):
    return jsonify({"message": "Bad request"}), 400

@app.route('/init', methods=['POST'])
def initModel():
    global model

    if request.method == 'POST':
        model = TrafficModel()
        agents["car"]["collection"] = lambda: model.schedule.agents
        agents["stoplight"]["collection"] = lambda: model.traffic_lights
        
        return jsonify({"message": "Model Initialized"})

@app.route('/agents/<agentType>', methods=['GET'])
def getAgents(agentType):
    global model, agents
    agentType == request.view_args['agentType']

    if request.method == 'GET':
        # Handle bad requests
        if model is None: abort(400)
        if agentType not in agents: abort(400)

        datatype = agents[agentType]['type']
        reducer = agents[agentType]['reducer']
        collect = agents[agentType]['collection']

        data = map(
            reducer,
            [agent for agent in collect() if isinstance(agent, datatype)]
        )

        return jsonify({'data': list(data)})

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
    global model
    if request.method == 'GET':
        model.step()
        return jsonify({
            'message': 'Model updated.', 
            'currentStep': model.num_steps
        })

if __name__ == '__main__':
    app.run(port="8080", debug=True)
