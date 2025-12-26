import networkx as nx
import pickle
import os
import sys

def convert_pkl_to_graphml(pkl_path):
    if not os.path.exists(pkl_path):
        print(f"File not found: {pkl_path}")
        return

    base_name = os.path.splitext(os.path.basename(pkl_path))[0]
    output_dir = os.path.join(os.path.dirname(pkl_path), f"{base_name}_graphml")
    
    os.makedirs(output_dir, exist_ok=True)
    print(f"Converting {pkl_path}...")
    print(f"Output directory: {output_dir}")

    try:
        with open(pkl_path, 'rb') as f:
            data = pickle.load(f)
    except Exception as e:
        print(f"Error loading pickle: {e}")
        return

    # Handle single graph or list of graphs
    if isinstance(data, nx.Graph):
        graphs = [data]
    elif isinstance(data, list):
        graphs = data
    else:
        print(f"Unknown data type in pickle: {type(data)}")
        return

    print(f"Found {len(graphs)} graphs.")

    for i, G in enumerate(graphs):
        # Convert node labels to strings as GraphML requires string or int/long ids usually, 
        # and attributes need to be valid types. NetworkX handles basic types.
        
        # Ensure graph has no complex objects as attributes that GraphML can't handle
        # For simple generated graphs, this is usually fine.
        
        output_file = os.path.join(output_dir, f"graph_{i}.graphml")
        try:
            nx.write_graphml(G, output_file)
        except Exception as e:
            print(f"Failed to write graph {i}: {e}")
            
    print(f"Successfully converted {len(graphs)} graphs to GraphML.")

if __name__ == "__main__":
    files_to_convert = [
        "Exploratory/Nauty/results/filtered_woodgraphs.pkl",
        "Exploratory/Nauty/results/generated_graphs_n16.pkl"
    ]
    
    for f in files_to_convert:
        # Resolve absolute path just in case
        full_path = os.path.abspath(f)
        convert_pkl_to_graphml(full_path)
