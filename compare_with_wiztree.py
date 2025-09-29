# compare_file_lists.py
txt_file = "preview_list.txt"
wiztree_csv = "WizTree_20250929212031.csv"

# Read your list
with open(txt_file, "r", encoding="utf-8") as f:
    txt_files = set(line.strip() for line in f if line.strip())

# Read WizTree export (file paths are usually in column 1)
wiz_files = set()
with open(wiztree_csv, "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith('"File Path"'):  # skip header
            continue
        path = line.split(",")[0].strip('"')
        wiz_files.add(path)

missing = txt_files - wiz_files
extra = wiz_files - txt_files

print("Missing files (in TXT but not in WizTree):")
for m in sorted(missing):
    print(m)

print("\nExtra files (in WizTree but not in TXT):")
for e in sorted(extra):
    print(e)
