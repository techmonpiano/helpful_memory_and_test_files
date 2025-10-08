# Quick PDF Generation from Markdown/Text

## Method 1: Python Script with WeasyPrint (Recommended)

### Setup (one-time)
```bash
pip install markdown weasyprint
```

### Quick PDF Generation Script
Create a Python script that:
1. Takes markdown content
2. Converts to HTML with styling
3. Generates PDF with WeasyPrint

### Example Usage
```python
#!/usr/bin/env python3
import markdown
from weasyprint import HTML
from pathlib import Path

# Your markdown content
markdown_content = '''# Your Title
Your content here...'''

# Convert to HTML
html_content = markdown.markdown(markdown_content, extensions=['codehilite', 'tables', 'fenced_code'])

# Add CSS styling
css_style = '''
@page { margin: 2cm; size: A4; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; line-height: 1.6; }
h1 { color: #2c3e50; border-bottom: 3px solid #3498db; }
h2 { color: #34495e; border-left: 4px solid #3498db; padding-left: 15px; }
code { background-color: #f8f9fa; padding: 2px 4px; border-radius: 3px; }
pre { background-color: #f8f9fa; border: 1px solid #e9ecef; padding: 15px; }
'''

# Create full HTML
full_html = f'''<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>{css_style}</style></head>
<body>{html_content}</body></html>'''

# Generate PDF
pdf_path = Path.home() / 'Downloads' / 'output.pdf'
HTML(string=full_html).write_pdf(pdf_path)
print(f'PDF saved to: {pdf_path}')
```

## Method 2: Command Line Tools

### Using pandoc (if available)
```bash
# Install pandoc
sudo apt install pandoc texlive-latex-base

# Convert markdown to PDF
pandoc input.md -o output.pdf
```

### Using wkhtmltopdf
```bash
# Install
sudo apt install wkhtmltopdf

# Convert HTML to PDF
wkhtmltopdf input.html output.pdf
```

## Method 3: Browser-based (Quick & Dirty)

### Save as HTML then print to PDF
```python
# Save as HTML file
html_path = Path.home() / 'Downloads' / 'temp.html'
with open(html_path, 'w') as f:
    f.write(full_html)

# Open in browser and use Ctrl+P -> Save as PDF
import webbrowser
webbrowser.open(f'file://{html_path}')
```

## Template for Future Use

### Create reusable script: ~/shawndev1/quick_pdf.py
```python
#!/usr/bin/env python3
import sys
import markdown
from weasyprint import HTML
from pathlib import Path

def text_to_pdf(content, output_name="output"):
    """Convert text/markdown to PDF"""
    
    # Convert markdown to HTML
    html_content = markdown.markdown(content, extensions=['codehilite', 'tables', 'fenced_code'])
    
    # Professional CSS styling
    css_style = '''
    @page { margin: 2cm; size: A4; }
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; line-height: 1.6; color: #333; }
    h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
    h2 { color: #34495e; margin-top: 30px; border-left: 4px solid #3498db; padding-left: 15px; }
    h3 { color: #7f8c8d; margin-top: 20px; }
    code { background-color: #f8f9fa; padding: 2px 4px; border-radius: 3px; font-family: monospace; }
    pre { background-color: #f8f9fa; border: 1px solid #e9ecef; padding: 15px; border-radius: 5px; }
    blockquote { border-left: 4px solid #bdc3c7; margin-left: 0; padding-left: 15px; font-style: italic; color: #7f8c8d; }
    strong { color: #2c3e50; }
    ul, ol { padding-left: 20px; }
    li { margin-bottom: 5px; }
    '''
    
    # Create full HTML
    full_html = f'''<!DOCTYPE html>
    <html><head><meta charset="utf-8"><title>{output_name}</title><style>{css_style}</style></head>
    <body>{html_content}</body></html>'''
    
    # Generate PDF
    pdf_path = Path.home() / 'Downloads' / f'{output_name}.pdf'
    HTML(string=full_html).write_pdf(pdf_path)
    print(f'PDF saved to: {pdf_path}')
    return pdf_path

# Usage: python3 quick_pdf.py "# Title\nContent..." "filename"
if __name__ == "__main__":
    if len(sys.argv) > 1:
        content = sys.argv[1]
        name = sys.argv[2] if len(sys.argv) > 2 else "output"
        text_to_pdf(content, name)
    else:
        print("Usage: python3 quick_pdf.py 'markdown content' 'filename'")
```

### Make it executable
```bash
chmod +x ~/shawndev1/quick_pdf.py
```

### Usage
```bash
# Quick PDF from command line
python3 ~/shawndev1/quick_pdf.py "# My Report\nContent here..." "my-report"

# Or from within Python scripts
from quick_pdf import text_to_pdf
text_to_pdf(content, "output-name")
```

## Best Practices

1. **Use WeasyPrint** - Best quality, most reliable
2. **Include CSS styling** - Makes PDFs look professional
3. **Test with sample content** - Verify formatting before large documents
4. **Save to ~/Downloads** - Standard location, easy to find
5. **Use descriptive filenames** - Include date/purpose

## Common Issues & Solutions

### WeasyPrint not found
```bash
pip install weasyprint
# If that fails:
sudo apt install python3-weasyprint
```

### Font issues
```css
/* Use system fonts for better compatibility */
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

### Large files/timeout
```python
# For very large documents, process in chunks
# Or increase timeout in WeasyPrint settings
```

## Pro Tips

- **Test CSS separately** - Create HTML first, then add PDF conversion
- **Use markdown extensions** - Enable code highlighting, tables, etc.
- **Check file permissions** - Ensure write access to output directory
- **Version control styles** - Save CSS templates for consistent formatting
