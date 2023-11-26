using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class StoplightController : MonoBehaviour {
    [Header("Lights")]
    Light lt;

    public void Start() {
        lt = GetComponentInChildren<Light>();
    }

    public void SetColor(string color) {
        if (lt == null)
            return;

        switch (color) {
            case "red":
                lt.color = Color.red;
                lt.intensity = 1.0f;
                break;
            case "yellow":
                lt.color = Color.yellow;
                lt.intensity = 1.0f;
                break;
            case "green":
                lt.color = Color.green;
                lt.intensity = 1.0f;
                break;
            default:
                lt.intensity = 0.0f;
                break;
        }
    }
}
