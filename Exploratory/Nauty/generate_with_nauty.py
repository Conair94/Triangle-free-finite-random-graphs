import subprocess
import networkx as nx
import matplotlib.pyplot as plt
import argparse
import pickle
import os
import sys
import itertools

def check_geng_availability():
    """Checks if geng is available in the system path."""
    try:
        subprocess.run(["geng", "--help"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        return True
    except FileNotFoundError:
        return False

def generate_graphs(n):
    """Generates triangle-free connected graphs of size n using geng."""
    # Command: geng -ct n
    # -c: connected
    # -t: triangle-free
    # -q: suppress auxiliary output
    cmd = ["geng", "-ctq", str(n)]
    
    print(f"Running command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running geng: {e}")
        return []

    graph_lines = result.stdout.strip().split('\n')
    graphs = []
    for line in graph_lines:
        if line:
            # graph6 strings might have trailing newlines or whitespace
            line = line.strip()
            if not line: continue
            try:
                G = nx.from_graph6_bytes(line.encode('ascii'))
                graphs.append(G)
            except Exception as e:
                print(f"Failed to parse graph6 line '{line}': {e}")
            
    return graphs

def is_independent_set(G, nodes):
    """Checks if the given set of nodes forms an Independent Set."""
    for u, v in itertools.combinations(nodes, 2):
        if G.has_edge(u, v):
            return False
    return True

def check_corollary_4_properties(G):
    """
    Checks if graph satisfies Corollary 4 properties:
    1. Every independent set of size <= 3 has a common neighbor.
    2. Twin-free (no two vertices have same neighbors).
    3. Not isomorphic to Andrasfai graph O_{3n-1}.
    """
    # Property 1: Common neighbor for IS of size <= 3
    nodes = list(G.nodes())
    for k in range(1, 4): # Sizes 1, 2, 3
        # If graph is smaller than k, we can't form size k sets, so strictly speaking condition holds vacuously?
        # Or does it fail? Usually implies "for all sets THAT EXIST".
        if len(nodes) < k:
            continue

        for subset in itertools.combinations(nodes, k):
            if is_independent_set(G, subset):
                # Check for common neighbor
                if not subset:
                    continue
                
                common_neighbors = set(G.neighbors(subset[0]))
                for node in subset[1:]:
                    common_neighbors &= set(G.neighbors(node))
                
                if not common_neighbors:
                    return False

    # Property 2: Twin-free
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            u, v = nodes[i], nodes[j]
            if set(G.neighbors(u)) == set(G.neighbors(v)):
                return False

    # Property 3: Not isomorphic to Andrasfai graph
    N = G.number_of_nodes()
    # Check if N is of form 3k - 1
    if (N + 1) % 3 == 0:
        # Construct Andrasfai graph of size N
        # Vertices 0..N-1
        # Edge (u, v) if (v-u) % N % 3 == 1
        A = nx.Graph()
        A.add_nodes_from(range(N))
        for u in range(N):
            for v in range(u + 1, N):
                diff = (v - u) % N
                if diff % 3 == 1:
                    A.add_edge(u, v)
        
        if nx.is_isomorphic(G, A):
            return False

    return True

def visualize_graphs(graphs, n, output_dir, n_show=4):
    """Visualizes a few graphs."""
    if not graphs:
        print("No graphs to visualize.")
        return

    n_show = min(len(graphs), n_show)
    cols = 2
    rows = (n_show + 1) // 2
    
    plt.figure(figsize=(10, 5 * rows))
    
    for i in range(n_show):
        plt.subplot(rows, cols, i + 1)
        nx.draw(graphs[i], with_labels=True, node_color='lightblue', edge_color='gray')
        plt.title(f"Graph {i+1}")
        
    output_img = os.path.join(output_dir, f"graphs_visualization_n{n}.png")
    plt.tight_layout()
    plt.savefig(output_img)
    print(f"Visualization saved to {output_img}")
    # plt.show() # Skip show in non-interactive environments if needed, but keeping it is fine as it just prints if no backend.

def main():
    parser = argparse.ArgumentParser(description="Generate triangle-free connected graphs using Nauty (geng) and filter by Corollary 4.")
    parser.add_argument("N", type=int, help="Number of vertices")
    parser.add_argument("--output", type=str, default="generated_graphs.pkl", help="Output file for graphs (pickle)")
    
    args = parser.parse_args()
    
    if not check_geng_availability():
        print("Error: 'geng' command not found. Please ensure Nauty is installed and in your PATH.")
        sys.exit(1)
    
    # Setup results directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(script_dir, "results")
    os.makedirs(results_dir, exist_ok=True)
        
    print(f"Generating triangle-free connected graphs of size {args.N}...")
    all_graphs = generate_graphs(args.N)
    print(f"Generated {len(all_graphs)} raw graphs. Filtering for Corollary 4 properties...")
    
    valid_graphs = []
    for G in all_graphs:
        if check_corollary_4_properties(G):
            valid_graphs.append(G)
            
    print(f"Found {len(valid_graphs)} graphs satisfying all properties.")
    
    if valid_graphs:
        # Determine output filename if default is used, to avoid overwriting or just use the arg
        output_filename = args.output
        if output_filename == "generated_graphs.pkl":
             output_filename = f"generated_graphs_n{args.N}.pkl"
        
        output_path = os.path.join(results_dir, output_filename)

        with open(output_path, "wb") as f:
            pickle.dump(valid_graphs, f)
        print(f"Graphs saved to {output_path}")
        
        visualize_graphs(valid_graphs, args.N, results_dir)
    else:
        print("No graphs found matching the criteria.")

if __name__ == "__main__":
    main()
