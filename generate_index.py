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

# Group by JD -> Model -> Date
jd_groups = defaultdict(lambda: defaultdict(list))
jd_pattern = re.compile(r'_JD_(\d{6})')
model_pattern = re.compile(r'^(gpt-4o|gpt-4o-mini|gemini-2\\.0-flash)_(\d{8}_\d{6})_JD_\d{6}')

all_files = []

for file in html_files:
    jd_match = jd_pattern.search(file)
    model_match = model_pattern.match(os.path.basename(file))
    if jd_match and model_match:
        jd_id = jd_match.group(1)
        model_type = model_match.group(1)
        date_str = model_match.group(2)
        jd_groups[jd_id][model_type].append((file, date_str))
        all_files.append((file, date_str))

# Sort by date descending
all_files.sort(key=lambda x: x[1], reverse=True)

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
    <h1>All Mock Resumes (Newest First)</h1>
    <ul>
""")
    for file, date_str in all_files:
        f.write(f'        <li>{date_str}: <a href="{data_dir}/{file}">{file}</a></li>\n')

    f.write("""
    </ul>
    <h2>Browse by JD</h2>
""")

    for jd_id, models in jd_groups.items():
        f.write(f'<h3><a href="{jd_id}.html">JD {jd_id}</a></h3>\n')

    f.write("""</body>
</html>""")

# Generate separate pages for each JD
for jd_id, models in jd_groups.items():
    with open(f'{jd_id}.html', 'w', encoding='utf-8') as f:
        f.write("""<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>JD {jd_id} Resumes</title>
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
    <h1>Resumes for JD {jd_id}</h1>
""")

        for model_type, files in models.items():
            f.write(f'<h3>{model_type}</h3>\n<ul>\n')
            for file, date_str in sorted(files, key=lambda x: x[1], reverse=True):
                f.write(f'    <li>{date_str}: <a href="{data_dir}/{file}">{file}</a></li>\n')
            f.write('</ul>\n')

        f.write("""</body>
</html>""")
