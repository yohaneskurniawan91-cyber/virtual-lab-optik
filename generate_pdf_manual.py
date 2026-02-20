from xhtml2pdf import pisa
import markdown
import os
import datetime
import re

def convert_md_to_beautiful_pdf(source_md, output_pdf):
    # 1. Read Markdown
    with open(source_md, 'r', encoding='utf-8') as f:
        md_text = f.read()

    # 2. Convert to HTML with extensions
    # TOC extension handles [TOC] marker if present, but we rely on pdf:toc
    html_body = markdown.markdown(md_text, extensions=['tables', 'fenced_code', 'def_list', 'attr_list', 'toc'])

    # 3. Create HTML Template with Advanced CSS
    html_template = f"""
    <html>
    <head>
        <title>Buku Panduan Virtual Lab</title>
        <style>
            @page {{
                size: A4;
                margin: 2.5cm;
                @frame footer_frame {{
                    -pdf-frame-content: footerContent;
                    bottom: 1cm;
                    margin-left: 2.5cm;
                    margin-right: 2.5cm;
                    height: 1cm;
                }}
            }}
            
            @page cover {{
                margin: 0cm;
                 background-color: #ecf0f1;
            }}

            body {{
                font-family: Helvetica, sans-serif;
                font-size: 11pt;
                line-height: 1.5;
                color: #333;
            }}

            /* Headers */
            h1 {{
                font-size: 24pt;
                color: #2c3e50;
                text-align: right;
                border-bottom: 3px solid #3498db;
                padding-bottom: 15px;
                margin-top: 50px;
                margin-bottom: 30px;
                page-break-before: always; 
            }}
            
            /* Specific class to avoid break on TOC/Lists pages */
            h1.no-break {{
                page-break-before: avoid;
            }}

            h2 {{
                font-size: 16pt;
                color: #2980b9;
                border-left: 5px solid #e74c3c;
                padding-left: 10px;
                margin-top: 25px;
                margin-bottom: 15px;
            }}

            h3 {{
                font-size: 13pt;
                color: #16a085;
                font-weight: bold;
                margin-top: 15px;
            }}
            
            /* TOC Styling applied by xhtml2pdf to its generated ToC */
            pdftoc {{
                color: #2c3e50;
            }}
            
            /* Levels of TOC */
            pdftoc.pdftoclevel0 {{
                font-weight: bold;
                margin-top: 10px;
                font-size: 14pt;
            }}
            
            pdftoc.pdftoclevel1 {{
                margin-left: 20px;
                font-style: italic;
                font-size: 11pt;
            }}

            /* Tables */
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                font-size: 10pt;
                box-shadow: 0 0 10px rgba(0,0,0,0.05);
            }}
            
            th {{
                background-color: #2c3e50;
                color: white;
                padding: 12px;
                text-align: left;
            }}
            
            td {{
                padding: 10px;
                border-bottom: 1px solid #eee;
            }}
            
            tr:nth-child(even) {{
                background-color: #f8f9fa;
            }}

            /* Code Blocks */
            pre {{
                background-color: #2d3436;
                color: #dfe6e9;
                padding: 15px;
                border-radius: 5px;
                font-family: "Courier New", monospace;
                font-size: 9pt;
                white-space: pre-wrap;
                border-left: 5px solid #00cec9;
            }}
            
            code {{
                background-color: #f0f0f0;
                padding: 2px 4px;
                border-radius: 2px;
                font-family: inherit;
            }}

            img {{
                max-width: 100%;
                height: auto;
                margin: 20px auto;
                display: block;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }}

            /* Cover Page Design */
            .cover-container {{
                text-align: center;
                position: absolute;
                top: 30%;
                left: 0;
                width: 100%;
            }}
            
            .cover-title-box {{
                background-color: #ffffff;
                padding: 40px;
                margin: 0 50px;
                border: 1px solid #bdc3c7;
                box-shadow: 0 10px 20px rgba(0,0,0,0.1);
            }}
            
            .main-title {{
                font-size: 36pt;
                color: #2c3e50;
                font-weight: bold;
                letter-spacing: 2px;
                margin: 0;
            }}
            
            .sub-title {{
                font-size: 18pt;
                color: #e67e22;
                margin-top: 10px;
                font-weight: 300;
            }}
            
            .author-box {{
                margin-top: 100px;
                color: #2c3e50;
                font-size: 14pt;
            }}

        </style>
    </head>
    <body>
        <!-- Footer -->
        <div id="footerContent" style="text-align: center; color: #7f8c8d; font-size: 9pt; border-top: 1px solid #bdc3c7; padding-top: 5px;">
            Buku Panduan Teknis Virtual Lab | Halaman <pdf:pagenumber />
        </div>

        <!-- Cover Page -->
        <div class="cover-container">
            <div class="cover-title-box">
                <div class="main-title">VIRTUAL LAB</div>
                <div class="sub-title">FISIKA DASAR & MODERN</div>
                <hr style="width: 50%; border: 0; border-top: 2px solid #3498db; margin: 20px auto;">
                <div style="font-size: 14pt; color: #34495e;">DOCUMENTATION & TECHNICAL SPECIFICATION</div>
            </div>
            
            <div class="author-box">
                <p><strong>Yohanes Kurniawan</strong></p>
                <p>Mahasiswa S3 Teknologi Pembelajaran</p>
                <p>Universitas Negeri Malang</p>
                <br>
                <p>Versi 2.0 - {datetime.date.today().strftime('%B %Y')}</p>
            </div>
        </div>

        <!-- Switch to normal page template -->
        <pdf:nextpage />

        <!-- Front Matter: TOC -->
        <div style="padding-top: 20px;">
            <h1 class="no-break" style="text-align: center; border: none; font-size: 20pt; page-break-before: avoid;">DAFTAR ISI</h1>
            <pdf:toc />
        </div>

        <pdf:nextpage />

        <!-- Front Matter: List of Figures -->
        <div style="padding-top: 20px;">
             <h1 class="no-break" style="text-align: center; border: none; font-size: 20pt; page-break-before: avoid;">DAFTAR GAMBAR</h1>
             <br>
             <ul>
                <li><strong>Gambar 2.1</strong> - Siklus SAM 2 (Successive Approximation Model) by Michael Allen</li>
             </ul>
        </div>
        
        <pdf:nextpage />

        <!-- Main Content -->
        {html_body}

    </body>
    </html>
    """

    # 4. Generate PDF
    try:
        with open(output_pdf, "wb") as pdf_file:
            pisa_status = pisa.CreatePDF(html_template, dest=pdf_file)

        if pisa_status.err:
            print(f"Error: {pisa_status.err}")
        else:
            print(f"PDF Successfully created: {os.path.abspath(output_pdf)}")
    except Exception as e:
        print(f"Exception during PDF generation: {e}")

if __name__ == "__main__":
    convert_md_to_beautiful_pdf("BUKU_PANDUAN_TEKNIS_V-LAB.md", "BUKU_PANDUAN_TEKNIS_V-LAB_FULL.pdf")
