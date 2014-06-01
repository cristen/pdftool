from . import url, Route
from io import BytesIO
from tempfile import TemporaryFile
from PyPDF2 import PdfFileReader, PdfFileMerger

@url(r'/')
class Index(Route):
    def get(self):
        return self.render('index.html')


@url(r'/merge/')
class Merge(Route):
    def get(self):
        return self.render('merge.html')

    def post(self):
        pdfs = self.request.files.get('pdfs', None)
        output = PdfFileMerger()
        if pdfs:
            # Sort files to merge in the right order
            # Files will be merged and queued according to their suffix (eg: file_1.pdf, file_2.pdf)
            pdfs = sorted(pdfs, key = lambda x: int(x.filename.rsplit(".")[0].rsplit("_")[1]))
            filename = pdfs[0].filename
            for pdf in pdfs:
                body = getattr(pdf, 'body', None)
                if body:
                    output.append(PdfFileReader(BytesIO(body)))
            _file = TemporaryFile()
            output.write(_file)
            _file.seek(0)
            self.set_header('Content-Type', 'application/pdf')
            self.set_header('Content-Disposition', 'attachment; filename=%s' % filename)
            self.write(_file.read())
            return self.finish()


@url(r'/rotate_pdfs/')
class RotatePDFs(Route):
    def get(self):
        return self.render('rotateall.html')
