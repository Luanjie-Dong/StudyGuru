from pdf2image import convert_from_path
import pytesseract
from PyPDF2 import PdfReader
import re
from pptx import Presentation
from PIL import Image
from io import BytesIO
from pathlib import Path

#StudyGuruExtractor = SGExtractor
class SGExtractor:

    def __init__(self,file_path):
        self.data = file_path
        


    def clean_text(self,content):
        content = re.sub(r"(\w+)-\n(\w+)", r"\1\2", content)
        unwanted_patterns = [
            "\\n",
            "  —",
            "——————————",
            "—————————",
            "—————",
            r"\\u[\dA-Fa-f]{4}",
            r"\uf075",
            r"\uf0b7",
        ]
        for pattern in unwanted_patterns:
            content = re.sub(pattern, "", content)

        content = re.sub(r"(\w)\s*-\s*(\w)", r"\1-\2", content)
        content = re.sub(r"\s+", " ", content)
        return content

    def read_pdf(self,pdf_path):
        reader = PdfReader(pdf_path)
        combined_text = ""

        for page_num, page in enumerate(reader.pages, start=1):
            print(f"Processing page {page_num}")

            selectable_text = page.extract_text()
            if selectable_text:
                print("Found selectable text.")
                combined_text += selectable_text

            try:
                images = convert_from_path(pdf_path, dpi=300, grayscale=True, first_page=page_num, last_page=page_num)
                for image in images:
                    print("Performing OCR on image...")
                    ocr_text = pytesseract.image_to_string(image)
                    combined_text += ocr_text
            except Exception as e:
                print(f"Error processing images on page {page_num}: {e}")

        cleaned_text = self.clean_text(combined_text)

        return cleaned_text
    
    def read_pptx(self,pptx_path):
        presentation = Presentation(pptx_path)
        
        text_content = ""
        
        for i, slide in enumerate(presentation.slides, start=1):
            print(f"Processing slide {i}")
            
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    text_content += shape.text + "\n"
                
                if shape.shape_type == 13: 
                    try:
                        image_bytes = shape.image.blob
                        image = Image.open(BytesIO(image_bytes))
                        
                        ocr_text = pytesseract.image_to_string(image)
                        text_content += ocr_text + "\n"
                    except Exception as e:
                        print(f"Error processing image on slide {i}: {e}")
        
        cleaned_text = self.clean_text(text_content)
        return cleaned_text
    

    def read_image(self,image_path):
        image = Image.open(image_path)
        return pytesseract.image_to_string(image)
    

    def extract_content(self):

        file_type = Path(self.data).suffix

        if file_type == ".pdf":
            return self.read_pdf(self.data)
        
        if file_type == ".pptx":
            return self.read_pptx(self.data)
        
        if file_type in (".jpg", ".png", ".bmp", ".tiff"):
            return self.read_image(self.data)
        
    
    def save_test_data(self,save_path):

        with open(save_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"test data saved as {save_path}!")

        

        
    



if __name__=="__main__":

    test_type = "pdf"
    test_path = f'test_data/test.{test_type}'
    extractor = SGExtractor(test_path)
    content = extractor.extract_content()
    print(content)

    save_path = f"test_data/test_result({test_type}).txt"
    save_test_content = extractor.save_test_data(save_path)

