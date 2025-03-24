import os
import glob
from datetime import datetime

# 데이터 폴더 경로
DATA_DIR = 'data'
OUTPUT_FILE = 'index.html'

# HTML 파일을 읽어오기
html_files = glob.glob(os.path.join(DATA_DIR, '*.html'))

# 파일을 수정 날짜 기준으로 정렬 (최신순)
html_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

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
    <h1>Mock Resumes</h1>
    <ul>
        <!-- Links to all resume files sorted by date will be inserted here dynamically -->
    </ul>
    <h2>JD</h2>
    <ul>
        <!-- JD-specific links (e.g., JD_XXXXXX.html) will be dynamically generated here -->
    </ul>
</body>
</html>"""

# HTML 파일 생성
def generate_index_html(html_files):
    # 전체 파일 링크 섹션
    all_links = ""
    jd_links = ""

    for file_path in html_files:
        file_name = os.path.basename(file_path)
        file_url = f"{DATA_DIR}/{file_name}"

        # 파일 수정 시간 가져오기
        modified_time = os.path.getmtime(file_path)
        formatted_time = datetime.fromtimestamp(modified_time).strftime('%Y-%m-%d %H:%M:%S')

        # 링크 생성
        link = f'<li><a href="{file_url}" target="_blank">{file_name}</a> (Last Modified: {formatted_time})</li>\n'

        # JD-specific 처리
        if "JD_" in file_name:
            jd_links += link
        else:
            all_links += link

    # 기본 HTML 템플릿에 동적으로 삽입
    updated_html = base_html.replace(
        '<!-- Links to all resume files sorted by date will be inserted here dynamically -->',
        all_links
    ).replace(
        '<!-- JD-specific links (e.g., JD_XXXXXX.html) will be dynamically generated here -->',
        jd_links
    )

    # index.html 파일 쓰기
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(updated_html)

# 실행
if __name__ == "__main__":
    generate_index_html(html_files)
    print(f"Index file '{OUTPUT_FILE}' has been successfully generated!")
