import os
from PyPDF2 import PdfReader, PdfWriter
from tqdm import tqdm


def pdf_splitter(path):
    fname = os.path.splitext(os.path.basename(path))[0]
    fname = fname.split('.')[0]
    pdf = PdfReader(path)
    for page in tqdm(range(len(pdf.pages))):
        pdf_writer = PdfWriter()
        pdf_writer.add_page(pdf.pages[page])

        output_filename = '{}_page_{}.pdf'.format(fname, page+1)
        output_path = os.path.join('data',output_filename)
        with open(output_path, 'wb') as out:
            pdf_writer.write(out)

if __name__ == '__main__':
    path = r"C:\Users\Nilanjan\Desktop\Copilot\office_assisstant\data"
    for pdf in os.listdir(path):
        print(pdf)
        pdf_path = os.path.join(path, pdf)
        pdf_splitter(pdf_path)