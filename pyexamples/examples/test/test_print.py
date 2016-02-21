__author__ = 'Fred'
#coding=utf-8

import wx
import os

FONTSIZE = 10


class TextDocPrintout(wx.Printout):
    """
    A printout class that is able to print simple text documents.
    Does not handle page numbers or titles, and it assumes that no
    lines are longer than what will fit within the page width.  Those
    features are left as an exercise for the reader. ;-)
    原始的Printout
    """
    def __init__(self, text, title, margins):
        wx.Printout.__init__(self, title)
        self.lines = text.split(' ')
        self.margins = margins

    def HasPage(self, page):
        # print 'HasPage'
        return page <= self.numPages

    def GetPageInfo(self):
        # print 'GetPageInfo'
        return (1, self.numPages, 1, self.numPages)

    def _CalculateScale(self, dc):
        # Scale the DC such that the printout is roughly the same as
        # the screen scaling.
        ppiPrinterX, ppiPrinterY = self.GetPPIPrinter()  # 返回打印机的像素密度
        ppiScreenX, ppiScreenY = self.GetPPIScreen()  # 返回屏幕的像素密度
        logScale = float(ppiPrinterX) / float(ppiScreenX)  # 打印机相对于屏幕的密度

        # Now adjust if the real page size is reduced (such as when
        # drawing on a scaled wx.MemoryDC in the Print Preview.)  If
        # page width == DC width then nothing changes, otherwise we
        # scale down for the DC.
        pw, ph = self.GetPageSizePixels()  # 打印机页面的大小，比打印纸的大小要小些
        dw, dh = dc.GetSize()  # 屏幕的大小
        scale = logScale * float(dw) / float(pw)  # 屏幕相对于打印机的实际尺寸（单位：毫米）

        # Set the DC's scale.
        dc.SetUserScale(scale, scale)  # 设置屏幕尺寸相对于打印机尺寸的比例（单位：毫米）

        # Find the logical units per millimeter (for calculating the margins)
        # self.logUnitsMM = float(ppiPrinterX) / (logScale * 25.4) #
        self.logUnitsMM = float(ppiScreenX) / 25.4 # 屏幕上每毫米多少个点

    def _CalculateLayout(self, dc):
        # 计算逻辑纸张上已有的页边距，它被用来限制页面的那一部分可以被打印。
        page_rect = self.GetLogicalPageRect()
        paper_rect = self.GetLogicalPaperRect()
        dl = page_rect.Left - paper_rect.Left
        dt = page_rect.Top - paper_rect.Top
        dr = paper_rect.Right - page_rect.Right
        db = paper_rect.Bottom - page_rect.Bottom

        # print "dl, dt, dr, db, ", dl, dt, dr, db

        # Determine the position of the margins and the page/line height
        topLeft, bottomRight = self.margins
        dw, dh = dc.GetSize()
        self.x1 = topLeft.x * self.logUnitsMM - dl
        self.y1 = topLeft.y * self.logUnitsMM - dt
        self.x2 = dc.DeviceToLogicalXRel(dw) - bottomRight.x * self.logUnitsMM + dr
        self.y2 = dc.DeviceToLogicalYRel(dh) - bottomRight.y * self.logUnitsMM + db

        # print 'Margin rect: ', self.x1, self.y1, self.x2, self.y2

        # use a 1mm buffer around the inside of the box, and a few
        # pixels between each line
        # 只是为了绘制文本而设置
        self.pageHeight = self.y2 - self.y1 - 2 * self.logUnitsMM
        font = wx.Font(FONTSIZE, wx.TELETYPE, wx.NORMAL, wx.NORMAL)
        dc.SetFont(font)
        self.lineHeight = dc.GetCharHeight()
        self.linesPerPage = int(self.pageHeight/self.lineHeight)

    def OnPreparePrinting(self):
        # print 'OnPreparePrinting'
        # calculate the number of pages
        # 有多少页是固定的，可以先计算到，故此处只是用来计算有多少页，而非设置dc
        dc = self.GetDC()
        self._CalculateScale(dc)
        self._CalculateLayout(dc)
        self.numPages = len(self.lines) / self.linesPerPage
        if len(self.lines) % self.linesPerPage != 0:
            self.numPages += 1

    def OnPrintPage(self, page):
        # print 'OnPrintPage'
        dc = self.GetDC()  # 获取绘图的DC
        self._CalculateScale(dc)
        self._CalculateLayout(dc)

        print 'Margin rect: ', self.x1, self.y1, self.x2, self.y2
        TextDocPrintout.dump_dc(self, dc)

        # draw a page outline at the margin points
        dc.SetPen(wx.Pen("black", 0))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        r = wx.RectPP((self.x1, self.y1),
                      (self.x2, self.y2))
        dc.DrawRectangleRect(r)
        dc.SetClippingRect(r)

        # Draw the text lines for this page
        line = (page-1) * self.linesPerPage
        x = self.x1 + self.logUnitsMM
        y = self.y1 + self.logUnitsMM
        while line < (page * self.linesPerPage):
            dc.DrawText(self.lines[line], x, y)
            y += self.lineHeight
            line += 1
            if line >= len(self.lines):
                break
        return True

    @staticmethod
    def dump_dc(self, dc):
        print 'dc.GetMapMode(), %d, wx.MM_METRIC, %d, wx.MM_TEXT, %d' % (dc.GetMapMode(), wx.MM_METRIC, wx.MM_TEXT)
        print 'dc.GetLogicalOrigin(), %s' % repr(dc.GetLogicalOrigin())
        print 'dc.GetPPI(), %s' % repr(dc.GetPPI())
        print 'dc.GetSize(), %s' % repr(dc.GetSize())
        print 'dc.GetSizeMM(), %s' % repr(dc.GetSizeMM())
        print 'dc.GetUserScale(), %s' % repr(dc.GetUserScale())
        # print 'self.GetLogicalPageRect(), %s' % repr(self.GetLogicalPageRect())
        print 'dc.GetLogicalOrigin(), %s' % repr(dc.GetLogicalOrigin())
        print 'dc.GetLogicalScale(), %s' % repr(dc.GetLogicalScale())

        # print 'self.GetLogicalPageMarginsRect(), %s' % repr(self.GetLogicalPageMarginsRect(self.data))
        print 'self.GetLogicalPageRect(), %s' % repr(self.GetLogicalPageRect())
        print 'self.GetLogicalPaperRect(), %s' % repr(self.GetLogicalPaperRect())
        print 'self.GetPPIPrinter(), %s' % repr(self.GetPPIPrinter())
        print 'self.GetPPIScreen(), %s' % repr(self.GetPPIScreen())
        print 'self.GetPageInfo(), %s' % repr(self.GetPageInfo())
        print 'self.GetPageSizeMM(), %s' % repr(self.GetPageSizeMM())
        print 'self.GetPageSizePixels(), %s' % repr(self.GetPageSizePixels())
        print 'self.GetPaperRectPixels(), %s' % repr(self.GetPaperRectPixels())
        print 'self.GetTitle(), %s' % repr(self.GetTitle())


