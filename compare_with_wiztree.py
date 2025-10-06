import csv
import re
import glob
import os

# --- CONFIG ---
# Find the first CSV file that starts with "WizTree_" in the data directory
wiztree_pattern = "data/WizTree_*.csv"
wiztree_files_found = glob.glob(wiztree_pattern)
if not wiztree_files_found:
    raise FileNotFoundError(f"No WizTree CSV files found matching pattern: {wiztree_pattern}")
wiztree_csv = wiztree_files_found[0]  # Use the first match

print(f"Using WizTree file: {wiztree_csv}")

rclone_log = "data/preview_list.txt"        # Path to rclone log file
output_file = "data/missing_in_rclone.txt"       # Output list of missing files
excess_file = "data/excess_in_rclone.txt"       # Output list of excess files

# Helper: determine if path should be treated as a file (avoid folders with dots)
def is_real_file(p: str) -> bool:
    return not os.path.isdir(p) and bool(os.path.splitext(p)[1])

# --- STEP 1: Read all file paths from WizTree CSV ---
wiztree_files = set()
with open(wiztree_csv, "r", encoding="utf-8-sig") as f:
    reader = csv.reader(f)
    next(reader, None)  # Skip header
    for row in reader:
        if not row:
            continue
        path = row[0].strip().strip('"')
        path = path.rstrip("\\/")  # normalize
        if path and ":" in path:
            if is_real_file(path):
                wiztree_files.add(path)

# --- STEP 2: Extract file paths from rclone dry-run log ---
rclone_files = set()
path_pattern = re.compile(r"NOTICE:\s+(.*?):")
with open(rclone_log, "r", encoding="utf-8") as f:
    for line in f:
        m = path_pattern.search(line)
        if m:
            rel_path = m.group(1).strip()
            full_path = "C:\\" + rel_path.replace("/", "\\")
            full_path = full_path.rstrip("\\/")
            if is_real_file(full_path):
                rclone_files.add(full_path)

# --- STEP 3: Find files that are in WizTree but not in rclone log ---
missing_files = sorted(wiztree_files - rclone_files)
excess_files = sorted(rclone_files - wiztree_files)

# --- STEP 4: Write results ---
with open(output_file, "w", encoding="utf-8") as out:
    for path in missing_files:
        out.write(path + "\n")
with open(excess_file, "w", encoding="utf-8") as out:
    for path in excess_files:
        out.write(path + "\n")

print(f"✅ Done! {len(missing_files)} files found missing in rclone log.")
print(f"Results saved to: {output_file}")
print(f"Excess files saved to: {excess_file}")
