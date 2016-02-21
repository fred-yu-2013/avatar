#encoding=utf-8

u""" 次例子为
初始化分三步：
1.创建engine和数据库对象的基类
2.定义实际的数据库对象，比如：Student，可以定义多个。
3.在数据库中创建表结构，并创建Session类，此类的对象用于在数据库中操作数据
"""

import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Integer, ForeignKey, func
from sqlalchemy.orm import aliased, relationship, backref
from sqlalchemy.orm.exc import NoResultFound

# engine = create_engine('sqlite:///storage.db', echo=False)
engine = create_engine('sqlite:///:memory:', echo=True)
Session = sessionmaker(bind=engine)

# Table defines.

Base = declarative_base()  # Model's base class.


class Student(Base):
    __tablename__ = 'quotation'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String)

# Create table as needed.

Base.metadata.create_all(engine)


class TestStudent(unittest.TestCase):
    def setUp(self):
        self.session = Session()

    def tearDown(self):
        pass

    def test_all(self):
        u"""
        对数据库的操作，就是对Session中的对象的操作。
        首先必须有对象在其中。
        最后必须执行Session.commit()
        """

        # 添加
        student = Student(name=u'张三', phone='000000')
        self.session.add(student)
        print '>>>>>> DIRTY:', self.session.dirty, student in self.session.dirty
        print '>>>>>> NEW:', self.session.new, student in self.session.new
        print '>>>>>> IDENTITY_MAP', self.session.identity_map
        self.session.commit()

        # 测试查询所有
        students = self.session.query(Student).filter_by(id=student.id).all()
        self.assertTrue(isinstance(students, list))

        # 验证是否添加
        student1 = self.session.query(Student).filter_by(id=student.id).one()
        print type(student1)
        self.assertEqual(student1.id, student.id)
        self.assertEqual(student1.name, student.name)
        self.assertEqual(student1.phone, student.phone)

        # 更新
        student1.name = u'李四'
        student1.phone = '111111'
        self.session.commit()

        # 验证是否更新
        student2 = self.session.query(Student).filter_by(id=student.id).one()
        self.assertEqual(student2.id, student1.id)
        self.assertEqual(student2.name, student1.name)
        self.assertEqual(student2.phone, student1.phone)

        # 删除
        self.session.delete(student1)
        self.session.commit()
        is_not_fount = False
        try:
            self.session.query(Student).filter_by(id=student.id).one()
        except NoResultFound as e:
            is_not_fount = True
        self.assertTrue(is_not_fount)

    def test_schema(self):
        print Student.__table__

    def test_address(self):
        student = Student(name=u'张三', phone='000000')
        # print student.addresses

