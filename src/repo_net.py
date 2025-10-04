import ast
import os
import sys
import networkx as nx
import pickle

# Optional: visualization
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

# -----------------------------
# 1. Get target repo path
# -----------------------------
if len(sys.argv) > 1:
    repo_path = sys.argv[1]
else:
    print("Usage: python repo_net.py /path/to/target_repo")
    sys.exit(1)

repo_name = os.path.basename(os.path.normpath(repo_path))
output_root = "/media/matthew/Projects_Vault/repo_net/graph_output"
output_folder = os.path.join(output_root, repo_name)
os.makedirs(output_folder, exist_ok=True)
output_gexf = os.path.join(output_folder, "repo_graph.gexf")
output_pickle = os.path.join(output_folder, "repo_graph.pkl")

# -----------------------------
# 2. Prepare Graph
# -----------------------------
G = nx.DiGraph()
fq_name_to_node = {}

# -----------------------------
# 3. Utility: get all python files recursively
# -----------------------------
def get_python_files(repo_path, max_file_size=None):
    files = []
    skip_dirs = {"__pycache__", ".git", "venv", "dmpenv", "tests/archived", "node_modules", "data"}
    for root, dirs, files_in_dir in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for file in files_in_dir:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                if max_file_size is None or os.path.getsize(full_path) <= max_file_size:
                    files.append(full_path)
    return files

# -----------------------------
# 4. Serialize lists to string
# -----------------------------
def list_to_str(lst):
    return ";".join(lst) if lst else ""

# -----------------------------
# 5. Parse a single file
# -----------------------------
def parse_file(file_path):
    module_name = os.path.relpath(file_path, repo_path).replace(os.sep, ".").rstrip(".py")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()
        tree = ast.parse(source)
    except (SyntaxError, IndentationError) as e:
        print(f"Skipping {file_path}: {e}")
        return []
    except UnicodeDecodeError:
        print(f"Skipping {file_path}: cannot decode (not UTF-8)")
        return []

    edges = []

    for node in ast.walk(tree):
        # Module-level variables
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
            node_name = f"{module_name}.{node.targets[0].id}"
            G.add_node(node_name, type="variable", module=module_name)
            fq_name_to_node[node_name] = node_name

        # Classes and methods
        if isinstance(node, ast.ClassDef):
            class_name = f"{module_name}.{node.name}"
            G.add_node(
                class_name,
                type="class",
                module=module_name,
                bases=list_to_str([ast.unparse(b) for b in node.bases]),
                decorators=list_to_str([ast.unparse(d) for d in node.decorator_list]),
                docstring=ast.get_docstring(node) or "",
                lineno=node.lineno,
            )
            fq_name_to_node[class_name] = class_name

            # Methods inside class
            for child in node.body:
                if isinstance(child, ast.FunctionDef):
                    method_name = f"{class_name}.{child.name}"
                    G.add_node(
                        method_name,
                        type="method",
                        module=module_name,
                        args=list_to_str([a.arg for a in child.args.args]),
                        returns=ast.unparse(child.returns) if child.returns else "",
                        decorators=list_to_str([ast.unparse(d) for d in child.decorator_list]),
                        docstring=ast.get_docstring(child) or "",
                        lineno=child.lineno,
                    )
                    fq_name_to_node[method_name] = method_name
                    edges.append((class_name, method_name))

                    # Method calls inside class
                    for call in [n for n in ast.walk(child) if isinstance(n, ast.Call)]:
                        if isinstance(call.func, ast.Attribute):
                            edges.append((method_name, call.func.attr))

        # Free functions
        if isinstance(node, ast.FunctionDef):
            func_name = f"{module_name}.{node.name}"
            G.add_node(
                func_name,
                type="function",
                module=module_name,
                args=list_to_str([a.arg for a in node.args.args]),
                returns=ast.unparse(node.returns) if node.returns else "",
                decorators=list_to_str([ast.unparse(d) for d in node.decorator_list]),
                docstring=ast.get_docstring(node) or "",
                lineno=node.lineno,
            )
            fq_name_to_node[func_name] = func_name

            # Function calls
            for call in [n for n in ast.walk(node) if isinstance(n, ast.Call)]:
                if isinstance(call.func, ast.Name):
                    edges.append((func_name, f"{module_name}.{call.func.id}"))
                elif isinstance(call.func, ast.Attribute):
                    edges.append((func_name, call.func.attr))

    return edges

# -----------------------------
# 6. Build the repo-wide graph
# -----------------------------
def main():
    all_edges = []
    files = get_python_files(repo_path, max_file_size=1_000_000)  # skip huge files
    skipped_files = 0

    for file_path in files:
        edges = parse_file(file_path)
        if not edges:  # could be skipped or empty
            skipped_files += 1
        all_edges.extend(edges)

    G.add_edges_from(all_edges)

    # -----------------------------
    # Safe visualization
    # -----------------------------
    if MATPLOTLIB_AVAILABLE:
        if len(G.nodes) < 2000:
            plt.figure(figsize=(12, 12))
            nx.draw(
                G,
                with_labels=True,
                node_size=2000,
                node_color="skyblue",
                font_size=8,
            )
            plt.show()
        else:
            print(f"Graph too large to visualize ({len(G.nodes)} nodes), skipping draw")
    else:
        print("Matplotlib not available, skipping visualization")

    # -----------------------------
    # Save graph: GEXF & pickle
    # -----------------------------
    nx.write_gexf(G, output_gexf)
    with open(output_pickle, "wb") as f:
        pickle.dump(G, f)

    print(f"Graph saved to GEXF: {output_gexf}")
    print(f"Graph saved to Pickle: {output_pickle}")

    # -----------------------------
    # Summary
    # -----------------------------
    print("---------- Scan Summary ----------")
    print(f"Total Python files scanned: {len(files)}")
    print(f"Files skipped due to parse errors or size: {skipped_files}")
    print(f"Total nodes in graph: {len(G.nodes)}")
    print(f"Total edges in graph: {len(G.edges)}")
    print("---------------------------------")

# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    main()
