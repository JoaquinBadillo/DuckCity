/*
    Wheel Movement

    Applies transformations to the wheels.

    Joaquín Badillo
    Last Update: 15/Nov/2023
*/

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Wheel_Movement : MonoBehaviour {
    private Mesh mesh;
    private Vector3[] position;
    private Vector3[] basePosition;
    [SerializeField] Vector3 initialTranslation;

    void Start() {
        mesh = GetComponentInChildren<MeshFilter>().mesh;
        position = mesh.vertices;
        basePosition = new Vector3[position.Length];
        for (int i = 0; i < position.Length; i++)
            basePosition[i] = position[i];
        
        for (int i = 0; i < position.Length; i++)
            position[i] += initialTranslation;

        mesh.vertices = position;
    }

    // Uses the matrix computed by the car to reduce computations.
    public void ApplyTransforms(Vector2 velocity, 
                                Matrix4x4 carComposite, 
                                float angSpeed, 
                                float time) {
        Matrix4x4 initial = Transformations.TranslationMat(
            initialTranslation.x,
            initialTranslation.y,
            initialTranslation.z
        );

        Matrix4x4 rotate = Transformations.RotateMat(
            angSpeed * time,
            AXIS.X
        );

        Matrix4x4 composite =  carComposite * initial * rotate;

        for (int i = 0; i < position.Length; i++) {
            Vector4 vertex = new Vector4(
                basePosition[i].x,
                basePosition[i].y,
                basePosition[i].z,
                1
            );

            position[i] = composite * vertex;
        }

        mesh.vertices = position;
    }
}
