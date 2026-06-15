import fitz  # PyMuPDF
import re
import csv
import glob

def extract_sbd_from_pdf(pdf_path):
    sbds = []
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            text = page.get_text()
            for line in text.split('\n'):
                line = line.strip()
                # Pattern: exactly 6 digits
                if re.match(r'^\d{6}$', line):
                    sbds.append(line)
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    return sbds

def main():
    pdf_files = ['fil1.pdf', 'fil2.pdf']
    all_sbds = set()
    
    for pdf_file in pdf_files:
        print(f"Extracting SBD from {pdf_file}...")
        sbds = extract_sbd_from_pdf(pdf_file)
        all_sbds.update(sbds)
        print(f"Found {len(sbds)} SBDs in {pdf_file}")
        
    all_sbds = sorted(list(all_sbds))
    print(f"Total unique SBDs found: {len(all_sbds)}")
    
    with open('danh_sach_sbd.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['SBD'])
        for sbd in all_sbds:
            writer.writerow([sbd])
            
    print("Saved SBDs to danh_sach_sbd.csv")

if __name__ == '__main__':
    main()