class MarginPrintout(wx.Printout):
    '''
    用于打印出来的Margin和设置的一致
    '''
    def __init__(self):
        wx.Printout.__init__(self, 'Margin printout')

    def HasPage(self, page):
        return page <= 1

    def GetPageInfo(self):
        return (1, 1, 1, 1)

    # def OnPreparePrinting(self):
    #     self.MapScreenSizeToPaper()

    def OnPrintPage(self, page):
        # self.MapScreenSizeToPaper() # 按屏幕ppi(默认96)绘图，不同的显示器ppi不同
        dc = self.GetDC()
        self._set_user_scale(dc)

        TextDocPrintout.dump_dc(self, dc)

        # 绘制页边距区域
        margins = (20, 20, 20, 20)
        self._draw_margins(dc, margins)

        # 绘制一个固定大小的矩形
        r = wx.Rect(self._mm2s(dc, 40), self._mm2s(dc, 40), self._mm2s(dc, 20), self._mm2s(dc, 20))
        dc.DrawRectangleRect(r)

    def _mm2s(self, dc, mm):
        # sppi, _ = self.GetPPIScreen()
        sppi = dc.GetPPI().x
        return int(float(mm) * float(sppi) / 25.4)

    def _set_user_scale(self, dc):
        sppi = dc.GetPPI().x
        ssize = dc.GetSize().x
        pppi, _ = self.GetPPIPrinter()
        psize, _ = self.GetPageSizePixels()

        # 不准
        # xsmm, ysmm = dc.GetSizeMM() # Screen size.
        # xpmm, ypmm = self.GetPageSizeMM()
        # sp_scale = float(xsmm) / float(xpmm)

        sp_scale = (float(ssize) * float(pppi)) / (float(psize) * float(sppi))

        dc.SetUserScale(sp_scale, sp_scale)

    def _draw_margins(self, dc, margins):
        xpppi, ypppi = self.GetPPIPrinter()
        page_r = self.GetPaperRectPixels()
        pw, ph = self.GetPageSizePixels()
        margin_l, margin_t, margin_r, margin_b = margins # mm
        orig_dl = int(float(0 - page_r.left) / float(xpppi) * 25.4)
        orig_dt = int(float(0 - page_r.top) / float(xpppi) * 25.4)
        orig_dr = int(float(pw - page_r.right) / float(xpppi) * 25.4)
        orig_db = int(float(ph - page_r.bottom) / float(xpppi) * 25.4)
        x1 = self._mm2s(dc, margin_l - orig_dl)
        y1 = self._mm2s(dc, margin_t - orig_dt)
        x2 = self._mm2s(dc, 210 - (margin_r - orig_dr))
        y2 = self._mm2s(dc, 297 - (margin_b - orig_db))
        print 'margins:', margin_l - orig_dl, margin_t - orig_dt, 210 - (margin_r - orig_dr), 297 - (margin_b - orig_db)
        r = wx.RectPP(wx.Point(x1, y1), wx.Point(x2, y2))
        print repr(r)
        dc.DrawRectangleRect(r)


