using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class StoplightController : MonoBehaviour {
    [Header("Lights")]
    [SerializeField] Light lt;

    public void SetColor(string color) {
        if (lt == null) {
            return;
        }

        switch (color) {
            case "red":
                lt.color = Color.red;
                lt.intensity = 0.5f;
                break;
            case "yellow":
                lt.color = Color.yellow;
                lt.intensity = 0.5f;
                break;
            case "green":
                lt.color = Color.green;
                lt.intensity = 0.5f;
                break;
            default:
                lt.intensity = 0.0f;
                break;
        }
    }
}
