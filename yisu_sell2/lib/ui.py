__author__ = 'Fred'
#coding=utf-8

import wx
import copy
from model import *
from log import log


class MenuMaker():
    """
    用于生成对话框中的菜单。
    """
    def __init__(self, parent):
        self.parent = parent

    def create_menu(self, items):
        """
        create_menu -> wx.Menu

        创建一组菜单（比如：文件），及菜单项
        :param items: 二维数组，每行中包含：id，名称，帮助信息，回调函数
        """
        menu = wx.Menu()
        for item in items:
            self._append_menu_item(menu, item[0], item[1], item[2], item[3])
        return menu

    def _append_menu_item(self, menu, id, name, helper_info, callback):
        if name == '-':
            menu.AppendSeparator()
        else:
            menu.Append(id, name, helper_info)
            if callback:
                self.parent.Bind(wx.EVT_MENU, callback, id=id)


class BaseListCtrl(wx.ListCtrl):
    """
    封装了wx.ListCtrl，设置了一些常用的属性。
    """
    def __init__(self, parent, size=(750, 500)):
        wx.ListCtrl.__init__(self, parent,
                             style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_HRULES | wx.LC_VRULES,
                             size=size)

    def _get_selected_indexes(self):
        indexes = []
        if self.GetSelectedItemCount() > 0:
            index = self.GetFirstSelected()
            while index != -1:
                indexes.append(index)
                index = self.GetNextSelected(index)
        return indexes


class PropertiesListCtrl(BaseListCtrl):
    """
    用于存放Properties对象数组的ListCtrl。
    """
    def __init__(self, parent, rows, columns, uuid, size=(750, 500), properties_type=None):
        BaseListCtrl.__init__(self, parent, size=size)
        self.properties_type = properties_type
        self.rows = rows
        self.selected_row = None

        for i in range(len(columns)):
            self.InsertColumn(i, columns[i])

        self.columns = columns

        index = 0
        for row in rows:
            self.save_row_item(index, row, is_add_to_rows=False)
            index += 1

        self.GetParent().Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_item_selected, self)
        self.GetParent().Bind(wx.EVT_LIST_ITEM_DESELECTED, self.on_item_deselected, self)

    def on_item_selected(self, event):
        self.selected_row = self._get_properties_by_index(event.m_itemIndex)

    def on_item_deselected(self, event):
        # self.selected_row = None
        pass

    def save_row_item(self, index, properties, is_add=True, is_add_to_rows=True):
        u"""
        添加或者更新列表项。
        """
        if is_add:
            self.InsertStringItem(index, properties[self.columns[0]])
        else:
            self.SetStringItem(index, 0, properties[self.columns[0]])
        if self.columns[0]: self.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        for i in range(1, len(self.columns)):
            value = properties[self.columns[i]]
            self.SetStringItem(index, i, value)
            if value: self.SetColumnWidth(i, wx.LIST_AUTOSIZE)
        properties.index = index
        if self.properties_type \
            and ((is_add and is_add_to_rows) or not is_add):
            properties.save(self.properties_type)
        if is_add and is_add_to_rows: self.rows.append(properties)
        self.Refresh()

    def _get_properties_by_index(self, index):
        for row in self.rows:
            if row.index == index:
                return row
        return None

    def delete_selected_row(self):
        indexes = self._get_selected_indexes()
        if len(indexes) == 1:
            row = self._get_properties_by_index(indexes[0])
            if self.properties_type: row.delete(self.properties_type)
            self.DeleteItem(indexes[0])
            self.rows.remove(row)
            for row in self.rows:
                if row.index > indexes[0]: row.index -= 1


