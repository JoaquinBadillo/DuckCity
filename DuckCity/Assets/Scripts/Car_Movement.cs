/*
    Car Movement

    Applies transformations to the car and executes the wheel transformations
    on all wheels each frame.

    Joaquín Badillo, Pablo Bolio
    Last Update: 15/Nov/2023
*/

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Car_Movement : MonoBehaviour {
    // Car Movement
    [SerializeField] Vector3[] wheelOffset;
    [SerializeField] GameObject[] wheels;
    [SerializeField] GameObject wheelPrefab;
    [SerializeField] float angularSpeed = 1.0f;
    private Mesh mesh;
    private Vector3[] position;
    private Vector3[] basePosition;
    private Wheel_Movement[] wheelMovements;
    bool started = false;

    // Lerp
    Vector3 direction;

    public void Start() {
        if (!started){
            mesh = GetComponentInChildren<MeshFilter>().mesh;
            position = mesh.vertices;
            basePosition = new Vector3[position.Length];
            for (int i = 0; i < position.Length; i++)
                basePosition[i] = position[i];

            wheels = new GameObject[4];
            wheelMovements = new Wheel_Movement[4];

            for (int i = 0; i < 4; i++){
                wheels[i] = Instantiate(wheelPrefab, new Vector3(0, 0, 0), Quaternion.identity);
                wheelMovements[i] = wheels[i].GetComponent<Wheel_Movement>();
                wheelMovements[i].Start();
                wheelMovements[i].initialTranslation = wheelOffset[i];
            }
            started = true;
        }
    }

    public void DuckMove(Vector3 destination) {
        Matrix4x4 composite = ApplyTransforms(destination);
        foreach (Wheel_Movement comp in wheelMovements)
            comp.ApplyTransforms(composite, angularSpeed);   
    }

    Matrix4x4 ApplyTransforms(Vector3 destination) {
        float y_angle = Mathf.Atan2(direction.x, direction.z) * Mathf.Rad2Deg;

        Matrix4x4 move = Transformations.TranslationMat(
            destination.x,
            destination.y,
            destination.z
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

    public Vector3 Lerp(Vector3 origin, Vector3 destination, float t){
        Vector3 direction = (destination - origin).normalized;
        
        if (direction != Vector3.zero){
            this.direction = direction;
        }

        return origin + (destination - origin) * t;
    }

    private void OnDestroy() {
        foreach (GameObject wheel in wheels){
            Destroy(wheel);
        }
    }
}
