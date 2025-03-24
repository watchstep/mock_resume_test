import os
from collections import defaultdict
import re

# Search local 'data' directory for HTML files
data_dir = 'data'
html_files = []
for root, dirs, files in os.walk(data_dir):
    for file in files:
        if file.endswith('.html') and file != 'index.html':
            relative_path = os.path.relpath(os.path.join(root, file), data_dir)
            html_files.append(relative_path)

html_files.sort()

# Group files by model type and date
model_groups = defaultdict(list)
date_groups = defaultdict(list)

# Updated regex to capture date in YYYYMMDD_HHMMSS format
model_pattern = re.compile(r'^(gpt-4o|gpt-4o-mini|gemini-2\\.0-flash)_(\\d{8}_\\d{6})')

for file in html_files:
    match = model_pattern.match(os.path.basename(file))
    if match:
        model_type = match.group(1)
        date_str = match.group(2)
        model_groups[model_type].append(file)
        date_groups[date_str].append(file)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write("""<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>Resume Files</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        h1 { border-bottom: 2px solid #333; }
        h2 { margin-top: 40px; }
        ul { list-style-type: none; padding: 0; }
        li { margin: 10px 0; }
        a { text-decoration: none; color: #007bff; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>Mock Resumes</h1>

    <h2>Model</h2>
""")
    for model_type, files in model_groups.items():
        f.write(f'<h3>{model_type}</h3>\n<ul>\n')
        for file in files:
            f.write(f'    <li><a href="{data_dir}/{file}">{file}</a></li>\n')
        f.write('</ul>\n')

    f.write("""
    <h2>Date</h2>
""")
    for date_str, files in sorted(date_groups.items(), reverse=True):
        f.write(f'<h3>{date_str}</h3>\n<ul>\n')
        for file in files:
            f.write(f'    <li><a href="{data_dir}/{file}">{file}</a></li>\n')
        f.write('</ul>\n')

    f.write("""
</body>
</html>
""")
