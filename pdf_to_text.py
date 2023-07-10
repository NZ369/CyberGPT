import os
import math
from io import BytesIO
from uploaders.main import get_pdf_text

def convert_pdfs_to_text(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)

            print("Formatting: ", pdf_path)

            with open(pdf_path, "rb") as pdf:
                file = pdf.read();
                file_content = BytesIO(file)
                text = get_pdf_text([file_content])

                print("content: ", text[:min(len(text), 100)])
            
                text_filename = os.path.splitext(filename)[0] + '.txt'
                
                text_path = os.path.join(
                    folder_path, "{}".format(text_filename)
                )
                
                with open(text_path, 'w', encoding='utf-8') as text_file:
                    text_file.write(text)

# Example usage
folder_path = 's3_source_docs'
convert_pdfs_to_text(folder_path)