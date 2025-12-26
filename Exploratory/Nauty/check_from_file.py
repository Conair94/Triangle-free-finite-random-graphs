import networkx as nx
import argparse
import pickle
import os
import sys
import time

# Import the property check function from the existing script
try:
    from generate_with_nauty import check_corollary_4_properties
except ImportError:
    # If running from a different directory, try to append the path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    try:
        from generate_with_nauty import check_corollary_4_properties
    except ImportError:
        print("Error: Could not import 'check_corollary_4_properties' from 'generate_with_nauty.py'.")
        sys.exit(1)

def load_graphs(file_path):
    """Loads graphs from a file (g6 or pickle)."""
    graphs = []
    if file_path.endswith('.g6') or file_path.endswith('.txt'):
        print(f"Loading graphs from g6 file: {file_path}")
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line: continue
                    try:
                        G = nx.from_graph6_bytes(line.encode('ascii'))
                        graphs.append(G)
                    except Exception as e:
                        print(f"Failed to parse graph6 line '{line}': {e}")
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return []
            
    elif file_path.endswith('.pkl') or file_path.endswith('.pickle'):
        print(f"Loading graphs from pickle file: {file_path}")
        try:
            with open(file_path, 'rb') as f:
                graphs = pickle.load(f)
        except Exception as e:
            print(f"Error reading pickle file {file_path}: {e}")
            return []
    else:
        print(f"Unsupported file extension for {file_path}. Please use .g6, .txt, .pkl, or .pickle")
        return []
    
    return graphs

def main():
    parser = argparse.ArgumentParser(description="Check graphs from a file against Corollary 4 properties.")
    parser.add_argument("input_file", type=str, help="Path to the input file containing graphs (.g6 or .pkl)")
    parser.add_argument("--output", type=str, default="filtered_graphs.pkl", help="Output file for matching graphs (pickle)")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' not found.")
        sys.exit(1)
        
    start_load = time.time()
    graphs = load_graphs(args.input_file)
    end_load = time.time()
    
    if not graphs:
        print("No graphs loaded. Exiting.")
        sys.exit(0)
        
    print(f"Loaded {len(graphs)} graphs in {end_load - start_load:.2f} seconds.")
    
    print("Checking graphs for Corollary 4 properties...")
    start_check = time.time()
    valid_graphs = []
    
    for i, G in enumerate(graphs):
        if check_corollary_4_properties(G):
            valid_graphs.append(G)
        
        # Progress update every 1000 graphs or 10%
        if (i + 1) % 1000 == 0 or (i + 1) == len(graphs):
             print(f"Tested {i+1}/{len(graphs)} | Found: {len(valid_graphs)}", end='\r')
             
    end_check = time.time()
    print(f"\nCheck complete. Found {len(valid_graphs)} matching graphs in {end_check - start_check:.2f} seconds.")
    
    if valid_graphs:
        # Ensure output directory exists if path contains dirs
        output_dir = os.path.dirname(args.output)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            
        with open(args.output, "wb") as f:
            pickle.dump(valid_graphs, f)
        print(f"Saved matching graphs to {args.output}")
    else:
        print("No matching graphs found.")

if __name__ == "__main__":
    main()
