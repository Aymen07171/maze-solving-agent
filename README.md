# 🧠 Maze Solving Robot (Goal-Based AI Agent)

An AI project that simulates a **Goal-Based Agent** solving a maze using the **A\*** (A-star) search algorithm with **Pygame visualization**.

---

## 🚀 Features
- Reads any maze grid from a `.txt` file
- Uses **A\*** algorithm for optimal pathfinding
- Real-time visualization with Pygame
- Highlights explored cells and final path

---

## 🧩 PEAS Description
- **Performance Measure:** Reach goal efficiently without hitting walls  
- **Environment:** 2D maze (grid)  
- **Actuators:** Movement (Up, Down, Left, Right)  
- **Sensors:** Detect walls, open paths, and goal position  

---

## ⚙️ Installation

### Clone the Repository
```bash
git clone https://github.com/Aymen07171/maze-solving-agent.git
cd maze-solving-agent
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🎮 Usage

Run the maze solver:
```bash
python src/main.py
```

The program will load a maze from the `mazes/` directory and visualize the A* pathfinding algorithm in action.

---

## 📁 Project Structure
```
maze-solving-agent/
├── src/
│   ├── main.py          # Main entry point
│   ├── maze.py          # Maze loading and visualization
│   └── astar.py         # A* algorithm implementation
├── mazes/               # Maze files (.txt)
└── requirements.txt     # Python dependencies
```
