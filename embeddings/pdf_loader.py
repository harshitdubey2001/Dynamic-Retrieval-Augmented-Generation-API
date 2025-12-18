import fitz
from pathlib import Path



def extract_pdf_text(pdf_path: str):
    doc = fitz.open(pdf_path)
    pages = []

    for i,page in enumerate(doc):
        text = page.get_text().strip()
        if text:
            pages.append({
                "page":i+1,
                "text":text
            })

    return pages 

def extract_image_from_pdf(pdf_path: str,output_dir:Path):
    doc = fitz.open(pdf_path)
    image_paths = []

    output_dir.mkdir(exist_ok=True,parents=True)

    for page_index,page,in enumerate(doc):
        for img_index,img in enumerate(page.get_images(full=True)):
            xref = img[0]
            pix = fitz.Pixmap(doc,xref)

            if pix.n > 4:
                pix = fitz.Pixmap(fitz.csRGB,pix)

            img_path = output_dir / f"page_{page_index+1}_img_{img_index}.png"
            pix.save(img_path)
            pix = None

            image_paths.append(str(img_path))

    return image_paths                   
