
from pypdf import PdfReader

def extract_pdf_content(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        print(f"Total Pages: {len(reader.pages)}")
        
        text_content = ""
        # Extract first 5 pages to capture Title, Approval, TOC, and Chapter 1
        for i, page in enumerate(reader.pages[:5]): 
            text = page.extract_text()
            print(f"--- Page {i+1} ---")
            print(text)
            text_content += text
            
        return text_content
    except Exception as e:
        print(f"Error reading PDF: {e}")

if __name__ == "__main__":
    extract_pdf_content("DOKUMENTASI_TEKNIS_VIRTUAL_LAB_FINAL.pdf")
