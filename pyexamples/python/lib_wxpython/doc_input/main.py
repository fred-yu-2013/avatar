# -*- coding: utf-8 -*-
import wx
import wx.richtext


class ExampleData:
    def __init__(self):
        self.remark = u''
        self.input_area = wx.Rect(100, 100, 320, 240)
        self.input_bg_default_color = (255, 255, 255)
        self.input_bg_edit_color = (200, 200, 200)
        self.input_bg_color = self.input_bg_default_color


class Example2(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(640, 480))
        # self.panel = wx.Panel(self, style=wx.FULL_REPAINT_ON_RESIZE)

        self.data = ExampleData()

        # self.input = wx.TextCtrl(self, -1, '', size=(125, -1))
        self.input = wx.richtext.RichTextCtrl(self, style=wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER,
                                              pos=(self.data.input_area.left, self.data.input_area.top),
                                              size=(self.data.input_area.width, self.data.input_area.height))
        self.input.Hide()

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnClick)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        # self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        # self.Bind(wx.EVT_CHAR, self.OnChar)  # 输入一个字符，可以是中文

        # # 手动处理文本输入，太麻烦，改为文本框
        # self.__show_caret()

        self.Centre()
        self.Show()

    def __show_caret(self):
        dc = wx.ClientDC(self)
        # dc.SetFont(self.m_font)
        self.m_heightChar = dc.GetCharHeight()
        self.m_widthChar = dc.GetCharWidth()
        self.caret = wx.Caret(self, wx.Size(self.m_widthChar,self.m_heightChar))
        self.SetCaret(self.caret)
        self.m_xCaret = self.m_yCaret = self.m_xChars = self.m_yChars = 0
        self.m_xMargin = self.m_yMargin = 100
        self.caret.MoveXY(self.m_xMargin, self.m_yMargin)
        self.caret.Show()

    def OnPaint(self, event):
        """
        窗口重绘事件，触发后，不会刷新窗口，需要self.Refresh()
        :param event:
        """
        dc = wx.PaintDC(self)
        dc.Clear()
        size = self.GetClientSize()
        # print size.width, size.height
        dc.DrawRectangle(10, 10, size.width - 20, size.height - 20)

        dc.SetBrush(wx.Brush(self.data.input_bg_color, wx.SOLID))
        dc.DrawRectangle(self.data.input_area.left - 5, self.data.input_area.top - 5,
                         self.data.input_area.width + 10, self.data.input_area.height + 10)
        dc.SetBrush(wx.Brush(self.data.input_bg_default_color, wx.SOLID))

        dc.DrawLine(50, 60, 190, 60)
        dc.DrawText(u'你好，DC！({}, {})'.format(size.width, size.height), 50, 65)
        parts = self.data.remark.split(u'\r')
        top = self.data.input_area.top + 5
        for part in parts:
            if part:
                dc.DrawText(part, self.data.input_area.left + 5, top)
                w, h = dc.GetTextExtent(part)
                # self.caret.MoveXY(100 + w, top)
                top += h
            else:
                w, h = dc.GetTextExtent('P')
                # self.caret.MoveXY(100, top)
                top += h

    def OnSize(self, event):
        self.Refresh()

    def OnClick(self, event):  # wx.MouseEvent
        pt = event.GetPosition()
        # print pt
        # self.caret.Hide()
        if self.data.input_area.left <= pt[0] <= self.data.input_area.right\
                and self.data.input_area.top <= pt[1] < self.data.input_area.bottom:
            self.input.SetValue(self.data.remark)
            self.data.input_bg_color = self.data.input_bg_edit_color
            self.input.Show()
            self.input.SetFocus()
            # TODO: 显示后，将文本框内的游标移动到指定的位置
        else:
            self.data.remark = self.input.GetValue()
            self.data.input_bg_color = self.data.input_bg_default_color
            self.input.Hide()
        self.Refresh()

    def OnKeyDown(self, event):
        print unichr(event.GetUnicodeKey()).encode('utf-8')

    def OnChar(self, event):
        uch = unichr(event.GetUnicodeKey())
        if uch == u'\b':
            if len(self.data.remark) > 0:
                self.data.remark = self.data.remark[:len(self.data.remark) - 1]
        else:
            self.data.remark += uch
        self.Refresh()

if __name__ == '__main__':
    app = wx.App()
    Example2(None, 'Line')
    app.MainLoop()
