# -*- coding: utf-8 -*-

#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode wxPython tutorial

This program draws a line on the
frame window after a while

author: Jan Bodnar
website: zetcode.com
last edited: November 2010
"""

import wx

class Example(wx.Frame):
    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title,
            size=(250, 150))

        wx.FutureCall(2000, self.DrawLine)

        self.Centre()
        self.Show()

    def DrawLine(self):
        dc = wx.ClientDC(self)
        dc.DrawLine(50, 60, 190, 60)

class Example2(wx.Frame):
    def __init__(self, parent, title):
        super(Example2, self).__init__(parent, title=title,
            size=(250, 150))

        self.Bind(wx.EVT_PAINT, self.OnPaint)

        self.Centre()
        self.Show()

    def OnPaint(self, e):
        dc = wx.PaintDC(self)
        dc.DrawLine(50, 60, 190, 60)

if __name__ == '__main__':
    app = wx.App()
    Example2(None, 'Line')
    app.MainLoop()
