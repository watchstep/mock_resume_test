import os

html_files = [f for f in os.listdir('.') if f.endswith('.html') and f != 'index.html']

html_files.sort()

with open('index.html', 'w', encoding='utf-8') as f:
    f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resume Files Index</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        h1 { border-bottom: 2px solid #333; }
        ul { list-style-type: none; padding: 0; }
        li { margin: 10px 0; }
        a { text-decoration: none; color: #007bff; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>Mock Resumes</h1>
    <ul>
""")

    for file in html_files:
        f.write(f'        <li><a href="{file}">{file}</a></li>\n')

    f.write("""    </ul>
</body>
</html>
""")
