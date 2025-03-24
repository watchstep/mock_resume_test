import os
import re
from collections import defaultdict
from datetime import datetime

DATA_DIR = 'data'
html_files = []

# Recursively search data directory for all html files
for root, dirs, files in os.walk(DATA_DIR):
    for file in files:
        if file.endswith('.html') and file != 'index.html':
            rel_path = os.path.relpath(os.path.join(root, file), DATA_DIR)
            html_files.append(rel_path)

html_files.sort(reverse=True)

# Regex pattern for filename structure: {model}_{date_time}_JD_{jd_id}.html
pattern = re.compile(r'^(gpt-4o|gpt-4o-mini|gemini-2\.0-flash)_(\d{8}_\d{6})_JD_(\d{6})')

jd_groups = defaultdict(list)

for file in html_files:
    match = pattern.match(file)
    if match:
        model_type = match.group(1)
        date_time = match.group(2)
        jd_id = match.group(3)
        jd_groups[jd_id].append({
            'file': file,
            'model': model_type,
            'date': date_time
        })

# Generate main index.html
with open('index.html', 'w', encoding='utf-8') as f:
    f.write("""<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>Mock Resume Index</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        h1, h2, h3 { margin-top: 30px; }
        ul { list-style-type: none; padding: 0; }
        li { margin: 8px 0; }
        a { text-decoration: none; color: #007bff; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>Mock Resumes</h1>
    <ul>
""")

    # Add all resume links sorted by date
    for jd_id, files in jd_groups.items():
        for entry in sorted(files, key=lambda x: x['date'], reverse=True):
            f.write(f'<li><a href=\"{DATA_DIR}/{entry["file"]}\">{entry["file"]}</a></li>\n')

    f.write("""
    </ul>
    <h2>JD</h2>
    <ul>
""")

    # Add JD links
    for jd_id in sorted(jd_groups.keys()):
        f.write(f'<li><a href=\"{jd_id}.html\">JD {jd_id}</a></li>\n')

    f.write("""
    </ul>
</body>
</html>
""")

# Generate individual JD pages
for jd_id, entries in jd_groups.items():
    with open(f'{jd_id}.html', 'w', encoding='utf-8') as f:
        f.write(f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>JD {jd_id} Resumes</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1, h2, h3 {{ margin-top: 30px; }}
        ul {{ list-style-type: none; padding: 0; }}
        li {{ margin: 8px 0; }}
        a {{ text-decoration: none; color: #007bff; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <h1>JD {jd_id} Mock Resumes</h1>

    <h2>Model</h2>
""")

        # Group by model
        model_group = defaultdict(list)
        for entry in entries:
            model_group[entry['model']].append(entry)

        for model_type, model_entries in model_group.items():
            f.write(f'<h3>{model_type}</h3>\n<ul>\n')
            for entry in sorted(model_entries, key=lambda x: x['date'], reverse=True):
                f.write(f'    <li><a href=\"{DATA_DIR}/{entry["file"]}\">{entry["file"]}</a></li>\n')
            f.write('</ul>\n')

        f.write("""
    <h2>Date</h2>
""")

        # Group by date
        date_group = defaultdict(list)
        for entry in entries:
            date_group[entry['date']].append(entry)

        for date_str, date_entries in sorted(date_group.items(), key=lambda x: x[0], reverse=True):
            f.write(f'<h3>{date_str}</h3>\n<ul>\n')
            for entry in date_entries:
                f.write(f'    <li><a href=\"{DATA_DIR}/{entry["file"]}\">{entry["file"]}</a></li>\n')
            f.write('</ul>\n')

        f.write("""
</body>
</html>
""")
