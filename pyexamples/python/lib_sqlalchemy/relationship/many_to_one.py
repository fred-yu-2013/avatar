# -*- coding: utf-8 -*-

"""
http://docs.sqlalchemy.org/en/rel_0_9/orm/relationships.html
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import aliased
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func

engine = create_engine('sqlite:///:memory:', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class Parent(Base):
    """ 单个Parent中包含一个Child。
    """
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    child_id = Column(Integer, ForeignKey('child.id'))
    child = relationship("Child")

    def __repr__(self):
        return 'Parent(%s, %s, %s, %s)' % (str(self.id),
                                           str(self.name),
                                           str(self.child_id),
                                           str(self.child))


class Parent2(Base):
    """ 单个Parent中包含一个Child，并在Child中设置反向引用。
    """
    __tablename__ = 'parent2'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    # 仅供数据库用
    child_id = Column(Integer, ForeignKey('child.id'))
    # 上层使用
    # backref在Child中增加了一个变量parent2s, 它代表了应用Child的Parent集合。
    child = relationship("Child", backref='parent2s')

    def __repr__(self):
        return 'Parent(%s, %s, %s, %s)' % (str(self.id),
                                           str(self.name),
                                           str(self.child_id),
                                           str(self.child))


class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return 'Child(%s, %s)' % (str(self.id), str(self.name))

Base.metadata.create_all(engine)  # Create tables that do not exist.

p = Parent(name='AA')
c = Child(name='CC')
print '>>>>>> After creating: %s, %s' % (str(p), str(c))
p.child = c
print '>>>>>> After appending client: %s, %s' % (str(p), str(c))
session = Session()
# 仅需添加Parent即可
session.add(p)
print '>>>>>> After adding to session: %s, %s' % (str(p), str(c))
session.commit()
print '>>>>>> After committing: %s, %s' % (str(p), str(c))

c.name = 'CC2'
session.commit()
print ">>>>>> After changing client's name: %s, %s" % (str(p), str(c))

p2 = Parent2(name='AAA')
print '>>>>>> 2 After creating: %s, %s' % (str(p2), str(c))
p2.child = c
session.add(p2)
session.commit()
print '>>>>>> 2 Child.parent2s: %s' % str(c.parent2s)
