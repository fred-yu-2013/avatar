__author__ = 'Fred'
#encoding=utf-8

import unittest
import wx


class MyDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, 'Test')
        wx.Button(self, wx.ID_OK)


class TestMyDialog(unittest.TestCase):

    def setUp(self):
        self.app = wx.App()
        self.frame = wx.Frame(None)
        self.frame.Show()

    def tearDown(self):
        wx.CallAfter(self.app.Exit)
        self.app.MainLoop()

    def testDialog(self):
        def clickOK():
            clickEvent = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, wx.ID_OK)
            self.dlg.ProcessEvent(clickEvent)
        wx.CallAfter(clickOK)  # 处理完此消息之后，调用指定函数，可用于退出模态对话框。
        self.ShowDialog()

    def ShowDialog(self):
        self.dlg = MyDialog(self.frame)
        self.dlg.ShowModal()
        self.dlg.Destroy()

if __name__ == '__main__':
    unittest.main()