// TC2008B. Sistemas Multiagentes y Gráficas Computacionales
// C# client to interact with Python. Based on the code provided by Sergio Ruiz.
// Octavio Navarro. October 2023

using System;
using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEngine.Networking;

public abstract class ServerData {
    public string id;
    public float x, y, z;
}

[Serializable]
public class AgentData : ServerData {
    public bool arrived;
    public AgentData(string id, float x, float y, float z, bool arrived) {
        this.id = id;
        this.x = x;
        this.y = y;
        this.z = z;
        this.arrived = arrived;
    }
}

[Serializable]
public class StoplightData : ServerData {
    public string color;
    public StoplightData(string id, string color) {
        this.id = id;
        this.color = color;
    }
}

[Serializable]
public class DataList<T> where T : ServerData {
    public List<T> data;
    public DataList() => this.data = new List<T>();
}


public class AgentController : MonoBehaviour {
    [Header("Server Configuration")]
    [SerializeField] string serverUrl = "http://localhost:8080";
    string getAgentsEndpoint = "/agents/";
    string updateEndpoint = "/update";
    string sendConfigEndpoint = "/init";
    DataList<AgentData> agentsData;
    Stack<string> DeathNote;
    DataList<StoplightData> stoplightData;
    Dictionary<string, GameObject> agents;
    Dictionary<string, GameObject> stoplights;
    Dictionary<string, Vector3> prevPositions, currPositions;

    bool updated = false, started = false;

    public GameObject agentPrefab, stoplightPrefab, floor;
    public int NAgents;
    public float timeToUpdate = 5.0f;
    private float timer, dt;

    void Start() {
        agentsData = new DataList<AgentData>();
        stoplightData = new DataList<StoplightData>();

        prevPositions = new Dictionary<string, Vector3>();
        currPositions = new Dictionary<string, Vector3>();

        agents = new Dictionary<string, GameObject>();
        stoplights = new Dictionary<string, GameObject>();

        timer = timeToUpdate;

        DeathNote = new Stack<string>();
        // Launches a couroutine to send the configuration to the server.
        StartCoroutine(SendConfiguration());
    }

    private void Update() {
        if(timer < 0) {
            timer = timeToUpdate;
            updated = false;

            while (DeathNote.Count > 0){
                string targetInSight = DeathNote.Pop();
                Destroy(agents[targetInSight]);
                agents.Remove(targetInSight);
                prevPositions.Remove(targetInSight);
                currPositions.Remove(targetInSight);
            }

            StartCoroutine(UpdateSimulation());
        }

        if (updated) {
            timer -= Time.deltaTime;
            dt = 1.0f - (timer / timeToUpdate);

            // Iterates over the agents to update their positions.
            // The positions are interpolated between the previous and current positions.
            foreach(var agent in currPositions) {
                Vector3 currentPosition = agent.Value;
                Vector3 previousPosition = prevPositions[agent.Key];

                Vector3 interpolated = Vector3.Lerp(previousPosition, currentPosition, dt);
                Vector3 direction = currentPosition - interpolated;

                agents[agent.Key].transform.localPosition = interpolated;
                if(direction != Vector3.zero) agents[agent.Key].transform.rotation = Quaternion.LookRotation(direction);
            }
            // float t = (timer / timeToUpdate);
            // dt = t * t * ( 3f - 2f*t);
        }
    }
 
    IEnumerator UpdateSimulation() {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + updateEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success) {
            Debug.Log(www.error);
        } else {
            StartCoroutine(GetCars());
            StartCoroutine(GetStoplights());
        }
    }

    IEnumerator SendConfiguration() {
        /*
        The SendConfiguration method is used to send the configuration to the server.

        It uses a WWWForm to send the data to the server, and then it uses a UnityWebRequest to send the form.
        */
        WWWForm form = new WWWForm();

        form.AddField("NAgents", NAgents.ToString());

        UnityWebRequest www = UnityWebRequest.Post(serverUrl + sendConfigEndpoint, form);
        www.SetRequestHeader("Content-Type", "application/x-www-form-urlencoded");

        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success) {
            Debug.Log(www.error);
        }
        else {
            Debug.Log("Configuration upload complete!");
            Debug.Log("Getting Agents positions");

            // Once the configuration has been sent, it launches a coroutine to get the agents data.
             StartCoroutine(GetCars());
            StartCoroutine(GetStoplights());
        }
    }

    IEnumerator GetCars() {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getAgentsEndpoint + "car");
        yield return www.SendWebRequest();
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else {
            agentsData = JsonUtility.FromJson<DataList<AgentData>>(www.downloadHandler.text);
            foreach(AgentData agent in agentsData.data) {
                Vector3 newAgentPosition = new Vector3(agent.x, agent.y, agent.z);
                    if(!agents.ContainsKey(agent.id)) {
                        prevPositions[agent.id] = newAgentPosition;
                        agents[agent.id] = Instantiate(agentPrefab, newAgentPosition, Quaternion.identity);
                    } else {
                        Vector3 currentPosition = new Vector3();
                        if(currPositions.TryGetValue(agent.id, out currentPosition))
                            prevPositions[agent.id] = currentPosition;
                        currPositions[agent.id] = newAgentPosition;
                    }
                    if (agent.arrived) DeathNote.Push(agent.id);
            }
            updated = true;
        }
    }

    IEnumerator GetStoplights() {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getAgentsEndpoint + "stoplight");
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else {
            stoplightData = JsonUtility.FromJson<DataList<StoplightData>>(www.downloadHandler.text);
            foreach(StoplightData stoplight in stoplightData.data) {
                Vector3 newStoplightPosition = new Vector3(stoplight.x, stoplight.y, stoplight.z);

                if (!stoplights.ContainsKey(stoplight.id))
                    stoplights[stoplight.id] = Instantiate(stoplightPrefab, newStoplightPosition, Quaternion.identity);

                StoplightController stoplightController = stoplights[stoplight.id].GetComponent<StoplightController>();
                if (stoplightController != null)
                    stoplightController.SetColor(stoplight.color);

            }
        }

        updated = true;
    }
}