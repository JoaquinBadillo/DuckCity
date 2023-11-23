/*
    Car Movement

    Applies transformations to the car and executes the wheel transformations
    on all wheels each frame.

    Joaquín Badillo
    Last Update: 15/Nov/2023
*/

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Car_Movement : MonoBehaviour {
    [SerializeField] GameObject[] wheels;
    [SerializeField] Vector2 velocity;
    [SerializeField] Vector2 direction;
    [SerializeField] float angularSpeed = 1.0f;
    private Mesh mesh;
    private Vector3[] position;
    private Vector3[] basePosition;
    private Wheel_Movement[] wheelMovements;

    void Start() {
        mesh = GetComponentInChildren<MeshFilter>().mesh;
        position = mesh.vertices;
        basePosition = new Vector3[position.Length];
        for (int i = 0; i < position.Length; i++)
            basePosition[i] = position[i];

        wheelMovements = new Wheel_Movement[wheels.Length];

        for (int i = 0; i < wheels.Length; i++)
            wheelMovements[i] = wheels[i].GetComponent<Wheel_Movement>();
    }

    void Update() {
        float t = Time.time;
        Matrix4x4 composite = ApplyTransforms(t);

        foreach (Wheel_Movement comp in wheelMovements)
            comp.ApplyTransforms(velocity, composite, angularSpeed, t);   
    }

    Matrix4x4 ApplyTransforms(float time) {
        float y_angle = Mathf.Atan2(direction.x, direction.y) * Mathf.Rad2Deg;

        Matrix4x4 move = Transformations.TranslationMat(
            velocity.x * time,
            0,
            velocity.y * time
        );

        Matrix4x4 y_rotate = Transformations.RotateMat(
            y_angle,
            AXIS.Y
        );

        Matrix4x4 composite =  move * y_rotate;

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

        return composite;
    }
}
