# Chapter 6: Retrieving Information from Users, Common Dialogs
# Recipe 5: PrintDialog
#
import wx

# Recipe 4's sample module
import imagedlg

class PrintBitmapApp(wx.App):
    def OnInit(self):
        self.frame = PrintBitmapFrame(None,
                                      title="Print Dialog")
        self.frame.Show()
        return True

ID_PRINT_PRE = wx.NewId()
class PrintBitmapFrame(imagedlg.ImageDialogFrame):
    def __init__(self, *args, **kwargs):
        super(PrintBitmapFrame, self).__init__(*args, **kwargs)

        # Attributes
        self.printer = BitmapPrinter(self)

        # Setup
        menub = wx.MenuBar()
        filemenu = wx.Menu()
        filemenu.Append(wx.ID_PAGE_SETUP, "Page Setup")
        filemenu.Append(ID_PRINT_PRE, "Print Preview")
        filemenu.Append(wx.ID_PRINT, "Print\tCtrl+P")
        menub.Append(filemenu, "File")
        self.SetMenuBar(menub)

        # Event Handlers
        self.Bind(wx.EVT_MENU, self.OnMenu)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI)

    def OnMenu(self, event):
        """Handle the Print actions"""
        event_id = event.GetId()
        bmp = self.panel.GetBitmap()
        if event_id == wx.ID_PAGE_SETUP:
            self.printer.PageSetup()
        elif event_id == wx.ID_PRINT:
            self.printer.Print(bmp)
        elif event_id == ID_PRINT_PRE:
            self.printer.Preview(bmp)
        else:
            event.Skip()

    def OnUpdateUI(self, event):
        event_id = event.GetId()
        if event_id in (wx.ID_PRINT,
                        ID_PRINT_PRE):
            # Only enable print when a bitmap has
            # been selected.
            bmp = self.panel.GetBitmap()
            event.Enable(bmp.IsOk())
        else:
            event.Skip()

#---- Printer Classes ----#

class BitmapPrinter(object):
    """Manages PrintData and Printing"""
    def __init__(self, parent):
        """Initializes the Printer
        @param parent: parent window
        """
        super(BitmapPrinter, self).__init__()

        # Attributes
        self.parent = parent
        self.print_data = wx.PrintData()

    def CreatePrintout(self, bmp):
        """Creates a printout object
        @param bmp: wx.Bitmap
        """
        assert bmp.IsOk(), "Invalid Bitmap!"
        data = wx.PageSetupDialogData(self.print_data)
        return BitmapPrintout(bmp, data)

    def PageSetup(self):
        """Show the PrinterSetup dialog"""
        # Make a copy of our print data for the setup dialog
        dlg_data = wx.PageSetupDialogData(self.print_data)
        print_dlg = wx.PageSetupDialog(self.parent, dlg_data)
        if print_dlg.ShowModal() == wx.ID_OK:
            # Update the printer data with the changes from
            # the setup dialog.
            newdata = dlg_data.GetPrintData()
            self.print_data = wx.PrintData(newdata)
            paperid = dlg_data.GetPaperId()
            self.print_data.SetPaperId(paperid)
        print_dlg.Destroy()

    def Preview(self, bmp):
        """Show the print preview
        @param bmp: wx.Bitmap
        """
        printout = self.CreatePrintout(bmp)
        printout2 = self.CreatePrintout(bmp)
        preview = wx.PrintPreview(printout, printout2,
                                  self.print_data)
        preview.SetZoom(100)
        if preview.IsOk():
            pre_frame = wx.PreviewFrame(preview,
                                        self.parent,
                                        "Print Preview")
            # The default size of the preview frame
            # sometimes needs some help.
            dsize = wx.GetDisplaySize()
            width = self.parent.GetSize()[0]
            height = dsize.GetHeight() - 100
            pre_frame.SetInitialSize((width, height))
            pre_frame.Initialize()
            pre_frame.Show()
        else:
            # Error
            wx.MessageBox("Failed to create print preview",
                          "Print Error",
                          style=wx.ICON_ERROR|wx.OK)

    def Print(self, bmp):
        """Prints the document"""
        pdd = wx.PrintDialogData(self.print_data)
        printer = wx.Printer(pdd)
        printout = self.CreatePrintout(bmp)
        result = printer.Print(self.parent, printout)
        if result:
            # Store copy of print data for future use
            dlg_data = printer.GetPrintDialogData()
            newdata = dlg_data.GetPrintData()
            self.print_data = wx.PrintData(newdata)
        elif printer.GetLastError() == wx.PRINTER_ERROR:
            wx.MessageBox("Printer error detected.",
                          "Printer Error",
                          style=wx.ICON_ERROR|wx.OK)
        printout.Destroy()

class BitmapPrintout(wx.Printout):
    """Creates an printout of a Bitmap"""
    def __init__(self, bmp, data):
        super(BitmapPrintout, self).__init__()

        # Attributes
        self.bmp = bmp
        self.data = data

    def GetPageInfo(self):
        """Get the page range information"""
        # min, max, from, to # we only support 1 page
        return (1, 1, 1, 1)

    def HasPage(self, page):
        """Is a page within range"""
        return page <= 1

    def OnPrintPage(self, page):
        """Scales and Renders the bitmap
        to a DC and prints it
        """
        dc = self.GetDC() # Get Device Context to draw on

        # Get the Bitmap Size
        bmpW, bmpH = self.bmp.GetSize()

        # Check if we need to scale the bitmap to fit
        self.MapScreenSizeToPageMargins(self.data)
        rect = self.GetLogicalPageRect()
        w, h = rect.width, rect.height
        if (bmpW > w) or (bmpH > h):
            # Image is large so apply some scaling
            self.FitThisSizeToPageMargins((bmpW, bmpH),
                                          self.data)
            x, y = 0, 0
        else:
            # try to center it
            x = (w - bmpW) / 2
            y = (h - bmpH) / 2

        # Draw the bitmap to DC
        dc.DrawBitmap(self.bmp, x, y)

        return True

if __name__ == '__main__':
    app = PrintBitmapApp(False)
    app.MainLoop()
