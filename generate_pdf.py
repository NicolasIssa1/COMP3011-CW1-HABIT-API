import markdown2
from weasyprint import HTML, CSS
import os

# Read the markdown file
with open('/workspaces/COMP3011-CW1-HABIT-API/TECHNICAL_REPORT.md', 'r') as f:
    md_content = f.read()

# Convert markdown to HTML
html_content = markdown2.markdown(md_content, extras=['tables', 'fenced-code-blocks'])

# Create output directory
os.makedirs('/workspaces/COMP3011-CW1-HABIT-API/docs', exist_ok=True)

# Wrap in HTML template with professional styling
full_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Technical Report - Habit & Productivity Analytics API</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: white;
            padding: 40px;
        }}
        h1 {{
            color: #0066cc;
            font-size: 28px;
            border-bottom: 3px solid #0066cc;
            padding-bottom: 10px;
            margin-top: 30px;
            margin-bottom: 20px;
            page-break-after: avoid;
        }}
        h2 {{
            color: #0066cc;
            font-size: 22px;
            margin-top: 25px;
            margin-bottom: 15px;
            page-break-after: avoid;
        }}
        h3 {{
            color: #0099ff;
            font-size: 16px;
            margin-top: 15px;
            margin-bottom: 10px;
            page-break-after: avoid;
        }}
        p {{
            margin-bottom: 10px;
            text-align: justify;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
            page-break-inside: avoid;
        }}
        table, th, td {{
            border: 1px solid #ddd;
        }}
        th {{
            background-color: #0066cc;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: bold;
        }}
        td {{
            padding: 10px;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        pre {{
            background-color: #f4f4f4;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 15px;
            overflow-x: auto;
            page-break-inside: avoid;
            font-family: 'Courier New', monospace;
            font-size: 11px;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 12px;
        }}
        pre code {{
            background: none;
            padding: 0;
        }}
        blockquote {{
            border-left: 4px solid #0066cc;
            margin: 15px 0;
            padding-left: 20px;
            color: #666;
            page-break-inside: avoid;
        }}
        ul, ol {{
            margin-left: 30px;
            margin-bottom: 15px;
        }}
        li {{
            margin-bottom: 5px;
        }}
        a {{
            color: #0066cc;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        .page-break {{
            page-break-after: always;
        }}
        @page {{
            margin: 1in;
            @bottom-center {{
                content: "Page " counter(page) " of " counter(pages);
                font-size: 10px;
            }}
            @top-right {{
                content: "Technical Report - Habit API";
                font-size: 10px;
                color: #999;
            }}
        }}
        @page :first {{
            @bottom-center {{
                content: "";
            }}
            @top-right {{
                content: "";
            }}
        }}
    </style>
</head>
<body>
    {html_content}
</body>
</html>
"""

# Generate PDF
output_path = '/workspaces/COMP3011-CW1-HABIT-API/docs/TECHNICAL_REPORT.pdf'
HTML(string=full_html).write_pdf(output_path)

print(f"✅ PDF generated successfully: {output_path}")
print(f"📄 File size: $(ls -lh {output_path} | awk '{{print $5}}')")