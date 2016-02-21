# -*- coding: utf-8 -*-

import StringIO
import wx
from pyPdf import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.lib.utils import ImageReader


def covert_page():
    """ 读取a.pdf文件的一个页面，添加一行字，存到b.pdf
    """
    packet = StringIO.StringIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)
    can.drawString(10, 100, "Hello world")
    can.save()

    #move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(file("document1.pdf", "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # finally, write "output" to a real file
    outputStream = file("destination.pdf", "wb")
    output.write(outputStream)
    outputStream.close()


def bmp2pdf():
    """ bmp -> pdf
    """
    c = canvas.Canvas('bmp2pdf.pdf', pagesize=landscape(A4))
    (w, h) = landscape(A4)
    width, height = letter
    #c.drawImage(filename, inch, height - 2 * inch) # Who needs consistency?
    c.drawImage('bmp2pdf.bmp', 0, 0, w, h)
    c.showPage()
    c.save()


def StringIO2pdf():
    """ bmp -> StringIO -> ImageReader -> pdf
    """
    with open('bmp2pdf.bmp', 'rb') as f:
        buf = StringIO.StringIO(f.read())
        ir = ImageReader(buf)
        c = canvas.Canvas('StringIO2pdf.pdf', pagesize=landscape(A4))
        (w, h) = landscape(A4)
        width, height = letter
        #c.drawImage(filename, inch, height - 2 * inch) # Who needs consistency?
        c.drawImage(ir, 0, 0, w, h)
        c.showPage()
        c.save()


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'wxBitmap2pdf')
        self.wxBitmap2pdf()
        self.Show()

    def wxBitmap2pdf(self):
        """ bmp -> StringIO -> ImageReader -> pdf
        """
        bitmap = wx.Bitmap('bmp2pdf.bmp', wx.BITMAP_TYPE_BMP)
        image = wx.ImageFromBitmap(bitmap)
        buf = StringIO.StringIO(image.GetDataBuffer())
        # bitmap.CopyToBuffer(buf)
        # bitmap.SaveFile(buf, wx.BITMAP_TYPE_BMP)
        fbuf = wx.FFileOutputStream(buf)
        image.SaveFile(buf, wx.BITMAP_TYPE_BMP)
        # bitmap.SaveFile(buf, wx.BITMAP_TYPE_BMP)
        # image.
        # ir = ImageReader(buf)
        # c = canvas.Canvas('wxBitmap2pdf.pdf', pagesize=landscape(A4))
        # (w, h) = landscape(A4)
        # width, height = letter
        # #c.drawImage(filename, inch, height - 2 * inch) # Who needs consistency?
        # c.drawImage(ir, 0, 0, w, h)
        # c.showPage()
        # c.save()

if __name__ == '__main__':
    # covert_page()
    # bmp2pdf()
    # StringIO2pdf()

    # INFO: Test with wx.
    app = wx.PySimpleApp()
    frame = MainFrame()
    app.MainLoop()
