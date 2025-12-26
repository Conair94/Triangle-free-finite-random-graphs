import subprocess
import argparse
import os
import sys
import math
import time

def compile_filter():
    """Compiles the custom C filter if it doesn't exist."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    source_file = os.path.join(script_dir, "custom_filter.c")
    output_file = os.path.join(script_dir, "custom_filter")
    
    if not os.path.exists(output_file) or os.path.getmtime(source_file) > os.path.getmtime(output_file):
        print("Compiling custom_filter.c...")
        # Try compiling. Assuming nauty is installed globally or headers are in include path.
        # You might need to adjust -I and -L paths depending on your nauty installation.
        # Common locations: /usr/local/include, /opt/homebrew/include (Mac)
        
        cmd = ["gcc", "-O3", source_file, "-o", output_file, "-lnauty"]
        
        # Add common include/lib paths for MacOS (Homebrew) or Linux
        # This is a heuristic; user might need to adjust.
        # We append these flags only if simple compilation fails? 
        # Or just add them optimistically if directories exist.
        possible_includes = ["/usr/local/include", "/opt/homebrew/include", "/usr/include/nauty", "/usr/local/include/nauty", "/opt/homebrew/include/nauty"]
        for inc in possible_includes:
            if os.path.exists(inc):
                cmd.extend(["-I", inc])
                
        possible_libs = ["/usr/local/lib", "/opt/homebrew/lib"]
        for lib in possible_libs:
            if os.path.exists(lib):
                cmd.extend(["-L", lib])

        try:
            subprocess.run(cmd, check=True)
            print("Compilation successful.")
        except subprocess.CalledProcessError as e:
            print(f"\nError: Compilation failed.")
            print("Please ensure 'nauty' is installed and 'nauty.h'/'gtools.h' are available.")
            print(f"Command tried: {' '.join(cmd)}")
            sys.exit(1)
            
    return output_file

def generate_custom_graphs(n, res, mod, output_file=None, quiet=False):
    """
    Generates graphs using geng and filters them using the custom C program.
    """
    filter_exe = compile_filter()
    
    # Calculate edge bounds
    # Min edges: 3n - 15
    # Max edges: floor(((n-1)^2)/4 + 1)
    
    nedges_min = 3 * n - 15
    nedges_max = math.floor((((n - 1) ** 2) / 4) + 1)
    
    # Ensure min edges is not negative
    if nedges_min < 0:
        nedges_min = 0
        
    edge_range = f"{nedges_min}:{nedges_max}"
    
    # Construct geng command
    # -C: biconnected
    # -t: triangle-free
    # -q: suppress aux output
    # Note: d4D9 (degree bounds) are OMITTED based on user instructions to focus on edge bounds.
    # If degree bounds are required, add "-d4D9" to the flags.
    
    geng_cmd = ["geng", "-Ctq", str(n), edge_range, f"{res}/{mod}"]
    
    if not quiet:
        print(f"Running pipeline: {' '.join(geng_cmd)} | {os.path.basename(filter_exe)}")
        print(f"Edge bounds: {edge_range}")

    start_time = time.time()
    count = 0
    
    try:
        # Create pipeline
        geng_proc = subprocess.Popen(geng_cmd, stdout=subprocess.PIPE, stderr=sys.stderr)
        filter_proc = subprocess.Popen([filter_exe], stdin=geng_proc.stdout, stdout=subprocess.PIPE, text=True)
        
        # Allow geng_proc to receive a SIGPIPE if filter_proc exits.
        geng_proc.stdout.close()
        
        # Read output from filter
        valid_graphs = []
        for line in filter_proc.stdout:
            line = line.strip()
            if line:
                valid_graphs.append(line)
                count += 1
                
        filter_proc.wait()
        geng_proc.wait()
        
    except Exception as e:
        if not quiet:
            print(f"Error during generation: {e}")
        return []
        
    end_time = time.time()
    elapsed = end_time - start_time
    
    if not quiet:
        print(f"Slice {res}/{mod} complete. Found {count} valid graphs in {elapsed:.2f}s.")
    
    if output_file and valid_graphs:
        with open(output_file, 'w') as f:
            for g6 in valid_graphs:
                f.write(g6 + "\n")
        if not quiet:
            print(f"Saved {count} graphs to {output_file}")
        
    return valid_graphs

def main():
    parser = argparse.ArgumentParser(description="Generate Twin-free Maximal Triangle-free Biconnected graphs.")
    parser.add_argument("N", type=int, help="Number of vertices")
    parser.add_argument("--res", type=int, default=0, help="Res for splitting (geng res/mod)")
    parser.add_argument("--mod", type=int, default=1, help="Mod for splitting (geng res/mod)")
    parser.add_argument("--output", type=str, default=None, help="Output file (optional)")
    
    args = parser.parse_args()
    
    # If output not specified, create a default name
    if args.output is None:
        args.output = f"graphs_n{args.N}_{args.res}_{args.mod}.g6"
        
    generate_custom_graphs(args.N, args.res, args.mod, args.output)

if __name__ == "__main__":
    main()
