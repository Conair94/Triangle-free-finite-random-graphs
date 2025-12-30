import argparse
import subprocess
import sys
import os
import glob
from google.cloud import bigquery

def run_generation(n, output_file, mod=None):
    """
    Runs the run_manager.py script to generate graphs for a specific N.
    """
    cmd = [sys.executable, "run_manager.py", str(n), "--output", output_file]
    
    # Heuristic for mod: Use 4 * cpu_count to keep pipeline full
    if mod is None:
        cpu_count = os.cpu_count() or 1
        mod = cpu_count * 4
    
    cmd.extend(["--mod", str(mod)])
    # Use all CPUs
    cmd.extend(["--jobs", str(os.cpu_count() or 1)])
    
    # We use default min/max degree from run_manager.py
    
    print(f"Running generation for N={n}...")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error generating graphs for N={n}: {e}")
        return False

def upload_to_bigquery(client, filename, table_ref):
    """
    Uploads a CSV file to BigQuery.
    """
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1, # Header
        schema=[
            bigquery.SchemaField("graph_g6", "STRING"),
            bigquery.SchemaField("is_3_existential", "INTEGER"),
            bigquery.SchemaField("num_vertices", "INTEGER"),
        ],
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
    )

    print(f"Uploading {filename} to {table_ref}...")
    
    try:
        with open(filename, "rb") as source_file:
            job = client.load_table_from_file(source_file, table_ref, job_config=job_config)

        job.result()  # Waits for the job to complete.
        print(f"Loaded {job.output_rows} rows into {table_ref}.")
        return True
    except Exception as e:
        print(f"Error uploading to BigQuery: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Generate graphs for N=6-16 and upload to BigQuery.")
    parser.add_argument("--project", required=True, help="Google Cloud Project ID")
    parser.add_argument("--dataset", required=True, help="BigQuery Dataset ID")
    parser.add_argument("--table", required=True, help="BigQuery Table ID")
    parser.add_argument("--start-n", type=int, default=6, help="Start N (inclusive)")
    parser.add_argument("--end-n", type=int, default=16, help="End N (inclusive)")
    parser.add_argument("--keep-files", action="store_true", help="Do not delete generated CSV files")
    
    args = parser.parse_args()
    
    # Initialize BigQuery client
    try:
        client = bigquery.Client(project=args.project)
        dataset_ref = client.dataset(args.dataset)
        table_ref = dataset_ref.table(args.table)
    except Exception as e:
        print(f"Failed to initialize BigQuery client: {e}")
        sys.exit(1)

    for n in range(args.start_n, args.end_n + 1):
        output_filename = os.path.abspath(f"graphs_n{n}_final.csv")
        
        # 1. Generate
        success = run_generation(n, output_filename)
        if not success:
            print(f"Skipping upload for N={n} due to generation failure.")
            continue
            
        # 2. Upload
        if os.path.exists(output_filename):
            upload_success = upload_to_bigquery(client, output_filename, table_ref)
            
            # 3. Cleanup
            if upload_success and not args.keep_files:
                os.remove(output_filename)
                print(f"Removed {output_filename}")
        else:
            print(f"Output file {output_filename} not found.")

if __name__ == "__main__":
    main()
