import os
# https://pyfpdf.readthedocs.io/en/latest/Tutorial/index.html

from fpdf import FPDF
from Book.book import Book


class PdfFile:
    OUTPUT_FOLDER = "Downloads"

    @staticmethod
    def _next_file_name():
        files = os.listdir(PdfFile.OUTPUT_FOLDER)
        max_file = 0
        for file in files:
            # https://stackoverflow.com/questions/35993549/python-parse-int-from-string
            current_file_number = int(file.title().upper().replace("VIVOD_(", "").replace(").PDF", ""))
            max_file = max(max_file, current_file_number)
        max_file = max_file + 1
        return 'Vivod_(%s).pdf' % max_file

    @staticmethod
    def save(results):
        if not os.path.exists(PdfFile.OUTPUT_FOLDER):
            os.mkdir(PdfFile.OUTPUT_FOLDER)

        pdf = FPDF('P', 'mm', 'A4')
        filename = PdfFile.OUTPUT_FOLDER + "/" + PdfFile._next_file_name()

        # https://stackoverflow.com/questions/67130517/fpdf-unicodeencodeerror-latin-1-codec-cant-encode-character-u2013-in-pos
        pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        pdf.set_font('DejaVu', '', 14)
        pdf.add_page()
        pdf.write(8, 'ID   Author   Title   Year')
        pdf.ln(8)
        print('ID   Название   Автор   Год')
        for result in results:
            (book_id, book) = result
            formatted_book = "%s: %s, %s %s" % (book_id, book.title, book.author, book.year)
            print(formatted_book)
            pdf.write(8, formatted_book)
            pdf.ln(8)
        pdf.output(filename, 'F')
        pdf.close()
        # os.system("start %s" % filename)
        # print(r"File opened '%s'" % filename)

    @staticmethod
    def save_one(result):
        PdfFile.save([result])



