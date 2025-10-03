RepoNet – Python Code Graph Builder

"A lot o' people don't realize what's really going on. They view life as a bunch o' unconnected incidents 'n things. They don't realize that there's this, like, lattice o' coincidence that lays on top o' everything. Give you an example, show you what I mean: suppose you're thinkin' about a plate o' shrimp. Suddenly someone'll say, like, 'plate,' or 'shrimp,' or 'plate o' shrimp' out of the blue, no explanation. No point in lookin' for one, either. It's all part of a cosmic unconsciousness."
– Miller (Harry Dean Stanton), Repo Man, 1984

Overview

RepoNet scans a Python codebase and produces a structured code graph, capturing:

Functions and methods

Classes and base classes

Module-level variables

Dependencies, including cross-file relationships

The resulting graph is ideal for analysis, visualization, or as a knowledge resource for language models.

Features

Recursively scans Python files in a repository

Extracts functions, classes, methods, and module-level variables

Tracks decorators, base classes, function arguments, and type hints

Captures call relationships within and across files

Stores optional metadata: docstrings, line numbers, file paths

Generates a fully connected directed graph

Exports graph in GraphML format for visualization or further processing

Requirements

Python 3.8 or higher

networkx

matplotlib (optional, for visualization)

Installation

Clone or copy this repository:

git clone https://github.com/<username>/repo_net.git


Create and activate a virtual environment:

python3 -m venv r_n
source r_n/bin/activate   # Linux/macOS


Upgrade pip (optional):

pip install --upgrade pip


Install dependencies:

pip install -r requirements.txt

Usage

Set the repo_path variable in main.py to the root of your Python repository.

Run the script:

python main.py


Output:

repo_graph.graphml in the project root

Optional popup window to visualize the graph

Notes and Tips

.gitignore excludes the virtual environment (r_n/), temporary files, and generated graph outputs.

Each user should create their own virtual environment when cloning the repo.

For large repositories, graph generation may take some time depending on the number of files and relationships.

Next Steps and Extensions

Add embeddings for nodes to integrate with a language model

Support additional metadata or external libraries

Extend support to other programming languages by adapting the AST parsing

Author

Matt Donnelly
