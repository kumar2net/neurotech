#!/usr/bin/env python3
"""
Markdown to PDF Converter
Converts the weekly neurosurgeon dossier from Markdown to PDF with professional styling.
"""

import markdown
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import os

def convert_md_to_pdf(md_file_path, pdf_file_path):
    """Convert Markdown file to professionally styled PDF."""
    
    # Read the markdown file
    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert markdown to HTML
    html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
    
    # Enhanced CSS for professional medical document styling
    css_styles = """
    @page {
        size: A4;
        margin: 2cm 1.5cm;
        @top-center {
            content: "NeuroTech Research Hub - Confidential";
            font-size: 10pt;
            font-family: "Helvetica", sans-serif;
            color: #666;
        }
        @bottom-center {
            content: "Page " counter(page) " of " counter(pages);
            font-size: 10pt;
            font-family: "Helvetica", sans-serif;
            color: #666;
        }
    }
    
    body {
        font-family: "Helvetica", "Arial", sans-serif;
        font-size: 11pt;
        line-height: 1.4;
        color: #333;
        max-width: 100%;
        margin: 0;
        padding: 0;
    }
    
    h1 {
        font-size: 24pt;
        font-weight: bold;
        color: #1e40af;
        text-align: center;
        margin: 0 0 10pt 0;
        border-bottom: 3px solid #1e40af;
        padding-bottom: 8pt;
    }
    
    h2 {
        font-size: 16pt;
        font-weight: bold;
        color: #1e40af;
        margin: 20pt 0 8pt 0;
        border-left: 4px solid #3b82f6;
        padding-left: 10pt;
        background: #f8fafc;
        padding: 8pt 10pt;
    }
    
    h3 {
        font-size: 13pt;
        font-weight: bold;
        color: #374151;
        margin: 12pt 0 6pt 0;
    }
    
    h4 {
        font-size: 12pt;
        font-weight: bold;
        color: #4b5563;
        margin: 10pt 0 4pt 0;
    }
    
    p {
        margin: 6pt 0;
        text-align: justify;
    }
    
    em {
        font-style: italic;
        color: #6b7280;
        font-size: 10pt;
        text-align: center;
        display: block;
        margin: 5pt 0 15pt 0;
    }
    
    ul {
        margin: 8pt 0;
        padding-left: 20pt;
    }
    
    li {
        margin: 4pt 0;
        line-height: 1.3;
    }
    
    strong {
        font-weight: bold;
        color: #1f2937;
    }
    
    hr {
        border: none;
        border-top: 2px solid #e5e7eb;
        margin: 15pt 0;
    }
    
    /* Specific styling for medical content */
    li strong {
        color: #059669;
    }
    
    /* PMID and journal styling */
    li em {
        font-style: italic;
        color: #6366f1;
        display: inline;
        font-size: inherit;
        text-align: left;
    }
    
    /* Bullet point enhancements */
    ul li::marker {
        color: #3b82f6;
        font-weight: bold;
    }
    
    /* Code and technical terms */
    code {
        font-family: "Monaco", "Courier New", monospace;
        font-size: 9pt;
        background: #f3f4f6;
        padding: 2pt 4pt;
        border-radius: 3pt;
        color: #1f2937;
    }
    
    /* Section separators */
    h2::before {
        content: "";
        display: block;
        width: 100%;
        height: 1pt;
        background: #e5e7eb;
        margin-bottom: 8pt;
    }
    
    /* Special styling for key findings */
    h3 + ul li:first-child {
        font-weight: 500;
        color: #1e40af;
    }
    
    /* Print optimization */
    @media print {
        body {
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }
    }
    """
    
    # Create complete HTML document
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Weekly Neurosurgical Dossier</title>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    # Convert to PDF
    font_config = FontConfiguration()
    html_doc = HTML(string=full_html)
    css_doc = CSS(string=css_styles, font_config=font_config)
    
    # Generate PDF
    html_doc.write_pdf(pdf_file_path, stylesheets=[css_doc], font_config=font_config)
    
    print(f"✅ Successfully converted {md_file_path} to {pdf_file_path}")
    return True

def main():
    """Main function to convert the neurosurgeon dossier."""
    md_file = "weekly_neurosurgeon_dossier_aug4_2025.md"
    pdf_file = "weekly_neurosurgeon_dossier_aug4_2025.pdf"
    
    if not os.path.exists(md_file):
        print(f"❌ Error: {md_file} not found!")
        return False
    
    try:
        convert_md_to_pdf(md_file, pdf_file)
        
        # Get file size for confirmation
        file_size = os.path.getsize(pdf_file)
        file_size_kb = file_size / 1024
        
        print(f"📄 PDF created: {pdf_file}")
        print(f"📊 File size: {file_size_kb:.1f} KB")
        print(f"📍 Location: {os.path.abspath(pdf_file)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error converting to PDF: {e}")
        return False

if __name__ == "__main__":
    main()