from . import url, Route
from .tools import pdf2png
from io import BytesIO
from base64 import b64encode
from PyPDF2 import PdfFileReader, PdfFileMerger, PdfFileWriter
from tornado.escape import json_encode


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
        pages = int(len(self.request.arguments) / 3)
        output = PdfFileWriter()
        bodies = {}
        for el in pdfs:
            if el.filename not in bodies:
                bodies[el.filename] = el.body
        if pdfs:
            filename = pdfs[0].filename
            for x in range(pages):
                pageparent = self.get_argument("pages[%d]['filename']" % x)
                pagenum = int(self.get_argument("pages[%d]['pagenum']" % x))
                rotation = int(
                    self.get_argument("pages[%d]['rotation']" % x) or 0)
                for name in bodies:
                    if name == pageparent:
                        page = PdfFileReader(
                            BytesIO(bodies.get(name))).getPage(pagenum)
                        if rotation and rotation != 0:
                            method = ('rotateClockwise' if rotation > 0
                                      else 'rotateCounterClockwise')
                            getattr(page, method)(abs(rotation))
                        output.addPage(page)
            _file = BytesIO()
            output.write(_file)
            _file.seek(0)
            self.set_header('Content-Type', 'application/pdf')
            self.set_header('Content-Disposition',
                            'attachment; filename=%s' % filename)
            self.write(b64encode(_file.read()))


@url(r'/preview/')
class Preview(Route):
    def post(self):
        pdf = self.request.files.get('file', None)[0]
        _file = PdfFileReader(BytesIO(pdf.body))
        numpages = _file.getNumPages()
        output = {}
        for i in range(numpages):
            currpage = _file.getPage(i)
            writer = PdfFileWriter()
            writer.addPage(currpage)
            tmp = BytesIO()
            writer.write(tmp)
            tmp.seek(0)
            image = pdf2png(tmp, (200, 200))
            image.seek(0)
            output[i] = b64encode(image.read()).decode('utf-8')
        self.set_header("Content-Type", "application/json")
        return self.write(json_encode(output))


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

        _file = BytesIO()
        output.write(_file)
        _file.seek(0)
        self.set_header('Content-Type', 'application/pdf')
        self.set_header('Content-Disposition', 'attachment; filename=%s' % filename)
        self.write(_file.read())
        return self.finish()
