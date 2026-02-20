from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Preformatted, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
import re
from datetime import datetime

class PDFGenerator:
    def __init__(self, md_file, pdf_file):
        self.md_file = md_file
        self.pdf_file = pdf_file
        self.styles = getSampleStyleSheet()
        self.setup_styles()
        
    def setup_styles(self):
        # Title Style
        self.styles.add(ParagraphStyle(
            name='MainTitle',
            parent=self.styles['Title'],
            fontSize=24,
            leading=30,
            alignment=TA_CENTER,
            spaceAfter=20,
            textColor=colors.darkblue
        ))
        
        # Subtitle/Meta Style
        self.styles.add(ParagraphStyle(
            name='MetaInfo',
            parent=self.styles['Normal'],
            fontSize=12,
            leading=14,
            alignment=TA_CENTER,
            textColor=colors.grey
        ))

        # Justfied Body Text
        self.styles['Normal'].alignment = TA_JUSTIFY
        self.styles['Normal'].fontSize = 11
        self.styles['Normal'].leading = 14
        
        # Code Style
        if 'Code' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='Code',
                parent=self.styles['Normal'],
                fontName='Courier',
                fontSize=9,
                leading=11,
                backColor=colors.whitesmoke,
                borderPadding=5,
                leftIndent=10,
                rightIndent=10,
                alignment=TA_LEFT
            ))

        # Bullet Style
        if 'Bullet' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='Bullet',
                parent=self.styles['Normal'],
                leftIndent=20,
                firstLineIndent=0,
                spaceBefore=2,
                spaceAfter=2
            ))
        
        # Numbered List Style
        if 'Numbered' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='Numbered',
                parent=self.styles['Normal'],
                leftIndent=20,
                firstLineIndent=0,
                spaceBefore=2,
                spaceAfter=2
            ))

    def add_page_number(self, canvas, doc):
        """Add page number to bottom of page"""
        page_num = canvas.getPageNumber()
        text = "Halaman %s" % page_num
        canvas.drawRightString(200*mm, 20*mm, text) # This might fail if units not imported, fixing below.
        
    def metadata_page(self, title, version, date, author):
        story = []
        story.append(Spacer(1, 100))
        story.append(Paragraph(title, self.styles['MainTitle']))
        story.append(Spacer(1, 20))
        story.append(Paragraph(f"Versi: {version}", self.styles['MetaInfo']))
        story.append(Paragraph(f"Tanggal: {date}", self.styles['MetaInfo']))
        story.append(Paragraph(f"Pengembang: {author}", self.styles['MetaInfo']))
        story.append(Spacer(1, 50))
        story.append(Paragraph("DOKUMEN TEKNIS RESMI", self.styles['MetaInfo']))
        story.append(PageBreak())
        return story

    def parse_markdown(self):
        story = []
        with open(self.md_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        # Extract Metadata first
        title = "Dokumen Teknis"
        version = "1.0"
        date = datetime.now().strftime("%d %B %Y")
        author = "Admin"
        
        # Simple extraction for cover page
        for line in lines[:10]:
            if line.startswith('# '): title = line[2:].strip()
            if '**Versi' in line: version = line.split(':')[-1].replace('**', '').strip()
            if '**Tanggal' in line: date = line.split(':')[-1].replace('**', '').strip()
            if '**Pengembang' in line: author = line.split(':')[-1].replace('**', '').strip()

        # Add Cover Page
        story.extend(self.metadata_page(title, version, date, author))
        
        in_code_block = False
        code_type = ""
        code_content = []

        for line in lines:
            line = line.strip()
            
            # Code Block Handling
            if line.startswith('```'):
                if in_code_block:
                    p = Preformatted('\n'.join(code_content), self.styles['Code'])
                    story.append(p)
                    story.append(Spacer(1, 12))
                    in_code_block = False
                    code_content = []
                else:
                    in_code_block = True
                    code_type = line[3:].strip()
                continue
                
            if in_code_block:
                code_content.append(line)
                continue
            
            # Headers
            if line.startswith('## '):
                story.append(Spacer(1, 12))
                story.append(Paragraph(line[3:], self.styles['Heading2']))
                story.append(Spacer(1, 6))
            elif line.startswith('### '):
                story.append(Paragraph(line[4:], self.styles['Heading3']))
                story.append(Spacer(1, 4))
            
            # Lists
            elif line.startswith('- ') or line.startswith('* '):
                text = self.format_text(line[2:])
                story.append(Paragraph(f'<bullet>&bull;</bullet> {text}', self.styles['Bullet']))
            elif re.match(r'^\d+\.', line):
                text = self.format_text(line.split('.', 1)[1].strip())
                num = line.split('.', 1)[0] + '.'
                story.append(Paragraph(f'{num} {text}', self.styles['Numbered']))

            # Horizontal Rule
            elif line.startswith('---'):
                 story.append(PageBreak())
                 
            # Standard Text
            elif line and not line.startswith('#') and not line.startswith('**Versi') and not line.startswith('**Tanggal') and not line.startswith('**Pengembang'):
                 text = self.format_text(line)
                 story.append(Paragraph(text, self.styles['Normal']))
                 story.append(Spacer(1, 6))
                 
        return story

    def format_text(self, text):
        # Escape XML
        text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        # Bold **text** -> <b>text</b>
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        # Italic *text* -> <i>text</i>
        text = re.sub(r'(?<!^)\*(.*?)\*', r'<i>\1</i>', text)
        # Code `text` -> Courier
        text = re.sub(r'`(.*?)`', r'<font name="Courier">\1</font>', text)
        return text

    def build(self):
        doc = SimpleDocTemplate(self.pdf_file, pagesize=letter)
        story = self.parse_markdown()
        doc.build(story) # customized footer requires fancier build, keeping simple for robustness
        print(f"PDF Generated: {self.pdf_file}")

if __name__ == "__main__":
    pdf_gen = PDFGenerator("Buku_Dokumen_Teknis_Virtual_Lab_Optik.md", "Buku_Dokumen_Teknis_Virtual_Lab_Optik.pdf")
    pdf_gen.build()

