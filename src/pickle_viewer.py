import pickle
import os
from pyvis.network import Network
import networkx as nx
import matplotlib.pyplot as plt

base_dir = os.path.dirname(os.path.dirname(__file__))  # go up from src/
path = os.path.join(base_dir, "graph_output", "DMP", "repo_graph.pkl")

with open(path, "rb") as f:
    G = pickle.load(f)

# --- Filter edges: keep only 'calls' relationships ---
H = nx.DiGraph([(u, v, d) for u, v, d in G.edges(data=True)
                if d.get("relation") == "calls"])

# (Optional) keep only largest connected component
if H.number_of_nodes() > 2000:
    # take the largest weakly connected component
    largest_cc = max(nx.weakly_connected_components(H), key=len)
    H = H.subgraph(largest_cc).copy()

net = Network(height="800px", width="100%", notebook=False)
net.from_nx(G)
net.show("graph.html", notebook=False)

plt.figure(figsize=(12, 8))
nx.draw_networkx(
    G, 
    with_labels=False, 
    node_size=20, 
    edge_color="lightgrey"
)
plt.show()
