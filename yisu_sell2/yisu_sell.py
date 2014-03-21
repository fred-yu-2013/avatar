__author__ = 'Fred'
#coding=utf-8

from model import *
from lib.ui import *
from lib.log import *


class ProjectPrintout(PropertiesPrintout):
    def __init__(self, printer, properties, bill_name):
        PropertiesPrintout.__init__(self, printer, properties)
        self.bill_name = bill_name # 绘制的表格名称，同按钮名称

    def OnPrintPage(self, page):
        dc = self.GetDC()
        helper = PrintPageHelper(self.printer, self, dc)

        if self.bill_name == u'报价单':
            self._draw_quotation_bill(dc, helper)
        else:
            # TODO:
            helper.set_font(6)
            helper.draw_text(u'# TODO: %s' % self.bill_name, wx.Rect(25, 25, 10, 10))

    def _draw_quotation_bill(self, dc, helper):
        gap = 2
        max_width = helper.margins_r_mm.width - 2 * gap

        # # 绘制一个固定大小的矩形
        # r = wx.Rect(100, 100, 100, 100)
        # dc.DrawRectangleRect(r)

        helper.set_font(6)
        r = wx.Rect(helper.margins_r_mm.left + gap, 34, max_width, 10)
        helper.draw_text(u'报价单', r)

        helper.set_font()
        contents = (({'text': u'询价单位'},
                     {'text': self.properties.get(u'询价单位', '')},
                     {'text': u'报价人'},
                     {'text': self.properties.get(u'报价人', '')}),
                    ({'text': u'联系人'},
                     {'text': self.properties.get(u'联系人')},
                     {'text': u'电话'},
                     {'text': self.properties.get(u'电话,B')}),
                    ({'text': u'电话'},
                     {'text': self.properties.get(u'电话')},
                     {'text': u'传真'},
                     {'text': self.properties.get(u'传真')}),
                    ({'text': u'邮箱'},
                     {'text': self.properties.get(u'邮箱')},
                     {'text': u'报价编号'},
                     {'text': self.properties.get(u'报价编号')}),
                    ({'text': u'项目名称'},
                     {'text': self.properties.get(u'项目名称')},
                     {'text': u'报价日期'},
                     {'text': self.properties.get(u'报价日期')}),)
        helper.draw_table(left=helper.margins_r_mm.left + gap,
                          top=50,
                          width=max_width,
                          col_ratios=[1.0, 2.5, 1.0, 2.5],
                          row_heights=[10, 10, 10, 10, 10],
                          contents=contents)

        # TODO: 按照个数绘制不同行数的表格。
        contents = (({'text': u'产品名称'},
                     {'text': u'规格型号'},
                     {'text': u'单位'},
                     {'text': u'数量'},
                     {'text': u'单价'},
                     {'text': u'金额'},
                     {'text': u'备注'}),
                    ({'text': u''},
                     {'text': u''},
                     {'text': u''},
                     {'text': u''},
                     {'text': u''},
                     {'text': u''},
                     {'text': u''}),
                    ({'text': u''},
                     {'text': u''},
                     {'text': u''},
                     {'text': u''},
                     {'text': u''},
                     {'text': u''},
                     {'text': u''}))
        helper.draw_table(left=helper.margins_r_mm.left + gap,
                          top=103,
                          width=max_width,
                          col_ratios=[3.0, 3.0, 1.0, 1.0, 2.0, 2.0, 3.0],
                          row_heights=[10, 10],
                          contents=contents)

        contents = (({'text': u'合计'},
                     {'text': u''},
                     {'text': u''},),)
        helper.draw_table(left=helper.margins_r_mm.left + gap,
                          top=123,
                          width=max_width,
                          col_ratios=[3.0, 7.0, 5.0],
                          row_heights=[10,],
                          contents=contents,
                          flag=wx.LEFT | wx.RIGHT | wx.BOTTOM)

        r = wx.Rect(helper.margins_r_mm.left + gap, 133,
                    max_width, helper.margins_r_mm.bottom - gap - 133)
        # print repr(r)
        helper.draw_rect(r, flag=wx.wx.LEFT | wx.RIGHT | wx.BOTTOM)


