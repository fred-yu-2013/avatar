__author__ = 'Fred'
#coding=utf-8

import wx
import json
import datetime
import copy

from sqlalchemy import func
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from lib.log import log

_engine = create_engine('sqlite:///storage.db', echo=False)
_Base = declarative_base()


class ContactModel(_Base):
    __tablename__ = 'contact'

    id = Column(Integer, primary_key=True)
    properties = Column(String)


class CompanyModel(_Base):
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True)
    properties = Column(String)


class ProjectModel(_Base):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True)
    properties = Column(String)

_Base.metadata.create_all(_engine)
Session = sessionmaker(bind=_engine)


class ModelManager():
    """
    用于管理所有的sqlalchemy库相关的对象。
    独立于具体的BaseModel对象。
    """

    def __init__(self):
        self.session = Session()

    def get_all(self, model_cls):
        return self.session.query(model_cls).order_by(model_cls.id).all()

    def add(self, model):
        self.session.add(model)
        self.session.commit()
        return model.id

    def update(self, id, model_cls, modify_callback):
        u"""
        :param id: 要修改的记录的id
        :param modify_callback: 回调函数用于修改数据库中的对象，modify_callback(model)
        """
        try:
            model = self.session.query(model_cls).filter_by(id=id).one()
            modify_callback(model)
            self.session.commit()
        except NoResultFound as e:
            log.e('Update non-existent model by id.')

    def delete(self, id, model_cls):
        model = self.session.query(model_cls).filter_by(id=id).one()
        self.session.delete(model)
        self.session.commit()


class Columns(list):
    """
    用于定义列表编辑对话框中的列名称表。
    self中的元素，表示列的名称，按顺序排列。
    """
    PROJECT = [u'工程名称', u'工程编号']
    # TODO: add u'性质'
    CONTACT = [u'姓名', u'手机', u'电话', u'传真', u'邮箱']
    # TODO: add u'性质'
    COMPANY = [u'名称', u'地址', u'邮编', u'电话', u'传真', u'法定代表人',
               u'委托代理人', u'开户银行', u'银行帐号', u'税号']
    DEVICE = [u'产品名称', u'规格型号', u'数量', u'单位', u'单价（元）', u'金额（元）', u'备注']


class Properties(dict):
    """ 属性集对象
    一个完成的数据体，包含了多个属性，这些属性被放置在字典中之后，就形成了属性集对象。
    比如：联系人有姓名、电话等属性，那么它可以描述为：{u'姓名': u'张三', u'电话': u'1234567890'}
    本类中，成员self.properties则代表了这样的一个属性集合。
    其它成员则是程序操作中需要用到的变量。

    属性名称规则：[属性名] = [名称],[区分符]
    [名称]用于显示在对话框的标签中，[区分符]只是为了防止名称重复的情况。
    [属性名]被用来当作数据的索引

    本对象也可以作为Model的一个属性存在，也可对应于数据库中的一条记录。
    关键看是否使用TYPE_*
    """

    TYPE_COMPANY = CompanyModel
    TYPE_CONTACT = ContactModel
    TYPE_PROJECT = ProjectModel

    UUID_COMPANY = 'company'
    UUID_CONTACT = 'contact'
    UUID_PROJECT = 'project'
    UUID_DEVICE  = 'device'

    INVALID_ID = -1

    def __init__(self, model=None):
        u"""

        :param model: 必须是数据库中取出来的model对象。
        """

        dict.__init__(self)
        self.id = Properties.INVALID_ID # 数据库中的id
        self.index = -1 # 在ListCtrl控件中的索引值。
        if model:
            self.id = model.id
            p = Properties.dict_to_properties(json.loads(model.properties))
            self.update(p)

    @staticmethod
    def dict_to_properties(d):
        """
        dict -> Properties
        """

        p = Properties()
        for key, value in d.items():
            if isinstance(d[key], dict):
                p[key] = Properties.dict_to_properties(d[key])
            elif isinstance(d[key], list):
                p[key] = [Properties.dict_to_properties(ld) for ld in d[key]]
            else:
                p[key] = value
        return p

    # def __nonzero__(self):  # bool(self)
    #     return bool(self.properties)

    def __getitem__(self, key):  # self[key]
        return self.get(key, '')

    # def __setitem__(self, key, value):  # self[key] = value
    #     self.properties[key] = value
    #
    # def __repr__(self):
    #     return repr(self.properties)

    # def __deepcopy__(self, memo):
    #     newone = type(self)()
    #     # newone.id = self.id
    #     newone.__dict__.update(self.__dict__)
    #     newone.update(copy.deepcopy(self))
    #     return newone

    def duplicate(self): # Duplicate a properties for dialog.
        p = Properties()
        p.update(copy.deepcopy(self))
        return p

    def __str__(self):
        if self[u'工程名称']: return self[u'工程名称'] # 工程
        elif self[u'姓名']: return self[u'姓名'] # 联系人
        elif self[u'名称']: return self[u'名称'] # 公司
        return ''

    @staticmethod
    def create_test_all(dict_list):
        rows = []
        for item in dict_list:
            p = Properties()
            p.update(item)
            rows.append(p)
        return rows

    @staticmethod
    def get_all(type): # Properties.TYPE_*
        model_cls = type
        mgr = ModelManager()
        models = mgr.get_all(model_cls)
        return [Properties(m) for m in models]

    def save(self, type): # Properties.TYPE_*
        model_cls = type
        mgr = ModelManager()
        if self.id == Properties.INVALID_ID:
            model = model_cls(properties=json.dumps(self))
            mgr.add(model)
            self.id = model.id
        else:
            def modify_callback(model):
                model.properties = json.dumps(self)
            mgr.update(self.id, model_cls, modify_callback)

    def delete(self, type):
        model_cls = type
        mgr = ModelManager()
        mgr.delete(self.id, model_cls)


class ToolTip(wx.ToolTip):
    def __init__(self, value):
        wx.ToolTip.__init__(self, self.get_tip_message(value))

    def get_tip_message(self, value):
        message = ''
        if isinstance(value, dict):
            columns = None
            if value['uuid'] == Properties.UUID_COMPANY:
                columns = Columns.COMPANY
            elif value['uuid'] == Properties.UUID_CONTACT:
                columns = Columns.CONTACT
            elif value['uuid'] == Properties.UUID_DEVICE:
                columns = Columns.DEVICE
            if columns:
                message += value[columns[0]] + '\n'
                message += '--------------------\n'
                for i in range(1, len(columns)):
                    message += columns[i] + ': ' + value[columns[i]] + '\n'
        elif isinstance(value, list):
            columns = None
            if value[0]['uuid'] == Properties.UUID_COMPANY:
                columns = Columns.COMPANY
            elif value[0]['uuid'] == Properties.UUID_CONTACT:
                columns = Columns.CONTACT
            elif value[0]['uuid'] == Properties.UUID_DEVICE:
                columns = Columns.DEVICE
            if columns:
                message += ', '.join(columns) + '\n'
                message += '--------------------\n'
                for p in value:
                    message += ', '.join([p[col] for col in columns]) + '\n'
        return message