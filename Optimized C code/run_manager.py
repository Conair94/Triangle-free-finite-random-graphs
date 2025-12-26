import argparse
import sys
import os
import time
import multiprocessing
import statistics
import datetime
import math

# Ensure we can import from the same directory
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

try:
    from generate_custom import generate_custom_graphs
except ImportError:
    print("Error: Could not import 'generate_custom.py'. Make sure it is in the same directory.")
    sys.exit(1)

def worker_task(args):
    """
    Wrapper for multiprocessing.
    args: (n, res, mod, min_deg, max_deg)
    Returns: (res, count, elapsed_time, graphs)
    """
    n, res, mod, min_deg, max_deg = args
    start = time.time()
    try:
        # Run quietly to avoid console spam
        graphs = generate_custom_graphs(n, res, mod, min_deg, max_deg, output_file=None, quiet=True)
        elapsed = time.time() - start
        return (res, len(graphs), elapsed, graphs)
    except Exception as e:
        return (res, 0, 0, str(e))

def main():
    print("=== Twin-free Maximal Triangle-free Graph Generation Manager ===")
    
    # Interactive input if no args
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(description="Manager for graph generation.")
        parser.add_argument("N", nargs='?', type=int, help="Number of vertices")
        parser.add_argument("--mod", type=int, help="Number of slices")
        parser.add_argument("--min-deg", type=int, default=3, help="Minimum degree (default 3)")
        parser.add_argument("--max-deg", type=int, default=None, help="Maximum degree (default ceil(N/2))")
        parser.add_argument("--jobs", "-j", type=int, default=os.cpu_count(), help="Parallel jobs")
        parser.add_argument("--output", "-o", type=str, default=None, help="Output file")
        args = parser.parse_args()
        
        n = args.N
        mod = args.mod
        min_deg = args.min_deg
        max_deg = args.max_deg
        jobs = args.jobs
        output_file = args.output
        
        # If N or mod are missing even with args, fall back to interactive
        interactive = False
        if n is None:
             interactive = True
    else:
        interactive = True

    if interactive:
        try:
            n_str = input("Enter number of vertices (N): ")
            if not n_str.strip():
                 print("N is required.")
                 sys.exit(1)
            n = int(n_str)
            
            mod_str = input("Enter number of slices (mod) [Default 1]: ")
            mod = int(mod_str) if mod_str.strip() else 1
            
            min_deg_str = input("Enter minimum degree [Default 3]: ")
            min_deg = int(min_deg_str) if min_deg_str.strip() else 3
            
            default_max = math.ceil(n / 2)
            max_deg_str = input(f"Enter maximum degree [Default {default_max}]: ")
            max_deg = int(max_deg_str) if max_deg_str.strip() else default_max
            
            default_jobs = os.cpu_count()
            jobs_str = input(f"Enter number of parallel jobs [Default {default_jobs}]: ")
            jobs = int(jobs_str) if jobs_str.strip() else default_jobs
            
            default_output = f"graphs_n{n}_deg{min_deg}_{max_deg}.g6"
            output_file_input = input(f"Enter output filename [Default '{default_output}']: ")
            if output_file_input.strip():
                output_file = output_file_input
            else:
                output_file = None
                
        except ValueError:
            print("Invalid input. Exiting.")
            sys.exit(1)

    # Calculate default max_deg if from CLI args it was None
    if max_deg is None and n is not None:
         max_deg = math.ceil(n / 2)
            
    # Default output filename if not set
    if not output_file:
        output_file = f"graphs_n{n}_deg{min_deg}_{max_deg}.g6"
        
    if mod is None: mod = 1
    
    # Save to Results folder
    results_dir = os.path.join(script_dir, "Results")
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
        
    # If output_file is just a filename, prepend results dir
    if not os.path.isabs(output_file) and os.path.dirname(output_file) == "":
        output_file = os.path.join(results_dir, output_file)

    print(f"\nConfiguration:")
    print(f"  Vertices (N): {n}")
    print(f"  Degree Bounds: {min_deg} - {max_deg}")
    print(f"  Slices (mod): {mod}")
    print(f"  Parallel Jobs: {jobs}")
    print(f"  Output File: {output_file}")
    print("-" * 40)
    
    if interactive:
        confirm = input("Start generation? [y/N]: ")
        if confirm.lower() != 'y':
            print("Aborted.")
            sys.exit(0)

    # Prepare tasks
    tasks = [(n, r, mod, min_deg, max_deg) for r in range(mod)]
    
    all_graphs = []
    stats = []
    
    start_total = time.time()
    
    print("\nStarting workers...")
    
    # Use multiprocessing Pool
    completed = 0
    with multiprocessing.Pool(processes=jobs) as pool:
        # Use imap_unordered to process results as they finish
        for res, count, elapsed, result_data in pool.imap_unordered(worker_task, tasks):
            completed += 1
            if isinstance(result_data, str):
                # Error happened
                print(f"[Slice {res}/{mod}] FAILED: {result_data}")
            else:
                all_graphs.extend(result_data)
                stats.append((res, count, elapsed))
                print(f"[Slice {res:>{len(str(mod))}}/{mod}] Finished in {elapsed:.2f}s | Found: {count} graphs | Progress: {completed}/{mod} ({(completed/mod)*100:.1f}%)")

    end_total = time.time()
    total_time = end_total - start_total
    
    # Sorting stats by slice index for the report (if we printed a table later, but we just summarized)
    stats.sort(key=lambda x: x[0])
    
    print("\n" + "=" * 40)
    print("GENERATION COMPLETE")
    print("=" * 40)
    print(f"Total time: {str(datetime.timedelta(seconds=total_time))}")
    print(f"Total graphs found: {len(all_graphs)}")
    
    if stats:
        times = [s[2] for s in stats]
        avg_time = statistics.mean(times)
        max_time = max(times)
        min_time = min(times)
        print(f"Average time per slice: {avg_time:.2f}s")
        print(f"Max time per slice: {max_time:.2f}s")
        print(f"Min time per slice: {min_time:.2f}s")
    
    # Writing to file
    if all_graphs:
        print(f"\nWriting {len(all_graphs)} graphs to '{output_file}'...")
        try:
            with open(output_file, 'w') as f:
                for g6 in all_graphs:
                    f.write(g6 + "\n")
            print("Done.")
        except Exception as e:
            print(f"Error writing to file: {e}")
    else:
        print("\nNo graphs found. File not created.")

if __name__ == "__main__":
    main()