class ProjectDialog(PropertiesDialog):
    """
    添加或编辑工程的对话框。
    """
    def __init__(self, parent, title, project):
        PropertiesDialog.__init__(self, parent, title, project)

        if not self.properties[u'工程编号']:
            self.properties[u'工程编号'] = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

        base_sizer = wx.BoxSizer(wx.VERTICAL)

        # 设置主界面的控件。
        group = wx.StaticBoxSizer(wx.StaticBox(self, -1, u'工程信息'), wx.VERTICAL)
        input = self.create_input(u'工程名称', size=(150, -1))
        group.Add(input, flag=wx.EXPAND)
        group.AddSpacer(2)
        input = self.create_input(u'工程编号', size=(150, -1))
        group.Add(input, flag=wx.EXPAND)
        group.AddSpacer(2)
        input = self.create_input_button(u'项目负责人', self.on_select_contact)
        group.Add(input, flag=wx.EXPAND)
        group.AddSpacer(2)
        input = self.create_input_button(u'收货人', self.on_select_contact)
        group.Add(input, flag=wx.EXPAND)
        group.AddSpacer(2)
        input = self.create_input_button(u'送货人', self.on_select_contact)
        group.Add(input, flag=wx.EXPAND)
        group.AddSpacer(2)
        base_sizer.Add(group, border=5, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM)

        group = wx.StaticBoxSizer(wx.StaticBox(self, -1, u'客户信息'), wx.VERTICAL)
        input = self.create_input_button(u'公司名称', self.on_select_company)
        group.Add(input, flag=wx.EXPAND)
        group.AddSpacer(2)
        input = self.create_input_button(u'联系人', self.on_select_contact)
        group.Add(input, flag=wx.EXPAND)
        group.AddSpacer(2)
        input = self.create_input_button(u'收货人,B', self.on_select_contact)
        group.Add(input, flag=wx.EXPAND)
        group.AddSpacer(2)
        base_sizer.Add(group, border=5, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM)

        group = wx.StaticBoxSizer(wx.StaticBox(self, -1, u'供货商信息'), wx.VERTICAL)
        input = self.create_input_button(u'公司名称,C', self.on_select_company)
        group.Add(input, flag=wx.EXPAND)
        group.AddSpacer(2)
        input = self.create_input_button(u'联系人,C', self.on_select_contact)
        group.Add(input, flag=wx.EXPAND)
        group.AddSpacer(2)
        input = self.create_input_button(u'送货人,C', self.on_select_contact)
        group.Add(input, flag=wx.EXPAND)
        group.AddSpacer(2)
        base_sizer.Add(group, border=5, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM)

        group = wx.StaticBoxSizer(wx.StaticBox(self, -1, u'产品流'), wx.HORIZONTAL)
        button = self.create_button(u'报价')
        button.SetToolTip(ToolTip(self.properties[u'报价']))
        self.Bind(wx.EVT_BUTTON, self.on_device_manager, button)
        group.Add(button)
        self.quotation_button = button
        group.AddSpacer(2)
        button = self.create_button(u'供方')
        button.SetToolTip(ToolTip(self.properties[u'供方']))
        self.Bind(wx.EVT_BUTTON, self.on_device_manager, button)
        group.Add(button)
        self.supplier_button = button
        group.AddSpacer(2)
        button = self.create_button(u'需方')
        button.SetToolTip(ToolTip(self.properties[u'需方']))
        self.Bind(wx.EVT_BUTTON, self.on_device_manager, button)
        group.Add(button)
        self.buyer_button = button
        group.AddSpacer(2)
        button = self.create_button(u'入库')
        button.SetToolTip(ToolTip(self.properties[u'入库']))
        self.Bind(wx.EVT_BUTTON, self.on_device_manager, button)
        group.Add(button)
        self.stock_in_button = button
        group.AddSpacer(2)
        button = self.create_button(u'出库')
        button.SetToolTip(ToolTip(self.properties[u'出库']))
        self.Bind(wx.EVT_BUTTON, self.on_device_manager, button)
        group.Add(button)
        self.stock_out_button = button
        group.AddSpacer(2)
        base_sizer.Add(group, border=5, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM)

        self._update_product_list_buttons()

        group = wx.StaticBoxSizer(wx.StaticBox(self, -1, u'表单生成'), wx.HORIZONTAL)
        button = self.create_button(u'报价单')
        self.Bind(wx.EVT_BUTTON, self.on_bill_generate, button)
        group.Add(button)
        group.AddSpacer(2)
        button = self.create_button(u'供方合同')
        self.Bind(wx.EVT_BUTTON, self.on_bill_generate, button)
        group.Add(button)
        group.AddSpacer(2)
        button = self.create_button(u'需方合同')
        self.Bind(wx.EVT_BUTTON, self.on_bill_generate, button)
        group.Add(button)
        group.AddSpacer(2)
        button = self.create_button(u'入库单')
        self.Bind(wx.EVT_BUTTON, self.on_bill_generate, button)
        group.Add(button)
        group.AddSpacer(2)
        button = self.create_button(u'出库单')
        self.Bind(wx.EVT_BUTTON, self.on_bill_generate, button)
        group.Add(button)
        group.AddSpacer(2)
        button = self.create_button(u'结算单')
        self.Bind(wx.EVT_BUTTON, self.on_bill_generate, button)
        group.Add(button)
        group.AddSpacer(2)
        base_sizer.Add(group, border=5, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM)

        sizer = self.create_dialog_buttons(has_printer=False)
        base_sizer.Add(sizer, border=5, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM)

        self._update_dialog_buttons()

        self.SetSizerAndFit(base_sizer)
        self.CenterOnParent()

    def _update_product_list_buttons(self):
        self.supplier_button.Enable(bool(self.properties[u'报价']))
        self.buyer_button.Enable(self.supplier_button.IsEnabled() and bool(self.properties[u'供方']))
        self.stock_in_button.Enable(self.buyer_button.IsEnabled() and bool(self.properties[u'需方']))
        self.stock_out_button.Enable(self.stock_in_button.IsEnabled() and bool(self.properties[u'入库']))

    def _update_dialog_buttons(self):
        self.ok_button.Enable(bool(self.properties[u'工程名称'] and self.properties[u'工程编号']))

    # override
    def on_properties_changed(self):
        self._update_dialog_buttons()

    def on_select_contact(self, event):
        rows = Properties.get_all(Properties.TYPE_CONTACT)
        dlg = PropertiesListDialog(self, u'选择联系人', rows, Columns.CONTACT, Properties.UUID_CONTACT,
                                   properties_type=Properties.TYPE_CONTACT)
        if dlg.ShowModal() == wx.ID_OK \
            and dlg.selected_properties:
            button = event.GetEventObject()
            name = button.GetHelpText()
            if not self.properties[name]:
                self.properties[name] = Properties()
                self.properties[name]['uuid'] = Properties.UUID_CONTACT
            self.properties[name].update(copy.deepcopy(dlg.selected_properties))
            button.SetLabel(dlg.selected_properties[u'姓名'])
            button.SetToolTip(ToolTip(self.properties[name]))
        dlg.Destroy()

    def on_select_company(self, event):
        rows = Properties.get_all(Properties.TYPE_COMPANY)
        dlg = PropertiesListDialog(self, u'选择公司', rows, Columns.COMPANY, Properties.UUID_COMPANY,
                                   properties_type=Properties.TYPE_COMPANY)
        if dlg.ShowModal() == wx.ID_OK \
            and dlg.selected_properties:
            button = event.GetEventObject()
            name = button.GetHelpText()
            if not self.properties[name]:
                self.properties[name] = Properties()
                self.properties[name]['uuid'] = Properties.UUID_COMPANY
            self.properties[name].update(copy.deepcopy(dlg.selected_properties))
            button.SetLabel(dlg.selected_properties[u'名称'])
            button.SetToolTip(ToolTip(self.properties[name]))
        dlg.Destroy()

    def on_device_manager(self, event): # 报价、供方、需方、入库、出库按钮
        button = event.GetEventObject()
        key = button.GetHelpText()

        rows = self.properties[key]
        if not rows: rows = []
        dlg = PropertiesListDialog(self, u'编辑%s的产品列表' % key, rows, Columns.DEVICE,
                                   Properties.UUID_DEVICE, is_select=False)
        if dlg.ShowModal() == wx.ID_OK and dlg.rows:
            self.properties[key] = dlg.rows
            self._update_product_list_buttons()
            button.SetToolTip(ToolTip(self.properties[key]))
        dlg.Destroy()

    def on_bill_generate(self, event):
        button = event.GetEventObject()
        key = button.GetHelpText()

        printer = Printer(BaseFrame.main_frame)
        printout = ProjectPrintout(printer, self.properties, key)
        printout_for_print = ProjectPrintout(printer, self.properties, key)
        printout_for_print.is_preview = False
        printer.preview(printout, printout_for_print, u'预览%s' % key)


