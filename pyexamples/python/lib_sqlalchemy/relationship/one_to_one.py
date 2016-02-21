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
    child = relationship("Child", uselist=False, backref="parent")

    def __repr__(self):
        return 'Parent(%s, %s, %s)' % (str(self.id), str(self.name), str(self.child))


class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    # 定义了一个外键，和表parent的id属性对应。
    parent_id = Column(Integer, ForeignKey('parent.id'))

    def __repr__(self):
        return 'Child(%s, %s, %s)' % (str(self.id), str(self.name), str(self.parent_id))

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
