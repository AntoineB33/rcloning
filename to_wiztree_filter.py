from pathlib import Path
import re
import pyperclip

input_path = Path(r".\data\sync-filter.txt")
output_path = Path(r".\data\WizTree_filters.txt")

filters = []
with input_path.open("r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line or not line.startswith("- "):
            continue

        # Extract path and clean up
        path = line[2:].strip()

        # Skip global patterns like '**' or '- **'
        if path.startswith("**") or path == "**":
            continue

        # Remove common trailing wildcard patterns
        path = re.sub(r"/\*\*.*$", "", path)
        path = re.sub(r"/\*$", "", path)

        # Convert forward slashes to backslashes
        path = path.replace("/", "\\")

        # Quote paths with spaces
        if " " in path:
            path = f'"{path}"'

        filters.append(path)

# Join paths with '|'
output = "|".join(filters)

with output_path.open("w", encoding="utf-8") as f:
    f.write(output)
pyperclip.copy(output)

print("Conversion complete!")
