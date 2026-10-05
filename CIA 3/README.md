# CampusNet – Minimum-Cost Campus Network Planner

## Project Overview

CampusNet is a small, educational prototype developed to demonstrate the practical application of **Kruskal's Algorithm** and the **Minimum Spanning Tree (MST)** concept in a college campus networking scenario.

The goal is to determine the minimum-cost network that connects every building on campus. This is a simplified educational simulation.

## Problem Being Solved

Given a set of buildings (vertices) and possible network connections between them with associated installation costs (weighted edges), the objective is to connect all buildings using the minimum total cost, ensuring there are no redundant loops (cycles). 

## Algorithm Used: Kruskal's Algorithm

Kruskal's algorithm is a greedy algorithm that finds a minimum spanning tree for a connected weighted graph. It finds a subset of the edges that forms a tree that includes every vertex, where the total weight of all the edges in the tree is minimized.

### How Kruskal's Algorithm Works

1. **Sort** all possible network connections (edges) by their installation cost from lowest to highest.
2. **Pick** the cheapest available connection.
3. **Check** whether adding this connection forms a loop (cycle) among the buildings.
4. **Accept** the connection if it does NOT create a cycle.
5. **Reject** the connection if it DOES create a cycle.
6. **Continue** this process until all buildings are connected (which requires exactly V-1 connections for V buildings).

To efficiently detect cycles, the implementation manually uses a **Disjoint Set (Union-Find)** data structure with Path Compression and Union by Rank.

## Complexity

- **Time Complexity:** `O(E log E)`
  - The dominant operation is sorting the edges based on their cost. The manual Union-Find operations take nearly `O(1)` time due to path compression and union by rank.
- **Space Complexity:** `O(V + E)`
  - Required to store the graph structures (nodes and edges) and the Union-Find parent/rank arrays.

## Installation Instructions

Ensure you have Python installed. It is recommended to use a virtual environment.

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

Run the Streamlit application using the following command:
```bash
streamlit run app.py
```

## How to Use the Interface

1. **View the Graph:** The initial graph displays all possible network connections between buildings as grey lines, with their respective costs.
2. **Next Step:** Click the "Next Step" button to manually advance the algorithm one edge at a time. The current edge being evaluated will be highlighted in orange.
3. **Run Automatically:** Click "Run Kruskal Automatically" to watch the algorithm execute step-by-step automatically until completion.
4. **Show Final MST:** Click to skip the step-by-step process and immediately view the completed Minimum Spanning Tree.
5. **Reset:** Start the algorithm over from the beginning.
6. **Edge Table:** Scroll down to see a real-time table of edges that have been accepted or rejected.
7. **Final Results:** Once finished, a summary of the total cost and connected buildings will be displayed.
