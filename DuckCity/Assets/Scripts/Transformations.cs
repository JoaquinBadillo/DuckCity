/*
    Transformation Matrices

    Includes rotations, traslation and scaling matrices.

    Gilberto Echeverria, Joaquín Badillo
    Last Update: 03/Nov/2023
*/


using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public enum AXIS {X, Y, Z};

public class Transformations : MonoBehaviour {
    public static Matrix4x4 TranslationMat(float tx, float ty, float tz) {
        Matrix4x4 matrix = Matrix4x4.identity;
        matrix[0, 3] = tx;
        matrix[1, 3] = ty;
        matrix[2, 3] = tz;
        return matrix;
    }

    public static Matrix4x4 ScaleMat(float sx, float sy, float sz) {
        Matrix4x4 matrix = Matrix4x4.identity;
        matrix[0, 0] = sx;
        matrix[1, 1] = sy;
        matrix[2, 2] = sz;
        return matrix;
    }

    // Angle is in degrees*
    public static Matrix4x4 RotateMat(float angle, AXIS axis) {
        float rads = angle * Mathf.Deg2Rad;
        float st = Mathf.Sin(rads);
        float ct = Mathf.Cos(rads);

        Matrix4x4 matrix = Matrix4x4.identity;
        if (axis == AXIS.X) {
            matrix[1, 1] = ct;
            matrix[1, 2] = -st;
            matrix[2, 1] = st;
            matrix[2, 2] = ct;
        } else if (axis == AXIS.Y) {
            matrix[0, 0] = ct;
            matrix[0, 2] = st;
            matrix[2, 0] = -st;
            matrix[2, 2] = ct;
        } else if (axis == AXIS.Z) {
            matrix[0, 0] = ct;
            matrix[0, 1] = -st;
            matrix[1, 0] = st;
            matrix[1, 1] = ct;
        }

        return matrix;
    }
}
