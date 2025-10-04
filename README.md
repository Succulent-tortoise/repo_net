# RepoNet – Python Code Graph Builder

> "A lot o' people don't realize what's really going on. They view life as a bunch o' unconnected incidents 'n things. They don't realize that there's this, like, lattice o' coincidence that lays on top o' everything. Give you an example, show you what I mean: suppose you're thinkin' about a plate o' shrimp. Suddenly someone'll say, like, 'plate,' or 'shrimp,' or 'plate o' shrimp' out of the blue, no explanation. No point in lookin' for one, either. It's all part of a cosmic unconsciousness."
> – Miller (Harry Dean Stanton), *Repo Man*, 1984

---

## Overview

**RepoNet** scans a Python codebase and produces a **structured code graph**, capturing:

* Functions and methods
* Classes and base classes
* Module-level variables
* Dependencies, including cross-file relationships
* Decorators and inheritance relationships

The resulting graph is ideal for **analysis, visualization**, or as a **knowledge resource for language models**.

---

## Folder Structure

```
repo_net/
│
├─ src/
│   └─ repo_net.py        # main scanning script
│
├─ graph_output/
│   └─ <scanned_repo>/    # one folder per scanned repository
│       ├─ repo_graph.gexf   # visualization-compatible graph (lists stored as strings)
│       └─ repo_graph.pkl    # Python-native graph (lists, dicts preserved)
│
├─ requirements.txt
└─ README.md
```

---

## Features

* Recursively scans Python files in a repository
* Extracts functions, classes, methods, and module-level variables
* Tracks decorators, base classes, function arguments, and type hints
* Captures call relationships within and across files
* Stores optional metadata: docstrings, line numbers, file paths
* Generates a fully connected **directed graph**
* Exports graph in **GEXF** and **Pickle** formats for visualization or further processing

---

## Requirements

* Python 3.11+
* `networkx`
* `matplotlib` (optional, for visualization)
* `lxml` (optional, for GraphML export if needed)
* `pickle` (built-in)

Install dependencies using:

```bash
python -m pip install -r requirements.txt
```

---

## Installation

1. Clone or copy this repository:

   ```bash
   git clone https://github.com/<username>/repo_net.git
   ```
2. Create and activate a virtual environment:

   ```bash
   python3 -m venv r_n
   source r_n/bin/activate   # Linux/macOS
   ```
3. Upgrade pip (optional):

   ```bash
   pip install --upgrade pip
   ```
4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

Run the script from the `src/` folder:

```bash
python repo_net.py /path/to/target_repo
```

* `<path/to/target_repo>` is the root folder of the repository you want to scan.
* The output will be written to `graph_output/<scanned_repo>/`.
* Large graphs (>2000 nodes) skip visualization automatically.
* Files with syntax errors, encoding issues, or very large size may be skipped.

---

## Output

1. **GEXF file (`repo_graph.gexf`)**

   * Can be opened in Gephi, yEd, Cytoscape, etc.
   * Node attributes that are lists (arguments, decorators, bases) are stored as semicolon-separated strings.

2. **Pickle file (`repo_graph.pkl`)**

   * Fully preserves all node attributes as Python-native types (lists, dicts).
   * Ideal for querying or processing in Python:

```python
import pickle
import networkx as nx

with open("graph_output/<scanned_repo>/repo_graph.pkl", "rb") as f:
    G = pickle.load(f)

print(len(G.nodes), len(G.edges))
```

---

## Notes and Tips

* `.gitignore` excludes the virtual environment (`r_n/`), temporary files, and generated graph outputs.
* Virtual environments, compiled files, and test archives are skipped by default.
* Each user should create their own virtual environment when cloning the repo.
* Visualization may be skipped automatically if the graph is too large.
* For large repositories, graph generation may take some time depending on the number of files and relationships.
* This tool is intended for reference, analysis, and as a resource for other coding tools or models.

---

## Next Steps and Extensions

* Add embeddings for nodes to integrate with a language model
* Support additional metadata or external libraries
* Extend support to other programming languages by adapting the AST parsing

---

"Did you take a lot acid Miller? Back in the 60's?" - Otto (Emilo Estevez), Repo Man, 1984


## Author

**Matt Donnelly**