class BaseDialog(wx.Dialog):
    """
    封装了wx.Dialog类，设置了常用的属性。
    """
    def __init__(self, parent, title):
        wx.Dialog.__init__(self, parent, title=title, size=(650, 570))
        self.properties = None
        self.ok_button = None

    def on_do_nothing(self, event):
        print 'on_do_nothing in BaseDialog.'

    def create_dialog_buttons(self, has_printer=True, is_save=True):
        sizer = wx.BoxSizer(wx.VERTICAL)

        line = wx.StaticLine(self, -1, size=(20, -1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, border=5, flag=wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT)
        sizer.AddSpacer(4)

        save = wx.Button(self, wx.ID_OK, u'保存' if is_save else u'确定')
        save.SetDefault()
        save.SetFocus()
        self.ok_button = save
        cancel = wx.Button(self, wx.ID_CANCEL, u'取消')
        button_sizer = wx.StdDialogButtonSizer()
        if has_printer:
            print_me = wx.Button(self, wx.ID_PRINT, u'打印')
            self.Bind(wx.EVT_BUTTON, self.on_print_me, print_me)
            button_sizer.Add(print_me, 0, wx.ALIGN_RIGHT)
        button_sizer.AddButton(save)
        button_sizer.AddButton(cancel)
        button_sizer.Realize()
        sizer.Add(button_sizer, flag=wx.EXPAND)
        return sizer

    def on_print_me(self, event):
        print 'on_print_me in BaseDialog.'


class PropertiesDialog(BaseDialog):
    """
    基于Properties对象的对话框。
    """
    def __init__(self, parent, title, properties):
        BaseDialog.__init__(self, parent, title)
        self.properties = properties

    def create_input(self, title, size=(125, -1)):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        label_title = title
        if ',' in title:
            label_title = title.split(',')[0]
        label_width = 50
        if len(label_title) > 4:
            label_width = len(label_title) * 13
        label = wx.StaticText(self, -1, label_title, style=wx.ALIGN_LEFT, size=(label_width, -1))
        text = wx.TextCtrl(self, -1, '', size=size)
        text.SetLabel(self.properties[title])
        text.SetHelpText(title)
        # TODO:
        if title == u'工程编号':
            text.Enable(False)
        self.Bind(wx.EVT_TEXT, self.on_text_changed, text)
        sizer.Add(label, proportion=0, flag=wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(text, proportion=1, flag=wx.ALIGN_CENTER_VERTICAL)
        return sizer

    def create_input_button(self, title, callback):
        """创建标签+按钮的组合
        标签表示数据的属性，按钮可以用来设置数据的属性，一般是弹一个新的对话框。
        """
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        label_title = title
        if ',' in title:
            label_title = title.split(',')[0]
        label_width = 50
        if len(label_title) > 4:
            label_width = len(label_title) * 13
        label = wx.StaticText(self, -1, label_title, style=wx.ALIGN_LEFT, size=(label_width, -1))
        button = wx.Button(self, -1, title, size=(125, -1))
        button.SetLabel(unicode(self.properties[title]))
        button.SetHelpText(title)
        button.SetToolTip(ToolTip(self.properties[title]))
        self.Bind(wx.EVT_BUTTON, callback, button)
        sizer.Add(label, proportion=0, flag=wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(button, proportion=1, flag=wx.ALIGN_CENTER_VERTICAL)
        return sizer

    def on_text_changed(self, event):
        text_ctrl = event.GetEventObject()
        name = text_ctrl.GetHelpText()
        self.properties[name] = text_ctrl.GetLabel()
        self.on_properties_changed()

    def create_button(self, title, size=(80, -1)):
        button = wx.Button(self, -1, title, size=size)
        button.SetHelpText(title)
        return button

    def on_properties_changed(self):
        # TODO:
        pass


class PropertiesListItemDialog(PropertiesDialog):
    """
    PropertiesListDialog中，用来添加、编辑Properties对象的对话框。
    """
    def __init__(self, parent, title, properties, columns):
        PropertiesDialog.__init__(self, parent, title, properties)

        base_sizer = wx.BoxSizer(wx.VERTICAL)

        base_sizer.AddSpacer(5)

        for col in columns:
            sizer = self.create_input(col, size=(180, -1))
            base_sizer.Add(sizer, border=5, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM)
        self.columns = columns

        sizer = self.create_dialog_buttons(has_printer=False, is_save=False)
        base_sizer.Add(sizer, border=5, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM)

        self._update_dialog_buttons()

        self.SetSizerAndFit(base_sizer)
        self.CenterOnParent()

    def _update_dialog_buttons(self):
        self.ok_button.Enable(bool(self.properties[self.columns[0]]))

    # override
    def on_properties_changed(self):
        self._update_dialog_buttons()


class PropertiesListDialog(BaseDialog):
    """
    用来管理Properties对象数组的对话框。
    """
    def __init__(self, parent, title, rows, columns, uuid, properties_type=None, is_select=True):
        BaseDialog.__init__(self, parent, title)
        self.uuid = uuid
        self.is_select = is_select # 是否选择一行
        base_sizer = wx.BoxSizer(wx.VERTICAL)

        # 设置主界面的控件。
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        add = wx.Button(self, -1, u'添加', size=(80, -1))
        self.Bind(wx.EVT_BUTTON, self.on_new_properties, add)
        edit = wx.Button(self, -1, u'编辑', size=(80, -1))
        self.Bind(wx.EVT_BUTTON, self.on_edit_properties, edit)
        delete = wx.Button(self, -1, u'删除', size=(80, -1))
        self.Bind(wx.EVT_BUTTON, self.on_delete_properties, delete)
        sizer.Add(add, flag=wx.EXPAND)
        sizer.AddSpacer(2)
        sizer.Add(edit, flag=wx.EXPAND)
        sizer.AddSpacer(2)
        sizer.Add(delete, flag=wx.EXPAND)
        base_sizer.Add(sizer, border=5, flag=wx.EXPAND | wx.LEFT | wx.TOP | wx.RIGHT)
        self.edit_button = edit
        self.delete_button = delete

        self.list = PropertiesListCtrl(self, rows, columns, uuid, size=(540, 360),
                                       properties_type=properties_type)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_list_item_selected, self.list)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.on_list_item_deselected, self.list)
        base_sizer.Add(self.list, border=5, flag=wx.EXPAND | wx.ALL)

        self._update_edit_buttons()

        sizer = self.create_dialog_buttons(has_printer=False, is_save=False)
        base_sizer.Add(sizer, border=5, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM)

        self._update_dialog_buttons()

        self.SetSizerAndFit(base_sizer)
        self.CenterOnParent()

    def _update_edit_buttons(self):
        """
        更新三个编辑按钮的状态
        """
        indexes = self.list._get_selected_indexes()
        self.edit_button.Enable(len(indexes) == 1)
        self.delete_button.Enable(len(indexes) == 1)

    def _update_dialog_buttons(self):
        self.ok_button.Enable(bool(self.is_select and len(self.list._get_selected_indexes()) == 1 \
            or not self.is_select))

    def on_list_item_selected(self, event):
        self._update_edit_buttons()
        self._update_dialog_buttons()
        event.Skip()

    def on_list_item_deselected(self, event):
        self._update_edit_buttons()
        self._update_dialog_buttons()
        event.Skip()

    def on_new_properties(self, event):
        properties = Properties()
        properties['uuid'] = self.uuid
        dlg = PropertiesListItemDialog(self, u'添加', properties, self.list.columns)
        if dlg.ShowModal() == wx.ID_OK:
            self.list.save_row_item(self.list.GetItemCount(), properties)
        dlg.Destroy()

    def on_edit_properties(self, event):
        indexes = self.list._get_selected_indexes()
        if len(indexes) == 1:
            properties = self.list._get_properties_by_index(indexes[0])
            dlg = PropertiesListItemDialog(self, u'编辑', properties.duplicate(), self.list.columns)
            if dlg.ShowModal() == wx.ID_OK:
                properties.update(dlg.properties)
                self.list.save_row_item(indexes[0], properties, is_add=False)
            dlg.Destroy()

    def on_delete_properties(self, event):
        self.list.delete_selected_row()

    def get_selected_properties(self):
        return self.list.selected_row
    selected_properties = property(get_selected_properties)

    def get_rows(self):
        return self.list.rows
    rows = property(get_rows)


class BaseFrame(wx.Frame):
    """
    封装了wx.Frame类，方便创建主Frame
    """
    main_frame = None

    def __init__(self, title):
        wx.Frame.__init__(self, None, title=title, size=(800, 600))
        self.on_init_menu()
        self.on_init_workspace()
        self.Centre()

    def on_init_menu(self):
        pass

    def on_init_workspace(self):
        pass

    def on_do_nothing(self, event):
        print 'on_do_nothing in BaseFrame.'


class Printer():
    """
    封装了所有打印机相关的操作，配置数据等。
    """

    def __init__(self, main_frame):
        self.main_frame = main_frame
        self.pdata = wx.PrintData()
        self.pdata.SetPaperId(wx.PAPER_A4)
        self.pdata.SetOrientation(wx.PORTRAIT)
        self.pdata.SetBin(wx.PRINTBIN_DEFAULT)
        self.margins = (wx.Point(25, 25), wx.Point(25, 25))
        self.cur_preview = None

    def preview(self, printout, printout_for_print=None, title=u'打印预览'):
        dlg_data = wx.PrintDialogData(self.pdata)
        preview = wx.PrintPreview(printout, printout_for_print, dlg_data)
        preview.SetZoom(75)
        if not preview.Ok():
            wx.MessageBox(u'无法创建预览窗口', u'出错')
            return
        self.cur_preview = preview
        frame = wx.PreviewFrame(preview, self.main_frame, title,
                                pos=self.main_frame.GetPosition(),
                                size=self.main_frame.GetSize())
        frame.Initialize()
        frame.Show()


class BasePrintout(wx.Printout):
    """
    wx.Printout的封装，仅包含一个页面
    """

    def __init__(self, printer):
        wx.Printout.__init__(self, 'BasePrintout')
        self.printer = printer

    def HasPage(self, page):
        return page <= 1

    def GetPageInfo(self):
        return 1, 1, 1, 1


class PropertiesPrintout(BasePrintout):
    """
    用于绘制Properties对象的Printout。
    """

    DEFAULT_FONT_SIZE = 3

    def __init__(self, printer, properties):
        BasePrintout.__init__(self, printer)
        self.properties = properties
        self.is_preview = True  # 是否在预览模式下，非预览模式下，传输更多的像素

class PrintPageHelper():
    """ Printout.OnPrintPage()函数中的辅助类
    默认的绘图尺寸都为毫米，采用绝对坐标定位
    规则二：
    绘图时，首先将映射模式设为：10个dc像素代表printer的1mm。
    预览时，根据缩放比例来调整user scale # screen -> dc
    长度转换为dc像素的规则：1mm = 10pixel
    绘图时，绘图在dc上，通过user scale，映射到screen上。
    """

    DEFAULT_FONT_SIZE = 3

    def __init__(self, printer, printout, dc):
        self.printer = printer
        self.printout = printout
        self.dc = dc
        # 仅适用于规则二
        self.dc.SetMapMode(wx.MM_LOMETRIC)
        # self.dump()
        self._init_user_scale()
        self._init_margins()

        self.set_font()
        self.dc.SetPen(wx.Pen("black", 2))
        self.dc.SetBrush(wx.TRANSPARENT_BRUSH)

    def _init_user_scale(self):
        """ 规则一：此计算基于screen映射到page上。
        根据screen和page的尺寸和大小来计算user scale，此时需要修改self.mm2s()，不修改dc的映射模式。
        """

        # 原始的sp_scale计算规则，屏幕映射到设备纸大小上。
        # sppi = self.dc.GetPPI().x
        # ssize = self.dc.GetSize().x
        # pppi, _ = self.printout.GetPPIPrinter()
        # psize, _ = self.printout.GetPageSizePixels()
        # sp_scale = (float(ssize) * float(pppi)) / (float(psize) * float(sppi))
        # self.dc.SetUserScale(sp_scale, sp_scale)

        sp_scale = 1
        if self.printout.is_preview:
            # 预览的情况下，需要按照缩放的比例来调整user scale.
            sppi = self.dc.GetPPI().x
            sw, _ = self.dc.GetSize()
            sw_mm, _ = self.dc.GetSizeMM()
            preview_ppi = (float(sw) / float(sw_mm)) * 25.4
            zoom = float(self.printer.cur_preview.GetZoom()) / 100.0
            sp_scale = zoom * float(sppi) / preview_ppi
        self.dc.SetUserScale(sp_scale, sp_scale)

    def _init_margins(self):
        """
        设置绘图的区域，区域之外，无法绘图。
        """
        xpppi, ypppi = self.printout.GetPPIPrinter()
        page_r = self.printout.GetPaperRectPixels()
        pw, ph = self.printout.GetPageSizePixels()
        margin_l, margin_t = self.printer.margins[0] # mm
        margin_r, margin_b = self.printer.margins[1] # mm
        orig_dl = int(float(0 - page_r.left) / float(xpppi) * 25.4)
        orig_dt = int(float(0 - page_r.top) / float(xpppi) * 25.4)
        orig_dr = int(float(pw - page_r.right) / float(xpppi) * 25.4)
        orig_db = int(float(ph - page_r.bottom) / float(xpppi) * 25.4)
        pt1 = wx.Point(margin_l - orig_dl, margin_t - orig_dt)
        pt2 = wx.Point(210 - (margin_r - orig_dr), 297 - (margin_b - orig_db))
        self.margins_r_mm = wx.RectPP(pt1, pt2)
        log.d('Margins mm rect: %s' % repr(self.margins_r_mm))
        self.margins_r = wx.RectPP(wx.Point(self.mm2s(pt1.x), self.mm2s(pt1.y)),
                                   wx.Point(self.mm2s(pt2.x), self.mm2s(pt2.y)))
        log.d('Margins rect: %s' % repr(self.margins_r))
        self.dc.SetClippingRect(self.margins_r)

    def mm2s(self, mm):
        # 规则一：
        # sppi = self.dc.GetPPI().x
        # return int(float(mm) * float(sppi) / 25.4)

        # 根据长度来计算需要多少个dc像素。
        return 10 * mm

    def set_font(self, size=-1, bold=False):
        if size == -1:
            size = PrintPageHelper.DEFAULT_FONT_SIZE
        font = wx.Font(self.mm2s(size), wx.FONTFAMILY_SWISS, wx.NORMAL, wx.NORMAL, False, u'宋体')
        self.dc.SetFont(font)

    def set_line_width(self, width):
        pass

    def draw_line(self, x1, y1, x2, y2):
        x1_p = self.mm2s(x1)
        y1_p = self.mm2s(y1)
        x2_p = self.mm2s(x2)
        y2_p = self.mm2s(y2)
        self.dc.DrawLine(x1_p, y1_p, x2_p, y2_p)

    def draw_rect(self, r, flag=wx.ALL):
        ''' 绘制矩形
        :param r: wx.Rect
        :param flag: wx.LEFT, wx.TOP, wx.RIGHT, wx.BOTTOM, wx.ALL
        '''
        if flag == wx.ALL:
            r_p = wx.Rect(self.mm2s(r.left), self.mm2s(r.top), self.mm2s(r.width), self.mm2s(r.height))
            self.dc.DrawRectangleRect(r_p)
        else:
            if flag & wx.LEFT:
                self.draw_line(r.left, r.top, r.left, r.bottom + 1)
            if flag & wx.TOP:
                self.draw_line(r.left, r.top, r.right + 1, r.top)
            if flag & wx.RIGHT:
                self.draw_line(r.right + 1, r.top, r.right + 1, r.bottom + 1)
            if flag & wx.BOTTOM:
                self.draw_line(r.left, r.bottom + 1, r.right + 1, r.bottom + 1)

    def draw_text(self, text, r, flag=wx.CENTER):
        ''' 在矩形框内绘制一个文本，按当前字体的设置
        :param r: wx.Rect
        :param flag: wx.LEFT, wx.CENTER, wx.RIGHT
        '''
        # TODO: flag
        if text:
            r_p = wx.Rect(self.mm2s(r.left), self.mm2s(r.top),
                          self.mm2s(r.width), self.mm2s(r.height))
            tw, th, desc, x = self.dc.GetFullTextExtent(text)
            left = r_p.left + (r_p.width - tw) / 2
            if tw > r_p.width:
                left = r_p.left
            top = r_p.top + (r_p.height - th) / 2
            if th > r_p.height:
                top = r_p.top
            self.dc.DrawText(text, left, top)

    def draw_table(self, left, top, width, col_ratios, row_heights, contents, flag=wx.ALL):
        """
        绘制表格宽度按比例，高度按毫米记
        :param left: 表格左边界
        :param width: 表格的宽度
        :col_ratios: 列的比例, 一维数组
        :row_heights: 每行的行高
        :param contents: 二维数组，每个元素代表一个Cell：text（内容），align(对齐, 默认居中
        :param flag: wx.LEFT, wx.TOP, wx.RIGHT, wx.BOTTOM, wx.ALL, 表格的边界是否画
        """
        # 画边框
        height = sum(row_heights)
        rect = wx.Rect(left, top, width, height)
        self.draw_rect(rect, flag)
        # 画其它部分
        all_ratios = sum(col_ratios)
        is_draw_col_lines = False
        tmp_x, tmp_y = left, top
        i, j = 0, 0
        for rh in row_heights:
            tmp_x = left
            j = 0
            for c in col_ratios:
                cw = width * c / all_ratios
                # 画竖线
                if not is_draw_col_lines and j > 0:
                    self.draw_line(tmp_x, top, tmp_x, top + height)
                    # 画文本
                rect = wx.Rect(tmp_x, tmp_y, cw, rh)
                self.draw_text(contents[i][j]['text'], rect)
                tmp_x += cw
                j += 1
                # 画横线
            if i > 0:
                self.draw_line(left, tmp_y, left + width, tmp_y)
            if not is_draw_col_lines:  is_draw_col_lines = True
            tmp_y += rh
            i += 1

    def dump(self):
        print 'dc.GetMapMode(), %d, wx.MM_METRIC, %d, wx.MM_TEXT, %d' % (self.dc.GetMapMode(), wx.MM_METRIC, wx.MM_TEXT)
        print 'dc.GetLogicalOrigin(), %s' % repr(self.dc.GetLogicalOrigin())
        print 'dc.GetPPI(), %s' % repr(self.dc.GetPPI())
        print 'dc.GetSize(), %s' % repr(self.dc.GetSize())
        print 'dc.GetSizeMM(), %s' % repr(self.dc.GetSizeMM())
        print 'dc.GetUserScale(), %s' % repr(self.dc.GetUserScale())
        # print 'self.GetLogicalPageRect(), %s' % repr(self.GetLogicalPageRect())
        print 'dc.GetLogicalOrigin(), %s' % repr(self.dc.GetLogicalOrigin())
        print 'dc.GetLogicalScale(), %s' % repr(self.dc.GetLogicalScale())
        # print 'self.GetLogicalPageMarginsRect(), %s' % repr(self.GetLogicalPageMarginsRect(self.data))
        print 'self.GetLogicalPageRect(), %s' % repr(self.printout.GetLogicalPageRect())
        print 'self.GetLogicalPaperRect(), %s' % repr(self.printout.GetLogicalPaperRect())
        print 'self.GetPPIPrinter(), %s' % repr(self.printout.GetPPIPrinter())
        print 'self.GetPPIScreen(), %s' % repr(self.printout.GetPPIScreen())
        print 'self.GetPageInfo(), %s' % repr(self.printout.GetPageInfo())
        print 'self.GetPageSizeMM(), %s' % repr(self.printout.GetPageSizeMM())
        print 'self.GetPageSizePixels(), %s' % repr(self.printout.GetPageSizePixels())
        print 'self.GetPaperRectPixels(), %s' % repr(self.printout.GetPaperRectPixels())
        print 'self.GetTitle(), %s' % repr(self.printout.GetTitle())