import json
import os
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

def render_resume_html(output_json_path, template_path):
    html_output_path = output_json_path.with_suffix('.html')
    
    # JSON 파일이 더 최신이거나 HTML이 없으면 렌더링
    if not html_output_path.exists() or os.path.getmtime(output_json_path) > os.path.getmtime(html_output_path):
        with open(output_json_path, 'r', encoding='utf-8') as json_file:
            output_json = json.load(json_file)
            
        env = Environment(loader=FileSystemLoader(str(template_path.parent)))
        template = env.get_template(template_path.name)
        
        html_content = template.render(resume=output_json['output'])
        
        with open(html_output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        print(f"HTML has been successfully generated! : {output_html_path}")

if __name__ == "__main__":
    data_dir = Path("data")
    template_file = Path("resume_template.html")

    json_files = data_dir.glob("*.json")

    for json_file in json_files:
        render_resume_html(json_file, template_file)