from . import url, Route
from io import BytesIO
from base64 import b64encode
from tempfile import TemporaryFile
from PyPDF2 import PdfFileReader, PdfFileMerger, PdfFileWriter


@url(r'/')
class Index(Route):
    def get(self):
        return self.render('index.html')


@url(r'/merge/')
class Merge(Route):
    def get(self):
        return self.render('merge.html')

    def post(self):
        pdfs = self.request.files.get('files[]', None)
        output = PdfFileMerger()
        if pdfs:
            filename = pdfs[0].filename
            for pdf in pdfs:
                body = getattr(pdf, 'body', None)
                if body:
                    output.append(PdfFileReader(BytesIO(body)))
            _file = TemporaryFile()
            output.write(_file)
            _file.seek(0)
            self.set_header('Content-Type', 'application/pdf')
            self.set_header('Content-Disposition',
                            'attachment; filename=%s' % filename)
            self.write(b64encode(_file.read()))


@url(r'/rotate_pdfs/')
class RotatePDFs(Route):
    def get(self):
        return self.render('rotateall.html')

    def post(self):
        way = self.get_argument('way', 'clockwise')
        degrees = int(self.get_argument('degrees') or 90)
        pages_only = self.get_argument('only-pages') or None
        if pages_only:
            if '-' in pages_only:
                pages_only = list((int(x) for x in pages_only.split('-')))
            else:
                pages_only = int(pages_only)
        pdf = self.request.files.get('pdf', None)
        if not pdf:
            return
        pdf = pdf[0]
        filename = pdf.filename
        body = getattr(pdf, 'body', None)
        if not body:
            return

        _input = PdfFileReader(BytesIO(body))
        output = PdfFileWriter()
        pages = _input.getNumPages()
        method = 'rotateClockwise' if way == 'clockwise' else 'rotateCounterClockwise'
        pages_condition, one_page_condition = None, None
        if pages_only:
            if hasattr(pages_only, '__iter__'):
                pages_condition = (pages_only[1] > pages_only[0]) and pages_only[1] < pages
            else:
                one_page_condition = True

        if pages_condition:
            for i in range(pages_only[0]-1):
                output.addPage(_input.getPage(i))
            for i in range(pages_only[0]-1, pages_only[1]):
                output.addPage(getattr(_input.getPage(i), method)(degrees))
            for i in range(pages_only[1], pages):
                output.addPage(_input.getPage(i))
        elif one_page_condition:
            for i in range(pages_only-1):
                output.addPage(_input.getPage(i))
            output.addPage(getattr(_input.getPage(pages_only-1), method)(degrees))
            for i in range(pages_only, pages):
                output.addPage(_input.getPage(i))
        else:
            for i in range(pages):
                output.addPage(getattr(_input.getPage(i), method)(degrees))

        _file = TemporaryFile()
        output.write(_file)
        _file.seek(0)
        self.set_header('Content-Type', 'application/pdf')
        self.set_header('Content-Disposition', 'attachment; filename=%s' % filename)
        self.write(_file.read())
        return self.finish()
