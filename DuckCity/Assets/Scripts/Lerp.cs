/* 
    Lerp - Linear Interpolation
    Lerp is a function that takes 3 parameters: 
    * a start value
    * an end value
    * and a "t" value (between 0 and 1)

    It then calculates an intermediate position between the 
    start and end values based on the t value.
*/

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Lerp : MonoBehaviour
{
    [SerializeField] private Vector3 startPos;
    [SerializeField] private Vector3 finalPos;
    [Range(0.0f, 1.0f)]
    [SerializeField] private float t;

    [SerializeField] float moveTime = 3.0f;
    [SerializeField] float elapsedTime = 0.0f;
    void Start() {

    }

    void Update() {
        t = (elapsedTime / moveTime);
        t *= t * (3.0f - 2.0f * t);
        Vector3 position = startPos + (finalPos - startPos) * t;
        
        transform.position = position;

        elapsedTime += Time.deltaTime;

        if (elapsedTime >= moveTime) {
            Vector3 temp = startPos;
            startPos = finalPos;
            finalPos = temp;

            elapsedTime = 0.0f;
        }
    }
}
