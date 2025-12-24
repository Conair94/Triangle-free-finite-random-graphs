import networkx as nx
import itertools
import argparse
import sys

def is_independent_set(G, nodes):
    """Checks if the given set of nodes forms an Independent Set."""
    for u, v in itertools.combinations(nodes, 2):
        if G.has_edge(u, v):
            return False
    return True

def check_properties(G, k):
    """
    Checks if Graph G satisfies property Psi_k.
    
    Psi_k: For all x_1,...,x_k (Independent Set), and y_1,...,y_k (disjoint from x),
    there exists a z which is connected to all x_i but not any y_i.
    """
    nodes = list(G.nodes())
    # Property requires existence of sets of size k.
    if len(nodes) < 2 * k + 1:
        # We need k nodes for X, k for Y, and 1 for z.
        # If not enough nodes, the condition "For all X, Y... exists z" fails if X, Y exist but z doesn't.
        # If X or Y can't even be formed, is it true or false?
        # Standard logic: vacuously true if X/Y don't exist.
        # BUT, if X and Y EXIST, and z DOES NOT, then false.
        # If X and Y CANNOT exist, then True.
        
        # Let's check if any valid X, Y pair exists.
        # If the graph is too small to have ANY disjoint X, Y of size k, then the condition is True vacuously.
        if len(nodes) < 2 * k:
             return True
        # If we have >= 2k nodes but < 2k+1, we might have X, Y but no room for z.
        # In that case, if we find such X, Y, return False.
        pass

    # 1. Iterate all Independent Sets X of size k
    for X in itertools.combinations(nodes, k):
        if not is_independent_set(G, X):
            continue
        
        X_set = set(X)
        remaining_nodes = [node for node in nodes if node not in X_set]
        
        # 2. Iterate all sets Y of size k disjoint from X
        # Note: If no such Y exists, the inner loop doesn't run, 
        # so we don't return False, effectively passing this X check.
        for Y in itertools.combinations(remaining_nodes, k):
            Y_set = set(Y)
            
            # 3. Search for a witness z
            candidates = [u for u in remaining_nodes if u not in Y_set]
            
            witness_found = False
            for z in candidates:
                neighbors = set(G.neighbors(z))
                # Connected to all X?
                if not X_set.issubset(neighbors):
                    continue
                # Not connected to any Y?
                if not Y_set.isdisjoint(neighbors):
                    continue
                
                witness_found = True
                break
            
            if not witness_found:
                # Found a pair (X, Y) with no witness z
                return False

    return True

def generate_triangle_free_graphs(N):
    """
    Generates all labeled triangle-free graphs of size N.
    Uses recursive backtracking by adding nodes one by one, 
    connecting only to independent sets of the previous graph.
    """
    # Start with a single node 0
    G = nx.Graph()
    G.add_node(0)
    yield from _recursive_build(G, N)

def _recursive_build(G, target_size):
    current_size = G.number_of_nodes()
    
    if current_size == target_size:
        yield G
        return

    new_node = current_size
    nodes = list(G.nodes())
    
    # Iterate over all subsets of current nodes
    # Only subsets that are Independent Sets can be neighbors of the new node
    # to maintain the triangle-free property.
    for r in range(len(nodes) + 1):
        for neighbors in itertools.combinations(nodes, r):
            if is_independent_set(G, neighbors):
                # Valid extension
                G_new = G.copy()
                G_new.add_node(new_node)
                for neighbor in neighbors:
                    G_new.add_edge(new_node, neighbor)
                
                yield from _recursive_build(G_new, target_size)

def main():
    parser = argparse.ArgumentParser(description="Search for triangle-free graphs with property Psi_k.")
    parser.add_argument("N", type=int, help="Size of the graph (number of vertices)")
    parser.add_argument("k", type=int, help="Parameter k for property Psi_k")
    parser.add_argument("--limit", type=int, default=0, help="Stop after finding this many graphs (0 for all)")
    parser.add_argument("--show", action="store_true", help="Print edges of found graphs")
    
    args = parser.parse_args()
    
    N = args.N
    k_param = args.k
    
    print(f"Searching for triangle-free graphs of size {N} with property Psi_{k_param}...")
    
    count = 0
    found_count = 0
    
    # We use a set of canonical string representations to avoid strict duplicates if desired, 
    # but the generator produces labeled graphs. 
    # For 'all models', we usually list them.
    
    for G in generate_triangle_free_graphs(N):
        count += 1
        if check_properties(G, k_param):
            found_count += 1
            if args.show:
                print(f"Graph {found_count}: Edges: {list(G.edges())}")
            else:
                # Just print a dot to show progress
                print(".", end="", flush=True)
            
            if args.limit > 0 and found_count >= args.limit:
                break
    
    print(f"\nSearch complete.")
    print(f"Generated {count} labeled triangle-free graphs.")
    print(f"Found {found_count} graphs satisfying Psi_{k_param}.")

if __name__ == "__main__":
    main()