class MainFrame(BaseFrame):
    def __init__(self):
        BaseFrame.__init__(self, u'依苏供销货管理系统')
        BaseFrame.main_frame = self

    def on_init_menu(self):
        maker = MenuMaker(self)
        menu_bar = wx.MenuBar()

        items = [
            (wx.NewId(), u'导入...(&I)', u'从文件导入数据', self.on_do_nothing),
            (wx.NewId(), u'导出...(&O)', '', self.on_do_nothing),
            # (wx.NewId(), '-', '', None),
            # (wx.NewId(), u'退出(&Q)', '', None),
            ]
        menu_bar.Append(maker.create_menu(items), u'文件(&F)')

        items = [
            (wx.NewId(), u'新建', '', self.on_menu_project_new),
            (wx.NewId(), u'编辑', '', self.on_menu_project_edit),
            (wx.NewId(), u'删除', '', self.on_menu_project_delete),
            ]
        self.menu_project = maker.create_menu(items)
        menu_bar.Append(self.menu_project, u'工程')

        items = [
            (wx.NewId(), u'公司', '', self.on_menu_info_company),
            (wx.NewId(), u'联系人', '', self.on_menu_info_contact),
            # (wx.NewId(), u'设备', '', None),
        ]
        menu_bar.Append(maker.create_menu(items), u'信息管理')

        self.SetMenuBar(menu_bar)

    def on_init_workspace(self):
        self.panel = wx.Panel(self)
        base_sizer = wx.BoxSizer(wx.VERTICAL)

        rows = Properties.get_all(Properties.TYPE_PROJECT)
        self.list = PropertiesListCtrl(self.panel, rows, Columns.PROJECT, Properties.UUID_PROJECT,
                                       properties_type=Properties.TYPE_PROJECT)
        self.panel.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_list_item_selected, self.list)
        self.panel.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.on_list_item_deselected, self.list)
        base_sizer.Add(self.list, proportion=1, border=5, flag=wx.EXPAND | wx.ALL)

        self._update_menu_project()

        self.panel.SetAutoLayout(True)
        self.panel.SetSizerAndFit(base_sizer)
        self.Fit()

    def _update_menu_project(self):
        indexes = self.list._get_selected_indexes()
        edit_item = self.menu_project.FindItemByPosition(1)
        edit_item.Enable(len(indexes) == 1)
        delete_item = self.menu_project.FindItemByPosition(2)
        delete_item.Enable(len(indexes) == 1)

    def on_menu_project_new(self, event):
        properties = Properties()
        properties['uuid'] = Properties.UUID_PROJECT
        dlg = ProjectDialog(self, u'添加工程', properties)
        if dlg.ShowModal() == wx.ID_OK:
            self.list.save_row_item(self.list.GetItemCount(), properties)
        dlg.Destroy()

    def on_menu_project_edit(self, event):
        indexes = self.list._get_selected_indexes()
        if len(indexes) == 1:
            properties = self.list._get_properties_by_index(indexes[0])
            dlg = ProjectDialog(self, u'编辑工程', properties.duplicate())
            if dlg.ShowModal() == wx.ID_OK:
                properties.update(dlg.properties)
                self.list.save_row_item(indexes[0], properties, is_add=False)
            dlg.Destroy()

    def on_menu_project_delete(self, event):
        self.list.delete_selected_row()

    def on_menu_info_company(self, event):
        rows = Properties.get_all(Properties.TYPE_COMPANY)
        dlg = PropertiesListDialog(self, u'公司', rows, Columns.COMPANY, Properties.UUID_COMPANY,
                                   properties_type=Properties.TYPE_COMPANY)
        dlg.ShowModal()
        dlg.Destroy()

    def on_menu_info_contact(self, event):
        rows = Properties.get_all(Properties.TYPE_CONTACT)
        dlg = PropertiesListDialog(self, u'联系人', rows, Columns.CONTACT, Properties.UUID_CONTACT,
                                   properties_type=Properties.TYPE_CONTACT)
        dlg.ShowModal()
        dlg.Destroy()

    def on_list_item_selected(self, event):
        # print 'on_list_item_selected in MainFrame'
        self._update_menu_project()
        event.Skip()

    def on_list_item_deselected(self, event):
        # print 'on_list_item_deselected in MainFrame'
        self._update_menu_project()
        event.Skip()

# if __name__ == '__main__':

log.d('Start Yi Su Sell Manager System')

# 打开控件帮助系统，有助于将TextCtrl控件和属性关联。
provider = wx.SimpleHelpProvider()
wx.HelpProvider_Set(provider)

app = wx.App(redirect=False)  # Show debug info in console.

# 添加内置对话框的中文支持
loc = wx.Locale()
loc.Init(wx.LANGUAGE_CHINESE_SIMPLIFIED)

win = MainFrame()
win.Show()
app.MainLoop()