import os
import glob
from datetime import datetime
import re

# 데이터 폴더 경로
DATA_DIR = 'data'
OUTPUT_FILE = 'index.html'

# HTML 파일을 읽어오기
html_files = glob.glob(os.path.join(DATA_DIR, '*.html'))

# 파일명을 날짜 기준(YYYYMMDD_HHMMSS)으로 정렬하는 함수
def extract_datetime_from_filename(filename):
    match = re.search(r'(\d{8}_\d{6})', filename)
    if match:
        return datetime.strptime(match.group(1), '%Y%m%d_%H%M%S')
    else:
        return datetime.min

# 파일을 파일명에 포함된 날짜 기준으로 정렬 (최신순)
html_files.sort(key=lambda x: extract_datetime_from_filename(os.path.basename(x)), reverse=True)

# index.html 기본 템플릿
base_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
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
    <h1>Mock Resumes (Latest First)</h1>
    <ul>
        <!-- ALL FILES INSERT -->
    </ul>
</body>
</html>"""

# HTML 파일 생성 함수
def generate_index_html():
    all_links = ""

    for file_path in html_files:
        file_name = os.path.basename(file_path)
        file_url = f"{DATA_DIR}/{file_name}"

        modified_time = os.path.getmtime(file_path)
        formatted_time = datetime.fromtimestamp(modified_time).strftime('%Y-%m-%d %H:%M:%S')

        match = re.search(r'_(\d{6})\.html$', file_name)
        jd_label = f"[JD: {match.group(1)}]" if match else ""
        label = f"{jd_label} {file_name}"
        all_links += f'<li><a href="{file_url}" target="_blank">{label}</a> (Last Modified: {formatted_time})</li>\n'

    index_html = base_html.replace("<!-- ALL FILES INSERT -->", all_links)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(index_html)

def generate_jd_index(jd_number):
    jd_files = []

    jd_pattern = re.compile(r'_(\d{6})\.html$')

    for file_path in html_files:
        file_name = os.path.basename(file_path)
        file_url = f"{DATA_DIR}/{file_name}"

        match = jd_pattern.search(file_name)
        if match and match.group(1) == jd_number:
            jd_files.append((file_name, file_url))

    # 파일명을 날짜 기준으로 정렬
    jd_files.sort(key=lambda x: extract_datetime_from_filename(x[0]), reverse=True)

    model_groups = {}
    for file_name, file_url in jd_files:
        model_name = file_name.split("_")[0]
        if model_name not in model_groups:
            model_groups[model_name] = []
        model_groups[model_name].append(f'<li><a href="/{file_url}" target="_blank">{file_name}</a></li>')

    base_jd_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mock Resumes for JD {jd_number}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1, h2 {{ margin-top: 30px; }}
        ul {{ list-style-type: none; padding: 0; }}
        li {{ margin: 8px 0; }}
        a {{ text-decoration: none; color: #007bff; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <h1>Mock Resumes for JD {jd_number}</h1>
    {content}
     <p><a href="/">Back to Main Page</a></p>
</body>
</html>"""

    model_sections = ""
    for model_name, links in model_groups.items():
        model_sections += f'<h2>{model_name}</h2>\n<ul>\n' + "\n".join(links) + "\n</ul>\n"

    jd_html = base_jd_html.format(jd_number=jd_number, content=model_sections)

    output_dir = os.path.join("jd", jd_number)

    with open(os.path.join(output_dir, "index.html"), 'w', encoding='utf-8') as f:
        f.write(jd_html)

# 실행
if __name__ == "__main__":
    generate_index_html()
    print(f"Index file '{OUTPUT_FILE}' has been successfully generated!")
