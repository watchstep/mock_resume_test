import os
from collections import defaultdict
import re

DATA_DIR = 'data'
html_files = []
for root, _, files in os.walk(DATA_DIR):
    for file in files:
        if file.endswith('.html') and file != 'index.html':
            relative_path = os.path.relpath(os.path.join(root, file), DATA_DIR)
            html_files.append(relative_path)

html_files.sort(reverse=True)  # 최신순 정렬

jd_groups = defaultdict(list)
model_pattern = re.compile(r'^(gpt-4o|gpt-4o-mini|gemini-2\.0-flash)_(\d{8}_\d{6})_JD_(\d{6})')

for file in html_files:
    match = model_pattern.match(file)
    if match:
        model_type = match.group(1)
        date_str = match.group(2)
        jd_code = match.group(3)
        jd_groups[jd_code].append({'file': file, 'model': model_type, 'date': date_str})

with open('index.html', 'w', encoding='utf-8') as f:
    f.write("""<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>Mock Resume Index</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        h1, h2, h3, h4 { margin-top: 30px; }
        ul { list-style-type: none; padding: 0; }
        li { margin: 8px 0; }
        a { text-decoration: none; color: #007bff; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>Mock Resumes</h1>

    <h2>All Files (Latest First)</h2>
    <ul>
""")
    for file in html_files:
        f.write(f'        <li><a href="{DATA_DIR}/{file}">{file}</a></li>\n')

    f.write("""
    </ul>

    <h2>JD</h2>
""")
    for jd_code, entries in jd_groups.items():
        f.write(f'<h3>JD {jd_code}</h3>\n')
        f.write("<h4>Model</h4>\n<ul>\n")
        for entry in entries:
            f.write(f'<li><a href="{DATA_DIR}/{entry["file"]}">{entry["model"]}</a></li>\n')
        f.write("</ul>\n")

        f.write("<h4>Date</h4>\n<ul>\n")
        for entry in entries:
            f.write(f'<li><a href="{DATA_DIR}/{entry["file"]}">{entry["date"]}</a></li>\n')
        f.write("</ul>\n")

    f.write("""
</body>
</html>
""")
