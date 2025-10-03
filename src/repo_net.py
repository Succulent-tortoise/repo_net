
import ast
import os
import networkx as nx

repo_path = "./repo"
G = nx.DiGraph()

# Map for fully qualified names to nodes
fq_name_to_node = {}

def get_python_files(repo_path):
    files = []
    for root, dirs, files_in_dir in os.walk(repo_path):
        for file in files_in_dir:
            if file.endswith(".py"):
                files.append(os.path.join(root, file))
    return files

def parse_file(file_path):
    module_name = os.path.relpath(file_path, repo_path).replace(os.sep, ".").rstrip(".py")
    with open(file_path, "r") as f:
        tree = ast.parse(f.read())
    
    nodes = []
    edges = []
    imported_modules = {}

    for node in ast.walk(tree):
        # Track imports
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported_modules[alias.asname or alias.name] = alias.name
        elif isinstance(node, ast.ImportFrom):
            imported_modules[node.module] = node.module

        # Module-level variables
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
            node_name = f"{module_name}.{node.targets[0].id}"
            G.add_node(node_name, type="variable", module=module_name)
            fq_name_to_node[node_name] = node_name

        # Classes
        if isinstance(node, ast.ClassDef):
            class_name = f"{module_name}.{node.name}"
            G.add_node(class_name,
                       type="class",
                       module=module_name,
                       bases=[ast.unparse(b) for b in node.bases],
                       decorators=[ast.unparse(d) for d in node.decorator_list],
                       docstring=ast.get_docstring(node),
                       lineno=node.lineno)
            fq_name_to_node[class_name] = class_name
            # Methods
            for child in node.body:
                if isinstance(child, ast.FunctionDef):
                    method_name = f"{class_name}.{child.name}"
                    G.add_node(method_name,
                               type="method",
                               module=module_name,
                               args=[a.arg for a in child.args.args],
                               returns=ast.unparse(child.returns) if child.returns else None,
                               decorators=[ast.unparse(d) for d in child.decorator_list],
                               docstring=ast.get_docstring(child),
                               lineno=child.lineno)
                    fq_name_to_node[method_name] = method_name
                    edges.append((class_name, method_name))
                    # Method calls inside class
                    for call in [n for n in ast.walk(child) if isinstance(n, ast.Call)]:
                        if isinstance(call.func, ast.Attribute):
                            edges.append((method_name, call.func.attr))

        # Free functions
        if isinstance(node, ast.FunctionDef):
            func_name = f"{module_name}.{node.name}"
            G.add_node(func_name,
                       type="function",
                       module=module_name,
                       args=[a.arg for a in node.args.args],
                       returns=ast.unparse(node.returns) if node.returns else None,
                       decorators=[ast.unparse(d) for d in node.decorator_list],
                       docstring=ast.get_docstring(node),
                       lineno=node.lineno)
            fq_name_to_node[func_name] = func_name
            # Calls inside the function
            for call in [n for n in ast.walk(node) if isinstance(n, ast.Call)]:
                if isinstance(call.func, ast.Name):
                    edges.append((func_name, f"{module_name}.{call.func.id}"))
                elif isinstance(call.func, ast.Attribute):
                    edges.append((func_name, call.func.attr))
    
    return edges

# Build the graph
all_edges = []
for file_path in get_python_files(repo_path):
    edges = parse_file(file_path)
    all_edges.extend(edges)

G.add_edges_from(all_edges)

# Optional: visualize
import matplotlib.pyplot as plt
plt.figure(figsize=(12, 12))
nx.draw(G, with_labels=True, node_size=2000, node_color="skyblue", font_size=8)
plt.show()

# Save graph for later use
nx.write_graphml(G, "repo_graph.graphml")
