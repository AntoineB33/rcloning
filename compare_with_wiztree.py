import csv
import re

# --- CONFIG ---
wiztree_csv = "WizTree_20250929212722.csv"          # Path to WizTree CSV file
rclone_log = "preview_list.txt"        # Path to rclone log file
output_file = "missing_in_rclone.txt"       # Output list of missing files

# --- STEP 1: Read all file paths from WizTree CSV ---
wiztree_files = set()
with open(wiztree_csv, "r", encoding="utf-8-sig") as f:
    reader = csv.reader(f)
    next(reader, None)  # Skip header
    for row in reader:
        if not row:
            continue
        path = row[0].strip().strip('"')
        if path and ":" in path:  # basic sanity check
            wiztree_files.add(path)

# --- STEP 2: Extract file paths from rclone dry-run log ---
rclone_files = set()
path_pattern = re.compile(r"NOTICE:\s+([A-Za-z0-9_/.\- ]+)")
with open(rclone_log, "r", encoding="utf-8") as f:
    for line in f:
        m = path_pattern.search(line)
        if m:
            rel_path = m.group(1).strip()
            # Convert from "Users/N6506/Home/..." → "C:\Users\N6506\Home\..."
            full_path = "C:\\" + rel_path.replace("/", "\\")
            rclone_files.add(full_path)

# --- STEP 3: Find files that are in WizTree but not in rclone log ---
missing_files = sorted(wiztree_files - rclone_files)

# --- STEP 4: Write results ---
with open(output_file, "w", encoding="utf-8") as out:
    for path in missing_files:
        out.write(path + "\n")

print(f"✅ Done! {len(missing_files)} files found missing in rclone log.")
print(f"Results saved to: {output_file}")
