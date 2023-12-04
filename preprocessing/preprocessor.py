import glob
from pdfminer.high_level import extract_text


def write_text_file(data_path,txt_file_name):
    
    for pdf_file in glob.glob(data_path):
        pdf_text = extract_text(pdf_file)

        with open(txt_file_name,"a",encoding="utf-8") as f:
            pdf_name = "\n#######\n" + pdf_file.split("\\")[-1].split(".")[0] + "\n#######\n"
            f.writelines(pdf_name)

            for text in pdf_text.split("\n\n"):
                f.write(text)
                f.writelines("\n*****************************\n")

if __name__ == "__main__":
    txt_file_name = "data.txt"
    pdf_path = r"C:\Users\Nilanjan\Desktop\Copilot\office_assisstant\preprocessing\data\*.pdf"
    write_text_file(pdf_path,txt_file_name)

