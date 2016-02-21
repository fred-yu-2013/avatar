# -*- coding: utf-8 -*-

""" Simulate Enter Key to Tab.
"""

import wx


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title=u'Test Enter to Tab Key', size=(800, 600))
        self.panel = wx.Panel(self)
        base_sizer = wx.BoxSizer(wx.VERTICAL)

        text = wx.TextCtrl(self.panel, -1, '', size=(160, -1))
        base_sizer.Add(text, border=5, flag=wx.EXPAND | wx.ALL)

        for i in range(5):
            bttn = wx.Button(self.panel, -1, 'Button %d' % i, size=(160, -1))
            base_sizer.Add(bttn, border=5, flag=wx.EXPAND | wx.ALL)

        return_id = wx.NewId()
        acc_table = wx.AcceleratorTable([(wx.ACCEL_NORMAL, wx.WXK_RETURN, return_id)])
        self.SetAcceleratorTable(acc_table)

        wx.EVT_MENU(self, return_id, self.on_return)

        self.panel.SetAutoLayout(True)
        self.panel.SetSizerAndFit(base_sizer)
        self.Fit()

    def on_return(self, event):
        ctl = wx.Window_FindFocus()
        ctl.Navigate()
        # self.SetAcceleratorTable(wx.NullAcceleratorTable)

if __name__ == '__main__':
    app = wx.App(redirect=False)
    win = MainFrame()
    win.Show()
    app.MainLoop()
