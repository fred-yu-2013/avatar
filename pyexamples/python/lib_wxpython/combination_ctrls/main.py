# -*- coding: utf-8 -*-

import wx
import wx.lib.newevent

# class and event type for Bind()
SomeNewEvent, EVT_SOME_NEW_EVENT = wx.lib.newevent.NewCommandEvent()


class MyInput(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)

        base_sizer = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "This is an example of static text", (20, 20))
        base_sizer.Add(label)
        text = wx.TextCtrl(self, -1, "Test it out and see", size=(125, -1))
        self.Bind(wx.EVT_TEXT, self.on_text_changed, text)
        base_sizer.Add(text)

        self.SetAutoLayout(True)
        self.SetSizerAndFit(base_sizer)

    def on_text_changed(self, event):
        print '[MyInput] on_text_changed'
        self.__send_event()

    def __send_event(self):
        event = SomeNewEvent(self.GetId(), arg1=5)
        # 下面两种方式都可以。
        self.GetEventHandler().ProcessEvent(event)
        # wx.PostEvent(self, event)

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title=u'测试组合控件', size=(800, 600))
        self.panel = wx.Panel(self)
        base_sizer = wx.BoxSizer(wx.VERTICAL)

        for i in range(5):
            my_input = MyInput(self.panel)
            base_sizer.Add(my_input, border=5, flag=wx.EXPAND | wx.ALL)
            self.Bind(EVT_SOME_NEW_EVENT, self.on_some_new_event, my_input)

        self.panel.SetAutoLayout(True)
        self.panel.SetSizerAndFit(base_sizer)
        self.Fit()

    def on_some_new_event(self, event):
        print '[MainFrame] on_some_new_event %s' % repr(event)
        print event.arg1

if __name__ == '__main__':
    app = wx.App(redirect=False)
    win = MainFrame()
    win.Show()
    app.MainLoop()