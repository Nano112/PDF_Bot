import os
import PyPDF2

class PDF_files:
    def __init__(self):
        self.reload()

    def reload(self):
        self.files = []
        for filename in sorted(os.listdir('pdf_files/')):
            self.files.append(filename)

    def list(self):
        return self.files

    def does_exist(self, name):
        return name in self.files

    def get_page_count(self,file_name):
        with open("pdf_files/" + file_name, 'rb') as f:
            pdf = PyPDF2.PdfFileReader(f)
            number_of_pages = pdf.getNumPages()
        return number_of_pages
