# Missionaries and Cannibals – BFS Search Project

## 📌 Project Overview

The **Missionaries and Cannibals** problem is a classic Artificial Intelligence (AI) search problem. The objective is to transport three missionaries and three cannibals from the left bank of a river to the right bank using a boat that can carry a maximum of two people.

The boat cannot cross the river empty, and the number of cannibals must never exceed the number of missionaries on either bank whenever missionaries are present.

This project uses **Breadth-First Search (BFS)** to find the shortest solution while ensuring that all intermediate states are valid and safe.

The project also provides an animated river-crossing simulation, state-space graph, BFS state-space tree, and a report of the solution.

## 🎯 Objectives

- Understand the working of Breadth-First Search (BFS).
- Represent the problem using states and transitions.
- Identify safe and unsafe states.
- Find the shortest sequence of river crossings.
- Visualize the state-space graph and search tree.
- Animate the river-crossing process.
- Generate a report containing the solution path and BFS exploration order.

## 🛠️ Technologies Used

- **Programming Language:** Python
- **Search Algorithm:** Breadth-First Search (BFS)
- **Graph Visualization:** NetworkX
- **Plotting and Animation:** Matplotlib
- **GIF Generation:** Pillow
- **Data Structure:** Queue using `collections.deque`

## 🧠 Problem Formulation

### Initial State

All three missionaries and three cannibals are on the left bank.

`(3, 3, L)`

### Goal State

All missionaries and cannibals are on the right bank.

`(0, 0, R)`

### State Representation

Each state is represented as:

`(M, C, B)`

Where:

- `M` = Number of missionaries on the left bank.
- `C` = Number of cannibals on the left bank.
- `B` = Position of the boat (`L` for left bank and `R` for right bank).

### Constraints

1. The boat can carry one or two people.
2. The boat cannot cross the river empty.
3. The number of missionaries and cannibals on either bank must remain valid.
4. Cannibals must not outnumber missionaries on a bank whenever missionaries are present.
5. Every crossing must produce a valid state.

## ⚙️ Algorithm: Breadth-First Search (BFS)

BFS explores states level by level using a queue. Since every river crossing has equal cost, BFS finds a solution with the minimum number of crossings.

### Algorithm Steps

1. Initialize the starting state.
2. Insert the starting state into the queue.
3. Maintain a visited set to avoid revisiting states.
4. Remove a state from the front of the queue.
5. Generate all possible boat crossings.
6. Validate each resulting state.
7. Add valid, unvisited states to the queue.
8. Store parent states to reconstruct the solution path.
9. Stop when the goal state is reached.
10. Generate the visualizations and solution report.

## 📂 Project Structure

```text
missionaries-and-cannibals/
│
├── missionaries_cannibals_animated.py
├── requirements.txt
├── README.md
│
└── bfs_outputs/
    ├── river_crossing.gif
    ├── state_space_graph.png
    ├── state_space_tree.png
    ├── crossing_sequence.png
    └── solution_report.txt
```

The `bfs_outputs/` folder is generated when the program runs successfully.

## 📦 Installation and Setup

### Prerequisites

- Python installed on your system.
- Git installed on your system (for uploading through the terminal).
- Visual Studio Code or another Python editor (optional).

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/missionaries-and-cannibals.git
```

Replace `YOUR_USERNAME` with your GitHub username.

### Step 2: Open the Project Folder

```bash
cd missionaries-and-cannibals
```

### Step 3: Install Dependencies

```bash
python -m pip install -r requirements.txt
```

The required libraries include:

- `matplotlib`
- `networkx`
- `pillow`

The `requirements.txt` file specifies the package versions used by the project.

### Step 4: Run the Program

```bash
python missionaries_cannibals_animated.py
```

After successful execution, the program displays the BFS solution and generates the output files inside `bfs_outputs/`.

## 📊 Project Outputs

### 1. Animated River Crossing

**File:** `river_crossing.gif`

Shows the river-crossing process, including the movement of the boat and the changing positions of missionaries and cannibals.

### 2. State-Space Graph

**File:** `state_space_graph.png`

Displays the discovered states and legal transitions. The shortest solution path is highlighted.

### 3. BFS State-Space Tree

**File:** `state_space_tree.png`

Displays the parent-child relationships created during BFS exploration.

### 4. Crossing Sequence Chart

**File:** `crossing_sequence.png`

Shows how the numbers of missionaries and cannibals on the left bank change throughout the solution.

### 5. Solution Report

**File:** `solution_report.txt`

Contains the initial and goal states, shortest solution path, crossing sequence, and BFS exploration order.

## 💡 Key Features

- BFS-based shortest-path search.
- Safe-state validation.
- Prevention of repeated state exploration.
- Parent tracking for solution reconstruction.
- State-space graph visualization.
- BFS tree visualization.
- Animated river-crossing simulation.
- Automatic generation of a solution report.

## 🎓 Learning Outcomes

By completing this project, students can understand:

- State-space representation in Artificial Intelligence.
- Uninformed search algorithms.
- Queue-based graph traversal.
- State validation and constraint satisfaction.
- Parent pointers and path reconstruction.
- Graph visualization using Python.
- Animation generation using Matplotlib.

## 🚀 Future Enhancements

- Add a graphical user interface.
- Allow users to change the number of missionaries and cannibals.
- Compare BFS with Depth-First Search (DFS) and Iterative Deepening Search.
- Display the explored states interactively.
- Add an interactive game mode.


