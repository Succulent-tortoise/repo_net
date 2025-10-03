
Repo Graph Builder
==================

Overview:
---------
This project scans a Python codebase and generates a structured graph
representing functions, classes, module-level variables, and their
dependencies, including cross-file relationships. The resulting graph
can be used for analysis, visualization, or as a coding knowledge
resource for language models.

Features:
---------
- Recursively scans a repository for Python files
- Extracts functions, classes, methods, and module-level variables
- Tracks decorators, base classes, function arguments, and type hints
- Captures call relationships within and across files
- Stores optional metadata: docstrings, line numbers, file paths
- Generates a fully connected directed graph
- Graph export in GraphML format for visualization or further processing

Requirements:
-------------
- Python 3.8+
- networkx
- matplotlib (optional, for visualization)

Installation:
-------------
1. Clone or copy this repo:
   git clone <repo_url>
2. Install dependencies:
   pip install networkx matplotlib

Usage:
------
1. Point the `repo_path` variable in `main.py` to the root of your Python repo.
2. Run:
   python main.py
3. Output:
   - `repo_graph.graphml` in the project root
   - Optional visualization of the graph in a popup window

Ne