class PrintFrameworkSample(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, size=(640, 480),
                          title="Print Framework Sample")
        self.CreateStatusBar()

        # A text widget to display the doc and let it be edited
        self.tc = wx.TextCtrl(self, -1, "",
                              style=wx.TE_MULTILINE|wx.TE_DONTWRAP)
        self.tc.SetFont(wx.Font(FONTSIZE, wx.TELETYPE, wx.NORMAL, wx.NORMAL))
        filename = os.path.join(os.path.dirname(__file__), "sample-text.txt")
        self.tc.SetValue(open(filename).read())
        self.tc.Bind(wx.EVT_SET_FOCUS, self.OnClearSelection)
        wx.CallAfter(self.tc.SetInsertionPoint, 0)

        # Create the menu and menubar
        menu = wx.Menu()
        item = menu.Append(-1, "Page Setup...	F5",
                           "Set up page margins and etc.")
        self.Bind(wx.EVT_MENU, self.OnPageSetup, item)
        item = menu.Append(-1, "Print Setup...	F6",
                           "Set up the printer options, etc.")
        self.Bind(wx.EVT_MENU, self.OnPrintSetup, item)
        item = menu.Append(-1, "Print Preview...	F7",
                           "View the printout on-screen")
        self.Bind(wx.EVT_MENU, self.OnPrintPreview, item)
        item = menu.Append(-1, "Print...	F8", "Print the document")
        self.Bind(wx.EVT_MENU, self.OnPrint, item)
        menu.AppendSeparator()
        item = menu.Append(-1, "E&xit", "Close this application")
        self.Bind(wx.EVT_MENU, self.OnExit, item)

        menubar = wx.MenuBar()
        menubar.Append(menu, "&File")
        self.SetMenuBar(menubar)

        # initialize the print data and set some default values
        self.pdata = wx.PrintData()
        # self.pdata.SetPaperId(wx.PAPER_LETTER)  # 设置页面的大小
        self.pdata.SetPaperId(wx.PAPER_A4)
        self.pdata.SetOrientation(wx.PORTRAIT)
        self.margins = (wx.Point(15,15), wx.Point(15,15))

    def OnExit(self, evt):
        self.Close()

    def OnClearSelection(self, evt):
        evt.Skip()
        wx.CallAfter(self.tc.SetInsertionPoint,
                     self.tc.GetInsertionPoint())

    def OnPageSetup(self, evt):
        """
        设置页面大小，页边距。
        """
        data = wx.PageSetupDialogData()
        data.SetPrintData(self.pdata)

        data.SetDefaultMinMargins(True)
        data.SetMarginTopLeft(self.margins[0])
        data.SetMarginBottomRight(self.margins[1])

        dlg = wx.PageSetupDialog(self, data)
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetPageSetupData()
            self.pdata = wx.PrintData(data.GetPrintData())  # force a copy
            self.pdata.SetPaperId(data.GetPaperId())
            self.margins = (data.GetMarginTopLeft(),
                            data.GetMarginBottomRight())
        dlg.Destroy()

    def OnPrintSetup(self, evt):
        """
        设置用哪台打印机打印。
        """
        data = wx.PrintDialogData(self.pdata)
        dlg = wx.PrintDialog(self, data)
        # dlg.GetPrintDialogData().SetSetupDialog(True)
        dlg.ShowModal()
        data = dlg.GetPrintDialogData()
        self.pdata = wx.PrintData(data.GetPrintData())  # force a copy
        dlg.Destroy()

    def OnPrintPreview(self, evt):
        """
        预览打印页面。
        """
        data = wx.PrintDialogData(self.pdata)
        text = self.tc.GetValue()
        # printout1 = TextDocPrintout(text, "title", self.margins)
        # # printout2 = None  # TextDocPrintout(text, "title", self.margins)
        # printout2 = TextDocPrintout(text, "title", self.margins)
        printout1, printout2 = MarginPrintout(), MarginPrintout()
        preview = wx.PrintPreview(printout1, printout2, data)
        if not preview.Ok():
            wx.MessageBox("Unable to create PrintPreview!", "Error")
        else:
            # create the preview frame such that it overlays the app frame
            frame = wx.PreviewFrame(preview, self, "Print Preview",
                                    pos=self.GetPosition(),
                                    size=self.GetSize())
            frame.Initialize()
            frame.Show()

    def OnPrint(self, evt):
        """
        打印内容到打印机。
        """
        data = wx.PrintDialogData(self.pdata)
        printer = wx.Printer(data)
        text = self.tc.GetValue()
        printout = TextDocPrintout(text, "title", self.margins)
        useSetupDialog = True
        if not printer.Print(self, printout, useSetupDialog) and printer.GetLastError() == wx.PRINTER_ERROR:
            wx.MessageBox(
                "There was a problem printing. "
                "Perhaps your current printer is not set correctly?",
                "Printing Error", wx.OK)
        else:
            data = printer.GetPrintDialogData()
            self.pdata = wx.PrintData(data.GetPrintData()) # force a copy
        printout.Destroy()


app = wx.PySimpleApp()
frm = PrintFrameworkSample()
frm.Show()
app.MainLoop()