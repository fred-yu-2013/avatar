# -*- coding: utf-8 -*-

""" this tutorial is from:
http://docs.sqlalchemy.org/en/rel_0_9/orm/tutorial.html
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import aliased
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func

engine = create_engine('sqlite:///:memory:', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (self.name, self.fullname, self.password)

print '============= define table ============='
print 'User:', repr(User.__table__)

Base.metadata.create_all(engine)  # Create tables that do not exist.

print '============= create instance ============='
ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
print ed_user.name
print ed_user.password
print str(ed_user.id)
print dir(ed_user)
print ed_user._sa_instance_state

# print '============= create session ============='
# session = Session()
# ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
# session.add(ed_user)
# print '>>>>>> before query'
# our_user = session.query(User).filter_by(name='ed').first()  # ed_user has been flushed to db.
# print repr(our_user)
# print ed_user is our_user
# print ed_user.id
# print '>>>>>> before all some users.'
# session.add_all([
#     User(name='wendy', fullname='Wendy Williams', password='foobar'),
#     User(name='mary', fullname='Mary Contrary', password='xxg527'),
#     User(name='fred', fullname='Fred Flinstone', password='blah')])
# ed_user.password = 'f8s7ccs'
# print repr(session.dirty)
# print repr(session.new)
# session.commit()  # Write to database and refresh instances in session.
# print ed_user.id
#
# print '============= rolling back ============='
# ed_user.name = 'Edwardo'
# fake_user = User(name='fakeuser', fullname='Invalid', password='12345')
# session.add(fake_user)
# # print session.query(User).filter(User.name.in_(['Edwardo', 'fakeuser'])).all()
# print ed_user.name
# print session.new
# # print session.query(User).filter(User.name.in_(['ed', 'fakeuser'])).all()
# session.rollback()
# print '>>>>>> after session.rollback()'
# print ed_user.name
# print fake_user in session
# print session.query(User).filter(User.name.in_(['ed', 'fakeuser'])).all()
#
# print '============= querying ============='
# for instance in session.query(User).order_by(User.id):
#     print instance.name, instance.fullname
# for name, fullname in session.query(User.name, User.fullname):
#     print name, fullname
# for row in session.query(User, User.name).all():
#     print row.User, row.name
# for row in session.query(User.name.label('name_label')).all():  # column label.
#     print(row.name_label)
# print '>>>>>> alias'
# user_alias = aliased(User, name='user_alias')
# for row in session.query(user_alias, user_alias.name).all():
#     print row.user_alias
# for u in session.query(User).order_by(User.id)[1:3]:  # select array members.
#     print u
# for name, in session.query(User.name).filter_by(fullname='Ed Jones'):
#     print name
# for name, in session.query(User.name).filter(User.fullname=='Ed Jones'):
#     print name
# for user in session.query(User).filter(User.name=='ed').filter(User.fullname=='Ed Jones'):
#     print user
#
# print '============= Returning Lists and Scalars ============='
