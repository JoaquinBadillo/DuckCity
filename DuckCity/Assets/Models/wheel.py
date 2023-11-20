# Wheel Generator Script
# Generates a wheel in a Wavefront .obj file using Unity's coordinate system
# Author: Joaquín Badillo
# Last Update: 08/Nov/2023

import math
import argparse
from functools import reduce


class Node:
    def __init__(self, x, y, z):
        self.coords = (x, y, z)

    # Inner Product
    def dot(self, node):
        return reduce(
            lambda x, y: x + y[0] * y[1], 
            zip(self.coords, node.coords),
            0
        )

    # Normalized Cross Product
    def cross(self, node: "Node"):
        mag = abs(self) * abs(node)
        x = self.coords[1] * node.coords[2] - self.coords[2] * node.coords[1]
        y = self.coords[2] * node.coords[0] - self.coords[0] * node.coords[2]
        z = self.coords[0] * node.coords[1] - self.coords[1] * node.coords[0]
        return Node(x / mag, y / mag, z / mag)

    # Magnitude
    def __abs__(self):
        return math.sqrt(self.dot(self))

    # (Normalized) Cross Product
    def __mul__(self, node):
        return self.cross(node)

    # Vector Subtraction
    def __sub__(self, node):
        x, y, z = tuple(ui - vi for ui, vi in zip(self.coords, node.coords))
        return Node(x, y, z)

    # Writing to file
    def __str__(self):
        return " ".join(f"{x:.7f}" for x in self.coords)


class Triangle:
    def __init__(self, nodes, normal):
        self.nodes = tuple(node for node in nodes)
        self.normal = normal

    def __str__(self):
        return " ".join(f"{point}//{self.normal}" for point in self.nodes)


def angle(i, n):
    return 2 * math.pi * i / n


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--nodes",
        nargs="?",
        default=8,
        dest="n",
        type=int,
        help="Number of nodes for a circle",
    )
    
    parser.add_argument(
        "--radius", 
        nargs="?", 
        default=1.0, 
        dest="r", 
        type=float, 
        help="Circle radius"
    )

    parser.add_argument(
        "--depth", 
        nargs="?", 
        default=0.5, 
        dest="d", 
        type=float, 
        help="Depth"
    )

    args = parser.parse_args()

    if (numNodes := args.n) < 3:
        raise Exception("Number of nodes must be at least 3")

    if (radius := args.r) <= 0:
        raise Exception("Radius must be positive")

    if (depth := args.d) <= 0:
        raise Exception("Depth must be positive")

    nodes = [Node(depth / 2, 0, 0), Node(-depth / 2, 0, 0)]

    normals = [Node(1, 0, 0), Node(-1, 0, 0)]

    faces = []

    currentNode = 2
    currentNormal = 2

    ang = angle(-1, numNodes)
    x = depth / 2

    y = radius * math.sin(ang)
    z = radius * math.cos(ang)

    memo = [
        [Node(x, y, z), 2 * numNodes + 1], 
        [Node(-x, y, z), 2 * numNodes + 2]
    ]

    for i in range(numNodes):
        ang = angle(i, numNodes)

        y = radius * math.sin(ang)
        z = radius * math.cos(ang)

        nodes.append(Node(x, y, z))
        currentNode += 1

        # Front
        faces.append(Triangle([1, currentNode, memo[0][1]], 1))

        nodes.append(Node(-x, y, z))
        currentNode += 1

        # Back
        faces.append(Triangle([2, memo[1][1], currentNode], 2))

        # Normals:
        n1 = nodes[currentNode - 2] - memo[0][0]
        n2 = memo[1][0] - memo[0][0]
        normals.append(n1 * n2)
        currentNormal += 1

        # Side T1
        faces.append(
            Triangle([memo[0][1], currentNode - 1, currentNode], currentNormal)
        )

        # Side T2
        faces.append(
            Triangle([currentNode, memo[1][1], memo[0][1]], currentNormal)
        )

        memo[0] = [nodes[currentNode - 2], currentNode - 1]
        memo[1] = [nodes[currentNode - 1], currentNode]

    # Dump Results to file
    with open("wheel.obj", "w") as f:
        f.write("# Wheel Model\n")
        f.write("# Joaquín Badillo\n")

        f.write(f"\n# {len(nodes)} Points\n")
        for node in nodes:
            f.write(f"v {node}\n")

        f.write(f"\n# {len(normals)} Normals\n")
        for normal in normals:
            f.write(f"vn {normal}\n")

        f.write(f"\n# {len(faces)} Faces\n")
        for face in faces:
            f.write(f"f {face}\n")
