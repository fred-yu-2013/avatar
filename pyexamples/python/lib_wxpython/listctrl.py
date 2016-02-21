__author__ = 'Fred'
#encoding=utf-8

import wx


class MyListItem(wx.ListItem):
    def __init__(self):
        wx.ListItem.__init__(self)


class MyListCtrl(wx.ListCtrl):
    def __init__(self, parent, size=(750, 500)):
        # 有行列线
        style = wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_HRULES | wx.LC_VRULES
        wx.ListCtrl.__init__(self, parent, style=style, size=size)

        self.InsertColumn(0, 'Id')
        self.InsertColumn(1, 'Year')

        self.InsertStringItem(0, '1')
        self.SetStringItem(0, 1, 'Fred')


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title=u'测试wxListCtrl', size=(800, 600))
        self.panel = wx.Panel(self)
        base_sizer = wx.BoxSizer(wx.VERTICAL)

        self.list = MyListCtrl(self.panel)
        base_sizer.Add(self.list, border=5, flag=wx.EXPAND | wx.ALL)

        # font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
        # font.SetPointSize(60)
        font = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL, False, face=u'@微软雅黑')
        # self.panel.SetFont(wx.Font(36, wx.SWISS, wx.NORMAL, wx.NORMAL, False,'MS Shell Dlg 2'))
        self.list.SetFont(font)

        self.panel.SetAutoLayout(True)
        self.panel.SetSizerAndFit(base_sizer)
        self.Fit()

if __name__ == '__main__':
    app = wx.App(redirect=False)
    win = MainFrame()
    win.Show()
    app.MainLoop()
