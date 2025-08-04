#!/usr/bin/env python3
"""
Simple Markdown to PDF Converter using ReportLab
Converts the weekly neurosurgeon dossier to a professional PDF.
"""

import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import os

def parse_markdown_content(md_file_path):
    """Parse markdown content and extract structured elements."""
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    elements = []
    lines = content.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Main title (starts with # )
        if line.startswith('# '):
            elements.append({
                'type': 'title',
                'content': line[2:].strip()
            })
        # Section headers (starts with ## )
        elif line.startswith('## '):
            elements.append({
                'type': 'heading',
                'content': line[3:].strip()
            })
        # Sub-sections (starts with ### )
        elif line.startswith('### '):
            elements.append({
                'type': 'subheading',
                'content': line[4:].strip()
            })
        # Bullet points (starts with •)
        elif line.startswith('• ') or line.startswith('- '):
            elements.append({
                'type': 'bullet',
                'content': line[2:].strip()
            })
        # Horizontal rule
        elif line.startswith('---'):
            elements.append({
                'type': 'spacer',
                'content': ''
            })
        # Italic/meta text (starts with *)
        elif line.startswith('*') and line.endswith('*'):
            elements.append({
                'type': 'meta',
                'content': line[1:-1].strip()
            })
        # Bold sections (contains **)
        elif '**' in line:
            elements.append({
                'type': 'paragraph',
                'content': line
            })
        # Regular paragraphs
        elif line and not line.startswith('#'):
            elements.append({
                'type': 'paragraph',
                'content': line
            })
    
    return elements

def create_pdf_styles():
    """Create custom styles for the PDF."""
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=20,
        spaceAfter=12,
        alignment=TA_CENTER,
        textColor=HexColor('#1e40af'),
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading1'],
        fontSize=14,
        spaceAfter=8,
        spaceBefore=12,
        textColor=HexColor('#1e40af'),
        fontName='Helvetica-Bold',
        leftIndent=0
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading2'],
        fontSize=12,
        spaceAfter=6,
        spaceBefore=8,
        textColor=HexColor('#374151'),
        fontName='Helvetica-Bold'
    )
    
    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=4,
        leftIndent=20,
        bulletIndent=10,
        fontName='Helvetica'
    )
    
    paragraph_style = ParagraphStyle(
        'CustomParagraph',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6,
        alignment=TA_JUSTIFY,
        fontName='Helvetica'
    )
    
    meta_style = ParagraphStyle(
        'CustomMeta',
        parent=styles['Normal'],
        fontSize=9,
        spaceAfter=8,
        alignment=TA_CENTER,
        textColor=HexColor('#6b7280'),
        fontName='Helvetica-Oblique'
    )
    
    return {
        'title': title_style,
        'heading': heading_style,
        'subheading': subheading_style,
        'bullet': bullet_style,
        'paragraph': paragraph_style,
        'meta': meta_style
    }

def clean_text(text):
    """Clean markdown formatting from text."""
    # Remove markdown formatting
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)  # Bold
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)      # Italic
    text = re.sub(r'`(.*?)`', r'<font name="Courier">\1</font>', text)  # Code
    
    # Clean up special characters
    text = text.replace('🧠', '').replace('🔬', '').replace('🎯', '')
    text = text.replace('🤖', '').replace('🧬', '').replace('⚡', '')
    text = text.replace('🏥', '').replace('📊', '').replace('🔮', '')
    text = text.replace('📚', '').replace('---', '')
    
    return text.strip()

def convert_md_to_pdf(md_file_path, pdf_file_path):
    """Convert markdown to PDF."""
    
    # Parse markdown content
    elements = parse_markdown_content(md_file_path)
    
    # Create PDF document
    doc = SimpleDocTemplate(
        pdf_file_path,
        pagesize=A4,
        rightMargin=inch*0.75,
        leftMargin=inch*0.75,
        topMargin=inch*1,
        bottomMargin=inch*0.75
    )
    
    # Get styles
    styles = create_pdf_styles()
    
    # Build PDF content
    story = []
    
    for element in elements:
        content = clean_text(element['content'])
        
        if element['type'] == 'title':
            story.append(Paragraph(content, styles['title']))
            story.append(Spacer(1, 12))
            
        elif element['type'] == 'heading':
            story.append(Spacer(1, 8))
            story.append(Paragraph(content, styles['heading']))
            
        elif element['type'] == 'subheading':
            story.append(Paragraph(content, styles['subheading']))
            
        elif element['type'] == 'bullet':
            bullet_text = f"• {content}"
            story.append(Paragraph(bullet_text, styles['bullet']))
            
        elif element['type'] == 'paragraph':
            if content:
                story.append(Paragraph(content, styles['paragraph']))
                
        elif element['type'] == 'meta':
            story.append(Paragraph(content, styles['meta']))
            
        elif element['type'] == 'spacer':
            story.append(Spacer(1, 8))
    
    # Build PDF
    doc.build(story)
    
    return True

def main():
    """Main function."""
    md_file = "weekly_neurosurgeon_dossier_aug4_2025.md"
    pdf_file = "weekly_neurosurgeon_dossier_aug4_2025.pdf"
    
    if not os.path.exists(md_file):
        print(f"❌ Error: {md_file} not found!")
        return False
    
    try:
        print("🔄 Converting Markdown to PDF...")
        convert_md_to_pdf(md_file, pdf_file)
        
        # Get file info
        file_size = os.path.getsize(pdf_file)
        file_size_kb = file_size / 1024
        
        print("✅ PDF conversion completed successfully!")
        print(f"📄 Output file: {pdf_file}")
        print(f"📊 File size: {file_size_kb:.1f} KB")
        print(f"📍 Full path: {os.path.abspath(pdf_file)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during conversion: {e}")
        return False

if __name__ == "__main__":
    main()