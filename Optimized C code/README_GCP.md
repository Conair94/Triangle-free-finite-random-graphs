# Google Cloud Compute Engine Execution Guide

This guide explains how to run the graph generation scripts using the **SSH-in-browser** feature on Google Cloud Platform.

## 1. Clean Slate (Optional)
If you need to clear the current directory on the VM to ensure a fresh run:

```bash
# WARNING: This deletes ALL files in the current directory!
rm -rf * .*.progress
```

## 2. Upload Files
Since `gcloud scp` is not available inside the browser SSH, you must use the **Upload** feature.

1.  Click the **Gear Icon** (Settings) in the top-right corner of the SSH window.
2.  Select **Upload file**.
3.  Upload the following files from your local `Optimized C code` folder:
    *   `gcp_runner.py`
    *   `run_manager.py`
    *   `generate_custom.py`
    *   `custom_filter.c`
    *   `requirements.txt`
    *   `setup_gce.sh`

## 3. Setup Dependencies
Run these commands to install system tools (Nauty, GCC) and Python libraries.

```bash
# 1. Make the setup script executable
chmod +x setup_gce.sh

# 2. Run the setup script (installs nauty, python deps)
./setup_gce.sh

# 3. (Optional but Recommended) Setup Virtual Environment
# If you run into "externally managed environment" errors:
sudo apt-get install -y python3-venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install google-cloud-bigquery
```

## 4. Verify Installation
Check that `geng` is installed and available:

```bash
which geng
# Should output: /usr/bin/geng or /usr/local/bin/geng
```

## 5. Start the Run (N=15)
Use `nohup` to keep the process running even if your browser window closes.

```bash
# Ensure you are in the virtual env (if used)
source venv/bin/activate 2>/dev/null || true

# Run the script
nohup python3 gcp_runner.py \
  --project protean-horizon-482807-j5 \
  --dataset k_ex_triangle_free \
  --table graphs_test_n15 \
  --start-n 15 \
  --end-n 15 > run_n15.log 2>&1 &
```

## 6. Monitor Progress
You can watch the logs in real-time:

```bash
tail -f run_n15.log
```

To stop following the log, press `Ctrl + C`.
The script will continue running in the background.

```